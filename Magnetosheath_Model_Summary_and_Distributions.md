---
title: "Tsyganenko et al. (2024, 2025) 마그네토시스 모델 정리 및 플라즈마 분포 해석"
tags:
  - space-physics
  - magnetosheath
  - tsyganenko-model
  - solar-wind
  - python
  - fortran
created: 2026-11-06
updated: 2026-11-06
references:
  - "Tsyganenko, N. A., Semenov, V. S., Erkaev, N. V., & Gubaidulin, N. T. (2024). Magnetosheath plasma flow and its response to IMF and geodipole tilt as obtained from the data-based modeling. JGR Space Physics, 129, e2024JA033233."
  - "Tsyganenko, N. A., Gubaidulin, N. T., Semenov, V. S., & Erkaev, N. V. (2025). Magnetosheath proton density and temperature as derived from data-constrained modeling. JGR Space Physics, 130, e2025JA034343."
---

# Tsyganenko et al. (2024, 2025) 마그네토시스 모델 정리 및 플라즈마 분포

> [!abstract] 
> 본 문서는 **Tsyganenko et al. (2024, 2025)** 논문에서 공유된 3개의 Fortran 77 코드(`Magnetosheath_density_sample_code.for`, `Magnetosheath_energy_sample_code.for`, `Magnetosheath_flow_model.for`)의 수학적·물리적 구조를 분석하고, 이를 통합하여 태양풍 조건에 따른 **지구 마그네토시스(Magnetosheath)의 양성자 밀도($N_p$), 벌크 유속($|V|$), 온도($T$)/열에너지($W$)의 2차원 공간 분포**를 산출하고 분석한 결과를 정리한 기술 노트입니다.

---

## 1. 모델 개요 및 핵심 배경

지구 자기권과 초음속 태양풍의 상호작용으로 형성되는 **마그네토시스(Magnetosheath, MS)** 는 보우 쇼크(Bow Shock, BS)와 자기권계면(Magnetopause, MP) 사이에 위치하는 전이 영역입니다. 이 영역은 태양풍 에너지가 압축, 가열, 감속되며 지구 자기권-이온층 시스템으로 유입되는 우주 기상(Space Weather)의 핵심 경로입니다.

- **Tsyganenko et al. (2024)**: THEMIS (2007–2024), Cluster (2001–2022), MMS-1 (2015–2024) 관측 데이터를 기반으로 **마그네토시스 플라즈마 벌크 유동($\mathbf{F} = n\mathbf{v}$)** 모델링 구축.
- **Tsyganenko et al. (2025)**: 동일한 3대 위성 미션의 방대한 데이터 풀을 활용하여 **양성자 수밀도($N_p$) 및 열에너지($W$)** 에 대한 고해상도 연속 팽창 모델 구축 (향후 SMILE 미션의 연X선 이미징 검증 표준 제공 목적).

---

## 2. 3개 포트란 코드의 구조 및 물리량 정의

### 2.1. 코드 구성 요약

| 소스 파일명 | 대상 물리량 | 파라미터 파일 | 출력 단위 | 주요 서브루틴 |
| :--- | :--- | :--- | :--- | :--- |
| `Magnetosheath_density_sample_code.for` | 양성자 수밀도 ($N_p$) | `Density_Best_par_so_far_em6.par` (1609 params) | $\mathrm{cm^{-3}}$ | `MODELVEC_DEN` |
| `Magnetosheath_energy_sample_code.for` | 양성자 열에너지 ($W$) 및 온도 ($T$) | `Energy_Best_par_so_far_em6.par` (1609 params) | $\mathrm{eV}$ / $\mathrm{K}$ | `MODELVEC_ENE` |
| `Magnetosheath_flow_model.for` | 입자 플럭스 벡터 ($\mathbf{F} = n\mathbf{v}$) | `Best_par_so_far_em4_VAC.par` (MP 5개)<br>`Best_par_so_far_TPS.par` (1632 params) | $10^8\ \mathrm{cm^{-2}s^{-1}}$ | `MSH_FLOW` / `MODEL_TPS` |

### 2.2. 입력 드라이버 변수

1. **태양풍 속도 ($V_{\mathrm{sw}}$)**: $[\mathrm{km/s}]$ (기본 nominal: $400\ \mathrm{km/s}$)
2. **태양풍 양성자 밀도 ($N_{\mathrm{sw}}$)**: $[\mathrm{cm^{-3}}]$ (기본 nominal: $5\ \mathrm{cm^{-3}}$)
3. **태양풍 양성자 열에너지 ($W_{\mathrm{sw}}$)**: $[\mathrm{eV}]$ (기본 nominal: $10\ \mathrm{eV} \approx 1.16 \times 10^5\ \mathrm{K}$)
4. **행성간 자기장(IMF)**: GSM 좌표계 $(B_x, B_y, B_z)\ [\mathrm{nT}]$
5. **지자기 쌍극자 경사각 ($\Psi$)**: Dipole Tilt Angle $[\mathrm{deg}]$ 또는 $[\mathrm{rad}]$

### 2.3. 물리량 변환 및 경계면 조건

- **동압 ($P_{\mathrm{dyn}}$) 및 자기압 ($P_{\mathrm{mag}}$)**:
  $$P_{\mathrm{dyn}} = 1.937 \times 10^{-6} \times N_{\mathrm{sw}} \times V_{\mathrm{sw}}^2\quad [\mathrm{nPa}]$$
  $$P_{\mathrm{mag}} = 0.0004 \times (B_x^2 + B_y^2 + B_z^2)\quad [\mathrm{nPa}]$$
- **열에너지 $\to$ 절대온도 환산**:
  $$T = W \times \frac{e}{k_B} \approx W \times 11604.525\quad [\mathrm{K}]$$
  - 예: 태양풍 $10\ \mathrm{eV} \to 1.16 \times 10^5\ \mathrm{K}$ ($0.116\ \mathrm{MK}$)
  - 마그네토시스 내부 $250\ \mathrm{eV} \to 2.90 \times 10^6\ \mathrm{K}$ ($2.90\ \mathrm{MK}$)
- **플럭스 $\to$ 벌크 속도 환산**:
  포트란 유동 모델의 출력 $\mathbf{F} = (F_x, F_y, F_z)$는 단위가 $10^8\ \mathrm{cm^{-2}s^{-1}}$입니다. 태양풍 영역에서 $F_x = -V_{\mathrm{sw}} N_{\mathrm{sw}} / 1000$으로 스케일링되어 있으므로, 국소 밀도 $N_p\ [\mathrm{cm^{-3}}]$를 결합하여 실제 벌크 유속 $\mathbf{v}$를 도출합니다:
  $$\mathbf{v} = \frac{\mathbf{F} \times 1000}{N_p}\quad [\mathrm{km/s}]$$
- **경계면 판정**:
  - **보우 쇼크(Bow Shock, BS)**: Lu et al. (2019) 경험적 축대칭 모델 (`SUBROUTINE BS`)
  - **자기권계면(Magnetopause, MP)**: Lin et al. (2010) 고정밀 비대칭 모델 (`SUBROUTINE LIN_ET_AL_2010`)
  - 영역 분기:
    - $R \le R_{\mathrm{MP}}$ 또는 $R \le 1.0\ R_E$: 자기권 내부 (값 0 또는 마스킹)
    - $R > R_{\mathrm{BS}}$: 태양풍 영역 ($N_p = N_{\mathrm{sw}}$, $W = W_{\mathrm{sw}}$, $V_x = -V_{\mathrm{sw}}$)
    - $R_{\mathrm{MP}} < R \le R_{\mathrm{BS}}$: 마그네토시스 영역 (모델 팽창식으로 실시간 평가)

---

## 3. 대표 시나리오별 플라즈마 분포 및 물리적 해석

### 3.1. Case 1: 정오-자정 자오면 (Noon-Midnight Meridian, Northward IMF)

- **조건**: $V_{\mathrm{sw}} = 400\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 5\ \mathrm{cm^{-3}}$, $W_{\mathrm{sw}} = 10\ \mathrm{eV}$, $\mathbf{B}_{\mathrm{IMF}} = (0, 0, +5)\ \mathrm{nT}$, $\Psi = 0^\circ$

![Meridional Northward Distribution](msh_meridional_distribution.png)
*(그림 1: 북향 자기장 하에서 정오-자정 자오면($Y_{\mathrm{GSM}}=0$)의 마그네토시스 플라즈마 분포)*

> [!note] 물리적 특징 분석
> 1. **양성자 밀도 ($N_p$)**:
>    - 아태양점(Subsolar nose, $X \approx 11\sim 14\ R_E$)에서 태양풍 밀도($5\ \mathrm{cm^{-3}}$) 대비 약 5배인 **$25\sim 28\ \mathrm{cm^{-3}}$까지 강력한 압축(Pile-up)** 이 발생합니다.
>    - 북향 IMF 조건에서는 아태양 부근의 마그네토시스 자기장과 지구 쌍극자 자기장이 같은 방향이어서 재결합에 의한 플라즈마 배출이 억제되고 강하게 축적됩니다.
> 2. **벌크 속도 ($|V|$) 및 유선(Streamlines)**:
>    - 태양풍 영역에서 $-400\ \mathrm{km/s}$로 직진하던 유동이 충격파(Bow Shock)를 통과하며 아태양 정체 영역(Stagnation point)에서 **$\sim 15\ \mathrm{km/s}$로 급격히 감속**됩니다.
>    - 정체된 플라즈마는 자기권계면을 따라 남·북 극첨두(Cusp) 방향으로 매끄럽게 우회 굴절되며, 고위도 및 후방으로 가면서 다시 $300\sim 360\ \mathrm{km/s}$로 가속되어 흘러나갑니다.
> 3. **양성자 온도 ($T$) 및 열에너지 ($W$)**:
>    - 감속된 플라즈마 유동의 거시적 운동에너지가 충격파 후방에서 열에너지로 전이되면서 아태양 부근의 온도가 **$3.0\times 10^6\ \mathrm{K}$ ($W \approx 260\sim 290\ \mathrm{eV}$)** 이상으로 강력하게 가열됩니다.

---

### 3.2. Case 2: 적도면 (Equatorial Plane, Parker Spiral IMF)

- **조건**: $V_{\mathrm{sw}} = 400\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 5\ \mathrm{cm^{-3}}$, $W_{\mathrm{sw}} = 10\ \mathrm{eV}$, $\mathbf{B}_{\mathrm{IMF}} = (-4, +5, 0)\ \mathrm{nT}$ (파커 나선각), $\Psi = 0^\circ$

![Equatorial Distribution](msh_equatorial_distribution.png)
*(그림 2: 파커 나선각 IMF 하에서 적도면($Z_{\mathrm{GSM}}=0$)의 마그네토시스 플라즈마 분포)*

> [!note] 물리적 특징 분석
> 1. **새벽-황혼 비대칭 (Dawn-Dusk Asymmetry)**:
>    - IMF의 $B_x, B_y$ 성분에 의해 충격파와 자기장 사이의 각도 $\theta_{Bn}$이 달라집니다.
>    - **황혼 측 ($Y > 0$, Quasi-perpendicular shock)**: 충격파 법선과 자기장이 수직에 가까워 자기장 압축과 유체 유선 편향이 강하게 일어납니다.
>    - **새벽 측 ($Y < 0$, Quasi-parallel shock)**: 파동-입자 상호작용 및 난류성 수송이 활발하여 비대칭적인 유동 및 밀도 피크 편향이 발생합니다.
> 2. **유선 편향**:
>    - Subsolar 정체점이 대칭 축에서 약간 벗어나며, 황혼과 새벽 측으로 빠져나가는 유출 속도 벡터에 Tangential 성분이 강하게 형성됩니다.

---

### 3.3. Case 3: 남향 자기장 (Southward IMF, $B_z = -5\ \mathrm{nT}$)

- **조건**: $V_{\mathrm{sw}} = 400\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 5\ \mathrm{cm^{-3}}$, $W_{\mathrm{sw}} = 10\ \mathrm{eV}$, $\mathbf{B}_{\mathrm{IMF}} = (0, 0, -5)\ \mathrm{nT}$, $\Psi = 0^\circ$

![Southward IMF Distribution](msh_meridional_southward.png)
*(그림 3: 남향 자기장 하에서 정오-자정 자오면의 마그네토시스 플라즈마 분포)*

> [!important] 북향 IMF 대비 핵심 차이점
> 1. **자기권계면 침식 (Dayside Magnetopause Erosion)**:
>    - Dungey 형태의 데이사이드 자기 재결합(Dayside Reconnection)에 의해 자기권계면의 서브솔라 거리가 북향($\approx 11.6\ R_E$)에 비해 **약 $1\ R_E$ 지구 쪽($\approx 10.6\ R_E$)으로 수축**됩니다.
> 2. **아태양 밀도 감소 및 Cusp 제트 방출**:
>    - 아태양 정체 영역의 밀도 피크가 재결합에 의해 플라즈마가 극방향으로 배출(draining)되면서 북향 대비 약 $2\sim 4\ \mathrm{cm^{-3}}$ 낮아집니다.
>    - Cusp 부근에서 남북 방향으로 뿜어져 나가는 유동 텅(Tongue) 구조가 형성됩니다.

---

### 3.4. Case 4: 지자기 쌍극자 경사 (Tilted Dipole, $\Psi = +25^\circ$)

- **조건**: $V_{\mathrm{sw}} = 400\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 5\ \mathrm{cm^{-3}}$, $W_{\mathrm{sw}} = 10\ \mathrm{eV}$, $\mathbf{B}_{\mathrm{IMF}} = (0, 0, +5)\ \mathrm{nT}$, $\Psi = +25^\circ$ (북반구 여름)

![Tilted Dipole Distribution](msh_meridional_tilted.png)
*(그림 4: 지자기 쌍극자가 태양 쪽으로 $25^\circ$ 기울어진 경우의 정오-자정 자오면 플라즈마 분포)*

> [!important] 남북 비대칭(North-South Asymmetry) 및 Cusp Pile-up
> 1. **지자기축($\mathbf{M}$) 경사 효과**:
>    - 북반구 극첨두(Summer Cusp, $Z > 0$)가 태양풍 유입 방향에 정면으로 노출됩니다.
> 2. **국소 자기벽(Magnetic Wall)에 의한 밀도 축적**:
>    - 노출된 북반구 Cusp 상부의 강한 지자기 로브(Lobe) 자기장이 '자기벽' 역할을 하여 태양풍 유동을 급격히 제동합니다.
>    - 결과적으로 **북반구 Cusp 바로 위쪽 마그네토시스 영역에서 밀도($N_p > 26\ \mathrm{cm^{-3}}$)와 온도가 극적으로 치솟는 강한 남북 비대칭 축적(Pile-up)** 이 나타납니다.

---

## 4. 코드 구현 및 실행 가이드

### 4.1. 작업 파일 구조

```
c:\Users\slee122\OneDrive - NASA\Desktop\Work\JSokol\MSheath\
├── Magnetosheath_density_sample_code.for  # 원본 밀도 코드 (2025)
├── Magnetosheath_energy_sample_code.for   # 원본 에너지 코드 (2025)
├── Magnetosheath_flow_model.for           # 원본 유동 코드 (2024)
├── Density_Best_par_so_far_em6.par       # 밀도 모델 파라미터 파일
├── Energy_Best_par_so_far_em6.par        # 에너지 모델 파라미터 파일
├── Best_par_so_far_em4_VAC.par           # 자기권계면 형상 파라미터 파일
├── Best_par_so_far_TPS.par               # 유동 모델 파라미터 파일
├── msh_combined.for                      # [통합] 세 모델 결합 단일 드라이버 코드
├── visualize_msh_distributions.py        # [실행] 그리드 연산 및 300DPI 플롯 스크립트
├── run_additional_cases.py               # [실행] 남향 IMF 및 경사각 케이스 스크립트
├── msh_meridional_distribution.png       # Case 1 플롯 이미지
├── msh_equatorial_distribution.png       # Case 2 플롯 이미지
├── msh_meridional_southward.png          # Case 3 플롯 이미지
└── msh_meridional_tilted.png             # Case 4 플롯 이미지
```

### 4.2. 포트란 컴파일 시 주의사항 (Troubleshooting Log)

> [!warning] 컴파일 최적화 옵션 주의
> - 원본 포트란 77 코드에는 레이블을 공유하는 비블록 형태의 구형 DO 루프(`DO 100 ... 100 F(1)=F(1)+...`)가 다수 포함되어 있습니다.
> - 최신 `gfortran`에서 `-O2` 이상의 높은 최적화 레벨을 사용할 경우 루프 레지스터 벡터화 과정에서 계산 순서 왜곡으로 인한 `NaN` 부동소수점 예외가 발생할 수 있습니다.
> - 반드시 **`-O1` 또는 `-O0` 플래그**와 **`-ffixed-line-length-none`** 옵션을 함께 사용하여 컴파일해야 전 구간에서 정확한 실수 연산이 보장됩니다:
>   ```bash
>   gfortran -O1 -ffixed-line-length-none msh_combined.for -o msh_calc_grid
>   ```

### 4.3. 임의의 태양풍 조건 시뮬레이션 방법

파이썬 환경에서 다음과 같이 원하는 조건으로 즉시 계산하고 플롯할 수 있습니다:

```python
from visualize_msh_distributions import run_grid, plot_case

# 예: 고속 태양풍(600 km/s) 및 강한 남향 자기장(-10 nT) 조건 계산
run_grid(
    plane_type=1,           # 1 = X-Z 자오면, 2 = X-Y 적도면
    vsw=600.0,              # 태양풍 속도 (km/s)
    dsw=8.0,                # 태양풍 양성자 밀도 (cm^-3)
    wsw=15.0,               # 태양풍 양성자 열에너지 (eV)
    bx=0.0, by=0.0, bz=-10.0,# IMF (nT)
    psi=0.0,                # 지자기 경사각 (도)
    xmin=-15.0, xmax=20.0, dx=0.25,
    gmin=-18.0, gmax=18.0, dg=0.25,
    outfile="custom_run.dat"
)

# 플롯 생성
plot_case(
    dat_file="custom_run.dat",
    title_text="Storm-time Compressed Magnetosheath Distribution",
    coord_label="Z",
    save_path="custom_run_plot.png",
    xmin=-15.0, xmax=20.0, gmin=-18.0, gmax=18.0
)
```

---

## 5. 요약 및 연구 활용 권장사항

1. **단일 점(Single point) 및 전역 그리드(Grid) 일관성**:
   - 세 코드는 구면조화함수(Spherical Harmonics) 팽창식에 기반하므로, 위성 관측 궤적을 따른 1차원 시계열 데이터 가상 관측(Virtual Spacecraft Flyby)과 전역 2차원/3차원 공간 맵핑에 완벽히 호환됩니다.
2. **SMILE 미션 및 다중 위성 분석 연계**:
   - 밀도($N_p$) 분포는 전하교환(Charge Exchange) 연X선 방출률 산출의 입력값으로 직결되며, 속도 유선 및 온도 분포는 MMS, THEMIS의 실제 통과 시 관측된 플라즈마 모멘트와의 정량적 잔차(Residual) 분석에 즉시 활용할 수 있습니다.
