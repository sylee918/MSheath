import os

with open('Magnetosheath_density_sample_code.for', 'r', encoding='latin1') as f:
    den_lines = f.readlines()

with open('Magnetosheath_energy_sample_code.for', 'r', encoding='latin1') as f:
    ene_lines = f.readlines()

with open('Magnetosheath_flow_model.for', 'r', encoding='latin1') as f:
    flow_lines = f.readlines()

# Extract LIN_ET_AL_2010 (lines 112 to 191 in density code)
lin_et_al = "".join(den_lines[111:191])

# Extract BS (lines 498 to 557 in density code)
bs_sub = "".join(den_lines[497:557])

# DENSITY SUBROUTINES: MODELVEC, FC_FS, LEGENDASS_SCHMIDT
den_part = "".join(den_lines[193:497])
den_part = den_part.replace('SUBROUTINE MODELVEC ', 'SUBROUTINE MODELVEC_DEN ')
den_part = den_part.replace('CALL FC_FS ', 'CALL FC_FS_DEN ')
den_part = den_part.replace('SUBROUTINE FC_FS ', 'SUBROUTINE FC_FS_DEN ')
den_part = den_part.replace('CALL LEGENDASS_SCHMIDT', 'CALL LEGENDASS_SCHMIDT_DEN')
den_part = den_part.replace('SUBROUTINE LEGENDASS_SCHMIDT', 'SUBROUTINE LEGENDASS_SCHMIDT_DEN')
den_part = den_part.replace('/SCHMIDT/', '/SCHMIDT_DEN/')
den_part = den_part.replace('/RS0_ALP/', '/RS0_ALP_DEN/')

# ENERGY SUBROUTINES: MODELVEC, FC_FS, LEGENDASS_SCHMIDT
ene_part = "".join(ene_lines[193:497])
ene_part = ene_part.replace('SUBROUTINE MODELVEC ', 'SUBROUTINE MODELVEC_ENE ')
ene_part = ene_part.replace('CALL FC_FS ', 'CALL FC_FS_ENE ')
ene_part = ene_part.replace('SUBROUTINE FC_FS ', 'SUBROUTINE FC_FS_ENE ')
ene_part = ene_part.replace('CALL LEGENDASS_SCHMIDT', 'CALL LEGENDASS_SCHMIDT_ENE')
ene_part = ene_part.replace('SUBROUTINE LEGENDASS_SCHMIDT', 'SUBROUTINE LEGENDASS_SCHMIDT_ENE')
ene_part = ene_part.replace('/SCHMIDT/', '/SCHMIDT_ENE/')
ene_part = ene_part.replace('/RS0_ALP/', '/RS0_ALP_ENE/')

# FLOW SUBROUTINES: MSH_FLOW, MODEL_TPS, B_CART, LEGENDASS_SCHMIDT, SHUE
flow_part = "".join(flow_lines[104:806])
flow_part = flow_part.replace('CALL LEGENDASS_SCHMIDT', 'CALL LEGENDASS_SCHMIDT_FLO')
flow_part = flow_part.replace('SUBROUTINE LEGENDASS_SCHMIDT', 'SUBROUTINE LEGENDASS_SCHMIDT_FLO')
flow_part = flow_part.replace('/SCHMIDT/', '/SCHMIDT_FLO/')

main_prog = """
      PROGRAM MSH_CALC_GRID
      IMPLICIT REAL*8 (A-H,O-Z)
      CHARACTER*80 OUTFILE
C
      PARAMETER (NLIN_D=1605, NNON_D=4, NTOT_D=1609)
      PARAMETER (NLIN_E=1605, NNON_E=4, NTOT_E=1609)
      PARAMETER (NLIN_F=1632, NNON_F=5, NTOT_F=1637)
      PARAMETER (NMAX_D=10, NMAX_F=8)
      PARAMETER (INDEPVAR=12, NDEPVAR=1)
      PARAMETER (INDPVR_F=10, NDPVR_F=3)
C
      DIMENSION A_DEN(NTOT_D), IA_DEN(NTOT_D), DER_DEN(NLIN_D)
      DIMENSION A_ENE(NTOT_E), IA_ENE(NTOT_E), DER_ENE(NLIN_E)
      DIMENSION A_VAC(NNON_F), A_TPS(NLIN_F), IA_FLO(NLIN_F)
      DIMENSION DERX(NLIN_F), DERY(NLIN_F), DERZ(NLIN_F)
      DIMENSION XI(INDEPVAR), F_DEN(NDEPVAR), F_ENE(NDEPVAR)
      DIMENSION XI_F(INDPVR_F), F_FLO(NDPVR_F)
      DIMENSION PARMOD(12)
C
      COMMON /SCHMIDT_DEN/ SNM_DEN(0:NMAX_D,0:NMAX_D)
      COMMON /RS0_ALP_DEN/ RS0_DEN, ALP_DEN
C
      COMMON /SCHMIDT_ENE/ SNM_ENE(0:NMAX_D,0:NMAX_D)
      COMMON /RS0_ALP_ENE/ RS0_ENE, ALP_ENE
C
      COMMON /SCHMIDT_FLO/ SNM_FLO(0:NMAX_F,0:NMAX_F)
      COMMON /NONLINEARS/ RS0_FLO,EPS_FLO,DFSC_FLO,ALP0_FLO,ALP1_FLO,
     *                    FSC_FLO,ALP_FLO
      COMMON /PAR_TPS/ A_TPS_COM(NLIN_F)
C
      DATA IA_DEN /NTOT_D*1/
      DATA IA_ENE /NTOT_E*1/
      DATA IA_FLO /NLIN_F*1/
C
C 1. LOAD DENSITY PARAMETERS
      OPEN(UNIT=1, FILE='Density_Best_par_so_far_em6.par', STATUS='OLD')
      READ(1, 811) (A_DEN(J), J=1,NTOT_D)
      CLOSE(1)
      RS0_DEN = 11.0D0
      ALP_DEN = 0.7D0
C
C 2. LOAD ENERGY PARAMETERS
      OPEN(UNIT=1, FILE='Energy_Best_par_so_far_em6.par', STATUS='OLD')
      READ(1, 811) (A_ENE(J), J=1,NTOT_E)
      CLOSE(1)
      RS0_ENE = 11.0D0
      ALP_ENE = 0.7D0
C
C 3. LOAD FLOW PARAMETERS
      OPEN(UNIT=1, FILE='Best_par_so_far_em4_VAC.par', STATUS='OLD')
      DO J=1, 4+NNON_F
        IF (J .LE. 4) READ(1, 811) DUMMY
        IF (J .GT. 4) READ(1, 811) A_VAC(J-4)
      ENDDO
      CLOSE(1)
      RS0_FLO  = A_VAC(1)*10.D0
      EPS_FLO  = A_VAC(2)
      DFSC_FLO = A_VAC(3)
      ALP0_FLO = A_VAC(4)
      ALP1_FLO = A_VAC(5)
C
      OPEN(UNIT=1, FILE='Best_par_so_far_TPS.par', STATUS='OLD')
      READ(1, 811) (A_TPS(J), J=1,NLIN_F)
      CLOSE(1)
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
C 5. READ RUN CONFIGURATION FROM STANDARD INPUT
C    PLANE: 1=XZ (Y=0), 2=XY (Z=0)
C    SW/IMF: VSW, DSW, WSW, BXIMF, BYIMF, BZIMF, PSID
C    GRID: XMIN, XMAX, DX, GMIN, GMAX, DG  (G is Z for plane 1, Y for plane 2)
C    OUTFILE: output filename
      READ(*, *) IPLANE
      READ(*, *) VSW, DSW, WSW, BXIMF, BYIMF, BZIMF, PSID
      READ(*, *) XMIN, XMAX, DX, GMIN, GMAX, DG
      READ(*, '(A)') OUTFILE
C
      PSI = PSID * 0.0174532925199D0
      PD  = 1.937D-6 * DSW * VSW**2
      PM  = 0.0004D0 * (BXIMF**2 + BYIMF**2 + BZIMF**2)
      XMS = 5.7D0
      BETA= 2.9D0
C
      FSC_FLO = (PD/2.0D0)**EPS_FLO + DFSC_FLO*(BZIMF/10.D0)
      ALP_FLO = ALP0_FLO + ALP1_FLO*EXP(-BZIMF/10.D0)
C
      PARMOD(1) = PSI
      PARMOD(2) = BXIMF
      PARMOD(3) = BYIMF
      PARMOD(4) = BZIMF
      PARMOD(5) = VSW
      PARMOD(6) = DSW
      PARMOD(7) = PD
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
      OPEN(UNIT=2, FILE=TRIM(OUTFILE), STATUS='REPLACE')
      WRITE(2, 820) '# X', 'Y', 'Z', 'DEN', 'W_eV', 'T_K',
     *              'VX', 'VY', 'VZ', 'VMAG',
     *              'FX', 'FY', 'FZ', 'RBS', 'RMP', 'IFLAG'
 820  FORMAT(A6,15A14)
C
      NX = NINT((XMAX - XMIN)/DX) + 1
      NG = NINT((GMAX - GMIN)/DG) + 1
C
      DO IX = 1, NX
        X = XMIN + (IX - 1)*DX
        DO IG = 1, NG
          G = GMIN + (IG - 1)*DG
          IF (IPLANE .EQ. 1) THEN
            Y = 0.D0
            Z = G
          ELSE
            Y = G
            Z = 0.D0
          ENDIF
C
          R = SQRT(X**2 + Y**2 + Z**2)
C
C Handle inside Earth / deep inner magnetosphere
          IF (R .LE. 1.0D0) THEN
            IFLAG = 0
            DEN = 0.D0
            W_EV = 0.D0
            FX = 0.D0
            FY = 0.D0
            FZ = 0.D0
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
              FX = -VSW * DSW / 1000.D0
              FY = 0.D0
              FZ = 0.D0
              VX = -VSW
              VY = 0.D0
              VZ = 0.D0
            ELSE IF (IDMP .GT. 0 .OR. R .LE. RMP_LIN) THEN
              IFLAG = 0
              DEN = 0.D0
              W_EV = 0.D0
              FX = 0.D0
              FY = 0.D0
              FZ = 0.D0
              VX = 0.D0
              VY = 0.D0
              VZ = 0.D0
            ELSE
              IFLAG = 1
              XI(1) = X
              XI(2) = Y
              XI(3) = Z
              CALL MODELVEC_DEN(1, A_DEN, XI, F_DEN, DER_DEN, IA_DEN,
     *                          NLIN_D, NTOT_D, NNON_D, INDEPVAR, NDEPVAR)
              DEN = F_DEN(1)
              IF (DEN .LT. 0.D0) DEN = 0.D0
C
              CALL MODELVEC_ENE(1, A_ENE, XI, F_ENE, DER_ENE, IA_ENE,
     *                          NLIN_E, NTOT_E, NNON_E, INDEPVAR, NDEPVAR)
              W_EV = F_ENE(1)
              IF (W_EV .LT. 0.D0) W_EV = 0.D0
C
              XI_F(1) = X
              XI_F(2) = Y
              XI_F(3) = Z
              CALL MODEL_TPS(0, A_TPS_COM, XI_F, F_FLO, DERX, DERY, DERZ,
     *                       IA_FLO, NLIN_F, NLIN_F, INDPVR_F, NDPVR_F)
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
          VMAG = SQRT(VX**2 + VY**2 + VZ**2)
          T_K  = W_EV * 11604.525D0
C
          WRITE(2, 830) X, Y, Z, DEN, W_EV, T_K,
     *                  VX, VY, VZ, VMAG,
     *                  FX, FY, FZ, RBS, RMP_LIN, IFLAG
 830      FORMAT(13F14.4, 2F14.4, I8)
        ENDDO
      ENDDO
C
      CLOSE(2)
      END
"""

with open('msh_combined.for', 'w', encoding='utf-8') as f:
    f.write(main_prog)
    f.write("\nC=====================================================================\n")
    f.write(lin_et_al)
    f.write("\nC=====================================================================\n")
    f.write(bs_sub)
    f.write("\nC=====================================================================\n")
    f.write(den_part)
    f.write("\nC=====================================================================\n")
    f.write(ene_part)
    f.write("\nC=====================================================================\n")
    f.write(flow_part)

print("Generated updated msh_combined.for successfully!")
