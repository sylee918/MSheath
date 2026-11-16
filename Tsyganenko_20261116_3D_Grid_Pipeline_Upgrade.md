---
project: Tsyganenko
type: setup
date: 2026-11-16
---

# Tsyganenko Magnetosheath HPC 파이프라인 3차원(3D) 계산 업그레이드 및 소요 시간 추정

## 1. 개요
기존 2차원 평면($XY$ 적도면 $Z_{\mathrm{GSE}}=0$, $XZ$ 자오면 $Y_{\mathrm{GSE}}=0$) 전용으로 구현되어 있던 NASA Pleiades 40코어 HPC 파이프라인을 **3차원 공간 격자(3D Volume)** 계산이 가능하도록 수정하였다.

- **3D 격자 영역 및 해상도**:
  - $X_{\mathrm{GSE}} \in [-10, 20]\,R_E$, $dx = 1.0\,R_E$ ($N_x = 31$)
  - $Y_{\mathrm{GSE}} \in [-25, 25]\,R_E$, $dy = 1.0\,R_E$ ($N_y = 51$)
  - $Z_{\mathrm{GSE}} \in [-15, 15]\,R_E$, $dz = 1.0\,R_E$ ($N_z = 31$)
  - 스텝당 총 격자점 수: $31 \times 51 \times 31 = 49,011$개
- **저장 및 메모리 전략**:
  - 4D 시계열 `(time, x_gse, y_gse, z_gse)` 전체를 메모리에 올리지 않고, 워커 내부에서 **float64 스트리밍 누적기(합계/제곱합/카운트)**로 월간 3D 통계장(`vol_*`)을 직접 계산하여 OOM을 방지한다.
  - 매 스텝 3D 계산 결과에서 추가 Fortran 호출 없이 $Z_{\mathrm{GSE}}=0$ (`eq_*`) 및 $Y_{\mathrm{GSE}}=0$ (`mer_*`, $X_{\mathrm{GSE}}<0$ 마스킹 유지) 2D 시계열 슬라이스를 동시에 추출해 기존 NetCDF4 구조와 호환된다.

---

## 2. 수정 파일 및 주요 변경 사항

| 파일 | 변경 내용 |
| :--- | :--- |
| [grid_engine.py](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/grid_engine.py) | • `GridConfig` 기본값을 3D 도메인(`dx=dy=dz=1.0`, `X=[-10,20]`, `Y=[-25,25]`, `Z=[-15,15]`)으로 변경<br>• `evaluate_time_chunk`에서 스텝당 `lib.msh_eval_batch`를 3D 격자(49,011점)에 1회 호출 후 3D 스트리밍 누적(`vol_valid_count`, `vol_msh_count`, `vol_bndry_count`, `vol_rbs_sum`, `vol_rmp_sum`, `vol_{v}_{sum,sum_sq,msh_sum,msh_sum_sq}`) 및 `eq_*`/`mer_*` 2D 슬라이스 추출<br>• `compute_monthly_statistics`에서 3D 월간 통계(`vol_*_mean`, `vol_*_std`, `vol_*_msh_mean`, `vol_*_msh_std`, `vol_msh_fraction`, `vol_rbs_mean`, `vol_rmp_mean`) 산출 |
| [hpc_pipeline.py](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/hpc_pipeline.py) | • `_merge_subchunks`가 서브청크별 3D 누적 배열을 합산(`+=`)하도록 확장하고 `_drop_vol_accumulators`로 통계 산출 후 원시 누적 버퍼 해제<br>• `run_annual_pipeline` 및 CLI에 `--dy`, `--dz`, `--xmin`, `--xmax`, `--ymin`, `--ymax`, `--zmin`, `--zmax` 추가, 기본 `--dx 1.0`, `--workers-per-month 10`으로 설정 |
| [nc_writer.py](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/nc_writer.py) | • 월별 NetCDF4 파일에 `(x_gse, y_gse, z_gse)` 차원의 3D 월간 통계 변수(`vol_*`) 저장 섹션 추가 |
| [PBS_MSheath.sh](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/PBS_MSheath.sh) | • 40코어 활용(`--workers-per-month 10 --concurrent-months 4`) 및 3D 도메인 인자(`--dx 1.0 --xmin -10.0 --xmax 20.0 --ymin -25.0 --ymax 25.0 --zmin -15.0 --zmax 15.0`) 반영 |
| [build_summary_stats.py](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/build_summary_stats.py) | • `PooledVolumeAccumulator3D` 추가: 월별 3D `(count, mean, std)`를 풀링하여 연간 3D 통계(`annual_vol_*`)와 월별 3D 통계(`monthly_vol_*`)를 요약 NetCDF4에 통합 |
| [test_hpc_pipeline.py](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/test_hpc_pipeline.py) | • 3D 파이프라인 실행 및 NetCDF4 내 `vol_*` 변수 shape `(31, 51, 31)`·`eq_*` 일치 여부 검증 추가 |

---

## 3. 검증 결과
1. **구문 검사 (`python -m py_compile`)**: 수정한 5개 Python 파일 모두 통과 (Exit 0).
2. **실제 `libmsh.so` 기반 3D 누적·병합·요약 검증 (WSL)**:
   - 단일 청크 vs 분할-병합(`_merge_subchunks`), `vol_*[:, :, iz0]` vs `eq_*`, `vol_*[ix0:, iy0, :]` vs `mer_*`, `PooledVolumeAccumulator3D` 연간 풀링 모두 `rtol=1e-4, atol=1e-4` 이내 일치 확인.
3. **전체 통합 테스트 (`wsl python3 test_hpc_pipeline.py`)**:
   - Test 1 (`libmsh.so` 정합성), Test 2 (OMNI 로더 및 좌표 변환 검증), Test 3 (2018-01 288스텝 8워커 실행: `12.28s`, 출력 `8.19 MB`, 3D 볼륨 `(31, 51, 31)` 확인) 모두 통과.

---

## 4. 계산 시간 비교 및 3차원 예상 소요 시간 (Pleiades `sky_ele` 40코어 기준)

### 4.1 기존 2D 실행 로그 분석 ([MSH_GSE_HPC.o25372708](file:///c:/Users/slee122/OneDrive%20-%20NASA/Desktop/Work/JSokol/MSheath/MSH_GSE_HPC.o25372708))
- **총 Walltime**: **17분 31초** (`1,051초`, 파이프라인 `1,042.49초`, `CPU Time Used: 02:07:41 = 7,661초`)
- **시간 세부 분해**:
  1. **병렬 Fortran/Python 계산 (3개 Wave, 실질 36코어 사용: `--workers-per-month 3` → 9×4)**: Wave당 약 **75~80초** × 3 ≈ **약 4분 (230~240초)**
  2. **월별 직렬 후처리 및 NetCDF4 zlib 저장**: 월별 시계열(`~930 MB/월`)에 대한 `np.nanmedian` 연산 및 NetCDF4 압축 쓰기가 메인 프로세스에서 순차 실행되며 월당 **65~69초** × 12개월 ≈ **약 13분 (780~800초)** 소요.

### 4.2 신규 3D 설정 벤치마크 및 예상 시간
- **WSL 동일 바이너리(`libmsh.so`) 20스텝 실측**:
  - 기존 2D (`12,342점`, 평균 MSH `2,266.2점`): `31.39 ms/step`
  - 신규 3D (`49,011점`, 평균 MSH `11,997.6점`): Fortran `186.24 ms/step` (**5.93배**), Python 포함 전체 `225.97 ms/step`
- **Pleiades 40코어 1년치 (105,120 스텝) 예상 소요 시간**:
  1. **병렬 3D 연산 시간**: 기존 4분(36코어) × Fortran 연산 증가율(~5.93배) × 코어 증가 보정(`36/40`) ≈ **약 21분** (Python 3D 누적 오버헤드 포함 **약 20~26분**)
  2. **월별 직렬 후처리 및 NetCDF4 저장 시간**: 2D 슬라이스 격자가 `12,342점` → `2,232점`(`1/5.5`)으로 축소되어 월별 NetCDF 파일 크기가 `~930 MB`에서 `~170–220 MB` 수준으로 줄고, 3D `vol_*`는 시간축 없는 요약 통계(`31×51×31`)만 저장하므로 월당 직렬 시간이 `~66초`에서 `~12–18초`로 감소 → 12개월 합계 **약 2.5~3.5분**
  3. **총 예상 Walltime**: **약 23분 ~ 30분 (여유 추정 최대 35분 내외)** — `PBS_MSheath.sh`의 `devel` 큐 기본 walltime(`02:00:00`) 내에서 여유롭게 완료 가능.
