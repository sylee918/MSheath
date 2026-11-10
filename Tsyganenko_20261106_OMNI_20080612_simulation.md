---
project: Tsyganenko
type: analysis
date: 2026-11-06
---

# Tsyganenko Magnetosheath Model: 2008-06-12 OMNI Event Simulation & Colorbar Saturation / Extrapolation Masking

## 1. 개요 (Overview)
본 문서는 Tsyganenko et al. (2024, 2025)의 경험적 마그네토시스(Magnetosheath) 모델을 바탕으로, 태양활동 극소기(Solar Minimum) 조건인 **2008년 6월 12일 06:00 UT** OMNI 관측 데이터를 입력하여 자기권계면(Magnetopause) 및 충격파(Bow Shock) 위치와 시스 내부 플라즈마 파라미터($N_p, T, |V|, V_x, V_y, V_z$)의 공간 분포를 산출·분석한 작업 노트이다.

또한, 2018년 1월 1일 사례에서 발견된 **자오면 북극 고위도 야간측($X < 0, Z > 12\ R_E$)의 비물리적 속도 발산 원인**을 Tsyganenko et al. (2024) 논문의 유효 범위(Validity boundary) 및 피팅 메커니즘 관점에서 규명하고, **적도면은 전체 범위($X \in [-10, 20]\ R_E$)를 유지하되 자오면은 $X < 0$ 전 영역을 회색 빗금(Hatch)으로 마스킹**하여 논문(Figure 10)과 동일한 기준의 물리적 시각화를 정립하였다.

---

## 2. OMNI 관측 조건 비교 (2018-01-01 vs 2008-06-12)

| 파라미터 | 2018-01-01 00:00 UT (00:01 UT) | 2008-06-12 06:00 UT (Solar Minimum) | 물리적 의미 및 영향 |
| :--- | :--- | :--- | :--- |
| **태양풍 속도 ($V_{\mathrm{sw}}$)** | $370.0\ \mathrm{km/s}$ | **$319.0\ \mathrm{km/s}$** | 저속 태양풍 스트림 |
| **양성자 밀도 ($N_{\mathrm{sw}}$)** | $13.46\ \mathrm{cm^{-3}}$ | **$6.90\ \mathrm{cm^{-3}}$** | 극소기 특유의 희박한 밀도 (절반 수준) |
| **양성자 온도 ($T_{\mathrm{sw}}$)** | $75,417\ \mathrm{K}$ | **$17,726\ \mathrm{K}$** | 극도로 차가운 태양풍 |
| **열에너지 ($W_{\mathrm{sw}}$)** | $6.50\ \mathrm{eV}$ | **$1.53\ \mathrm{eV}$** | 모델 입력값 ($k_B T / e$) |
| **IMF $B_x, B_y, B_z$ (GSM)** | $(+1.54, -6.64, -4.20)\ \mathrm{nT}$ | **$(+0.60, +0.60, +1.60)\ \mathrm{nT}$** | 남향($B_z < 0$) vs **북향($B_z > 0$)** |
| **IMF 크기 ($|B_{\mathrm{IMF}}|$)** | $7.99\ \mathrm{nT}$ | **$1.81\ \mathrm{nT}$** | 자기장 세기 4.4배 감소 |
| **지구 자기쌍극자 기울기 ($\Psi$)** | $-25.40^\circ$ (북반구 겨울) | **$+13.57^\circ$ (북반구 여름)** | 태양 방향으로 북극이 기욺 |
| **동압 ($P_{\mathrm{dyn}} = \rho V^2$)** | **$3.08\ \mathrm{nPa}$** | **$1.16\ \mathrm{nPa}$** | **동압 약 2.7배 감소** |
| **자기권계면 정체점 ($X_{\mathrm{MP}}$)** | **$\approx 9.5\ R_E$** | **$\approx 11.2\ R_E$** | **자기권이 외부로 대폭 확장** |
| **보우쇼크 정체점 ($X_{\mathrm{BS}}$)** | **$\approx 12.8\ R_E$** | **$\approx 14.8\ R_E$** | **보우쇼크도 전방으로 크게 확장** |

---

## 3. 자오면 야간측($X < 0$) 마스킹 및 유효 범위 정립

### 3.1 논문 명시 근거 (Tsyganenko et al. 2024, JGR, Section 5, Fig. 10)
- *"Unlike in the previous Figure 9, the plots are limited to only the dayside, due to virtually no high-latitude data at the nightside and, hence, invalid model results in that region."*
- 위성 궤도(THEMIS, MMS, Cluster)상 자오면 야간측 고위도는 관측 데이터가 존재하지 않으며, 이 영역의 다항식 외삽값은 수학적으로 무의미한 발산(분모 $N_p \to 0$에 의한 $V \approx 250,000\ \mathrm{km/s}$)을 초래함.

### 3.2 영역별 마스킹 정책
1. **적도면 (Equatorial Plane, $Z=0$)**:
   - THEMIS, MMS 등의 궤도로 인해 $X \ge -10\ R_E$까지 데이터가 충분히 커버되므로, **$X \in [-10, 20]\ R_E, Y \in [-30, 30]\ R_E$ 전 영역을 원형 그대로 유지**.
2. **자오면 (Meridional Plane, $Y=0$)**:
   - 공간 축 범위는 $X \in [-10, 20]\ R_E, Z \in [-30, 30]\ R_E$로 통일하되, **$X < 0$ 전 영역을 회색 대각 빗금(Hatch `///`)으로 마스킹**하여 주간측($X \ge 0$) 물리량만 명확히 노출.

---

## 4. 2018년 1월 1일 최종 시뮬레이션 결과

### 4.1 자오면 분포 ($Y = 0$, $X < 0$ Masked)
![2018-01-01 Meridional Masked](omni_20180101_meridional_masked.png)

- $X < 0$ 전 영역이 회색 빗금으로 명확히 마스킹되어 비물리적 색상 왜곡(Solid Red/Blue 아티팩트)이 완전히 제거됨.
- 주간측($X \ge 0$) 마그네토시스 유선이 보우쇼크를 통과해 자기권계면을 따라 매끄럽게 우회함.

### 4.2 적도면 분포 ($Z = 0$, Full Domain)
![2018-01-01 Equatorial Masked](omni_20180101_equatorial_masked.png)

- 적도면은 $X \ge -10\ R_E$까지 안정적으로 계산되며, 포화 없는 동적 스케일링으로 정체점 밀도($\sim 80\ \mathrm{cm^{-3}}$) 및 $V_y$의 새벽-황혼 대칭 유동이 선명하게 표현됨.

---

## 5. 2008년 6월 12일 06:00 UT (태양활동 극소기) 시뮬레이션 결과

### 5.1 자오면 분포 ($Y = 0$, $X < 0$ Masked)
![2008-06-12 Meridional Masked](omni_20080612_meridional_masked.png)

- 북반구 여름 쌍극자 기울기($\Psi = +13.6^\circ$)와 저속 태양풍($319\ \mathrm{km/s}$) 조건.
- $V_z$ 패널에서 정체점 분기(북반구 $V_z > 0$, 남반구 $V_z < 0$)가 주간측에서 명확하게 대비됨.

### 5.2 적도면 분포 ($Z = 0$, Full Domain)
![2008-06-12 Equatorial Masked](omni_20080612_equatorial_masked.png)

- 낮은 동압($1.16\ \mathrm{nPa}$)에 의해 자기권계면($X \approx 11.2\ R_E$)과 보우쇼크($X \approx 14.8\ R_E$)가 크게 확장된 상태를 직관적으로 확인 가능.
