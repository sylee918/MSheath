---
project: Tsyganenko
type: bugfix
date: 2026-11-10
---

# NAS Pleiades Geopack IGRF 오프라인 로드 오류 분석 및 해결

## 1. 발생 에러 요약 (`MSH_TEST.o25372686`)
NASA Pleiades `devel` 큐(노드 `r141i5n5`)에서 테스트 잡 실행 중 아래 에러와 함께 파이프라인이 중단됨:

```text
Load IGRF coefficients ...
Failed to get the list of IGRF coefficients.
Traceback (most recent call last):
  File "/nobackupp28/slee122/MSheath/test_hpc_pipeline.py", line 11, in <module>
    from grid_engine import get_msh_lib
  File "/nobackupp28/slee122/MSheath/grid_engine.py", line 16, in <module>
    from coord_transform import compute_epoch_rotations, gse_to_gsm_coords, gsm_to_gse_vector
  File "/nobackupp28/slee122/MSheath/coord_transform.py", line 31, in <module>
    from geopack import geopack as _gp
  File "/home6/slee122/.local/lib/python3.11/site-packages/geopack/geopack.py", line 1442, in <module>
    init_igrf()
  File "/home6/slee122/.local/lib/python3.11/site-packages/geopack/geopack.py", line 78, in init_igrf
    version = max(versions, key=int)
              ^^^^^^^^^^^^^^^^^^^^^^
ValueError: max() arg is an empty sequence
```

---

## 2. 원인 분석 (Root Cause)
1. **Pleiades 계산 노드 네트워크 단절**:
   - 계산 노드(`r141i5n5` 등)는 외부 인터넷 접속이 차단되어 있음.
2. **`geopack` 모듈의 기본 동작**:
   - `geopack`은 `import`될 때 자동으로 `init_igrf()` -> `update_igrf()`를 호출하여 NOAA 웹사이트(`http://www.ngdc.noaa.gov/IAGA/vmod/coeffs/`)에서 최신 IGRF 계수 파일(`igrf*coeffs.txt`) 목록을 다운로드하려고 시도함.
   - 프론트엔드(`pfe`)에서 `pip install geopack`만 수행하고 한 번도 `import`하지 않은 채 계산 노드로 잡을 던졌기 때문에, 계산 노드에서 최초 import가 일어남.
   - 외부망 접속 실패로 다운로드가 생략되었고, `~/.local/lib/python3.11/site-packages/geopack/igrf_coeffs/` 디렉토리가 비어 있는 상태(`versions = []`)로 남아 `max(versions)`에서 `ValueError` 발생.

---

## 3. 해결 방안 (Permanent Fix)
1. **IGRF 계수 파일 번들링 (`assets/igrf_coeffs/`)**:
   - 공식 IGRF 계수 파일(`igrf9coeffs.txt` ~ `igrf14coeffs.txt`)을 레포지토리 내 `assets/igrf_coeffs/`에 포함.
2. **사전 자동 복사 로직 구현 (`coord_transform.py`)**:
   - `from geopack import geopack` 임포트 직전에 `_ensure_geopack_coeffs()` 함수를 실행.
   - 만약 사용자의 `geopack/igrf_coeffs/` 디렉토리에 계수 파일이 없으면, 레포지토리의 번들 파일들을 즉시 복사하여 세팅하도록 구성.
   - 계산 노드가 오프라인 상태여도 인터넷 요청 없이 로컬 계수 파일(IGRF 13/14)을 즉각 로드할 수 있도록 완전 격리 자립형으로 전환.
3. **프론트엔드 다운로드 스크립트 보강 (`download_omni.sh`)**:
   - 프론트엔드에서 데이터 다운로드 시 `geopack`도 함께 사전 초기화(`import geopack.geopack`)하도록 1줄 추가.

---

## 4. 검증 결과
- 로컬 환경(WSL)에서 `python3 test_hpc_pipeline.py` 실행 검증 완료:
  - `[Test 1] Fortran Shared Library (libmsh.so)`: 29,161 그리드 포인트 95ms 통과.
  - `[Test 2] OMNI Loader & GSM<->GSE Transform`: 직교성 오차 $2.22 \times 10^{-16}$, 왕복 오차 $1.07 \times 10^{-14} R_E$ 통과.
  - `[Test 3] End-to-End Pipeline & NetCDF4`: 월별 288 스텝 NetCDF 생성(26.97 MB) 및 $X_{\mathrm{GSE}} < 0$ 슬라이스 마스킹 검증 완료.
- 변경 사항 GitHub 반영 완료: Commit `576d8dd`.
