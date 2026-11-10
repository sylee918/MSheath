      IMPLICIT REAL*8 (A-H,O-Z)
      CHARACTER NAMEPAR*80
c
      PARAMETER (NAMEPAR='Best_par_so_far_TPS.par')           ! name of TPS parameter file (magnetosheath)
      PARAMETER (NLIN=1632,NNON=5,NNON1=6,NTOT=1637)  ! NLIN depends on LMAX & NMAX (here 2 & 8); update if necessary
c
      PARAMETER (NMAX=8)    !  upper limit of the spherical function order     
c
      DIMENSION A_VAC(NNON) !  this array contains magnetopause model parameters
      DIMENSION PARMOD(12)
      COMMON /SCHMIDT/ SNM(0:NMAX,0:NMAX)        ! Schmidt normalization factors      
C
      COMMON /NONLINEARS/ RS0,EPS,DFSC,ALP0,ALP1,FSC,ALP  ! first 5 are forwarded from the magnetopause parameter file
c  
C                             RS0:           location of Delta=0 reference point at the MP
c                                 EPS:         EPS exponent for Pdyn dependence of MP standoff distance
c                                     DFSC:      coefficient in standoff scaling sensitivity to BSIMF
c                                          ALP0:  free term in MP flaring parameter    
c                                               ALP1:   coeff by exp(-Bz/10) in MP flaring parameter             
C                                                    FSC: scaling factor for coords and standoff distance 
c                                                        ALP added to forward it to B_CART                                            
      COMMON /PAR_TPS/ A_TPS(NLIN)
c
c    Read magnetopause model parameters:
c
      OPEN(UNIT=1,FILE='Best_par_so_far_em4_VAC.par',STATUS='OLD')  
       DO J=1,4+NNON
       IF (J.LE.4) READ (1,811) DUMMY      ! skip first 4 records (linears) in the VAC parameter file
       IF (J.GT.4) READ (1,811) A_VAC(J-4) ! read A_VAC(1) - A_VAC(NNON)
       ENDDO
      CLOSE(1)
811   FORMAT (G15.6)

      RS0 =A_VAC(1)*10. ! best-fit average standoff distance           
      EPS =A_VAC(2)     ! m-pause standoff compression/expansion exponent: (P/<P>)^EPS
      DFSC=A_VAC(3)     ! m-pause Bz-related erosion coeffcnt in: DFSC*(Bz/10)
      ALP0=A_VAC(4)     ! MP flaring Shue parameter: free term
      ALP1=A_VAC(5)     ! MP flaring Shue parameter: coefficient by exp(-BzIMF/10)   
C
      open (unit=8,file='Best_par_so_far_TPS.par')   ! read magnetosheath flow model parameters
      read (8,811) (A_TPS(j),j=1,NLIN)
      close(8)
c________________________________________________________________________________________________________
c
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
      VSW=400.D0  !  nominal solar wind speed, km/s
      DSW=  5.D0  !  nominal s.w. proton density, cm^-3

456   print *,
     *' Enter dipole tilt (degs), IMF B, cone, and clock angles (degs)'

      read *, PSI_d,BIMF,Cone_d,Clock_d
      PSI=PSI_d*0.0174532925199d0
      Cone=Cone_d*0.0174532925199d0
      Clock=Clock_d*0.0174532925199d0
      BXIMF_GSW= BIMF*cos(Cone)
      BYIMF_GSW= BIMF*sin(Cone)*sin(Clock)
      BZIMF_GSW= BIMF*sin(Cone)*cos(Clock)

      PARMOD(1)=PSI
      PARMOD(2)=BXIMF_GSW 
      PARMOD(3)=BYIMF_GSW 
      PARMOD(4)=BZIMF_GSW 
      PARMOD(5)=VSW            ! s.w. speed in km/s
      PARMOD(6)=DSW            ! s.w. ion (proton) density in cm^-3
      PDSW=1.937D-6*DSW*VSW**2
      PARMOD(7)=PDSW            

      FSC   = (PDSW/2.0D0)**EPS +DFSC*(BZIMF_GSW/10.) ! scale standoff distance by (PD/2.0D0)^EPS & (BZIMF/10) 
      ALP   = ALP0 + ALP1*EXP(-BZIMF_GSW/10.D0) 

      XMS  =  5.7   !  mean value of MS Mach # (see d:\Useful_stuff_and_tools\OMNI_statistics\...)
      XMA  = 10.2   !  mean value of Alfven Mach # (see d:\Useful_stuff_and_tools\OMNI_statistics\...)
      BETA =  2.9   !  mean beta (see ..\02_10_From_NN_approach_back_to_global_universal_model\)  ! USED FOR PLOTTING THE BOW SHOCK

      PRINT *,''
      PRINT *, ' PSI  =',PSI
      PRINT *, ' PD   =',PDSW 
      PRINT *, ' BXIMF=',BXIMF_GSW
      PRINT *, ' BYIMF=',BYIMF_GSW
      PRINT *, ' BZIMF=',BZIMF_GSW
c
1234   print *,''
       print *,'  Enter x,y,z'
       read *, x,y,z
       call MSH_FLOW (PARMOD,X,Y,Z,FX,FY,FZ)        
       print *,' Fx=',FX,' Fy=',FY,' Fz=',FZ
       goto 1234 
C
      END
C_________________________________________________________________________________________
C
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
      CALL LEGENDASS_SCHMIDT (NMAX,CT,ST,ASLPNM,DASLPNM,D2ASLPNM,1) ! calculates full set of ass. Legendre polynomials
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
      SUBROUTINE LEGENDASS_SCHMIDT(N,CT,ST,PNM,DPNMDT,D2PNMDT2,IFL)   
      IMPLICIT REAL*8 (A-H,O-Z)
      PARAMETER (NMAX=8)                                       
      DIMENSION PNM(0:N,0:N),DPNMDT(0:N,0:N),D2PNMDT2(0:N,0:N)
      COMMON /SCHMIDT/ SNM(0:NMAX,0:NMAX)
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
C
      PS=PSI      !     assume that Psi are in radians (not clear from the LU's paper)
C                      NOTE OF 12/08/22: BASED ON THE VALUE OF A4 IN LU's PAPER, PSI IS, OF COURSE, IN RADIANS, NOT DEGS!
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
c@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
