---
project: Tsyganenko
type: setup
date: 2026-11-10
---

# Tsyganenko Magnetosheath Model: 40-Core HPC GSE 2D Distribution Pipeline 설계 및 검증 노트

## 1. 개요 (Overview)
본 문서는 NASA SPDF 5분 해상도 OMNI 데이터를 활용하여 Tsyganenko et al. (2024, 2025) 마그네토시스 모델의 **GSE(Geocentric Solar Ecliptic) 좌표계 기준 적도면(Equatorial, $Z_{\mathrm{GSE}}=0$) 및 자오면(Meridional, $Y_{\mathrm{GSE}}=0$) 2D 공간 분포**($N_p, V_x, V_y, V_z, |V|, T, R_{\mathrm{BS}}, R_{\mathrm{MP}}$)를 계산하고, **월 단위 NetCDF4(`.nc`) 파일**로 저장하는 40코어 HPC 병렬 파이프라인의 아키텍처, 좌표 변환 검증, 결측치 처리 규칙, 그리고 벤치마크 결과를 기록한 기술 문서이다.

---

## 2. 모듈 구성 및 실행 파이프라인

| 파일명 | 역할 및 주요 기능 |
| :--- | :--- |
| `msh_core_lib.for` / `libmsh.so` | • [`msh_combined.for`](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/msh_combined.for)를 C-ABI 호환 공유 라이브러리(`msh_init`, `msh_eval_batch`)로 래핑<br>• 워커 프로세스당 `.par` 계수 파일 1회 로드 및 인메모리 포인터 연산으로 서브프로세스/디스크 I/O 오버헤드 제거 |
| `omni_loader.py` | • NASA SPDF `omni_5minYYYY.asc` 자동 다운로드 및 로컬 캐시(`data/omni_5min/`) 관리<br>• 공식 Fill Value(`9999.99`, `99999.9`, `999.99`, `9999999.`) 필터링 및 단기 결측($\le 15$분, 3 스텝) 선형 보간<br>• 품질 플래그 `omni_quality_flag` (`2=관측`, `1=단기보간`, `0=장기결측 스킵`) 부여 |
| `coord_transform.py` | • `geopack.recalc(ut)` 및 `geopack.gsmgse` 기반 시간별 쌍극자 기울기 $\Psi(t)$ 및 $\mathrm{GSE} \leftrightarrow \mathrm{GSM}$ 회전 행렬 성분 $(\cos\alpha, \sin\alpha)$ 계산<br>• 직교성, 가역성(Round-trip), 속력 불변성, OMNI 공식 자기장 성분 교차 검증(`verify_coordinate_transforms`) |
| `grid_engine.py` | • **적도면($Z_{\mathrm{GSE}}=0$)**: $X_{\mathrm{GSE}} \in [-10, 20]\ R_E$, $Y_{\mathrm{GSE}} \in [-30, 30]\ R_E$ ($\Delta=0.5\ R_E$, $61 \times 121 = 7,381$ 셀)<br>• **자오면($Y_{\mathrm{GSE}}=0$)**: **$X_{\mathrm{GSE}} < 0$ 구간 계산 자체를 스킵**하고 $X_{\mathrm{GSE}} \in [0, 20]\ R_E$, $Z_{\mathrm{GSE}} \in [-30, 30]\ R_E$ ($41 \times 121 = 4,961$ 셀)만 계산 후 `NaN` 및 `flag = -1` 마스킹<br>• 월별 각 그리드 셀의 **평균(`mean`), 중앙값(`median`), 표준편차(`std`), 유효 카운트(`valid_count`), 시스 체류 카운트(`msh_count`)** 산출 |
| `nc_writer.py` | • 월별 `output_nc/MSH_GSE_YYYY-MM.nc` 생성 (`NETCDF4`, `zlib=True, complevel=4`, `float32`)<br>• 5분 간격 3D 시계열 배열 `(time, x_gse, y_gse/z_gse)` + 월간 2D 대표 통계 배열 동시 저장 |
| `hpc_pipeline.py` & `run_pbs.sh` | • 40코어 ProcessPool 오케스트레이터 (월별 청크 분할 + 월당 3~4 워커 할당 + 월별 저장 직후 `gc.collect()` 메모리 해제)<br>• NASA NAS/Pleiades (PBS Pro, `model=sky_ele`, `s3015`) 슈퍼컴퓨터용 배치 스크립트 |

---

## 3. 좌표계 변환 수식 및 검증 결과 ($\mathrm{GSE} \leftrightarrow \mathrm{GSM}$)

### 3.1 변환 알고리즘
1. **격자점 회전 ($\mathrm{GSE} \to \mathrm{GSM}$)**:
   $$X_{\mathrm{GSM}} = X_{\mathrm{GSE}}$$
   $$Y_{\mathrm{GSM}} = Y_{\mathrm{GSE}} \cos\alpha(t) - Z_{\mathrm{GSE}} \sin\alpha(t)$$
   $$Z_{\mathrm{GSM}} = Y_{\mathrm{GSE}} \sin\alpha(t) + Z_{\mathrm{GSE}} \cos\alpha(t)$$
2. **출력 속도 벡터 역회전 ($\mathrm{GSM} \to \mathrm{GSE}$)**:
   $$V_{x,\mathrm{GSE}} = V_{x,\mathrm{GSM}}$$
   $$V_{y,\mathrm{GSE}} = V_{y,\mathrm{GSM}} \cos\alpha(t) + V_{z,\mathrm{GSM}} \sin\alpha(t)$$
   $$V_{z,\mathrm{GSE}} = -V_{y,\mathrm{GSM}} \sin\alpha(t) + V_{z,\mathrm{GSM}} \cos\alpha(t)$$

### 3.2 자동 검증 결과 (`test_hpc_pipeline.py`)
- **행렬 직교성 오차 ($|\cos^2\alpha + \sin^2\alpha - 1|$)**: `2.22e-16` (Machine Epsilon 수준)
- **좌표 가역성 오차 ($\|\mathbf{r}_{\mathrm{GSE}} - \mathbf{r}'_{\mathrm{GSE}}\|_\infty$)**: `1.07e-14 R_E`
- **속력 보존 오차 ($||\mathbf{V}_{\mathrm{GSE}}| - |\mathbf{V}_{\mathrm{GSM}}||$)**: `7.11e-15 km/s`
- **NASA SPDF OMNI 공식 $(B_{y,\mathrm{GSE}}, B_{z,\mathrm{GSE}})$ 대비 RMS 오차**: `0.0153 nT` (OMNI 텍스트 파일의 소수점 둘째 자리 반올림 한계와 일치)

---

## 4. 성능 벤치마크 및 실행 방법

### 4.1 벤치마크 측정 결과
- **단일 스텝 연산 속도 비교 ($0.25\ R_E$, $29,161$ 격자점 기준)**:
  - 기존 서브프로세스 + ASCII `.dat` I/O: `~650 ms`
  - 신규 `libmsh.so` 인메모리 호출: **`96.5 ms`** (정확도 차이 `< 5.0e-5`, Region Flag 100% 일치)
- **5분 간격 멀티워커 파이프라인 처리 속도 ($\Delta = 0.5\ R_E$, 자오면 $X<0$ 스킵 포함)**:
  - 12 워커 기준 처리량: **`48.0 steps/sec`** (24시간 288 스텝 처리 및 NetCDF4 압축 저장에 `6.00초` 소요)
  - **40코어 Skylake 노드에서 1년치 ($105,120$ 스텝) 전체 예상 소요 시간**: **약 11분**

### 4.2 CLI 및 PBS 슈퍼컴퓨터 실행 명령어
```bash
# 1. 공유 라이브러리 빌드 (최초 1회, Intel ifort 또는 GNU gfortran)
ifort -O2 -fPIC -shared -extend-source 132 msh_core_lib.for -o libmsh.so
# 또는: gfortran -O1 -fPIC -shared -ffixed-line-length-none msh_core_lib.for -o libmsh.so

# 2. 로컬 또는 인터랙티브 노드 단일 실행 (2018년 전체)
python3 hpc_pipeline.py --year 2018 --total-cores 40 --workers-per-month 3 --concurrent-months 4 --dx 0.5 --out-dir output_nc

# 3. 특정 월(예: 1월, 6월) 지정 실행
python3 hpc_pipeline.py --year 2018 --months 1 6 --total-cores 40 --dx 0.5

# 4. NASA Pleiades/NAS 슈퍼컴퓨터 PBS 배치 작업 제출 (기본 2018년)
qsub run_pbs.sh

# 5. 특정 연도 지정 제출 (예: 2019년)
qsub -v TARGET_YEAR=2019 run_pbs.sh
```
