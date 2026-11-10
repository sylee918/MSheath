with open("msh_combined.for", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Find line where SUBROUTINE LIN_ET_AL_2010 starts
sub_start = None
for idx, line in enumerate(lines):
    if "SUBROUTINE LIN_ET_AL_2010" in line:
        sub_start = idx - 1
        break

assert sub_start is not None, "Could not find LIN_ET_AL_2010"

header_code = """C=====================================================================
C  MSH_CORE_LIB.FOR - Shared Library Wrapper for Tsyganenko (2024, 2025)
C  Exposes C-callable subroutines: msh_init() and msh_eval_batch(...)
C=====================================================================

      SUBROUTINE MSH_INIT() BIND(C, NAME="msh_init")
      USE ISO_C_BINDING
      IMPLICIT REAL*8 (A-H,O-Z)
C
      PARAMETER (NLIN_D=1605, NNON_D=4, NTOT_D=1609)
      PARAMETER (NLIN_E=1605, NNON_E=4, NTOT_E=1609)
      PARAMETER (NLIN_F=1632, NNON_F=5, NTOT_F=1637)
      PARAMETER (NMAX_D=10, NMAX_F=8)
C
      DIMENSION A_VAC(NNON_F), A_TPS(NLIN_F)
C
      COMMON /MODEL_PARAMS/ A_DEN(NTOT_D), A_ENE(NTOT_E),
     *                      IA_DEN(NTOT_D), IA_ENE(NTOT_E),
     *                      IA_FLO(NLIN_F)
      COMMON /SCHMIDT_DEN/ SNM_DEN(0:NMAX_D,0:NMAX_D)
      COMMON /RS0_ALP_DEN/ RS0_DEN, ALP_DEN
      COMMON /SCHMIDT_ENE/ SNM_ENE(0:NMAX_D,0:NMAX_D)
      COMMON /RS0_ALP_ENE/ RS0_ENE, ALP_ENE
      COMMON /SCHMIDT_FLO/ SNM_FLO(0:NMAX_F,0:NMAX_F)
      COMMON /NONLINEARS/ RS0_FLO,EPS_FLO,DFSC_FLO,ALP0_FLO,ALP1_FLO,
     *                    FSC_FLO,ALP_FLO
      COMMON /PAR_TPS/ A_TPS_COM(NLIN_F)
C
      DO J=1,NTOT_D
        IA_DEN(J) = 1
      ENDDO
      DO J=1,NTOT_E
        IA_ENE(J) = 1
      ENDDO
      DO J=1,NLIN_F
        IA_FLO(J) = 1
      ENDDO
C
C 1. LOAD DENSITY PARAMETERS
      OPEN(UNIT=11, FILE='Density_Best_par_so_far_em6.par', STATUS='OLD')
      READ(11, 811) (A_DEN(J), J=1,NTOT_D)
      CLOSE(11)
      RS0_DEN = 11.0D0
      ALP_DEN = 0.7D0
C
C 2. LOAD ENERGY PARAMETERS
      OPEN(UNIT=12, FILE='Energy_Best_par_so_far_em6.par', STATUS='OLD')
      READ(12, 811) (A_ENE(J), J=1,NTOT_E)
      CLOSE(12)
      RS0_ENE = 11.0D0
      ALP_ENE = 0.7D0
C
C 3. LOAD FLOW PARAMETERS
      OPEN(UNIT=13, FILE='Best_par_so_far_em4_VAC.par', STATUS='OLD')
      DO J=1, 4+NNON_F
        IF (J .LE. 4) READ(13, 811) DUMMY
        IF (J .GT. 4) READ(13, 811) A_VAC(J-4)
      ENDDO
      CLOSE(13)
      RS0_FLO  = A_VAC(1)*10.D0
      EPS_FLO  = A_VAC(2)
      DFSC_FLO = A_VAC(3)
      ALP0_FLO = A_VAC(4)
      ALP1_FLO = A_VAC(5)
C
      OPEN(UNIT=14, FILE='Best_par_so_far_TPS.par', STATUS='OLD')
      READ(14, 811) (A_TPS(J), J=1,NLIN_F)
      CLOSE(14)
      DO J=1,NLIN_F
        A_TPS_COM(J) = A_TPS(J)
      ENDDO
C
 811  FORMAT(G15.6)
C
C 4. INITIALIZE SCHMIDT FACTORS
      SNM_DEN(0,0)=1.D0
      DO N=1,NMAX_D
        SNM_DEN(N,0)=SNM_DEN(N-1,0)*DFLOAT(2*N-1)/N
        DO M=1,NMAX_D
          IF (M.EQ.1) THEN
            XJ=2.D0
          ELSE
            XJ=1.D0
          ENDIF
          SNM_DEN(N,M)=SNM_DEN(N,M-1)*SQRT(DFLOAT(N-M+1)*XJ/(N+M))
        ENDDO
      ENDDO
C
      DO N=0,NMAX_D
        DO M=0,NMAX_D
          SNM_ENE(N,M) = SNM_DEN(N,M)
        ENDDO
      ENDDO
C
      SNM_FLO(0,0)=1.D0
      DO N=1,NMAX_F
        SNM_FLO(N,0)=SNM_FLO(N-1,0)*DFLOAT(2*N-1)/N
        DO M=1,NMAX_F
          IF (M.EQ.1) THEN
            XJ=2.D0
          ELSE
            XJ=1.D0
          ENDIF
          SNM_FLO(N,M)=SNM_FLO(N,M-1)*SQRT(DFLOAT(N-M+1)*XJ/(N+M))
        ENDDO
      ENDDO
C
      RETURN
      END

C=====================================================================
      SUBROUTINE MSH_EVAL_BATCH(N_PTS, XGSM, YGSM, ZGSM,
     *                          VSW, DSW, WSW, BXIMF, BYIMF, BZIMF, PSID,
     *                          DEN_OUT, TK_OUT, VX_OUT, VY_OUT, VZ_OUT,
     *                          RBS_OUT, RMP_OUT, IFLAG_OUT)
     *                          BIND(C, NAME="msh_eval_batch")
      USE ISO_C_BINDING
      IMPLICIT REAL*8 (A-H,O-Z)
C
      INTEGER(C_INT), VALUE, INTENT(IN) :: N_PTS
      REAL(C_DOUBLE), VALUE, INTENT(IN) :: VSW, DSW, WSW
      REAL(C_DOUBLE), VALUE, INTENT(IN) :: BXIMF, BYIMF, BZIMF, PSID
      REAL(C_DOUBLE), INTENT(IN)  :: XGSM(N_PTS), YGSM(N_PTS), ZGSM(N_PTS)
      REAL(C_DOUBLE), INTENT(OUT) :: DEN_OUT(N_PTS), TK_OUT(N_PTS)
      REAL(C_DOUBLE), INTENT(OUT) :: VX_OUT(N_PTS), VY_OUT(N_PTS), VZ_OUT(N_PTS)
      REAL(C_DOUBLE), INTENT(OUT) :: RBS_OUT(N_PTS), RMP_OUT(N_PTS)
      INTEGER(C_INT), INTENT(OUT) :: IFLAG_OUT(N_PTS)
C
      PARAMETER (NLIN_D=1605, NNON_D=4, NTOT_D=1609)
      PARAMETER (NLIN_E=1605, NNON_E=4, NTOT_E=1609)
      PARAMETER (NLIN_F=1632, NNON_F=5, NTOT_F=1637)
      PARAMETER (NMAX_D=10, NMAX_F=8)
      PARAMETER (INDEPVAR=12, NDEPVAR=1)
      PARAMETER (INDPVR_F=10, NDPVR_F=3)
C
      DIMENSION DER_DEN(NLIN_D), DER_ENE(NLIN_E)
      DIMENSION DERX(NLIN_F), DERY(NLIN_F), DERZ(NLIN_F)
      DIMENSION XI(INDEPVAR), F_DEN(NDEPVAR), F_ENE(NDEPVAR)
      DIMENSION XI_F(INDPVR_F), F_FLO(NDPVR_F)
C
      COMMON /MODEL_PARAMS/ A_DEN(NTOT_D), A_ENE(NTOT_E),
     *                      IA_DEN(NTOT_D), IA_ENE(NTOT_E),
     *                      IA_FLO(NLIN_F)
      COMMON /NONLINEARS/ RS0_FLO,EPS_FLO,DFSC_FLO,ALP0_FLO,ALP1_FLO,
     *                    FSC_FLO,ALP_FLO
      COMMON /PAR_TPS/ A_TPS_COM(NLIN_F)
C
      PSI  = PSID * 0.0174532925199D0
      PD   = 1.937D-6 * DSW * VSW**2
      PM   = 0.0004D0 * (BXIMF**2 + BYIMF**2 + BZIMF**2)
      XMS  = 5.7D0
      BETA = 2.9D0
C
      FSC_FLO = (PD/2.0D0)**EPS_FLO + DFSC_FLO*(BZIMF/10.D0)
      ALP_FLO = ALP0_FLO + ALP1_FLO*EXP(-BZIMF/10.D0)
C
      XI(4)  = PSI
      XI(5)  = BXIMF
      XI(6)  = BYIMF
      XI(7)  = BZIMF
      XI(8)  = DSW
      XI(9)  = VSW
      XI(10) = WSW
      XI(11) = PD
      XI(12) = 1.D0
C
      XI_F(4)  = PSI
      XI_F(5)  = BXIMF
      XI_F(6)  = BYIMF
      XI_F(7)  = BZIMF
      XI_F(8)  = VSW
      XI_F(9)  = DSW
      XI_F(10) = PD
C
      DO I = 1, N_PTS
        X = XGSM(I)
        Y = YGSM(I)
        Z = ZGSM(I)
        R = SQRT(X**2 + Y**2 + Z**2)
C
        IF (R .LE. 1.0D0) THEN
          IFLAG = 0
          DEN = 0.D0
          W_EV = 0.D0
          VX = 0.D0
          VY = 0.D0
          VZ = 0.D0
          RBS = 24.D0
          RMP_LIN = 10.D0
        ELSE
          CALL BS(X, Y, Z, PSI, PD, BZIMF, XMS, BETA, RBS, IDBS)
          CALL LIN_ET_AL_2010(X, Y, Z, PSI, PD, PM, BZIMF, RMP_LIN, IDMP)
C
          IF (IDBS .LT. 0 .OR. R .GT. RBS) THEN
            IFLAG = 2
            DEN = DSW
            W_EV = WSW
            VX = -VSW
            VY = 0.D0
            VZ = 0.D0
          ELSE IF (IDMP .GT. 0 .OR. R .LE. RMP_LIN) THEN
            IFLAG = 0
            DEN = 0.D0
            W_EV = 0.D0
            VX = 0.D0
            VY = 0.D0
            VZ = 0.D0
          ELSE
            IFLAG = 1
            XI(1) = X
            XI(2) = Y
            XI(3) = Z
            CALL MODELVEC_DEN(1, A_DEN, XI, F_DEN, DER_DEN, IA_DEN,
     *                        NLIN_D, NTOT_D, NNON_D, INDEPVAR, NDEPVAR)
            DEN = F_DEN(1)
            IF (DEN .LT. 0.D0) DEN = 0.D0
C
            CALL MODELVEC_ENE(1, A_ENE, XI, F_ENE, DER_ENE, IA_ENE,
     *                        NLIN_E, NTOT_E, NNON_E, INDEPVAR, NDEPVAR)
            W_EV = F_ENE(1)
            IF (W_EV .LT. 0.D0) W_EV = 0.D0
C
            XI_F(1) = X
            XI_F(2) = Y
            XI_F(3) = Z
            CALL MODEL_TPS(0, A_TPS_COM, XI_F, F_FLO, DERX, DERY, DERZ,
     *                     IA_FLO, NLIN_F, NLIN_F, INDPVR_F, NDPVR_F)
            FX = F_FLO(1)
            FY = F_FLO(2)
            FZ = F_FLO(3)
C
            IF (DEN .GT. 0.05D0) THEN
              VX = FX * 1000.D0 / DEN
              VY = FY * 1000.D0 / DEN
              VZ = FZ * 1000.D0 / DEN
            ELSE
              VX = 0.D0
              VY = 0.D0
              VZ = 0.D0
            ENDIF
          ENDIF
        ENDIF
C
        DEN_OUT(I)   = DEN
        TK_OUT(I)    = W_EV * 11604.525D0
        VX_OUT(I)    = VX
        VY_OUT(I)    = VY
        VZ_OUT(I)    = VZ
        RBS_OUT(I)   = RBS
        RMP_OUT(I)   = RMP_LIN
        IFLAG_OUT(I) = IFLAG
      ENDDO
C
      RETURN
      END
"""

with open("msh_core_lib.for", "w", encoding="utf-8") as out:
    out.write(header_code)
    out.write("\n")
    out.writelines(lines[sub_start:])

print("Successfully generated msh_core_lib.for")
