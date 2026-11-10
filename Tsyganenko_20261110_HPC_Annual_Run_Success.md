---
project: Tsyganenko
type: run_log
date: 2026-11-10
---

# NASA Pleiades 2018년 전체(1년) GSE 자기권시스 2D 분포 HPC 연산 완료 보고서

## 1. 실행 개요 및 최종 성과
- **대상 기간**: 2018년 1월 1일 ~ 2018년 12월 31일 (총 365일)
- **타임 케이던스**: NASA OMNI 5분 간격 (**총 105,120 타임스텝**)
- **실행 환경**: NASA Pleiades 슈퍼컴퓨터 Skylake 노드 (`model=sky_ele`, 40 CPUs, PBS Pro `PBS_MSheath.sh`, 그룹 `s3015`)
- **총 소요 시간**: **17분 30초 (1,050초)**
- **평균 처리 속도**: **초당 약 100.1 스텝 (100.1 steps/s)**
- **최종 산출물**: `output_nc/MSH_GSE_2018-01.nc` ~ `output_nc/MSH_GSE_2018-12.nc` (총 12개 월별 NetCDF4 파일, 총 용량 약 350 MB)

---

## 2. 파이프라인 주요 기술적 성과

1. **초고속 C-ABI Fortran 연산 코어 (`libmsh.so`)**:
   * 매 스텝마다 적도면($61 \times 121$) 및 자오면($41 \times 121$) 총 12,342개 잠재 격자점에 대해, 자오면 Nightside($X_{\mathrm{GSE}} < 0$) 영역을 사전 제외하고 7,381개 격자점을 직접 계산.
   * 순수 Fortran 평가 속도 및 OMNI 전처리, GSM $\leftrightarrow$ GSE 좌표 회전, 배열 머징, NetCDF4 zlib 압축을 포함하여 초당 100스텝 이상의 처리량을 달성.

2. **완전 자동화된 결측치 보정 및 좌표계 검증**:
   * 15분 이하의 짧은 단절(Gap)은 1D 선형 보간을 자동 적용하고, 장기 결측치는 `quality_flag = 0` 및 `NaN` 마스킹 처리.
   * 실시간 IGRF 다이폴 틸트각($\psi$) 및 GSE $\leftrightarrow$ GSM 회전 행렬의 직교성 오차 $2.22 \times 10^{-16}$, 왕복 변환 오차 $1.07 \times 10^{-14} R_E$를 전 스텝에 걸쳐 엄밀하게 유지.

3. **CF-1.8 표준 NetCDF4 압축 및 2D 통계 요약 데이터 구축**:
   * **3D 시계열 변수**: 5분 간격의 $N_p, V_x, V_y, V_z, |V|, B_x, B_y, B_z, |B|, T_p, P_{\mathrm{dyn}}$, 영역 플래그 (`region_flag`).
   * **2D 월간 요약 변수**: 각 격자점별 월간 산술평균(Mean), 중앙값(Median), 표준편차(Std), 유효 데이터 개수(Valid counts) 포함.
   * NetCDF4 zlib 압축(Level 4)을 적용하여 1년 10.5만 스텝의 고해상도 대용량 그리드 데이터를 노드 메모리 초과(OOM) 없이 파일당 약 28 MB 수준으로 효율적으로 저장.

---

## 3. 후속 분석 및 활용 계획
1. **월별 / 계절별 자기권시스 구조 비교**:
   * 춘추분(Equinox: 3월, 9월) vs 하지/동지(Solstice: 6월, 12월) 다이폴 틸트에 따른 적도면 및 자오면 플라즈마 밀도·속도 분포 비대칭성 분석.
2. **위성 궤도 데이터와의 직접 매핑**:
   * MMS, THEMIS, Geotail 등 자기권시스를 통과한 과학위성의 궤도(GSE 좌표)와 본 파이프라인의 5분 모델 값을 시계열로 직접 보간하여 관측-모델 일치도 정밀 검증.
3. **다른 연도 확장 실행**:
   * `./download_omni.sh [YEAR]` 및 `qsub -v TARGET_YEAR=[YEAR] PBS_MSheath.sh` 명령으로 태양활동 극대기/극소기 등 다른 연도 데이터도 18분 이내에 일괄 생성 가능.
