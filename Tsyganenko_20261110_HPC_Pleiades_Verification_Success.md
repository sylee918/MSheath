---
project: Tsyganenko
type: run_log
date: 2026-11-10
---

# NASA Pleiades HPC 검증 테스트 성공 보고서 (`MSH_TEST.o25372698`)

## 1. 개요 및 실행 환경
- **작업 ID**: `Job 25372698.pbspl1.nas.nasa.gov`
- **호스트 및 노드**: NASA Pleiades `r137i6n33` (PBS Pro `devel` 큐, `s3015`)
- **할당 자원**: 8 CPUs (`ncpus=8`, `place=scatter:excl`), Walltime 10분 설정
- **실행 결과**: **Exit Status 0 (성공)**
- **소요 자원**:
  - Walltime: **22초**
  - CPU Time: 38초
  - Real Memory: ~1.48 GB

---

## 2. 세부 테스트 검증 결과

### [Test 1] Fortran C-ABI 공유 라이브러리 (`libmsh.so`)
- 7,381개 그리드 포인트 계산 속도: **44.34 ms**
- 자기권계면 및 충격파면 식별: MSH 포인트 1,694개, 태양풍 영역 3,727개 정상 분류 완료.

### [Test 2] NASA SPDF 5분 OMNI 로더 및 GSM <-> GSE 좌표계 변환 정밀도
- 2018년 1월 5분 OMNI 레코드: **8,928개 (100% 정상 로드)**
- GSE <-> GSM 4단계 정밀도 검증:
  - 변환 행렬 행렬식 직교성 오차: $2.22 \times 10^{-16}$ (기계 정밀도 한계 달성)
  - 좌표 왕복(Roundtrip) 변환 오차: $1.07 \times 10^{-14} R_E$
  - 벡터 크기 보존(Norm preservation) 오차: $7.11 \times 10^{-15} \text{ km/s}$
  - OMNI IMF $B$ 벡터 vs 회전 행렬 RMS 편차: **$0.0153\text{ nT}$** (NASA OMNI 공식 데이터 일치)

### [Test 3] Multi-Worker 병렬 파이프라인 및 NetCDF4 출력 생성
- 2018년 1월 샘플 (288 스텝, 1일 치 분량):
  - 8코어 병렬 연산 완료 시간: **4.78초** (처리 속도: 60.2 steps/sec)
  - 생성 파일: `test_nc/MSH_GSE_2018-01.nc` (27.80 MB, zlib compression level 4)
  - 좌표계 속성: `coordinate_system = "GSE (Geocentric Solar Ecliptic)"`
  - $X_{\mathrm{GSE}} < 0$ 슬라이스 마스킹: 20개 슬라이스 전원 NaN 및 `region_flag = -1` 처리 검증 완료.

---

## 3. 성능 벤치마크 및 1년 치 연산 시간 추정
- 8코어 처리 속도: **60.2 steps/s**
- **40코어 전체 노드(`model=sky_ele`) 실행 시 예상 속도**:
  - 2018년 전체 1년 데이터 (105,120 타임스텝): **약 8.7분 ~ 10분 이내 완료 예상**
  - 월별 NetCDF 파일 약 12개 생성 (총 약 350 MB)

---

## 4. 본 실행(Annual Production Run) 안내
검증이 완벽하게 끝났으므로, 2018년 1년 치 전체 연산 잡을 `PBS_MSheath.sh`로 제출할 준비가 완료됨:
```bash
# 1. 2018년 OMNI 데이터 다운로드 (프론트엔드 pfe에서 1회 실행)
./download_omni.sh 2018

# 2. 40코어 정규 배치 잡 제출
qsub PBS_MSheath.sh
```
