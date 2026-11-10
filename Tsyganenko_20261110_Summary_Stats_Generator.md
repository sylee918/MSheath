---
project: Tsyganenko
type: analysis
date: 2026-11-10
---

# 2018년 GSE 자기권시스 경량 요약 통계 데이터 생성 및 시각화 파이프라인

## 1. 개요
NASA Lou 대용량 스토리지(`/u/slee122/MSheath/Tsy2018/`)에 보관된 2018년 12개 월별 NetCDF4 파일(`MSH_GSE_2018-01.nc` ~ `MSH_GSE_2018-12.nc`, 총 ~350 MB)로부터, 로컬 환경으로 즉시 가져와 다각도의 통계 분석과 시각화를 수행할 수 있도록 **단일 경량 요약 파일 (`summary_stats/MSH_GSE_2018_Summary.nc`, 약 5~6 MB)**을 생성하는 스크립트(`build_summary_stats.py`)와 시각화 코드(`plot_summary_stats.py`)를 구축함.

---

## 2. 요약 데이터(`MSH_GSE_2018_Summary.nc`) 포함 항목

1. **월별 2D 통계 (`month = 1..12`, `61 x 121` 그리드, 적도면 `eq` & 자오면 `mer`)**:
   * **전체 유효 영역(MSH + 태양풍)**: `mean`, `median`, `std`, `valid_count`, `msh_count`, `msh_fraction` (MSH 체류 확률)
   * **순수 자기권시스 내부 전용(`region_flag == 1`)**: 태양풍 영역 값의 혼입을 배제한 순수 MSH 내부의 $N_p, T_p, V_x, V_y, V_z, |V|$ 평균(`msh_mean`) 및 표준편차(`msh_std`)
   * **월평균 경계면 위치**: 충격파면(`rbs_mean`) 및 자기권계면(`rmp_mean`) 2D 필드

2. **연간(Full-Year 2018) 통합 2D 통계 (`61 x 121` 그리드)**:
   * 1년 105,120 스텝 전체에 대한 정확한(Exact streaming accumulation) 산술평균, 중앙값, 표준편차, MSH 체류 확률 및 연평균 경계면(`annual_{eq,mer}_*`)

3. **8대 물리 조건(Regime)별 2D 합성장 (`regime = 0..7`, `61 x 121` 그리드)**:
   * `[0]` `all_year`: 2018년 전체 기준선
   * `[1]` `imf_south_bz_lt_m2`: 남향 IMF ($B_{z,\mathrm{GSM}} < -2\text{ nT}$)
   * `[2]` `imf_north_bz_gt_p2`: 북향 IMF ($B_{z,\mathrm{GSM}} > +2\text{ nT}$)
   * `[3]` `pdyn_high_gt_2p5`: 고동압력 태양풍 ($P_{\mathrm{dyn}} > 2.5\text{ nPa}$)
   * `[4]` `pdyn_low_lt_1p2`: 저동압력 태양풍 ($P_{\mathrm{dyn}} < 1.2\text{ nPa}$)
   * `[5]` `tilt_pos_gt_p15`: 북반구 여름 다이폴 틸트 ($\psi > +15^\circ$)
   * `[6]` `tilt_neg_lt_m15`: 북반구 겨울 다이폴 틸트 ($\psi < -15^\circ$)
   * `[7]` `tilt_equinox_abs_le_5`: 춘추분 다이폴 틸트 ($|\psi| \le 5^\circ$)

4. **연간 5분 간격 1D 시계열 (`time = 105,120`)**:
   * 태양풍·IMF 드라이버 (`sw_vsw`, `sw_np`, `sw_temp_k`, `sw_pdyn_npa`, `imf_bx_gsm`, `imf_by_gsm`, `imf_bz_gsm`, `dipole_tilt_deg`)
   * **Subsolar Nose ($Y_{\mathrm{GSE}}=0, Z_{\mathrm{GSE}}=0$) 시계열**: 충격파면 거리($R_{\mathrm{BS},0}$), 자기권계면 거리($R_{\mathrm{MP},0}$), 자기권시스 두께($\Delta R_{\mathrm{MSH}}$), Nose 라인 MSH 평균 밀도·속도·온도

---

## 3. 실행 및 로컬 반입 절차

### Step 1: Lou(`lfe`) 또는 Pleiades(`pfe`)에서 요약 파일 생성 및 Git Push
```bash
git pull
python3 build_summary_stats.py --in-dir /u/slee122/MSheath/Tsy2018 --year 2018
git add summary_stats/MSH_GSE_2018_Summary.nc
git commit -m "data: add 2018 GSE MSheath summary stats"
git push
```

### Step 2: 로컬 환경에서 Git Pull 및 5종 종합 분석 플롯 생성
```bash
git pull
python plot_summary_stats.py --summary summary_stats/MSH_GSE_2018_Summary.nc --out-dir figures
```
