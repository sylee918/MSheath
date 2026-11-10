C=====================================================================
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

C=====================================================================
      SUBROUTINE LIN_ET_AL_2010 (X,Y,Z,PSI,PD,PM,BZIMF,RMP_LIN,ID) 
      IMPLICIT REAL*8 (A-H,O-Z)
C
c     (c) N. A. Tsyganenko, Jan.23, 2025
c
C Input: 
C        X,Y,Z: GSM/GSW coordinates of a point 
c        PSI: dipole tilt in radians
c        PD: s.w. ram pressure in nPa
c        PM: s.w. magnetic pressure in nPa: PM = 0.0004*SQRT(BXIMF**2+BYIMF**2+BZIMF**2)
c        BZIMF: IMF Bz in nT
C
C Output:
c        RMP_LIN:  geocentric distance to the magnetopause along the ray vector {X,Y,Z}
c        ID: integer flag; ID=+1/-1, if the point {X,Y,Z} is inside/outside the MP, respectively

      DATA A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,
     * A17,A18,A19,A20,A21/12.544D0,-0.194D0,0.305D0,0.0573D0,2.178D0,
     * 0.0571D0,-0.999D0,16.473D0,0.00152D0,0.382D0,0.0431D0,-0.00763D0,
     * -0.210D0,0.0405D0,-4.430D0,-0.636D0,-2.600D0,0.832D0,-5.328D0,
     * 1.103D0,-0.907D0,1.450D0/
C
      A10=0.D0  !  ELIMINATE RESIDUAL TILT-UNRELATED ASYMMETRIES
      A11=0.D0
      A12=0.D0
      A13=0.D0

      EN=A21
      ES=A21
      THETAN=A19+A20*PSI
      THETAS=A19-A20*PSI
      CTN=DCOS(THETAN)
      CTS=DCOS(THETAS)
      STN=DSIN(THETAN)
      STS=DSIN(THETAS)

      R=SQRT(X**2+Y**2+Z**2)
      CT=X/R                    
      ST=SQRT(Y**2+Z**2)/R
      THETA=DATAN2(ST,CT)
   
      RHO=SQRT(Y**2+Z**2)  
      IF (RHO.LT.1.D-8.AND.X.GT.1.D-6) RHO=1.D-8
      IF (RHO.LT.1.D-8.AND.X.LT.0.D0) THEN
c      PRINT *, ' INVALID DEEP TAIL LOCATION'
      RETURN
      ENDIF
      CP=Y/RHO
      SP=Z/RHO

      BRN=CT*CTN+ST*STN*SP
      PSIN=DACOS(BRN)
      BRS=CT*CTS-ST*STS*SP
      PSIS=DACOS(BRS)

      DN=A16+(A17+A18*PSI)*PSI
      DS=A16-(A17-A18*PSI)*PSI

      CN=A14*(PD+PM)**A15
      CS=CN

      B0=A6+A7*(DEXP(A8*BZIMF)-1.D0)/(DEXP(A9*BZIMF)+1.D0)
      B1=A10
      B2=A11+A12*PSI
      B3=A13
      BETA=B0+B1*CP+B2*SP+B3*SP**2
      BRF=DSQRT(0.5D0*(1.D0+CT))+A5*2.D0*ST*CT*(1.D0-DEXP(-THETA))

      F=BRF**BETA
      R0=A0*(PD+PM)**A1*(1.D0+A2*(DEXP(A3*BZIMF)-1.D0)/(DEXP(A4*BZIMF)
     * +1.D0))
      RMP_LIN=R0*F+CN*DEXP(DN*PSIN**EN)+CS*DEXP(DS*PSIS**ES)
      IF (RMP_LIN.GT.R) THEN
      ID=1
      ELSE
      ID=-1
      ENDIF
c
      RETURN
      END

C=====================================================================
      SUBROUTINE BS (X,Y,Z,PSI,PD,BZIMF,XMS,BETA,RBS,ID)   ! XMS & BETA are magnetosonic Mach number & plasma beta (from OMNI)
C
c     Based on bow shock model by Lu et al., 2019;
c     
c     Input:  X,Y,Z (in Re, GSM or GSE, does not matter, since the model BS shape is assumed axisymmetric around X)
c             PSI (tilt angle in radians; again, here does not affect anything due to the symmetry)
c             PD (ram pressure from OMNI; not sure if Lu et al. included the alpha-particle component)
c             BZIMF
c             BETA (plasma beta)
c
c     Output: RBS (geocentric distance to the B.S. in the direction of the {X,Y,Z} point
c             ID (position flag; equals 1 or -1, if the {X,Y,Z} point is inside or outside the BS, resp.
c
      IMPLICIT REAL*8 (A-H,O-Z)
      DIMENSION AA(20)
C
      DATA A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,
     * A18,A19,A20/13.132D0,4.5875D0,.0016D0,.3341D0,6.1115D0,18.9096D0,
     *0.3029D0,0.0429D0,-0.0056D0,-0.0072D0,-0.0054D0,-0.0019D0,.0217D0,
     *0.1479D0,0.0241D0,0.0842D0,0.0094D0,0.0908D0,0.0682D0,0.0398D0/

      PS=PSI      !     assume that Psi are in radians (not clear from the LU's paper)
C           NOTE OF 12/08/22: BASED ON THE VALUE OF A4 IN LU's PAPER, PSI IS, OF COURSE, IN RADIANS, NOT DEGS!
c
      ALPHA0=A6*(1.D0+A7*DSIGN(1.D0,BZIMF)*DTANH(A8*BZIMF))*(1.D0+A9*PD)
     * *(1.D0+A10*DLOG(BETA))*(A11*PS**2+A12*PS+A13)*(1.D0+A14*XMS)
      ALPHA1=A15*PS**2+A16*PS+A17
      ALPHA2=A18*PS**2+A19*PS+A20

      RHO2=Y**2+Z**2
      R=DSQRT(X**2+RHO2)
      RHO=DSQRT(RHO2)

      IF (RHO.GT.1.D-8) THEN  ! WE ARE NOT ON THE X-AXIS - NO SINGULARITIES TO WORRY ABOUT
        CT=X/R
        ST=RHO/R
        T=DATAN2(ST,CT)
        CP=Z/RHO
      ELSE                      !   ON THE X-AXIS
        IF (X.GT.0.D0) THEN     !   ON THE DAYSIDE
         CT=X/R
         ST=1.0D-8/R            !   SET RHO=10^-8, TO AVOID SINGULARITY OF GRAD_FI (IF MODE=1, SEE GRADFIP=... BELOW)
         T=DATAN2(ST,CT)
         CP=1.D0
        ELSE                    !  ON THE TAIL AXIS; TO AVOID SINGULARITY:
         RM=1000.D0             !  ASSIGN RM=1000 (A CONVENTIONAL SUBSTITUTE VALUE)
         RETURN                 !  AND EXIT
        ENDIF
      ENDIF

      R0=A1*(1.D0+A2/XMS**2)*(1.D0+A3/BETA)*(1.D0+A4*PS**2)
     *  *PD**(-1.D0/A5)
      RBS=R0*(2.D0/(1.D0+CT))**(ALPHA0+ALPHA1*CP+ALPHA2*CP**2)

      ID=1
      IF (RBS.LT.R) ID=-1

      RETURN
      END
c

C=====================================================================
      SUBROUTINE MODELVEC_DEN (ID,A,XI,F,DER,IA,NLIN,NTOT,NNON,
     * INDEPVAR,NDEPVAR)
C
C        ***  N.A. Tsyganenko ***  28.10.1997  ***  modified 30.04.2016,..., June 2025
C
C  Calculates dependent model variables and their derivatives with respect to
c  both linear and nonlinear parameters, to be used in the RMS minimization procedure.
C
C      Description of parameters:
C
C     ID              - number of a current point in the data set (initial assignments can be made only for ID=1, saving thus CPU time)
C     A               - input vector containing model parameters;
C     XI              - input vector containing independent variables;
C     F               - output double precision scalar variable, containing calculated value of the dependent variable (modeled quantity);
C     DER             - output double precision scalar variable, containing calculated value for derivatives
c                                                of the dependent variable with respect to model coefficients;
C     IA              - integer vector; IA(L)=0 means that the Lth parameter should be kept fixed in the search,
c                       and hence there is no need to calculate derivatives of B components w.r. to this parameter;
c                       IA(L)=1 means that the derivatives are needed.
c     NLIN            - number of linear parameters (coefficients)
c     NTOT            - total number of parameters (coefficients+nonlinears)
C     NNON            - total number of nonlinear parameters
c     INDEPVAR        - number of independent variables in the model input
c     NDEPVAR         - number of dependent variables in the model input (here only 1, for 1 modeled scalar quantity)
c
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      IMPLICIT  REAL * 8  (A - H, O - Z)
C
      PARAMETER (LMIN=0,LMAX=2,NMAX=10)

      DIMENSION F(NDEPVAR),DER(NLIN),A(NTOT),XI(INDEPVAR),IA(NTOT)
C
      DIMENSION FC(LMIN:LMAX,1:NMAX,0:NMAX),FS(LMIN:LMAX,1:NMAX,0:NMAX)  ! FC and FS are cos(phi)- and sin(phi)- associated basis elements of the modeled quantity F
c
      COMMON /RS0_ALP_DEN/ RS0,ALP   ! conveys here RS0 and ALP from the main program

      AL1=A(NLIN+1)  ! AL1: exponent for Dsw factor in the MSheath density values 
      AL2=A(NLIN+2)  ! AL2: exponent for Vsw factor in the MSheath density values 
      AL3=A(NLIN+3)  ! AL3: exponent for Wsw factor in the MSheath density values 
      EPS=A(NLIN+4)  ! EPS: exponent for coordinate scaling factor 

      X     = XI(1)      !  UNSCALED GSW COORDS
      Y     = XI(2)      !  UNSCALED GSW COORDS
      Z     = XI(3)      !  UNSCALED GSW COORDS
      PSI   = XI(4)      !  GEODIPOLE TILT ANGLE (radians)
      BXIMF = XI(5)/5.0      !  IMF BX
      BYIMF = XI(6)/5.0      !  IMF BY
      BZIMF = XI(7)/5.0      !  IMF BZ
      DSWn  = XI(8)/5.0  !  SOLAR WIND PROTON DENSITY, normalized by 5 protons per 1 cubic cm
      VSWn  = XI(9)/400. !  SOLAR WIND SPEED, normalized by 400km/s
      WSWn  = XI(10)/10. !  SOLAR WIND PROTON THERMAL ENERGY, normalized by 10 eV (i.e., 116 000 degs K)
      PD    = XI(11)  !  solar wind dynamic ram pressure
      FLAG  = XI(12)  !  record affiliation (either +1 if inside BS, or -1 if outside)

      FSC   = (PD/2.12D0)**EPS        ! scale coords by (PD/2.12D0)^EPS  2.12 is MEAN PD value
      Xs    = X * FSC
      Ys    = Y * FSC
      Zs    = Z * FSC

      R=SQRT(Xs**2+Ys**2+Zs**2)
      CT=Xs/R
      RS = R*((1.D0+CT)/2.D0)**ALP   ! RS is bow shock standoff distance from Shue formula, corresponding to the given R and T (theta)
      D  = 1.D0-RS/RS0

      I=0           !   INITIALIZE THE COUNTER OF UNKNOWN LINEAR PARAMETERS
C
c____ CALCULATE C- and S- COMPONENTS OF THE BASIS ELEMENTS: ___________________________
c
      CALL FC_FS_DEN (LMIN,LMAX,Xs,Ys,Zs,FC,FS)
      P1=DSWn**AL1*VSWn**AL2*WSWn**AL3
C
C   based on given {Xs,Ys,Zs}, LMIN & LMAX, the s/r FC_FS fills the arrays FC and FS with values of basis elements, corresponding to a given range of
C    (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0)
C    (2) spherical harmonic orders: 1<=N<=NMAX
C    (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX for C- (cos(m*phi)) and S (sin(m*phi))  modes

      DO L=LMIN,LMAX
       DO N=1,NMAX
        DO M=0,N

         FCC=FC(L,N,M)
         FSS=FS(L,N,M)
C
C  (1) First, for terms prop to solar wind proton density (main term, independent of IMF, nor PSI):
c
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values (symmetric w/r to Y & Z)
         I=I+1                  !   (terms without IMF)
         DER(I) = FCC*P1
        ENDIF
c
c  (2) Terms containing only linear dependence on tilt PSI (times FCC)
c
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and only odd M values (symmetric in Y and antisymmetric in Z)
         I=I+1
         DER(I) = FCC*P1*PSI  !  (terms linear by PSI)
        ENDIF
c
c  (3) Term with tilt PSI**2 (times FCC)
c
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values (symmetric both in Y & Z)
         I=I+1
         DER(I) = FCC*P1*PSI**2 !  (terms with PSI**2, no tilt)
        ENDIF
c
c  (4) Terms with BxIMF - only rec.-related (correction of 05/17) 
c
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and only odd M values (symm. in Y, antisymm. in Z)  AGAIN RECORRECTED 05/18
         I=I+1
         DER(I) = FCC*P1*BxIMF  !  (terms with IMF Bx, including reconnection, no tilt)
        ENDIF
C
C  (5) Term with ByIMF (reconnection-related only - odd in Y, odd in Z, rec.related ONLY AGAIN RECORRECTED 05/18
C
        IF (MOD(M,2).EQ.0.AND.M.NE.0) THEN !  C-type terms with only even M values  
         I=I+1
         DER(I) = FSS*P1*ByIMF
        ENDIF
C
C  (6) Term with BzIMF; reconnection-related ONLY!  AGAIN RECORRECTED 05/18
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only EVEN M values
         I=I+1
         DER(I) = FCC*P1*BzIMF
        ENDIF
C
C  (7) Term with BxIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*BxIMF**2
        ENDIF
C
C  (8) Term with ByIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*ByIMF**2
        ENDIF
C
C  (9) Term with BzIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*BzIMF**2
        ENDIF
C
C  (10) Term with BxIMF*ByIMF
C
        IF (MOD(M,2).EQ.0) THEN        !  C-type terms and even M values (changed 05/17)
         I=I+1                           ! even in BOTH Y and Z  ;  REC.-UNRELATED
         DER(I) = FCC*P1*BxIMF*ByIMF
        ENDIF
C
        IF (MOD(M,2).NE.0) THEN        !  only S-type terms and only odd M values (changed 05/07)
         I=I+1                           !  odd in Y even in Z   ;  REC.-RELATED
         DER(I) = FSS*P1*BxIMF*ByIMF
        ENDIF
c
C  (11) Term with BxIMF*BzIMF     !  only C-type terms and ODD M values (changed 05/18)
C
        IF (MOD(M,2).NE.0) THEN
         I=I+1
         DER(I) = FCC*P1*BxIMF*BzIMF
        ENDIF
C
C  (12a) C-term with ByIMF*BzIMF  !  central symmetry!
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms with even M values
         I=I+1
         DER(I) = FCC*P1*ByIMF*BzIMF
        ENDIF
C
C  (12b) S-term with ByIMF*BzIMF
C
        IF (MOD(M,2).EQ.0.AND.M.GT.0) THEN !  only S-type terms and even nonzero M values
         I=I+1
         DER(I) = FSS*P1*ByIMF*BzIMF
        ENDIF
C
C  (13) C-term with BxIMF*PSI
C
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and even M values (corrected 05/17)
         I=I+1                       !  because parallel dipole field (Psi=90deg) and radial IMF Bx Y- and Z-symmetric!
         DER(I) = FCC*P1*BxIMF*PSI
        ENDIF
C
C  (14) S-term with ByIMF*PSI
C
        IF (MOD(M,2).EQ.0.AND.M.NE.0) THEN !  only S-type terms and even M values (again corrected 05/17)
         I=I+1
         DER(I) = FSS*P1*ByIMF*PSI
        ENDIF
C
C  (15) C-term with BzIMF*PSI
C
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and odd M values
         I=I+1                       !  parallel dipole plus N-S IMF are even in Y and odd in Z
         DER(I) = FCC*P1*BzIMF*PSI
        ENDIF
C
        ENDDO
       ENDDO
      ENDDO
c
C -------------   TOTAL VALUE OF THE MODELED QUANTITY : ----------------------------------------------------------
C
         F(1)=0.D0

         DO 100 I=1,NLIN
 100     F(1)=F(1)+A(I)*DER(I)
C
      RETURN
      END
C______________________________________________________________________________________________________
C
      SUBROUTINE FC_FS_DEN (LMIN,LMAX,X,Y,Z,FC,FS)                             ! based on given {X,Y,Z}, LMIN & LMAX, fills the arrays FC and FS 
      IMPLICIT REAL*8 (A-H,O-Z)                                            ! with values of basis elements, corresponding to a given range of
      PARAMETER (NMAX=10)                                                   ! (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0) 
      DIMENSION FC(LMIN:LMAX,1:NMAX,0:NMAX),FS (LMIN:LMAX,1:NMAX,0:NMAX)  ! (2) spherical harmonic orders: 1<=N<=NMAX
C                                                                          ! (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX
C                                                                          !    for C- (cos(m*phi)) and S (sin(m*phi))  modes
      DIMENSION ASLPNM(0:NMAX,0:NMAX)
C  
      COMMON /RS0_ALP_DEN/ RS0,ALP                             ! conveys here RS0 and ALP from MODELVEC and main program
C     
c  RS0 is subsolar distance of the reference boundary; ALP is its flaring rate 
c
       RHO=SQRT(Y**2+Z**2)
       R=SQRT(X**2+Y**2+Z**2)
       IF (RHO.LT.1.D-8) RHO=1.D-8
       ST=RHO/R
       CT=X/R
       T=DATAN2(ST,CT)
       IF (RHO.GT.1.D-8) THEN
        P=DATAN2(Y,Z) ! needed for CM & SM below
       ELSE
        P=0.D0
       ENDIF
       CP=COS(P)     ! needed for converting from sph. to cart. in the end
       SP=SIN(P)     ! needed for converting from sph. to cart. in the end

       CHT=COS(0.5D0*T)
       THT=TAN(0.5D0*T)

       RS = R*((1.D0+CT)/2.D0)**ALP   ! RS is Shue standoff distance, corresponding to given R and T (theta)
       D    = 1.D0-RS/RS0
c
       CALL LEGENDASS_SCHMIDT_DEN (NMAX,CT,ST,ASLPNM)                           ! calculates full set of ass. Legendre polynomials
c                                                                             for given CT=cos(theta), ST=sin(theta) and 1<=N<=NMAX
       DO L=LMIN,LMAX  ! L is exponent in coefficient expansions in L powers
        DO N=1,NMAX
         DO M=0,N
          CM=COS(M*P)
          SM=SIN(M*P)
          FC(L,N,M) = ASLPNM(N,M)*CM *D**L
          FS(L,N,M) = ASLPNM(N,M)*SM *D**L
         ENDDO
        ENDDO
       ENDDO

      RETURN
      END
C
C===========================================================================================
C
      SUBROUTINE LEGENDASS_SCHMIDT_DEN(N,CT,ST,PNM)   
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (NMAX=10)                         
      DIMENSION PNM(0:N,0:N)                                       
      COMMON /SCHMIDT_DEN/ SNM(0:NMAX,0:NMAX)
C
C     INPUT:  N - UPPER LIMIT ON N & M;  CT = COS(THETA); ST=SIN(THETA)  
C
      PNM     (0,0)=1.D0 
c
      DO I=1,N                        ! calculate diagonal PNM,DPNMDT,D2PNMDT2
       IM1=I-1
       PNM(I,I)=ST*PNM(IM1,IM1) 
      ENDDO
c
      DO I=1,N
       IM1=I-1
       DO J=0,IM1
        IF (I.EQ.1) THEN
         PNM(I,J)=CT*PNM(IM1,J)
        ELSE
         XK=DFLOAT((IM1)*(IM1)-J*J)/DFLOAT((2*IM1)*(2*I-3))
         PNM(I,J)=CT*PNM(IM1,J)-XK*PNM(I-2,J)
        ENDIF
       ENDDO
      ENDDO
c
      DO I=1,N   !  normalize by Schmidt
      DO J=0,I
       PNM(I,J)=PNM(I,J)*SNM(I,J)
      ENDDO
      ENDDO

      RETURN
      END
C
cooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C                    

C=====================================================================
      SUBROUTINE MODELVEC_ENE (ID,A,XI,F,DER,IA,NLIN,NTOT,NNON,
     * INDEPVAR,NDEPVAR)
C
C        ***  N.A. Tsyganenko ***  28.10.1997  ***  modified 30.04.2016,..., June 2025
C
C  Calculates dependent model variables and their derivatives with respect to
c  both linear and nonlinear parameters, to be used in the RMS minimization procedure.
C
C      Description of parameters:
C
C     ID              - number of a current point in the data set (initial assignments can be made only for ID=1, saving thus CPU time)
C     A               - input vector containing model parameters;
C     XI              - input vector containing independent variables;
C     F               - output double precision scalar variable, containing calculated value of the dependent variable (modeled quantity);
C     DER             - output double precision scalar variable, containing calculated value for derivatives
c                                                of the dependent variable with respect to model coefficients;
C     IA              - integer vector; IA(L)=0 means that the Lth parameter should be kept fixed in the search,
c                       and hence there is no need to calculate derivatives of B components w.r. to this parameter;
c                       IA(L)=1 means that the derivatives are needed.
c     NLIN            - number of linear parameters (coefficients)
c     NTOT            - total number of parameters (coefficients+nonlinears)
C     NNON            - total number of nonlinear parameters
c     INDEPVAR        - number of independent variables in the model input
c     NDEPVAR         - number of dependent variables in the model input (here only 1, for 1 modeled scalar quantity)
c
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      IMPLICIT  REAL * 8  (A - H, O - Z)
C
      PARAMETER (LMIN=0,LMAX=2,NMAX=10)

      DIMENSION F(NDEPVAR),DER(NLIN),A(NTOT),XI(INDEPVAR),IA(NTOT)
C
      DIMENSION FC(LMIN:LMAX,1:NMAX,0:NMAX),FS(LMIN:LMAX,1:NMAX,0:NMAX)  ! FC and FS are cos(phi)- and sin(phi)- associated basis elements of the modeled quantity F
c
      COMMON /RS0_ALP_ENE/ RS0,ALP   ! conveys here RS0 and ALP from the main program

      AL1=A(NLIN+1)  ! AL1: exponent for Wsw factor in the MSheath proton energy values 
      AL2=A(NLIN+2)  ! AL2: exponent for Vsw factor in the MSheath proton energy values 
      AL3=A(NLIN+3)  ! AL3: exponent for Dsw factor in the MSheath proton energy values 
      EPS=A(NLIN+4)  ! EPS: exponent for coordinate scaling factor 

      X     = XI(1)      !  UNSCALED GSW COORDS
      Y     = XI(2)      !  UNSCALED GSW COORDS
      Z     = XI(3)      !  UNSCALED GSW COORDS
      PSI   = XI(4)      !  GEODIPOLE TILT ANGLE (radians)
      BXIMF = XI(5)/5.0      !  IMF BX
      BYIMF = XI(6)/5.0      !  IMF BY
      BZIMF = XI(7)/5.0      !  IMF BZ
      DSWn  = XI(8)/5.0  !  SOLAR WIND PROTON DENSITY, normalized by 5 protons per 1 cubic cm
      VSWn  = XI(9)/400. !  SOLAR WIND SPEED, normalized by 400km/s
      WSWn  = XI(10)/10. !  SOLAR WIND PROTON THERMAL ENERGY, normalized by 10 eV (i.e., 116 000 degs K)
      PD    = XI(11)  !  solar wind dynamic ram pressure
      FLAG  = XI(12)  !  record affiliation (either +1 if inside BS, or -1 if outside)

      FSC   = (PD/2.12D0)**EPS        ! scale coords by (PD/2.12D0)^EPS  2.12 is MEAN PD value
      Xs    = X * FSC
      Ys    = Y * FSC
      Zs    = Z * FSC

      R=SQRT(Xs**2+Ys**2+Zs**2)
      CT=Xs/R
      RS = R*((1.D0+CT)/2.D0)**ALP   ! RS is bow shock standoff distance from Shue formula, corresponding to the given R and T (theta)
      D  = 1.D0-RS/RS0

      I=0           !   INITIALIZE THE COUNTER OF UNKNOWN LINEAR PARAMETERS
C
c____ CALCULATE C- and S- COMPONENTS OF THE BASIS ELEMENTS: ___________________________
c
      CALL FC_FS_ENE (LMIN,LMAX,Xs,Ys,Zs,FC,FS)
      P1=WSWn**AL1*VSWn**AL2*DSWn**AL3
C
C   based on given {Xs,Ys,Zs}, LMIN & LMAX, the s/r FC_FS fills the arrays FC and FS with values of basis elements, corresponding to a given range of
C    (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0)
C    (2) spherical harmonic orders: 1<=N<=NMAX
C    (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX for C- (cos(m*phi)) and S (sin(m*phi))  modes

      DO L=LMIN,LMAX
       DO N=1,NMAX
        DO M=0,N

         FCC=FC(L,N,M)
         FSS=FS(L,N,M)
C
C  (1) First, for terms prop to solar wind proton density (main term, independent of IMF, nor PSI):
c
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values (symmetric w/r to Y & Z)
         I=I+1                  !   (terms without IMF)
         DER(I) = FCC*P1
        ENDIF
c
c  (2) Terms containing only linear dependence on tilt PSI (times FCC)
c
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and only odd M values (symmetric in Y and antisymmetric in Z)
         I=I+1
         DER(I) = FCC*P1*PSI  !  (terms linear by PSI)
        ENDIF
c
c  (3) Term with tilt PSI**2 (times FCC)
c
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values (symmetric both in Y & Z)
         I=I+1
         DER(I) = FCC*P1*PSI**2 !  (terms with PSI**2, no tilt)
        ENDIF
c
c  (4) Terms with BxIMF - only rec.-related (correction of 05/17) 
c
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and only odd M values (symm. in Y, antisymm. in Z)  AGAIN RECORRECTED 05/18
         I=I+1
         DER(I) = FCC*P1*BxIMF  !  (terms with IMF Bx, including reconnection, no tilt)
        ENDIF
C
C  (5) Term with ByIMF (reconnection-related only - odd in Y, odd in Z, rec.related ONLY AGAIN RECORRECTED 05/18
C
        IF (MOD(M,2).EQ.0.AND.M.NE.0) THEN !  C-type terms with only even M values  
         I=I+1
         DER(I) = FSS*P1*ByIMF
        ENDIF
C
C  (6) Term with BzIMF; reconnection-related ONLY!  AGAIN RECORRECTED 05/18
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only EVEN M values
         I=I+1
         DER(I) = FCC*P1*BzIMF
        ENDIF
C
C  (7) Term with BxIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*BxIMF**2
        ENDIF
C
C  (8) Term with ByIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*ByIMF**2
        ENDIF
C
C  (9) Term with BzIMF**2
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms and only even M values
         I=I+1                  !
         DER(I) = FCC*P1*BzIMF**2
        ENDIF
C
C  (10) Term with BxIMF*ByIMF
C
        IF (MOD(M,2).EQ.0) THEN        !  C-type terms and even M values (changed 05/17)
         I=I+1                           ! even in BOTH Y and Z  ;  REC.-UNRELATED
         DER(I) = FCC*P1*BxIMF*ByIMF
        ENDIF
C
        IF (MOD(M,2).NE.0) THEN        !  only S-type terms and only odd M values (changed 05/07)
         I=I+1                           !  odd in Y even in Z   ;  REC.-RELATED
         DER(I) = FSS*P1*BxIMF*ByIMF
        ENDIF
c
C  (11) Term with BxIMF*BzIMF     !  only C-type terms and ODD M values (changed 05/18)
C
        IF (MOD(M,2).NE.0) THEN
         I=I+1
         DER(I) = FCC*P1*BxIMF*BzIMF
        ENDIF
C
C  (12a) C-term with ByIMF*BzIMF  !  central symmetry!
C
        IF (MOD(M,2).EQ.0) THEN !  only C-type terms with even M values
         I=I+1
         DER(I) = FCC*P1*ByIMF*BzIMF
        ENDIF
C
C  (12b) S-term with ByIMF*BzIMF
C
        IF (MOD(M,2).EQ.0.AND.M.GT.0) THEN !  only S-type terms and even nonzero M values
         I=I+1
         DER(I) = FSS*P1*ByIMF*BzIMF
        ENDIF
C
C  (13) C-term with BxIMF*PSI
C
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and even M values (corrected 05/17)
         I=I+1                       !  because parallel dipole field (Psi=90deg) and radial IMF Bx Y- and Z-symmetric!
         DER(I) = FCC*P1*BxIMF*PSI
        ENDIF
C
C  (14) S-term with ByIMF*PSI
C
        IF (MOD(M,2).EQ.0.AND.M.NE.0) THEN !  only S-type terms and even M values (again corrected 05/17)
         I=I+1
         DER(I) = FSS*P1*ByIMF*PSI
        ENDIF
C
C  (15) C-term with BzIMF*PSI
C
        IF (MOD(M,2).NE.0) THEN !  only C-type terms and odd M values
         I=I+1                       !  parallel dipole plus N-S IMF are even in Y and odd in Z
         DER(I) = FCC*P1*BzIMF*PSI
        ENDIF
C
        ENDDO
       ENDDO
      ENDDO
c
C -------------   TOTAL VALUE OF THE MODELED QUANTITY : ----------------------------------------------------------
C
         F(1)=0.D0

         DO 100 I=1,NLIN
 100     F(1)=F(1)+A(I)*DER(I)
C
      RETURN
      END
C______________________________________________________________________________________________________
C
      SUBROUTINE FC_FS_ENE (LMIN,LMAX,X,Y,Z,FC,FS)                             ! based on given {X,Y,Z}, LMIN & LMAX, fills the arrays FC and FS 
      IMPLICIT REAL*8 (A-H,O-Z)                                            ! with values of basis elements, corresponding to a given range of
      PARAMETER (NMAX=10)                                                   ! (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0) 
      DIMENSION FC(LMIN:LMAX,1:NMAX,0:NMAX),FS (LMIN:LMAX,1:NMAX,0:NMAX)  ! (2) spherical harmonic orders: 1<=N<=NMAX
C                                                                          ! (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX
C                                                                          !    for C- (cos(m*phi)) and S (sin(m*phi))  modes
      DIMENSION ASLPNM(0:NMAX,0:NMAX)
C  
      COMMON /RS0_ALP_ENE/ RS0,ALP                             ! conveys here RS0 and ALP from MODELVEC and main program
C     
c  RS0 is subsolar distance of the reference boundary; ALP is its flaring rate 
c
       RHO=SQRT(Y**2+Z**2)
       R=SQRT(X**2+Y**2+Z**2)
       IF (RHO.LT.1.D-8) RHO=1.D-8
       ST=RHO/R
       CT=X/R
       T=DATAN2(ST,CT)
       IF (RHO.GT.1.D-8) THEN
        P=DATAN2(Y,Z) ! needed for CM & SM below
       ELSE
        P=0.D0
       ENDIF
       CP=COS(P)     ! needed for converting from sph. to cart. in the end
       SP=SIN(P)     ! needed for converting from sph. to cart. in the end

       CHT=COS(0.5D0*T)
       THT=TAN(0.5D0*T)

       RS = R*((1.D0+CT)/2.D0)**ALP   ! RS is Shue standoff distance, corresponding to given R and T (theta)
       D    = 1.D0-RS/RS0
c
       CALL LEGENDASS_SCHMIDT_ENE (NMAX,CT,ST,ASLPNM)                           ! calculates full set of ass. Legendre polynomials
c                                                                             for given CT=cos(theta), ST=sin(theta) and 1<=N<=NMAX
       DO L=LMIN,LMAX  ! L is exponent in coefficient expansions in L powers
        DO N=1,NMAX
         DO M=0,N
          CM=COS(M*P)
          SM=SIN(M*P)
          FC(L,N,M) = ASLPNM(N,M)*CM *D**L
          FS(L,N,M) = ASLPNM(N,M)*SM *D**L
         ENDDO
        ENDDO
       ENDDO

      RETURN
      END
C
C===========================================================================================
C
      SUBROUTINE LEGENDASS_SCHMIDT_ENE(N,CT,ST,PNM)   
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (NMAX=10)                                                                                         
      DIMENSION PNM(0:N,0:N)                                       
      COMMON /SCHMIDT_ENE/ SNM(0:NMAX,0:NMAX)
C
C     INPUT:  N - UPPER LIMIT ON N & M;  CT = COS(THETA); ST=SIN(THETA)  
C
      PNM     (0,0)=1.D0 
c
      DO I=1,N                        ! calculate diagonal PNM,DPNMDT,D2PNMDT2
       IM1=I-1
       PNM(I,I)=ST*PNM(IM1,IM1) 
      ENDDO
c
      DO I=1,N
       IM1=I-1
       DO J=0,IM1
        IF (I.EQ.1) THEN
         PNM(I,J)=CT*PNM(IM1,J)
        ELSE
         XK=DFLOAT((IM1)*(IM1)-J*J)/DFLOAT((2*IM1)*(2*I-3))
         PNM(I,J)=CT*PNM(IM1,J)-XK*PNM(I-2,J)
        ENDIF
       ENDDO
      ENDDO
c
      DO I=1,N   !  normalize by Schmidt
      DO J=0,I
       PNM(I,J)=PNM(I,J)*SNM(I,J)
      ENDDO
      ENDDO

      RETURN
      END
C
cooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C                    

C=====================================================================
      SUBROUTINE MSH_FLOW (PARMOD,X,Y,Z,FX,FY,FZ)
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (INDPVR=10,NDPVR=3) 
      PARAMETER (NLIN=1632,NTOT=1632) 
      DIMENSION IA(NTOT),F(NDPVR),DERX(NLIN),DERY(NLIN),DERZ(NLIN)
      DIMENSION XI(INDPVR),PARMOD(12)

      COMMON /PAR_TPS/ A(NTOT)
      COMMON /NONLINEARS/ RS0,EPS,DFSC,ALP0,ALP1,FSC,ALP  ! first 5 are forwarded from the VAC fitting output file
c  
C                             RS0:           location of Delta=0 reference point at the MP
c                                 EPS:         EPS exponent for Pdyn dependence of MP standoff distance
c                                     DFSC:      coefficient in standoff scaling sensitivity to BSIMF
c                                          ALP0:  free term in MP flaring parameter    
c                                               ALP1:   coeff by exp(-Bz/10) in MP flaring parameter             
C                                                    FSC: scaling factor for coords and standoff distance 
c                                                        ALP added to forward it to B_CART                                            
c
      DATA IA/NTOT*1/
C
      XI(1) =X
      XI(2) =Y
      XI(3) =Z
      XI(4) =PARMOD(1)  ! psi
      XI(5) =PARMOD(2)  ! BXIMF
      XI(6) =PARMOD(3)  ! BYIMF
      XI(7) =PARMOD(4)  ! BZIMF
      XI(8) =PARMOD(5)  ! VSW
      XI(9) =PARMOD(6)  ! DSW
      XI(10)=PARMOD(7)  ! PDSW
C
      RS=RS0/FSC                                           
      R=SQRT(X**2+Y**2+Z**2)           
      THETA=DACOS(X/R) ; PHI=DATAN2(Y,Z)
      CALL SHUE (RS,THETA,PHI,ALP,XMP,YMP,ZMP,EXN,EYN,EZN)  ! check if inside the MP; if yes, set FX=FY=FZ=0,
      RMP=SQRT(XMP**2+YMP**2+ZMP**2)

      CALL BS (X,Y,Z,XI(4),XI(10),XI(7),5.9D0,3.0D0,RBS,ID)          ! check if outside the BS; if yes, set FX equal to the S.W. flux

      IF (R.LT.RMP) THEN 
       FX=0.D0; FY=0.D0; FZ=0.D0
      ENDIF

      IF (R.GT.RBS) THEN
       FX=-PARMOD(5)*PARMOD(6)/1000.D0  ! PARMOD(5) and PARMOD(6) are the solar wind speed (km/s) and proton density (cm^-3)
       FY= 0.D0                         !  such that FX is number of ions per cm^2 per second TIMES 10^-8
       FZ= 0.D0
      ENDIF

      IF (R.GE.RMP.AND.R.LE.RBS) THEN             
       CALL MODEL_TPS(0,A,XI,F,DERX,DERY,DERZ,IA,NLIN,NTOT,INDPVR,NDPVR)     
       FX=F(1)
       FY=F(2)
       FZ=F(3)
      ENDIF
C
      RETURN
      END
C
c&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
c
      SUBROUTINE MODEL_TPS (ID,A,XI,F,DERX,DERY,DERZ,IA,NLIN,NTOT,
     * INDEPVAR,NDEPVAR)
C
C        ***  N.A. Tsyganenko ***  28.10.1997  ***  modified 30.04.2016, ..., etc.
C
C  Calculates dependent model variables and their derivatives with respect to
c  both linear and nonlinear parameters, to be used in the RMS minimization procedure.
C
C      Description of parameters:
C
C  ID  - number of a current point from the data set (initial assignments can
c        be made for ID=1 only, saving thus CPU time)
C  A   - input vector containing model parameters;
C  XI  - input vector containing independent variables;
C  F   - output double precision vector containing
C        calculated values of dependent variables;
C  DERX,DERY,DERZ  - output double precision vectors containing
C        calculated values for derivatives of dependent
C        variables with respect to model parameters;
C  IA -  integer vector; IA(L)=0 means that the Lth parameter should be kept
c        fixed in the search, and hence there is no need in calculating
c        derivatives of field components with regard to this parameter;
c        IA(L)=1 means that the derivatives are needed.
c
c  NLIN - total number of coefficients
c
C  ICO - input parameter coded as follows:
c
c       ICO = 0 - derivatives with respect to nonlinear parameters are calculated;
c       ICO = 1 - only derivatives with respect to linear parameters are calculated
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      IMPLICIT  REAL * 8  (A - H, O - Z)
C
      PARAMETER (LMIN=0,LMAX=2,NMAX=8)

      DIMENSION F(NDEPVAR),DERX(NLIN),DERY(NLIN),DERZ(NLIN),A(NTOT),
     * XI(INDEPVAR), IA(NTOT)                                
C                                                         
      DIMENSION
     *  BXC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BXS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BXC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BXS_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYS_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZS_POL(LMIN:LMAX,1:NMAX,0:NMAX) 
c
      COMMON /NONLINEARS/ RS0,EPS,DFSC,ALP0,ALP1,FSC,ALP  ! first 5 to be read from the result of VAC fitting
  
C                         RS0:           location of Delta=0 reference point at the MP
c                             EPS:         EPS exponent for Pdyn dependence of MP standoff distance
c                                 DFSC:      coefficient in standoff scaling sensitivity to BSIMF
c                                      ALP0:  free term in MP flaring parameter    
c                                           ALP1:   coeff by exp(-Bz/10) in MP flaring parameter             
C                                                FSC: scaling factor for coords and standoff distance 
c                                                    ALP added to forward it to B_CART                                            
      X     = XI(1)   !  UNSCALED GSW COORDS
      Y     = XI(2)   !  UNSCALED GSW COORDS
      Z     = XI(3)   !  UNSCALED GSW COORDS
      PSI   = XI(4)
      BXIMF = XI(5)
      BYIMF = XI(6)
      BZIMF = XI(7)
      VSW   = XI(8)   !  S.W. SPEED
      DSW   = XI(9)   !  S.W. PROTON DENSITY
      PDSW  = XI(10)  !  S.W. RAM PRESSURE

      ALP   = ALP0 + ALP1*EXP(-BZIMF/10.D0) 

      FSC   = (PDSW/2.D0)**EPS +DFSC*(BZIMF/10.)  !   SCALING FACTOR FOR COORDS AND STANDOFF DIST.
      Xs    =  X * FSC
      Ys    =  Y * FSC
      Zs    =  Z * FSC

      FACTOR=VSW*DSW/1000.D0   ! such that with VSW in km/s and DSW in cm^-3, the particle flux is in units 10^8 cm^-2 sec^-1 (in the range 1-10)
      BXIMFN=BXIMF/5.D0        ! normalize by 5nT (added 09/02/24, NT)
      BYIMFN=BYIMF/5.D0        
      BZIMFN=BZIMF/5.D0        
                                 
      C=COS(PSI)                                              
      S=SIN(PSI)

      I=0           !   INITIALIZE THE COUNTER OF UNKNOWN LINEAR PARAMETERS

      CALL B_CART(LMIN,LMAX,Xs,Ys,Zs,BXC_TOR,BXS_TOR,BYC_TOR,BYS_TOR,
     * BZC_TOR,BZS_TOR,BXC_POL,BXS_POL,BYC_POL,BYS_POL,BZC_POL,BZS_POL)                         

      DO L=LMIN,LMAX          !  ATTENTION: HERE THE DIFFERENCE FROM ALL PREVIOUS VARIANTS
       DO N=1,NMAX     
        DO M=0,N        

        FXCT    = BXC_TOR (L,N,M)
        FYCT    = BYC_TOR (L,N,M)
        FZCT    = BZC_TOR (L,N,M)
        FXST    = BXS_TOR (L,N,M)
        FYST    = BYS_TOR (L,N,M)
        FZST    = BZS_TOR (L,N,M)
        FXCP    = BXC_POL (L,N,M)
        FYCP    = BYC_POL (L,N,M)
        FZCP    = BZC_POL (L,N,M)
        FXSP    = BXS_POL (L,N,M)
        FYSP    = BYS_POL (L,N,M)
        FZSP    = BZS_POL (L,N,M)
C__________________________________________________________________________________________
c
C  First, for reconnection-unrelated terms:  free terms + those prop to F*Bx, F*By, & F*Bz 
c
        IF ((N.GE.2).AND.(M.GE.2).AND.(MOD(M,2).EQ.0)) THEN   ! ----------  BEGINNING OF TOROIDAL PART    
c                                                              
         I=I+1    
         DERX(I) = FXST*FACTOR                  ! FXST,FYST,FZST ~ Ht_lnm   
         DERY(I) = FYST*FACTOR    
         DERZ(I) = FZST*FACTOR    

         I=I+1    
         DERX(I) = FXST*FACTOR*C                  ! FXST,FYST,FZST ~ Ht_lnm   !   added on 10/07/24 
         DERY(I) = FYST*FACTOR*C    
         DERZ(I) = FZST*FACTOR*C    

         I=I+1    
         DERX(I) = FXST*FACTOR*BXIMFN           ! FXST,FYST,FZST ~ Ht_lnm   
         DERY(I) = FYST*FACTOR*BXIMFN
         DERZ(I) = FZST*FACTOR*BXIMFN                           

         I=I+1    
         DERX(I) = FXST*FACTOR*BYIMFN           ! FXST,FYST,FZST ~ Ht_lnm          
         DERY(I) = FYST*FACTOR*BYIMFN
         DERZ(I) = FZST*FACTOR*BYIMFN                           

         I=I+1    
         DERX(I) = FXST*FACTOR*BZIMFN           ! FXST,FYST,FZST ~ Ht_lnm         
         DERY(I) = FYST*FACTOR*BZIMFN
         DERZ(I) = FZST*FACTOR*BZIMFN                           
C
C  Now for reconnection-associated terms Bz*cos(psi) and Bx*sin(psi) (same rules for N and M):
c
         I=I+1    
         DERX(I) = FXST*FACTOR*BXIMFN*S         ! FXST,FYST,FZST ~ Ht_lnm       
         DERY(I) = FYST*FACTOR*BXIMFN*S
         DERZ(I) = FZST*FACTOR*BXIMFN*S                            

        ENDIF                                   !  -----------  END OF TOROIDAL PART    ----------
c ____________________________________________________________________________________________________

        IF (MOD(M,2).EQ.0) THEN                 !  ----------  BEGINNING OF POLOIDAL PART    

         I=I+1    
         DERX(I) = FXCP*FACTOR            !  FXCP,FYCP,FZCP ~ Gp_lnm             
         DERY(I) = FYCP*FACTOR                  
         DERZ(I) = FZCP*FACTOR                                                          

         I=I+1    
         DERX(I) = FXCP*FACTOR*C            !  FXCP,FYCP,FZCP ~ Gp_lnm             
         DERY(I) = FYCP*FACTOR*C                  
         DERZ(I) = FZCP*FACTOR*C                                                          

         I=I+1    
         DERX(I) = FXCP*FACTOR*BXIMFN     !  FXCP,FYCP,FZCP ~ Gp_lnm                 
         DERY(I) = FYCP*FACTOR*BXIMFN
         DERZ(I) = FZCP*FACTOR*BXIMFN                           

         I=I+1    
         DERX(I) = FXCP*FACTOR*BYIMFN     !  FXCP,FYCP,FZCP ~ Gp_lnm                
         DERY(I) = FYCP*FACTOR*BYIMFN
         DERZ(I) = FZCP*FACTOR*BYIMFN                           

         I=I+1    
         DERX(I) = FXCP*FACTOR*BZIMFN     !  FXCP,FYCP,FZCP ~ Gp_lnm                
         DERY(I) = FYCP*FACTOR*BZIMFN
         DERZ(I) = FZCP*FACTOR*BZIMFN                           

C  Now for reconnection-associated terms IMF Bz*cos(psi) and Bx*sin(psi):
c
         I=I+1    
         DERX(I) = FXCP*FACTOR*BZIMFN*C   !  FXCP,FYCP,FZCP ~ Gp_lnm                
         DERY(I) = FYCP*FACTOR*BZIMFN*C
         DERZ(I) = FZCP*FACTOR*BZIMFN*C                            
C
         I=I+1    
         DERX(I) = FXCP*FACTOR*BXIMFN*S   !  FXCP,FYCP,FZCP ~ Gp_lnm                 
         DERY(I) = FYCP*FACTOR*BXIMFN*S
         DERZ(I) = FZCP*FACTOR*BXIMFN*S                            

        ENDIF            !              --------------  end of poloidal part  ------------
c
C ____________________   NOW FOR RECONNECTION-RELATED IMF BY EFFECT: _______
C
        IF (MOD(M,2).EQ.0) THEN                !  ----------------  begin of toroidal part  
         I=I+1    
         DERX(I) = FXCT*FACTOR*BYIMFN*C   !  FXCT,FYCT,FZCT ~ Gt_lnm                    
         DERY(I) = FYCT*FACTOR*BYIMFN*C       
         DERZ(I) = FZCT*FACTOR*BYIMFN*C        !  ------------------  end of toroidal part
        ENDIF       

        IF ((N.GE.2).AND.(M.GE.2).AND.(MOD(M,2).EQ.0)) THEN    !  ----  begin of poloidal part
         I=I+1    
         DERX(I) = FXSP*FACTOR*BYIMFN*C   !  FXSP,FYSP,FZSP ~ Hp_lnm                     
         DERY(I) = FYSP*FACTOR*BYIMFN*C              
         DERZ(I) = FZSP*FACTOR*BYIMFN*C                            

        ENDIF   !                    -------------------------  end of poloidal part -------
c
C____________  NOW FOR RECONNECTION-RELATED EFFECT OF IMF Bx*cos(psi) AND Bz*sin(psi)
C              AND R-UNRELATED EFFECT OF CROSS TERM Bx*Bz AND IMF-UNRELATED TERM ~TO SIN(PSI) (same restrictions on M):
C
        IF ((M.GE.1).AND.(MOD(M,2).NE.0)) THEN          
C                                             ------------- begin of toroidal part  ------------
         I=I+1
         DERX(I) = FXST*FACTOR*S   !  FXST,FYST,FZST ~ Ht_lnm         !  added on 10/07/24 
         DERY(I) = FYST*FACTOR*S             
         DERZ(I) = FZST*FACTOR*S                          

         I=I+1
         DERX(I) = FXST*FACTOR*BXIMFN*C   !  FXST,FYST,FZST ~ Ht_lnm                     
         DERY(I) = FYST*FACTOR*BXIMFN*C             
         DERZ(I) = FZST*FACTOR*BXIMFN*C                           

         I=I+1    
         DERX(I) = FXST*FACTOR*BZIMFN*S   !  FXST,FYST,FZST ~ Ht_lnm                  
         DERY(I) = FYST*FACTOR*BZIMFN*S         
         DERZ(I) = FZST*FACTOR*BZIMFN*S                       

         I=I+1
         DERX(I) = FXST*FACTOR*BXIMFN*BZIMFN  !  FXST,FYST,FZST ~ Ht_lnm                   
         DERY(I) = FYST*FACTOR*BXIMFN*BZIMFN    
         DERZ(I) = FZST*FACTOR*BXIMFN*BZIMFN  !   end of toroidal part                         

C   ------------------------------------      !  begin of poloidal part  (same parity rules as just above) -----------------

         I=I+1
         DERX(I) = FXCP*FACTOR*S   !  FXST,FYST,FZST ~ Ht_lnm         !  added on 10/07/24 
         DERY(I) = FYCP*FACTOR*S             
         DERZ(I) = FZCP*FACTOR*S                          

         I=I+1
         DERX(I) = FXCP*FACTOR*BXIMFN*C       !  FXCP,FYCP,FZCP ~ Gp_lnm                
         DERY(I) = FYCP*FACTOR*BXIMFN*C             
         DERZ(I) = FZCP*FACTOR*BXIMFN*C                           

         I=I+1    
         DERX(I) = FXCP*FACTOR*BZIMFN*S       !  FXCP,FYCP,FZCP ~ Gp_lnm                
         DERY(I) = FYCP*FACTOR*BZIMFN*S         
         DERZ(I) = FZCP*FACTOR*BZIMFN*S                       

         I=I+1
         DERX(I) = FXCP*FACTOR*BXIMFN*BZIMFN  !  FXCP,FYCP,FZCP ~ Gp_lnm                  
         DERY(I) = FYCP*FACTOR*BXIMFN*BZIMFN    
         DERZ(I) = FZCP*FACTOR*BXIMFN*BZIMFN                           
c                                               --------   end of poloidal part --------

C   NOW FOR R-RELATED EFFECT OF IMF By*sin(psi) AND RECONNECTION-UNRELATED EFFECTS OF CROSS TERM IMF Bx*By
C____________________________________________________   (SAME RESTRICTIONS ON M INDEX):
C
         I=I+1
         DERX(I) = FXCT*FACTOR*BYIMFN*S         !  toroidal part, By*sin(psi)
         DERY(I) = FYCT*FACTOR*BYIMFN*S        
         DERZ(I) = FZCT*FACTOR*BYIMFN*S                      

         I=I+1
         DERX(I) = FXCT*FACTOR*BXIMFN*BYIMFN    !  toroidal part, Bx*By    
         DERY(I) = FYCT*FACTOR*BXIMFN*BYIMFN          
         DERZ(I) = FZCT*FACTOR*BXIMFN*BYIMFN                        

         I=I+1    
         DERX(I) = FXSP*FACTOR*BYIMFN*S         !  poloidal part, By*sin(psi)
         DERY(I) = FYSP*FACTOR*BYIMFN*S         
         DERZ(I) = FZSP*FACTOR*BYIMFN*S                       

         I=I+1    
         DERX(I) = FXSP*FACTOR*BXIMFN*BYIMFN    !  poloidal part, Bx*By                 
         DERY(I) = FYSP*FACTOR*BXIMFN*BYIMFN         
         DERZ(I) = FZSP*FACTOR*BXIMFN*BYIMFN                       

        ENDIF
c
        ENDDO
       ENDDO
      ENDDO
c
C -------------   TOTAL FIELD: ----------------------------------------------------------
C
         F(1)=0.D0
         F(2)=0.D0
         F(3)=0.D0

         DO 100 I=1,NLIN
          F(1)=F(1)+A(I)*DERX(I)
          F(2)=F(2)+A(I)*DERY(I)
 100      F(3)=F(3)+A(I)*DERZ(I)
C
      RETURN
      END
C_________________________________________________________________________________
c
      SUBROUTINE B_CART(LMIN,LMAX,X,Y,Z,BXC_TOR,BXS_TOR,BYC_TOR,BYS_TOR, ! based on given {X,Y,Z}, LMIN & LMAX, 
     * BZC_TOR,BZS_TOR,BXC_POL,BXS_POL,BYC_POL,BYS_POL,BZC_POL,BZS_POL)  ! fills the arrays BXC_TOR - ... - BZS_POL
      IMPLICIT REAL*8 (A-H,O-Z)                                          ! with values of Cartesian toro- & polo-
      PARAMETER (NMAX=8)                                                ! components, corresponding to a given range of
      DIMENSION                                                          ! (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0) 
     *  BXC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),                                ! (2) spherical harmonic orders: 1<=N<=NMAX
     *  BXS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),                                ! (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX
     *  BYC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),                                !    for C- (cos(m*phi)) and S (sin(m*phi))  modes 
     *  BYS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZC_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZS_TOR(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BXC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BXS_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BYS_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZC_POL(LMIN:LMAX,1:NMAX,0:NMAX),
     *  BZS_POL(LMIN:LMAX,1:NMAX,0:NMAX) 

      DIMENSION ASLPNM(0:NMAX,0:NMAX),DASLPNM(0:NMAX,0:NMAX),
     * D2ASLPNM(0:NMAX,0:NMAX)
C  
      COMMON /NONLINEARS/ RS0,EPS,DFSC,ALP0,ALP1,FSC,ALP  ! first 5 to be read from the result of VAC fitting
c  
C                         RS0:           location of Delta=0 reference point at the MP
c                             EPS:         EPS exponent for Pdyn dependence of MP standoff distance
c                                 DFSC:      coefficient in standoff scaling sensitivity to BSIMF
c                                      ALP0:  free term in MP flaring parameter    
c                                           ALP1:   coeff by exp(-Bz/10) in MP flaring parameter             
C                                                FSC: scaling factor for coords and standoff distance 
c                                                    ALP added to forward it to B_CART                                            
       RHO=SQRT(Y**2+Z**2)
       R=SQRT(X**2+Y**2+Z**2)
       IF (RHO.LT.1.D-8) RHO=1.D-8
       ST=RHO/R
       CT=X/R
       T=DATAN2(ST,CT)
       IF (RHO.GT.1.D-8) THEN
        P=DATAN2(Y,Z) ! needed for CM & SM below
       ELSE
        P=0.D0
       ENDIF
       CP=COS(P)     ! needed for converting from sph. to cart. in the end
       SP=SIN(P)     ! needed for converting from sph. to cart. in the end

       CHT=COS(0.5D0*T)
       THT=TAN(0.5D0*T)

       RS = R*((1.D0+CT)/2.D0)**ALP   ! RS is Shue standoff distance, corresponding to given R and T (theta)

       D    = 1.D0-RS/RS0
       DDDR = (D-1.D0)/R
       DDDT = ALP*(1.D0-D)*THT
       D2DDT2  = ALP*((1.D0-D)/(2.D0*CHT**2)-DDDT*THT)
       D2DDRDT = DDDT/R
c
      CALL LEGENDASS_SCHMIDT_FLO (NMAX,CT,ST,ASLPNM,DASLPNM,D2ASLPNM,1) ! calculates full set of ass. Legendre polynomials
c                                                                   for given CT=cos(theta), ST=sin(theta) and 1<=N<=NMAX
       DO L=LMIN,LMAX  ! L is power of D in coefficient expansions 

       DO N=1,NMAX
       DO M=0,N

       CM=COS(M*P)
       SM=SIN(M*P)

       YNM_C     =   ASLPNM(N,M)*CM
       YNM_S     =   ASLPNM(N,M)*SM
       DYNMDT_C  =  DASLPNM(N,M)*CM
       DYNMDT_S  =  DASLPNM(N,M)*SM
       DYNMDP_C  =  -ASLPNM(N,M)*SM*M
       DYNMDP_S  =   ASLPNM(N,M)*CM*M
       D2YNMDT2_C= D2ASLPNM(N,M)*CM
       D2YNMDT2_S= D2ASLPNM(N,M)*SM
       D2YNMDP2_C=-M**2*YNM_C
       D2YNMDP2_S=-M**2*YNM_S

       D2YNMDTDP_C=-DASLPNM(N,M)*M*SM
       D2YNMDTDP_S= DASLPNM(N,M)*M*CM

c----------------------------------------------------------------------
c  Polo (C):
C______________________________________________________________________
c
      IF (L.EQ.0) THEN
       D_PSIP_DR   =0.D0
       D_PSIP_DT   =DYNMDT_C
       D_PSIP_DP   =DYNMDP_C
       D2_PSIP_DR2 =0.D0
       D2_PSIP_DRDT=0.D0
       D2_PSIP_DRDP=0.D0
       D2_PSIP_DT2 =D2YNMDT2_C
       D2_PSIP_DTDP=D2YNMDTDP_C
       D2_PSIP_DP2 =D2YNMDP2_C
      ENDIF

      IF (L.EQ.1) THEN
       D_PSIP_DR   =DDDR*YNM_C
       D_PSIP_DT   =D*DYNMDT_C+DDDT*YNM_C
       D_PSIP_DP   =D*DYNMDP_C
       D2_PSIP_DR2 =0.D0
       D2_PSIP_DRDT=DDDR*DYNMDT_C+D2DDRDT*YNM_C
       D2_PSIP_DRDP=DDDR*DYNMDP_C
       D2_PSIP_DT2 =D2DDT2*YNM_C+2.D0*DDDT*DYNMDT_C+D*D2YNMDT2_C
       D2_PSIP_DTDP=DDDT*DYNMDP_C+D*D2YNMDTDP_C
       D2_PSIP_DP2 =D*D2YNMDP2_C
      ENDIF

      IF (L.EQ.2) THEN
       D_PSIP_DR   =2.D0*D*DDDR*YNM_C
       D_PSIP_DT   =D*(2.D0*DDDT*YNM_C+D*DYNMDT_C)
       D_PSIP_DP   =D**2*DYNMDP_C
       D2_PSIP_DR2 =2.D0*DDDR**2*YNM_C
       D2_PSIP_DRDT=2.D0*(DDDR*(DDDT*YNM_C+D*DYNMDT_C)+D*D2DDRDT*YNM_C)
       D2_PSIP_DRDP=2.D0*D*DDDR*DYNMDP_C                 
       D2_PSIP_DT2 =2.D0*YNM_C*(DDDT**2+D*D2DDT2)+D*(4.D0*DDDT*DYNMDT_C
     *  +D*D2YNMDT2_C)
       D2_PSIP_DTDP=D*(D*D2YNMDTDP_C+2.D0*DDDT*DYNMDP_C)
       D2_PSIP_DP2 =D**2*D2YNMDP2_C
      ENDIF

      IF (L.EQ.3) THEN                    
       D_PSIP_DR   =3.D0*D**2*DDDR*YNM_C
       D_PSIP_DT   =D**2*(3.D0*DDDT*YNM_C+D*DYNMDT_C)
       D_PSIP_DP   =D**3*DYNMDP_C
       D2_PSIP_DR2 =6.D0*D*DDDR**2*YNM_C
       D2_PSIP_DRDT=3.D0*D*((2.D0*DDDR*DDDT+D*D2DDRDT)*YNM_C
     *  +D*DDDR*DYNMDT_C)
       D2_PSIP_DRDP=3.D0*D**2*DDDR*DYNMDP_C                 
       D2_PSIP_DT2 =3.D0*D*(YNM_C*(2.D0*DDDT**2+D*D2DDT2)
     *  +2.D0*D*DDDT*DYNMDT_C)+D**3*D2YNMDT2_C
       D2_PSIP_DTDP=D**2*(3.D0*DDDT*DYNMDP_C+D*D2YNMDTDP_C)
       D2_PSIP_DP2 =D**3*D2YNMDP2_C
      ENDIF

      BRC_POL=(D2_PSIP_DRDT*DDDT+D_PSIP_DR*D2DDT2-D2_PSIP_DT2*DDDR
     * -D_PSIP_DT*D2DDRDT+CT/ST*(D_PSIP_DR*DDDT-D_PSIP_DT*DDDR)
     * -DDDR*D2_PSIP_DP2/ST**2)/R**2

      BTC_POL=-(D2_PSIP_DP2/R**2*DDDT/ST**2+D2_PSIP_DR2*DDDT
     *  +D_PSIP_DR*D2DDRDT-D2_PSIP_DRDT*DDDR)/R

      BPC_POL=(D2_PSIP_DRDP*DDDR+(D2_PSIP_DTDP*DDDT+D_PSIP_DP*D2DDT2
     *-CT/ST*D_PSIP_DP*DDDT)/R**2)/(R*ST)
C
c-----------------------------------------------------------------------
C  Toro (C):
C_______________________________________________________________________
c
      BRC_TOR=-D_PSIP_DP*DDDT/(R**2*ST)
      BTC_TOR= D_PSIP_DP*DDDR/(R*ST)     
      BPC_TOR=(D_PSIP_DR*DDDT-D_PSIP_DT*DDDR)/R     
c
c-----------------------------------------------------------------------
c  Polo (S):
C_______________________________________________________________________
C
      IF (L.EQ.0) THEN
       D_PSIP_DR   =0.D0
       D_PSIP_DT   =DYNMDT_S
       D_PSIP_DP   =DYNMDP_S
       D2_PSIP_DR2 =0.D0
       D2_PSIP_DRDT=0.D0
       D2_PSIP_DRDP=0.D0
       D2_PSIP_DT2 =D2YNMDT2_S
       D2_PSIP_DTDP=D2YNMDTDP_S
       D2_PSIP_DP2 =D2YNMDP2_S
      ENDIF

      IF (L.EQ.1) THEN
       D_PSIP_DR   =DDDR*YNM_S
       D_PSIP_DT   =D*DYNMDT_S+DDDT*YNM_S
       D_PSIP_DP   =D*DYNMDP_S
       D2_PSIP_DR2 =0.D0
       D2_PSIP_DRDT=DDDR*DYNMDT_S+D2DDRDT*YNM_S
       D2_PSIP_DRDP=DDDR*DYNMDP_S
       D2_PSIP_DT2 =D2DDT2*YNM_S+2.D0*DDDT*DYNMDT_S+D*D2YNMDT2_S
       D2_PSIP_DTDP=DDDT*DYNMDP_S+D*D2YNMDTDP_S
       D2_PSIP_DP2 =D*D2YNMDP2_S
      ENDIF

      IF (L.EQ.2) THEN
       D_PSIP_DR   =2.D0*D*DDDR*YNM_S
       D_PSIP_DT   =D*(2.D0*DDDT*YNM_S+D*DYNMDT_S)
       D_PSIP_DP   =D**2*DYNMDP_S
       D2_PSIP_DR2 =2.D0*DDDR**2*YNM_S
       D2_PSIP_DRDT=2.D0*(DDDR*(DDDT*YNM_S+D*DYNMDT_S)+D*D2DDRDT*YNM_S)
       D2_PSIP_DRDP=2.D0*D*DDDR*DYNMDP_S                 
       D2_PSIP_DT2 =2.D0*YNM_S*(DDDT**2+D*D2DDT2)+D*(4.D0*DDDT*DYNMDT_S
     *  +D*D2YNMDT2_S)
       D2_PSIP_DTDP=D*(D*D2YNMDTDP_S+2.D0*DDDT*DYNMDP_S)
       D2_PSIP_DP2 =D**2*D2YNMDP2_S
      ENDIF

      IF (L.EQ.3) THEN                                               
       D_PSIP_DR   =3.D0*D**2*DDDR*YNM_S
       D_PSIP_DT   =D**2*(3.D0*DDDT*YNM_S+D*DYNMDT_S)
       D_PSIP_DP   =D**3*DYNMDP_S
       D2_PSIP_DR2 =6.D0*D*DDDR**2*YNM_S
       D2_PSIP_DRDT=3.D0*D*((2.D0*DDDR*DDDT+D*D2DDRDT)*YNM_S
     *  +D*DDDR*DYNMDT_S)
       D2_PSIP_DRDP=3.D0*D**2*DDDR*DYNMDP_S                 
       D2_PSIP_DT2 =3.D0*D*(YNM_S*(2.D0*DDDT**2+D*D2DDT2)
     *  +2.D0*D*DDDT*DYNMDT_S)+D**3*D2YNMDT2_S
       D2_PSIP_DTDP=D**2*(3.D0*DDDT*DYNMDP_S+D*D2YNMDTDP_S)
       D2_PSIP_DP2 =D**3*D2YNMDP2_S
      ENDIF

      BRS_POL=(D2_PSIP_DRDT*DDDT+D_PSIP_DR*D2DDT2-D2_PSIP_DT2*DDDR
     * -D_PSIP_DT*D2DDRDT+CT/ST*(D_PSIP_DR*DDDT-D_PSIP_DT*DDDR)
     * -DDDR*D2_PSIP_DP2/ST**2)/R**2

      BTS_POL=-(D2_PSIP_DP2/R**2*DDDT/ST**2+D2_PSIP_DR2*DDDT
     *  +D_PSIP_DR*D2DDRDT-D2_PSIP_DRDT*DDDR)/R

      BPS_POL=(D2_PSIP_DRDP*DDDR+(D2_PSIP_DTDP*DDDT+D_PSIP_DP*D2DDT2
     *-CT/ST*D_PSIP_DP*DDDT)/R**2)/(R*ST)
c 
C-----------------------------------------------------------------------
c  Toro (S):
c_______________________________________________________________________
c
      BRS_TOR=-D_PSIP_DP*DDDT/(R**2*ST)
      BTS_TOR= D_PSIP_DP*DDDR/(R*ST)     
      BPS_TOR=(D_PSIP_DR*DDDT-D_PSIP_DT*DDDR)/R     
c_______________________________________________________________________
c
c  Convert to Cartesian:
c
      BT=BRC_TOR*ST+BTC_TOR*CT
      BXC_TOR(L,N,M)=BRC_TOR*CT-BTC_TOR*ST
      BYC_TOR(L,N,M)=BT*SP+BPC_TOR*CP 
      BZC_TOR(L,N,M)=BT*CP-BPC_TOR*SP 

      BT=BRS_TOR*ST+BTS_TOR*CT
      BXS_TOR(L,N,M)=BRS_TOR*CT-BTS_TOR*ST
      BYS_TOR(L,N,M)=BT*SP+BPS_TOR*CP 
      BZS_TOR(L,N,M)=BT*CP-BPS_TOR*SP 

      BT=BRC_POL*ST+BTC_POL*CT
      BXC_POL(L,N,M)=BRC_POL*CT-BTC_POL*ST
      BYC_POL(L,N,M)=BT*SP+BPC_POL*CP 
      BZC_POL(L,N,M)=BT*CP-BPC_POL*SP 

      BT=BRS_POL*ST+BTS_POL*CT
      BXS_POL(L,N,M)=BRS_POL*CT-BTS_POL*ST
      BYS_POL(L,N,M)=BT*SP+BPS_POL*CP 
      BZS_POL(L,N,M)=BT*CP-BPS_POL*SP 

      ENDDO
      ENDDO
      ENDDO

      RETURN
      END
C
C=================================================================================
C
      SUBROUTINE LEGENDASS_SCHMIDT_FLO(N,CT,ST,PNM,DPNMDT,D2PNMDT2,IFL)   
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (NMAX=8)                                       
      DIMENSION PNM(0:N,0:N),DPNMDT(0:N,0:N),D2PNMDT2(0:N,0:N)
      COMMON /SCHMIDT_FLO/ SNM(0:NMAX,0:NMAX)
C
C     INPUT:  N - UPPER LIMIT ON N & M;  CT = COS(THETA); ST=SIN(THETA)  
C           IFL - TURNS ON/OFF 2ND DERIVATIVE CALCULATION (1/0)
C
      PNM     (0,0)=1.D0 
      DPNMDT  (0,0)=0.D0 
      D2PNMDT2(0,0)=0.D0 
c
      DO I=1,N                        ! calculate diagonal PNM,DPNMDT,D2PNMDT2
       IM1=I-1
       PNM   (I,I)  =ST*PNM(IM1,IM1) 
       DPNMDT(I,I)  =ST*DPNMDT(IM1,IM1)+CT*PNM(IM1,IM1)
       IF (IFL.NE.0) D2PNMDT2(I,I)=2.D0*CT*DPNMDT(IM1,IM1)
     * +ST*(D2PNMDT2(IM1,IM1)-PNM(IM1,IM1))
      ENDDO
c
      DO I=1,N
       IM1=I-1
       DO J=0,IM1
        IF (I.EQ.1) THEN
         PNM(I,J)=CT*PNM(IM1,J)
         DPNMDT(I,J)=CT*DPNMDT(IM1,J)-ST*PNM(IM1,J)
         IF (IFL.NE.0) D2PNMDT2(I,J)=-2.D0*ST*DPNMDT(IM1,J)
     *   +CT*(D2PNMDT2(IM1,J)-PNM(IM1,J))  
        ELSE
         XK=DFLOAT((IM1)*(IM1)-J*J)/DFLOAT((2*IM1)*(2*I-3))
         PNM(I,J)=CT*PNM(IM1,J)-XK*PNM(I-2,J)
         DPNMDT(I,J)=CT*DPNMDT(IM1,J)-ST*PNM(IM1,J)-XK*DPNMDT(I-2,J)
         IF (IFL.NE.0) D2PNMDT2(I,J)=-2.D0*ST*DPNMDT(IM1,J)
     *   +CT*(D2PNMDT2(IM1,J)-PNM(IM1,J))-XK*D2PNMDT2(I-2,J)
        ENDIF
       ENDDO
      ENDDO
c
      DO I=1,N   !  normalize by Schmidt
      DO J=0,I
       PNM(I,J)=PNM(I,J)*SNM(I,J)
       DPNMDT(I,J)=DPNMDT(I,J)*SNM(I,J)
       IF (IFL.NE.0) D2PNMDT2(I,J)=D2PNMDT2(I,J)*SNM(I,J)
      ENDDO
      ENDDO

      RETURN
      END
C
C===========================================================================================
C
      SUBROUTINE SHUE (RS,THETA,PHI,ALP,X,Y,Z,EXN,EYN,EZN) 
      IMPLICIT REAL*8 (A-H,O-Z)   ! input: RS,THETA,PHI,ALP; output: X,Y,Z,EXN,EYN,EZN
c
c  THETA & PHI define a ray from origin; 
c    RS is the standoff distance, 
c   ALP is the flaring parameter (ALP=0.5 gives a cylindrical distant MP; 
c                                 ALP >/< 0.5 gives expanding/tapering tail)
c  X,Y,Z are coords of the ray intersection with the MP, EXN,EYN,EZN are local normal compts
c
      CT=COS(THETA)
      ST=SIN(THETA)
    
      RMP=RS*(2.D0/(1.D0+CT))**ALP
      X  =RMP*CT
      Y  =RMP*ST*SIN(PHI)
      Z  =RMP*ST*COS(PHI)

      DFDX=(X+ALP*(RMP-X))/RMP
      FACTOR=(1.D0-ALP/(RMP+X)*X)/RMP
      DFDY=Y*FACTOR
      DFDZ=Z*FACTOR
     
      GRADF=SQRT(DFDX**2+DFDY**2+DFDZ**2)
      EXN=DFDX/GRADF
      EYN=DFDY/GRADF
      EZN=DFDZ/GRADF

      RETURN
      END
C
C========================================================================================== 
C                    
