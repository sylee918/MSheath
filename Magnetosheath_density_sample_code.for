      P r o g r a m   RUNMODEL
c
      IMPLICIT  REAL * 8  (A - H, O - Z)
      CHARACTER*80 NAMEPAR  ! name of the model parameter file
C
      PARAMETER (NLIN=1605,NNON=4,NNON1=5,NTOT=1609)  ! NLIN & NNON, are the numbers of linear & nonlinear model parameters
c                                                       NTOT=NLIN+NNON
c  
      PARAMETER (NMAX=10)                             ! max order of Legendre polynomials in the model density expansions  
c
      PARAMETER (INDEPVAR=12)  ! 12 input variables: XGSW,YGSW,ZGSW,PSI,BXIMF,BYIMF,BZIMF,DSW,VSW,WSW,PDSW,IFL 
c
      PARAMETER (NDEPVAR =1)   ! output variable: magnetosheath proton density  
      PARAMETER (NUMVTOT =13)  ! NUMVTOT=INDEPVAR+NDEPVAR
c
      DIMENSION XI(INDEPVAR),F(NDEPVAR),DER(NLIN),A(NTOT),IA(NTOT)
c
c     Array A is the vector of independent model parameters (coefficients)
C
      COMMON /SCHMIDT/ SNM(0:NMAX,0:NMAX)   !  Schmidt normalization factors for spherical functions
      COMMON /RS0_ALP/ RS0,ALP              !  Reference boundary subsolar distance and flaring parameter, resp.
      DATA  IA /NTOT*1/                     !  ALL PARAMETERS UNFIXED BY DEFAULT

      RS0=11.0d0     ! subsolar position of the reference boundary  
      ALP=0.7d0      ! flaring parameter 
c
C$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
c
c  Read initial parameter file (only nonlinears are actually needed at this point):
c
      NAMEPAR='Density_Best_par_so_far_em6.par' ! name of the input parameter file, created earlier by AMOEBA 

      OPEN (UNIT=1,FILE=NAMEPAR,STATUS='OLD')  
      READ (1,811) (A(jjj),jjj=1,NTOT)
811   FORMAT(G15.6)
      CLOSE(1)
C
      SNM(0,0)=1.D0   !  populate array SNM with Schmidt normalization factors
      DO N=1,NMAX
       SNM(N,0)=SNM(N-1,0)*DFLOAT(2*N-1)/N
       DO M=1,NMAX
        IF (M.EQ.1) THEN 
         XJ=2.D0 
        ELSE 
         XJ=1.D0 
        ENDIF
        SNM(N,M)=SNM(N,M-1)*SQRT(DFLOAT(N-M+1)*XJ/(N+M))
       ENDDO
      ENDDO
C
c________________________________________________________________

6789  PRINT *,''
      PRINT *, 'Enter:'
      PRINT *,   ' S.W.speed, proton density, thermal energy, BxIMF,
     * ByIMF,BzIMF, dipole tilt'
      PRINT *, 
     *'    (km/s,  cm^-3,          eV,             nT (GSM),                  
     *degrees)'
      READ *, VSW,DSW,WSW,BxIMF,ByIMF,BzIMF,PSID
      PSI=PSID*0.01745329252D0

12345 PRINT *,''
      PRINT *,'Enter GSM coordinates XGSM,YGSM,ZGSM (in Re)'
      PRINT *,
     *' (to change S.W parameters or dipole tilt angle, enter XGSM>100)'
      READ *,X,Y,Z
      IF (X.GT.100.D0) GOTO 6789

      PD=1.937D-6*DSW*VSW**2
      PM=0.0004D0*(BxIMF**2+ByIMF**2+BzIMF**2)
      XMS  =  5.7   !  mean value of the solar wind magnetosonic Mach # (used by Lu et al. bow shock model)
      BETA =  2.9   !  mean solar wind beta (used by Lu et al. bow shock model)

      PDPM=PD+PM    ! SOLAR WIND TOTAL PRESSURE (GAS + IMF)
c
      XI(1)=X
      XI(2)=Y
      XI(3)=Z
      XI(4)=PSI
      XI(5)=BxIMF
      XI(6)=ByIMF
      XI(7)=BzIMF
      XI(8)=DSW
      XI(9)=VSW
      XI(10)=WSW
      XI(11)=PD
      FFMAX=0.
        
      CALL BS (X,Y,Z,PSI,PD,BZIMF,XMS,BETA,RBS,IDBS)
        IF (IDBS.LT.0) THEN
         DEN=XI(8)                       ! in the solar wind (outside the BS)
        ELSE                             ! inside bow shock (and, maybe, in the magnetosphere)
         R=SQRT(X**2+Y**2+Z**2)
         CALL LIN_ET_AL_2010 (X,Y,Z,PSI,PD,PM,BZIMF,RMP_LIN,ID) 
         IF (R.GT.RMP_LIN) THEN                       ! in the magnetosheath
         CALL MODELVEC(1,A,XI,F,DER,IA,NLIN,NTOT,NNON,INDEPVAR,NDEPVAR)
          DEN= F(1)
         ELSE
          DEN=0.D0
         ENDIF          
        ENDIF    

      PRINT *, 'PROTON DENSITY = ',DEN       

      GOTO 12345

      END
c
C=================================================================================================
C
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
c_______________________________________________________________________________________________
c
      SUBROUTINE MODELVEC (ID,A,XI,F,DER,IA,NLIN,NTOT,NNON,
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
      COMMON /RS0_ALP/ RS0,ALP   ! conveys here RS0 and ALP from the main program

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
      CALL FC_FS (LMIN,LMAX,Xs,Ys,Zs,FC,FS)
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
      SUBROUTINE FC_FS (LMIN,LMAX,X,Y,Z,FC,FS)                             ! based on given {X,Y,Z}, LMIN & LMAX, fills the arrays FC and FS 
      IMPLICIT REAL*8 (A-H,O-Z)                                            ! with values of basis elements, corresponding to a given range of
      PARAMETER (NMAX=10)                                                   ! (1) powers D^L (LMIN<=L<=LMAX; D=1-RS/RS0) 
      DIMENSION FC(LMIN:LMAX,1:NMAX,0:NMAX),FS (LMIN:LMAX,1:NMAX,0:NMAX)  ! (2) spherical harmonic orders: 1<=N<=NMAX
C                                                                          ! (3) spherical harmonic azimuthal ##s: 0<=M<=NMAX
C                                                                          !    for C- (cos(m*phi)) and S (sin(m*phi))  modes
      DIMENSION ASLPNM(0:NMAX,0:NMAX)
C  
      COMMON /RS0_ALP/ RS0,ALP                             ! conveys here RS0 and ALP from MODELVEC and main program
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
       CALL LEGENDASS_SCHMIDT (NMAX,CT,ST,ASLPNM)                           ! calculates full set of ass. Legendre polynomials
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
      SUBROUTINE LEGENDASS_SCHMIDT(N,CT,ST,PNM)   
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (NMAX=10)                         
      DIMENSION PNM(0:N,0:N)                                       
      COMMON /SCHMIDT/ SNM(0:NMAX,0:NMAX)
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
