RESEARCH ARTICLE Magnetosheath Plasma Flow and Its Response to IMF and
10.1029/2024JA033233 Geodipole Tilt as Obtained From the Data‐Based Modeling
KeyPoints: N.A.Tsyganenko1 ,V.S.Semenov1 ,N.V.Erkaev2,3,andN.T.Gubaidulin1
• Large‐scalepatternsofthemagneto-
sheathplasmaflowarereconstructed 1SaintPetersburgStateUniversity,SaintPetersburg,Russia,2InstituteofComputationalModellingofSiberianBranchof
frommulti‐yearsetsofinsitudataand theRussianAcademyofSciences,Krasnoyarsk,RussianFederation,3AppliedMechanicsCathedra,SiberianFederal
anadvancedempiricalmodel
• Substantialinterplanetarymagnetic University,Krasnoyarsk,RussianFederation
fieldinfluenceontheflowpatternsis
revealed,inducedbymagneticfield
compressionandtensionsinsidethe Abstract Large‐scalepatternsofthesteady‐statemagnetosheathplasmaflowandtheirdependenceonthe
magnetosheath interplanetarymagneticfield(IMF)havebeenreconstructedforthefirsttimeonthebasisoflargemulti‐year
• Plasmaflowssignificantlydependon
multi‐missionpoolofspacecraftobservations,concurrentinterplanetarydata,andanempiricalhigh‐resolution
thedipoletilt,indicatingtheimportant
roleofreconnectioneffectsaroundthe model.Theflowmodelarchitecturebuildsuponarecentlydevelopedmagnetosheathmagneticfield
daysidemagnetopause representationbyflexibleexpansionsofitstoroidalandpoloidalcomponentsinacoordinatesystem,naturally
conformedwiththemagnetopauseandbowshockshapes.Themodelincludestwophysics‐basedflow
Correspondenceto: symmetrymodes:thefirstonetreatsthemagnetosphereasanaxisymmetricunmagnetizedobstacle,whereasthe
N.A.Tsyganenko, secondmodetakesintoaccountthegeodipoletilt,animportantfactorinthereconnectioneffects.Thespacecraft
n.tsyganenko@spbu.ru datapoolincludes1‐minaveragedatabyThemis(2007–2024),Cluster(2001–2022),andMMS‐1(2015–2024)
missions,aswellasOMNIinterplanetarydata.Themodeldriversincludethesolarwindparticleflux,IMF
Citation: components,andthegeodipoletiltangle.Themodelcalculationsfaithfullyreproducetheaverageplasmaflow
Tsyganenko,N.A.,Semenov,V.S., geometryandsubstantialeffectshavebeenfoundoftheIMForientationandmagnitude,aprincipalfactorthat
Erkaev,N.V.,&Gubaidulin,N.T.(2024).
defineselectromagneticforcesinsidethemagnetosheath.Astrongdependenceofthemagnetosheathflow
Magnetosheathplasmaflowandits
responsetoIMFandgeodipoletiltas patternsontheEarth'sdipoletiltindicatesanimportantcontributionofreconnectioneffectsatthemagnetopause
obtainedfromthedata‐basedmodeling. tothesolarwindparticletransportaroundthedaysidemagnetosphere.
JournalofGeophysicalResearch:Space
Physics,129,e2024JA033233.https://doi.
Plain Language Summary Asaresultofthesolarwindinteractionwiththegeomagneticfield,the
org/10.1029/2024JA033233
Earth'smagnetospherebecomesembeddedwithinahuge“cocoon”,avastregionbetweenthebowshockand
Received27AUG2024 themagnetopause,wheretheincomingplasmastreamgetscompressed,heated,anddivertedsidewaysaround
Accepted19OCT2024
themagnetosphericboundary.Animportantfactorthatsignificantlyaffectsthemagnetosheathflowisthe
interplanetarymagneticfield(IMF),transportedtotheEarth'sorbitfromthesolarcorona.TheIMFundergoes
AuthorContributions:
compressionanddeformationinsidethemagnetosheath;theresultingelectromagneticforcessubstantially
Conceptualization:N.A.Tsyganenko,
V.S.Semenov,N.V.Erkaev affecttheplasmaflow.Furthermore,themagneticfieldsofsolarandterrestrialorigincanreconnectatthe
Datacuration:N.A.Tsyganenko, magnetopause,whichresultsinadditionalmodificationsoftheplasmaflowpattern.Duringthelastdecades,
N.T.Gubaidulin
hugeamountsofsatellitedatawereobtainedinthenear‐Earthspace;usingthemincombinationwithaflexible
Formalanalysis:N.A.Tsyganenko,
N.V.Erkaev mathematicalmodelallowedustoquantitativelyreconstructthemagnetosheathplasmaflowsandtheir
Fundingacquisition:V.S.Semenov dependenceontheinterplanetaryfactorsandorientationoftheEarth'smagneticdipole.Thepresentpaper
Investigation:N.A.Tsyganenko
describesfirstresultsofthatstudy.
Methodology:N.A.Tsyganenko,
V.S.Semenov
Projectadministration:V.S.Semenov
Resources:V.S.Semenov
1. Introduction
Software:N.A.Tsyganenko
Supervision:V.S.Semenov
Notwithstanding the widespread and fast‐expanding use of first‐principle simulations, the data‐constrained
Validation:N.A.Tsyganenko
Visualization:N.A.Tsyganenko modeling remains an effective instrument for studying the geospace and its response to interplanetary condi-
Writing–originaldraft: tions.Thisisespeciallytrueinviewofthetremendousinflowofnewdataandrapidlygrowinghistoricaldata
N.A.Tsyganenko
archivesduringthelastdecades.Sincealmosttwocenturiesago,atraditionalobjectofthedata‐basedmodeling
Writing–review&editing:
N.A.Tsyganenko,V.S.Semenov, hasbeenthegeomagneticfield,startingfromthefirstmainfieldmodeldevelopedbyGaussinthelate1830sand
N.V.Erkaev followedmuchlaterbyfirstsuccessfulattempts(Mead&Fairfield,1975)toexpandthemodelingregionfromthe
groundandlowaltitudestothedistantmagnetosphere.Exceptforpurelystatisticalstudies(e.g.,Dimmocketal.,
2020;Zhang etal.,2019), relativelylessattention was paidto the data‐basedmodeling ofthe turbulentmag-
netosheath.FirstsuccessfuleffortsinthatareaweremaderecentlybyMichottedeWelleetal.(2022,2024),who
directlyreconstructedthemagnetosheathmagneticfieldfromalargepoolofspacecraftdata,makingitpossibleto
visualize the field line draping about the magnetosphere. Jung et al. (2024) provideda parameterized magne-
©2024.AmericanGeophysicalUnion.All
RightsReserved. tosheathmodel,thoughbasedsolelyonsimulationsandtheory.Adifferentapproach,employinganadvanced
TSYGANENKOETAL. 1of17

 21699402, 2024, 11, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233 by Nasa Goddard, Wiley Online Library on [06/11/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical | Research: | Space | Physics |     |     |     |     |     |     |
| ------- | -------------- | --------- | ----- | ------- | --- | --- | --- | --- | --- | --- |
10.1029/2024JA033233
|     |     | mathematicalmodel |     | of  | themagnetosheath |     | field andalargespacecraft |     |     | data |
| --- | --- | ----------------- | --- | --- | ---------------- | --- | ------------------------- | --- | --- | ---- |
archivewaspursuedintworecentstudiesbyTsyganenkoetal.(2023,2024;
|     |     | referred       | henceforth | as  | TSE23        | and TSEG24), | which        | made     | it possible | to      |
| --- | --- | -------------- | ---------- | --- | ------------ | ------------ | ------------ | -------- | ----------- | ------- |
|     |     | quantitatively | represent  |     | the magnetic | field        | and electric | currents | for         | various |
IMForientationsbymeansofself‐containedmodelalgorithms.
Thenextnaturalandchallengingquestionis,whetheritispossibletousethe
archiveddataandasimilarempiricalapproachtoreconstructtheplasmabulk
flowsaroundthemagnetosphereandexploretheirresponsetoIMForienta-
tionandmagnitude?Previouseffortsinthisdirectionshouldbementioned,
namely,astudybySoucekandEscoubet(2012)andamorerecentworkby
Naritaetal.(2023).Bothofthemadheredtoanearlierdevelopedapproachby
|     |     | Kobel | and Flückiger | (1994), | based | on a grossly |     | simplified | assumption | of  |
| --- | --- | ----- | ------------- | ------- | ----- | ------------ | --- | ---------- | ---------- | --- |
current‐freemagneticfield.Moreover,thestudybyNaritaetal.wasbasedon
representingtheplasmavelocityasthegradientofascalarpotential.Given
Figure1. (FromTSE23/TSEG24).Illustratingthecoordinates.Cartesian: the complex turbulent nature of the observed magnetosheath with strongly
GSWsystemwithX‐axisantiparalleltosolarwindflow;spherical:radial compressed/deformedmagneticfieldsandsheared(hence,rotational)plasma
distancer,coneandclockanglesθ = arccos(X/r)andϕ = arctan(Y/Z), flows,neitheroftheaboveassumptionsisrealistic.
resp.Thegray‐shadedsurfacesarethoseofconstantδ(r,θ),suchthatδ =0
correspondstothemodelmagnetopause. Inthispaperwepresentfirstresultsofanattempttoempiricallymodelthe
|     |     | magnetosheath |     | plasma | flow, based | on a large | pool | of in | situ plasma | and |
| --- | --- | ------------- | --- | ------ | ----------- | ---------- | ---- | ----- | ----------- | --- |
magnetometerdatatakenduringthelastdecadesandaflexiblemathematicalmodel,derivedalongthesamelines
asthepreviouslydevelopedmagnetosheathmagneticfieldrepresentations.Thepaperisorganizedasfollows:the
nextSection2describesthemodelarchitecture,Section3brieflyoutlinesthedatabase,Section4presentsmain
results,theDiscussionSection5focusesonthedipoletilteffects,andSection6summarizestheresults.
| 2.  | Model |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
FollowingtheapproachofTSE23andTSEG24,weemployCartesianGSWsystem,similartothestandardGSM,
butwithXaxisantiparalleltotheobservedsolarwindflowandZaxislyingintheplanedefinedbytheXaxisand
thegeodipolemoment.ThusdefinedX ,Y ,andZ arethentransformedintothe{δ,θ,ϕ}coordinate
|     |     | GSW | GSW | GSW |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
system,naturallyconformedwiththeobservedshapeofthemagnetopauseandbowshock,asshowninFigure1
(reproducedfromourabovecitedpapers).Thecoordinate
|     |     |     | δ(r,θ)=1− | rcos2α(θ/2)/R |     |     |     |     |     | (1) |
| --- | --- | --- | --------- | ------------- | --- | --- | --- | --- | --- | --- |
S
serves as a measure of separation between an arbitrary point {r,θ,ϕ} and the axially symmetric surface
= R/cos2α(θ/2),
r S (θ,R S ,α) S first proposed by Shue et al. (1997) as a simple model approximation for the
magnetopause shape and size. Here R is the subsolar radius of the boundary, while α quantifies its dayside
S
curvatureandtailwardexpansionrate.
ThemodelarchitectureisbasedonrepresentingthebulkparticleflowvectorF = ρvwithasumoftoroidaland
poloidalparts
|                           |     | F= ∑∇Ψ(lnm)×∇δ+∇×                  |     |     | ∑∇Ψ(lnm)×∇δ |     |     |     |     | (2) |
| ------------------------- | --- | ---------------------------------- | --- | --- | ----------- | --- | --- | --- | --- | --- |
|                           |     |                                    | t   |     |             | p   |     |     |     |     |
|                           |     | l,n,m                              |     |     | l,n,m       |     |     |     |     |     |
| whosegeneratingfunctionsΨ |     | andΨ areeachexpandedintotriplesums |     |     |             |     |     |     |     |     |
t p
|     |     |                     | L   |     | N n           |     |     |     |     |     |
| --- | --- | ------------------- | --- | --- | ------------- | --- | --- | --- | --- | --- |
|     |     | Ψ(r,θ,ϕ)=∑δl(r,θ)∑  |     |     | ∑V(lnm)(θ,ϕ)  |     |     |     |     | (3) |
|     |     | t                   |     |     |               | t   |     |     |     |     |
|     |     |                     | l=0 |     | n=1 m=0       |     |     |     |     |     |
|     |     |                     | L   |     | N n           |     |     |     |     |     |
|     |     | Ψ (r,θ,ϕ)=∑δl(r,θ)∑ |     |     | ∑V(lnm)(θ,ϕ), |     |     |     |     | (4) |
|     |     | p                   |     |     | p             |     |     |     |     |     |
|     |     |                     | l=0 |     | n=1 m=0       |     |     |     |     |     |
TSYGANENKOETAL. 2of17

 21699402, 2024, 11, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233 by Nasa Goddard, Wiley Online Library on [06/11/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical |     |     | Research: |     | Space | Physics |     |     |     |     |
| ------- | -------------- | --- | --- | --------- | --- | ----- | ------- | --- | --- | --- | --- |
10.1029/2024JA033233
| whereV(lnm) |     | andV(lnm) |     |     |     |     |     |     |     |     |     |
| ----------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arestandardsphericalfunctions
|                                      | t   |     | p   |                      |                          |         |            |     |        |     |     |
| ------------------------------------ | --- | --- | --- | -------------------- | ------------------------ | ------- | ---------- | --- | ------ | --- | --- |
|                                      |     |     |     | V(lnm)=Pm(cosθ)(g(t) |                          |         | cosmϕ+h(t) |     |        |     |     |
|                                      |     |     |     |                      |                          |         |            |     | sinmϕ) |     | (5) |
|                                      |     |     |     | t                    |                          | n lnm   |            | lnm |        |     |     |
|                                      |     |     |     | V(lnm)               | =Pm(cosθ)(g(p)cosmϕ+h(p) |         |            |     |        |     |     |
|                                      |     |     |     |                      |                          |         |            |     | sinmϕ) |     | (6) |
|                                      |     |     |     | p                    |                          | n lnm   |            | lnm |        |     |     |
| withfreeunknowncoefficientsg(t),h(t) |     |     |     |                      | ,g(p),andh(p).           |         |            |     |        |     |     |
|                                      |     |     |     | lnm                  | lnm                      | lnm lnm |            |     |        |     |     |
Accordingly,thetotaltoroidalandpoloidalcomponentsoftheflowvectorread
|     |     |     |     |      | L N | n           |     | L N     | n        |     |     |
| --- | --- | --- | --- | ---- | --- | ----------- | --- | ------- | -------- | --- | --- |
|     |     |     |     | F =∑ | ∑   | ∑f(lnm) and | F   | =∑ ∑    | ∑f(lnm), |     | (7) |
|     |     |     |     | t    |     | t           | p   |         | p        |     |     |
|     |     |     |     | l=0  | n=1 | m=0         |     | l=0 n=1 | m=0      |     |     |
wherethepartialflowsf(lnm)andf(lnm)implicitlyincludethecoefficientsg(t),h(t) ,g(p),h(p),eachofwhichis
|     |     |     | t   |     | p   |     |     |     | lnm | lnm lnm lnm |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- |
expandedintolinearcombinationsofconcurrentexternaldrivers:(a)thesolarwindprotonfluxF = n v ,(b)
sw p sw
| IMFB | ,B  | ,B,and(c)sine/cosineofthegeodipoletiltangleψ,suchthat |     |     |     |     |     |     |     |     |     |
| ---- | --- | ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
x y z
|     |     | g(t,p)= |     | [g(t,p,0)+g(t,p,1)cosψ+g(t,p,2)sinψ+g(t,p,3)B |     |     |     |     | +g(t,p,4)B | +g(t,p,5)B |     |
| --- | --- | ------- | --- | --------------------------------------------- | --- | --- | --- | --- | ---------- | ---------- | --- |
F
|     |     | lnm | sw          | lnm | lnm             | lnm             |                | lnm | x lnm  | y lnm z |     |
| --- | --- | --- | ----------- | --- | --------------- | --------------- | -------------- | --- | ------ | ------- | --- |
|     |     |     | +g(t,p,6)B  |     | +g(t,p,7)B      | +g(t,p,8)B      | sinψ+g(t,p,9)B |     |        |         | (8) |
|     |     |     |             | x B | y               | x B z           | x              |     | x cosψ |         |     |
|     |     |     |             | lnm | lnm             | lnm             |                |     | lnm    |         |     |
|     |     |     | +g(t,p,10)B |     | sinψ+g(t,p,11)B | cosψ+g(t,p,12)B |                |     |        |         |     |
sinψ]
|     |     |         |     | lnm y                                         |     | lnm y | lnm | z   |            |            |     |
| --- | --- | ------- | --- | --------------------------------------------- | --- | ----- | --- | --- | ---------- | ---------- | --- |
|     |     | h(t,p)= |     | [h(t,p,0)+h(t,p,1)cosψ+h(t,p,2)sinψ+h(t,p,3)B |     |       |     |     | +h(t,p,4)B | +h(t,p,5)B |     |
F
|     |     | lnm | sw          | lnm | lnm             | lnm             |                | lnm | x lnm | y lnm z |     |
| --- | --- | --- | ----------- | --- | --------------- | --------------- | -------------- | --- | ----- | ------- | --- |
|     |     |     | +h(t,p,6)B  |     | +h(t,p,7)B      | +h(t,p,8)B      | sinψ+h(t,p,9)B |     |       |         | (9) |
|     |     |     |             | x B | y               | x B z           | x              |     | x     | cosψ    |     |
|     |     |     |             | lnm | lnm             | lnm             |                |     | lnm   |         |     |
|     |     |     | +h(t,p,10)B |     | sinψ+h(t,p,11)B | cosψ+h(t,p,12)B |                |     |       |         |     |
sinψ]
|     |     |     |     | lnm y |     | lnm y | lnm | z   |     |     |     |
| --- | --- | --- | --- | ----- | --- | ----- | --- | --- | --- | --- | --- |
Beforeproceedingfurther,threeimportantcaveatsshouldbehighlighted.First,thetoroidal/poloidalrepresen-
tation (Equation 2) is divergence‐free by construction. While this property is required and thus perfectly
appropriateforthemagneticfieldmodeling,inthecaseofparticleflowreconstructionthecontinuityequation
∂ρ/∂t+∇⋅(ρv) = 0 restricts the analysis to only steady‐state conditions with ∂ρ/∂t = 0, such that
∇⋅(ρv)= ∇⋅F = 0.Second,aswasalreadyrealizedintheearlierTSE23andTSEG24studies,includinginthe
representationEquations3–9alltermswitheverypossiblecombinationoftheindicesnandmisutterlyunfeasible
becauseof(a)unevendatadistributioninbothgeometricandparametricspace,(b)veryhighturbulencelevelin
thedata,and(b)unreasonablylargenumberofunknowncoefficients.Allthesefactorscombinedwouldresultnot
onlyincomputationallyexpensiveandunstableinversionalgorithms,butalsomakeithardtodistinguishbetween
realfeaturesandmodelingartifacts.Toavoidthesecomplications,weintroducephysics‐basedsymmetrycon-
ditions, explained in detail below, which greatly simplify the model and effectively eliminate 70%–80% of
(virtuallyredundant)unknowncoefficients.Third,inourpreviouslydevelopedmagneticfieldmodelsTSE23and
TSEG24, the IMF was a principal driving factor, such that the main linear terms in the magnetosheath field
expansionswerethoseproportionaltoIMFB ,B ,andB.Inthepresentcase,thesituationissomewhatdifferent:
|     |     |     |     |     |     | x y | z   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
themagnetosheathplasmabulkflowismainlycontrolledbytheincomingsolarwind,alwaysdirectedalongthe
X axis(bydefinitionorientedantiparalleltothesolarwind),whiletheIMFplaysaroleofasecond‐order
GSW
disturbance factor, modifying the diverging magnetosheath flow lines due to (a) magnetic forces caused by
IMFcompression/deformationinsidethemagnetosheathand(b)reconnectionphenomenaattheboundary.
Thedifferencebetweenthelattertwoeffectsentailsimportantimplicationsregardingthemodelflowsymmetry.
Namely, when representing the magnetosheath flow deformations due to the IMF compression/tension, the
axisymmetric magnetopause can be viewed as an unmagnetized blunt obstacle, such that the flow symmetry
propertiesareentirelydictatedbytheIMForientationandhavenorelationtothemagnetosphericmagneticfield
insidethemagnetopause.
TSYGANENKOETAL. 3of17

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure2. Explainingthehierarchyofmodelexpansionterms,theirindexlimits,andthefluxcomponentparities,graphically
illustratedinthediagramsontheright.Intheleftcolumn,interplanetarydriversunrelated/relatedtothereconnectionare
showninblack/redfonts,respectively.
Bycontrast,thereconnectioneffectsdependonthemutualorientationofIMFandtheunderlyingmagnetospheric
field,whichmakesitnecessarytoincludeintheexpansionsEquations8–9termscontrolledbythegeodipoletilt
angleψ.TheaboveconsiderationsaresummarizedinFigure2intheformofatableontheleftandparitydi-
agramsintherightmostcolumn.Thedrivingtermsintheleftcolumnfallintotwogroups:(a)Thoseunrelatedto
thereconnection(shownbyblackfont),and(b)reconnection‐relatedtermsthatdependbothonIMFcomponents
andonthegeodipoletiltangleψ (showninred).
Thefirstrowcorrespondstofourgroupsofterms,includingthesolarwindparticlefluxF anditsproductswith
sw
three IMF components. All these terms are unrelated to reconnection and represent a radially diverging anti‐
sunward flow, symmetric with respect to both equatorial and noon meridian planes, as illustrated in the last
columndiagrams.Thecoefficientsg(t) andh(p) areentirelyomittedfromthisgroup(markedbyzeros),because
lnm lnm
the corresponding terms do not satisfy the required symmetry conditions and, hence, only even m values are
allowed.Undereachofthefourcoefficientsthestarting/endingvaluesofnandpermittedmindexparitiesare
shown,suchthatredundantzerotermsbeexcludedfromtheexpansions.
ThenextrowincludesanIMF‐independenttermF cosψ,whoseroleistotakeintoaccounttilt‐relatedchanges
sw
of the magnetopause shape, mirror‐symmetric about the equatorial plane. Two other terms, F B sinψ and
sw x
F B cosψareresponsibleforthereconnectioneffectsand,hence,includesinesandcosinesofthetiltangleψ.
sw z
The reconnection‐associated flow geometries and parities for each term can be qualitatively understood by
overlayingeachofthreeIMFcomponentsontosubsolarmagnetosphericfieldlinesofaperpendicular(ψ = 0)or
parallel(ψ = 90°)dipolefield,shieldedwithinanaxisymmetricmagnetopause.Forexample,inthecaseofa
purelyazimuthal IMFB andperpendicular dipole(3rd row in Figure 2), theterm F B cosψ represents the
y sw y
outwardtransportofreconnectedmagneticfluxtubeswithfrozen‐inplasmainthenorthern‐dawnandsouthern‐
dusksectors(2nd/4thquadrants,resp.),accompaniedwithanoppositelydirectedtransportinthenorthern‐dusk
and southern‐dawn sectors (1st/3rd quadrants). This is exactly the convection type, responsible for the asym-
metric magnetic flux loading in the tail lobes, which results in the nightside plasma sheet twisting under the
TSYGANENKOETAL. 4of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

 21699402, 2024, 11, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233 by Nasa Goddard, Wiley Online Library on [06/11/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical |     | Research: | Space | Physics |     |     |     |
| ------- | -------------- | --- | --------- | ----- | ------- | --- | --- | --- |
10.1029/2024JA033233
Table1
Magnetosheath/MagnetosphereDataSet:ContributingMissions,GSWLatitude/LONGITUDERange,NumbersofRecords,
Timespans
|     |     | Latmin | Latmax | Lonmin | Lonmax | Numberof | Begindate | Enddate |
| --- | --- | ------ | ------ | ------ | ------ | -------- | --------- | ------- |
Mission (degs) (degs) (degs) (degs) Records (year/doy) (year/doy)
|     | Cluster1 | − 89.0 | 73.3 | − 117.1 | 115.9  | 70,762    | 2001/033 | 2004/170 |
| --- | -------- | ------ | ---- | ------- | ------ | --------- | -------- | -------- |
|     | Cluster3 | − 88.7 | 68.5 | − 121.0 | 119.4  | 70,076    | 2001/035 | 2009/129 |
|     | Cluster4 | − 83.8 | 73.0 | − 125.8 | 132.4  | 568,856   | 2001/033 | 2022/171 |
|     | ThemisA  | − 31.0 | 32.1 | − 105.6 | 100.5  | 160,015   | 2008/149 | 2024/144 |
|     | ThemisB  | − 32.6 | 24.7 | − 115.5 | 114.1  | 3,951     | 2008/097 | 2009/358 |
|     | ThemisC  | − 24.7 | 19.4 | − 110.6 | 117.0  | 18,525    | 2007/139 | 2010/009 |
|     | ThemisD  | − 27.3 | 27.9 | − 101.9 | 97.0   | 132,373   | 2007/161 | 2024/144 |
|     | ThemisE  | − 27.2 | 29.0 | − 100.1 | 93.8   | 71,312    | 2007/161 | 2024/114 |
|     |          | −      |      | −       |        |           |          |          |
|     | MMS–1    | 51.8   | 34.1 | 122.4   | 126.4  | 266,249   | 2015/245 | 2024/142 |
|     |          |        |      |         | Total: | 1,362,119 |          |          |
influenceofIMFB (Cowley,1981;Owenetal.,1995;Russell,1972;Sibecketal.,1985;Tsyganenko,1990;
y
Tsyganenkoetal.,1998).
The4thand5throwsincludebothreconnection‐relatedandunrelateddriversthataffecttheflowcomponentsin
thenorth‐southanddawn‐duskdirections.ThetermF sinψ isthetilt‐antisymmetriccounterpartoftheIMF‐
sw
independent term in the second row; the terms containing the cross products B B and B B induce, respec-
|     |     |     |     |     |     |     | x y x z |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- |
tively,dawn‐duskandnorth‐southasymmetriesintheIMFdrapingatconeanglesintermediatebetweenthosefor
strictlyparallelandperpendicularIMForientations.Inparticular,thedawn‐duskasymmetriesassociatedwith
B B correspondtothecommonParkerandortho‐spiralIMFstructures;thatkindofasymmetrywasaddressedin
x y
manysimulationsanddata‐basedstudies(e.g.,Samsonov,2006;Walshetal.(2012)andrefs.therein).In the
present modeling experiment, we assumed L = 2 and N = 8 as the upper summation limits in (Equation 7).
Givenallthesymmetry/paritylimitationslistedinFigure2,thisresultedinatotalof1632unknowncoefficients
tobederivedfromthedata.
Next,notethattheflowvectorexpansionsEquations3–9arequantifiedbytheexternalinputnotonlyviathe
parameters F , IMF B , B , B, and ψ, listed in the first column of the table in Figure 2, but also by the
|     |     | sw  | x y z |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- |
magnetopausesubsolarstandoffdistanceR andtheflaringparameterα,enteringinthecoordinateδin(Equa-
S
tion 1). These two parameters were assumed as functions of the solar wind ram pressure P and IMF B,
d z
determinedforeachdatarecordusingapreviouslydevelopedmodelapproximation(TSEG24,Equation3):
|     |     |     | R =R [(P | /2)ε+γ(B/10)], | α=α | +Δαexp(− | B10), | (10) |
| --- | --- | --- | -------- | -------------- | --- | -------- | ----- | ---- |
|     |     |     | S S0     | d z            |     | 0        | z     |      |
Calculation of the parameter values entering in (Equation 10) was made in TSEG24 using (a) the 2D
magnetosphere‐magnetosheathdataselectiondiagrams(similartothoseinFigures4–7inthenextsectionbelow)
and(b)a“dynamicalweighting”ofdata,performedateverystepofthenonlinearfittingofthemagneticfield
model.Inthepresentstudy,weusethefollowingspecificvaluesobtainedinTSEG24forthetrainingdataset:
R = 11.1R , ε = 0.16, γ = − 0.08, α = 0.49, and Δα = 0.22 (TSEG24, Table 2). For all the remaining
|     | S0  | E   |     | 0   | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
detailsoftheprocedure,thereaderisreferredtotheabovecitedopen‐accesspublication.
|     | 3. Data |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- |
The 1‐min plasma and magnetic field data used in this study are mostly the same as those used in TSE23
and TSEG24, but with two differences. First, a portion of the most recently published data for the period
2022–2024 has been appended to the previously used data set (2001–2022). Specifically, for Themis A, D,
and E probes, the newly added data cover the interval from 11/01/2022 to 05/22/2024; for MMS‐1: from
10/20/2022 to 05/21/2024; for Cluster 4: from 01/01/2022 to 09/30/2022 (a more detailed summary of the
data used to create the model is also given in Table 1 below). Second, since the Geotail CPI solar wind
TSYGANENKOETAL. 5of17

 21699402, 2024, 11, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233 by Nasa Goddard, Wiley Online Library on [06/11/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical | Research: | Space Physics |
| ------- | -------------- | --------- | ------------- |
10.1029/2024JA033233
Figure3. Equatorial(a)andmeridional(b)diagramsofthedatacoverageofthemodelingregion.Theone‐minutedatapoints
=0andZ =0planes,respectively,rotatedintothe
areselectedfrom30°‐widesphericalsectorscenteredonY GSM GSM
|     |     | =0.5 | × 0.5R |
| --- | --- | ---- | ------ |
centerplanes,andbinnedintodS E squares.Thecolorcodingquantifiesthecoveragedensitybythelogarithmof
thepointnumbersdNineachbin.Nominalmagnetopauseandbowshocksectionsareshownwithdarkblueandpurple
contours,respectively.
plasma analyzer (unlike its magnetometer) did not fully operate in the magnetosheath, its data were
| completely | excluded | from the present | study. |
| ---------- | -------- | ---------------- | ------ |
ThespatialcoverageoftheemployeddatabaseisillustratedinFigure3intheformofequatorial(panelA)and
meridional (panel B) diagrams of data density distributions. Since the nightside magnetosheath plasma and
magneticfieldbecomeincreasinglyturbulentatlargerdistancesfromthesubsolararea,thedatatailwardlimitwas
restricted by X ≥ − 10R . The data in each diagram were selected from spherical sectors with angular
|     | GSM | E   |     |
| --- | --- | --- | --- |
Figure4. TheD/D versusB/B diagram,illustratingThemisA,B,C,D,Emagnetosheathdataselection,basedonJelinek
|     |     | sw sw |     |
| --- | --- | ----- | --- |
etal.(2012)method.Heavyclosedlineencirclestheareaassociatedwiththemagnetosheathregion.
TSYGANENKOETAL. 6of17

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure5. SameasinFigure4,butforMMS‐1data.
halfwidth15°,centeredatZ = 0(panelA)andY = 0(panelB)planes,respectively.Eachdatapointwas
GSM GSM
rotatedintothecorrespondingcenterplaneandbinnedthereintoasetofdS=0.5 × 0.5 R squares.
E
Thedatadensitydistributionswerequantifiedbyd = log (dN/dS)ofthenumbersdN ofdatapointsthatfell 10
intoeachbin,presentedintheplotintheformofcolor‐codedmaps(toavoidsingularitiesinno‐dataareas,empty
binswithdN = 0wereassignedwithd = 0).Comparisonofthepanelsshowsastrongdifferencebetweenthe
low‐ and high‐latitude coverage. The near‐equatorial data (panel A) fill the entire space between the nominal
Figure6. SameasinFigures4and5,butforCluster1,3,and4data.Notethelackofadistinctgapbetweenthe
magnetosheathandmagnetosphereareas,clearlyvisibleinthepreviousplotsforThemisandMMSdata.
TSYGANENKOETAL. 7of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure7. Vth/Vth versusV /V diagramsforThemis(left)andMMS(right).Asinthepreviousfigures,thesolidclosedlinesencircletheareaassociatedwiththe
sw b sw
magnetosheath.
magnetopauseandbowshock,calculatedusingLinetal.(2010)andLuetal.(2019)models(shownbyblueand
purplelinesinbothpanels).Thelargestdatadensityintheredcrescent‐shapedareaonthedaysideismostlydue
tothecontributionfromThemisA,D,andEprobeswithapogeesbetween11and13R .Bycontrast,thedata
E
aroundthemeridionalplane(panelB)almostentirelyconcentrateonthedayside.Thenorthernhemispacedatado
notextendabovelatitudes60− 63°;inthesouthernsector,thelatituderangeislargerandreachestheterminator
plane,duetothehighlyinclinedClusterorbit.However,eventherethecoverageisfarfromuniformandgets
progressively scarcer at latitudes higher than ∼− 66°. As discussed below, the lack of high‐latitude data sub-
stantiallylimitsthelatitudinalrangeofthemodeling.
As in our two previous studies, the newly updated data pool was first subject to a rough selection, based on
average magnetopause and bow shock models, respectively compressed and expanded by a factor 1.4. At the
secondstage,atwo‐stepfilteringprocedurewasapplied,usingamodificationofthediagrammethodbyJelinek
etal.(2012).Specifically,atthefirststepthedatapointswereplottedasa2DdiagramoftheprotondensitiesD
andmagneticfieldmagnitudesB,normalizedbyconcurrentvaluesD andB intheincomingsolarwind.
SW SW
Threedenselygroupedareasofenhanceddatapointconcentrationcanbeimmediatelyidentified,corresponding
tothemagnetosphere(lowD,highB),solarwind(lowD,lowB),andthemagnetosheath(highD,intermediateB).
Themagnetosheathdatasubsetwascreatedbyencirclingitsareaonthediagramwithapolygonandapplyinga
winding selection algorithm. Although the procedure has already been described in TSE23 and TSEG24, we
brieflyreproduceitsresultshere,inviewoftherecentdataupdateandinordertokeepthepapermoreorlessself‐
contained.
Figures4–6illustratetheD− BselectionofThemis,MMS,andClusterdata.Theassignedshapesandsizesofthe
selectionpolygonsareinevitablysomewhatsubjective,especiallyinthecaseofCluster(Figure6),whoseorbits
spentrelativelymuchtimeintheouterpolarcuspswhereplasmaandfieldpropertiesarerathersimilartothosein
themagnetosheath.Forthatreason,thereisnodistinctclearancenoristhmusbetweenthemagnetosheathand
magnetospheredataofCluster,suchthatthedividinglineinFigure6wasdrawnbasedonpurelyvisualcriteria.
Atthenextstep,anotherroundoffilteringwasappliedtothedataselectedatthefirststepbymeansoftheabove
D/D versusB/B diagrams.Inthiscase,asimilardiagrammethodwasused,butwiththenormalizedproton
sw sw
bulkspeedV /V andthermalspeedVth/Vth astheselectionparameters.Thiskindoffilteringwasappliedto
b sw sw
onlyThemisandMMSdata,becauseofthealreadymentionedambiguityindistinguishingcuspandmagneto-
sheathdatainCluster'sobservations.Figure7showsthecorrespondingVth/Vth versusV /V diagramsfor
sw b sw
Themis(left)andMMS(right)data.Inthisselectionstep,thefilteringcontourwasdrawninordertoleaveoutthe
TSYGANENKOETAL. 8of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
data with Vth/Vth ≥ 9− 10, most likely associated with the outermost magnetosphere or low‐latitude
sw
magnetopausewithprotonenergiesbytwoordersofmagnitudelargerthaninthesolarwind.
Again,thisinterpretationandthecontourplacementmayappearsubjective;however,inanycaseapossibleloss
of some portion of the magnetosheath data is insignificant (around 10%) and, based on the size of final data
subsets(ontheorderofhalfmillionrecords),isunlikelytoresultinanoverfittedmodel.
Table 1 provides principal information of the final data set, generated as a result of the two‐step selection/
refinementprocedure.ItsformatissimilartothatofTable1inTSE23,butthenumbersaredifferentduetothe
addedmostrecentdata,thedoublefiltering,andtheabsenceofGeotaildata.Abouthalfofthetotal1,362,119
recordsarecontributedbythreeClusterprobes(709,694records).
Following the approach of our two previous studies, the entire data set was again split into training (T) and
validation(V)subsets,inwhichallconsecutivedatawerealternatelyseparatedbycontiguous10‐dayintervals,
thusensuringtheirindependence.TherespectivesizesofthusgeneratedTandVsubsetswerefoundnearlyequal:
685,260 and 676,859 one‐minute records. Finally, before calculating the model parameters, the data in both
subsetsunderwentthelastroundoffiltering:namely,inordertoavoidabnormalinterplanetaryconditionsand
extreme magnetospheric states, all data records with principal solar wind parameters outside their 5%–95%
percentiles were excluded. More specifically, the IMF components were limited to |B |≤5.5, |B |≤6.0, and
x y
|B|≤5.0nT,thesolarwindprotondensity,bulkspeed,andrampressurewererestrictedto2 ≤ N ≤ 15cm−3,
z p
300 ≤ V ≤ 600km/s, 0.5 ≤ P ≤ 4.5nPa, and Alfvénic and magnetosonic Mach numbers were limited to
sw dyn
4.5≤MA≤19.0and3.8≤Ms≤7.5,respectively.Also,allvectorquantitiesweretransformedfromthestandard
GSM into GSW (magnetospheric solar‐wind) coordinates, with X‐axis directed antiparallel to the currently
observedsolarwindflow.Duetoalltherestrictions,thefinalsizeoftheTandVsubsetsforthemodelfitting
furtherdecreasedto417,404and417,329one‐minuterecords,respectively.
4. Results
Theabovedescribedplasmaflowmodelwith1632freecoefficientswasfittedtothedatausingastandardSVD
algorithmwiththetoleranceparameterequalto5⋅10−6(theinverseconditionnumber,i.e.,theratioofthesmallest
tothelargestsingularvalue,seePressetal.,1992,Ch.2.6).Asusual,wedefinethefittingtargetfunctionasthe
residual r.m.s. deviation of the model flow from the observed one: Q = {〈(F − F )2〉} 1/2 , such that the
mod obs
measureofthefittingqualityistheratioQ/FwhereF = {〈F2 〉}1/2 istheobservedr.m.s.Flowmagnitudeover
obs
themodelingdatasubset.FortheTandVsubsets,theobtainedQ/Fvalueswerefound,inpercent,equalto39.2%
and 42.3%, respectively. These values are notably better (lower) than those obtained in the magnetosheath
magneticfieldmodelinginTSE23andTSEG24(around50%–60%),whichiswhatonecouldexpect,giventhe
moreorderlyandsmoothpatternsoftheplasmabulkflow,incomparisonwithmoreturbulentandstronglyIMF‐
dependentmagneticfieldsinthesameregion.
Beforegoingtothemodelflowpatterns,wepresentinFigure8thescatterdiagramsbetweentheobservedand
modeledflowcomponentsF,F,andF,illustratingthefittingquality.
x y z
Theflowvaluesareinunits108cm−2s−1(forreference,equivalenttoaflowwithparticledensityof2.0cm−3and
speed of 500 km/s) and the top/bottom rows correspond, respectively, to the training (T) and validation (V)
subsets.FortheTsubset,theregressionslopesSandPearsoncorrelationsRforallthreeflowcomponentsare
remarkablyhigh,intherangeS=0.98–1.00andR=0.82–0.91.Asexpected,almostalldatapointsintheF
x
diagrams(leftpanel)concentrateinthe3rdquadrant,indicatingtheoverwhelmingdominanceofantisunward
bulk flows in the magnetosheath (a small group of data points in the 4th quadrant with F >0 may belong to
x
sunwardforeshockflows).Becauseofthelowestvariationrangeandthehighestscatterabouttheregressionline,
thatcomponenthasthesmallestcorrelationbetweenthemodelanddata(R=0.824).Thecenterpanelforthe
dawn‐duskflowF demonstratesthebestperformanceofthemodelforthatcomponent,withR=0.905.Thisis
y
what one should naturally expect, based on much wider coverage of the near‐equatorial region (panel A in
Figure3)incomparisonwiththerelativelynarrowmeridionaldatadistribution(panelB,thesameFigure).The
correlationvalueforthenorth‐southcomponentF (rightpanel)isintermediate(R=0.836)betweenthoseforF
z x
andF,butthehighestslope(S=0.998).Notethesignificantlylargersizeofthedatacloudinthe3rdquadrant,
y
TSYGANENKOETAL. 9of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure8. Scatterplotsofmodelagainstobservedflowcomponents.Topandbottomrowscorrespondtothetrainingandvalidationsubsets.LettersA/D,B/E,andC/F
correspondtoF,F,andF flowcomponents,respectively.
x y z
reflectingastrongnorth‐southasymmetryofCluster'sorbitalcoverage,whoseapogeesliefarsouthwardfromthe
equatorialplane(panelBinFigure3).
AsshowninthebottomrowofFigure8,theslopesandcorrelationvaluesforthevalidationsetaresomewhat
lowerthanthoseforthetrainingsubset,asitnormallyshouldbe.Thedifference,however,isnotlarge,which
indicatesthatthedegreeofthemodel'scomplexityisnotfarfromtheoptimum(seeGershenfeld,2003,Ch.12.4),
suchthattheassumedsummationlimitsL = 2,N = 8inEquations3and7donotresultinatangibleover‐or
underfitting.
Figure9showstwodiagramsoftheplasmaflowaroundthemagnetosphereintheequatorialplane,derivedfrom
themodelusingnominalsolarwindconditions(V = 400km/s,N = 5cm−3,F = 2⋅108cm−2s−1),untilted
p sw
geodipole(Ψ = 0),andpurelytransverseIMFwithB = B = 0.PanelsAandBcorrespond,respectively,to
x y
purelynorthward(B = +5andsouthward(B = − 5)IMForientations.Themagnetopause(bluecontour)in z z
this and following plots corresponds to the model surface δ = 0 given by Equation 1 with R and α from
S
Equation10,andthebowshocktrace(purple)isbasedontheempiricalmodelbyLuetal.(2019).Noteherethat
ourmagnetosheathflowmodel,byconstruction,hasnosharpboundariesandbothcontoursaregivenonlyforthe
reader'sorientation.
Inbothdiagrams,onecanseeastagnationoftheplasmaflowinthesubsolararea,changingintoagradualin-
creaseawayfromtheSun‐Earthline,especiallyvisibleonapproachingtheterminatorandfurthertailward.The
subsolarstagnationisclearlymore pronounced in thediagramBforthesouthward IMF, where,according to
Equation10,themagnetopauseisshiftedearthwardby∼0.9R fromR = 11.6R to10.7R .Inthatcase,the
E S E E
flowstagnationareaexpandssideways,suchthatthepre‐noonandpost‐noonflowaccelerationregionsshifttothe
terminator plane. Note also that the flow vectors in both diagrams are not strictly tangential to the model
magnetopause, but have a tangible inward normal component. Although that can be partially ascribed to the
inevitabledatascatterandmodelimperfections,notethattheplasma’penetration’isclearlystrongerinthecaseof
southwardIMF,whichmaywellbeaneffectoftheclassicalDungey‐typereconnectionatthemagnetopause.
However, given all the weaknesses of the method, the conjecture cannot be uniquely and unambiguously
confirmedintheframeworkofthedata‐constrainedmodeling.
TSYGANENKOETAL. 10of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure9. Equatorialdiagramsoftheplasmaflowaroundthemagnetosphereforpurelytransverseinterplanetarymagnetic
field(IMF)orientationwithB = B =0.PanelsAandBcorrespondtonorthward(B = +5nT)andsouthward
x y z
(B = − 5nT)IMF.Thesolarwindandmagnetosheathflowsaredisplayedwitharrowsandthecolorcodingisinunits108 z
cm−2s−1.
Figure 10 shows in a similar format the plasma flow distribution in the noon meridional plane. Unlike in the
previousFigure9,theplotsarelimitedtoonlythedayside,duetovirtuallynohigh‐latitudedataatthenightside
and,hence,invalidmodelresultsinthatregion.Also,becauseoflowermeridionalvalues,themaximumofthe
flowcolorscaleisreducedherefrom5⋅108 to3⋅108 cm−2 s−1.Togivethereaderatleastaroughideaofthe
Figure10. Plasmaflowsinthemeridionalplane.PanelsAandBcorrespondtointerplanetarymagneticfieldB = +5and
z
B = − 5,respectively.
z
TSYGANENKOETAL. 11of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
daysidecusppositions,asetofTA15quiet‐timefieldlines(Tsyganenko&Andreeva,2015)wasoverlaidonto
eachplot(inviewofadifferentmagnetopauseshapeusedinthatmodel,anon‐uniformseparatere‐scalingwas
appliedalongXandZaxes,tobetterfitthelinesintotheShue‐typeboundary).Inaddition,thecolorcodingand
flowarrowsarelimitedtothelatitudeintervalwithin±68°,coveredwithdata(seepanelBinFigure3).Sincethe
datadensityrapidlydropstozerobeyondthatinterval,themodeldestablilizesathigherlatitudesandproduces
unphysicalsunwardflows;theseartifactsarenotshownandtheno‐dataareasarefilledwiththesameuniform
colorasinsidethemagnetopause.AsintheequatorialdiagramsinFigure9,oneagainseesastagnationregionat
lowlatitudes,moredistinctandspatiallyextendedinthecaseofnegativeIMFB.Also,theflowacceleration
z
towardthecuspsissignificantlystrongerinthelattercase,whichmaybeattributedtotheformationofnorthward
andsouthwardplasmastreamsawayfromtheequatorialplane,associatedwithreconnectionatthemagnetopause.
TofurtherillustratetheIMFeffectsupontheflowgeometry,thenextFigure11showsdistributionsoftheplasma
flowinthevicinityofthemodelmagnetopausefornominalsolarwindconditionswithF = 2⋅108cm−2s−1,
sw
perpendicularorientationoftheIMFwithB = 5nT,B = 0(i.e.,coneangleθ = 90°),andthreeclockangles: ⊥ x
ϕ = 0°(A),90°(B),and180°(C).Theinitialideabehindcreatingthosediagramswastotrytofindsignaturesof
themagneticfieldinfluenceontheplasmaflownearthemagnetopause,whichisbelievedtocriticallydependon
the mutual orientation of IMF in the incident solar wind and the terrestrial field inside the boundary (Erkaev
etal.,1998,2006;Phanetal.,1994;Pudovkinetal.,2001;Pudovkin&Semenov,1985;Siscoeetal.,2002;Wang
etal.,2004).
ForallthreeclockanglesinFigure11,oneseesasignificantdecelerationoftheflowinthesubsolararea,withF
below≤108 cm−2 s−1,thatis,lessthanhalfofthatinthesolarwind(F = 2⋅108 cm−2 s−1).Themostinter-
sw
estingfeature(persistentfromonenumericalexperimenttoanother)isthespatialevolutionoftheflowretardation
area.Morespecifically,inthecaseofapurelynorthwardIMF(topdiagramA),theflowisointensitycontoursare
slightlyelongatedinthedawn‐duskdirection(i.e.,normaltobothIMFandunderlyingmagnetosphericfield).In
themiddlediagramB,correspondingtothepurelydawn‐duskIMF,thestagnationareaismoreelongatedand
somewhatinclinedtotheZaxis.Finally,astheIMFbecomespurelysouthward(panelC),theflowretardation
areafurtherexpandsalongYaxis,butcontractsinZdirection,andthusdevelopsintoahighlystretchedstagnation
region, manifesting the formation of a transverse stagnation line, usually associated with the interplanetary
magneticfluxinjectionrateandthecross‐polarpotentialdrop(e.g.,Siscoeetal.,2002).
Theabovedescribedeffectsagreewellwithatraditionalviewoftheglobalmagnetosphericconvection,dating
backtotheDungey'sseminalconcept.Basedonthisparadigm,northwardIMFconditionsleadtothemagnetic
fluxpile‐upinfrontofthedaysidemagnetopauseand,duetothedusk‐dawnelectricfield,increasethetrans-
parencyoftheboundaryfortheincomingplasmaflow.Bycontrast,southwardIMFlaunchesreconnectioninthe
subsolarregionandintensifieslarge‐scaletangentialflowsatthesubsolarmagnetopause.Atthesametime,the
dawn‐duskelectricfieldassociatedwiththemerginginitiatessunwardplasmaflowsfrominsidethemagneto-
sphere,directedagainsttheincomingflow.Thisresultsinaweakerplasmatransportacrossthemagnetopause,
manifestedasthewidedarkareainthebottompanelCofFigure11.
5. Discussion: Dipole Tilt Effects
From a theoretical viewpoint, the seasonal/diurnal variations of the geodipole orientation should affect the
magnetosheathflowsintwoways.First,themagnetopauseshape,especiallyaroundtheoutercusps,isdipoletilt‐
dependent(e.g.,Boardsenetal.,2000;Linetal.,2010)and,hence,mustresultinmodificationsoftheflowina
purelyhydrodynamicsense.Second,andmoreimportant,thedipoletiltchangesthemagneticfieldconfiguration
justinsidethedaysidemagnetopauseand,togetherwiththeIMFdraping,definesthedistributionoffieldmerging
areasonthemagnetopause(e.g.,Fuselieretal.,2024),therebyaffectingtheglobalflowgeometry.
Inviewof theseconsiderations,it isofinterestto visualizethedipoletilt effectsasinferredfromthepresent
modeling.Figure12showstwomeridionalsectionsofthemagnetosheathflow,similartothoseinFigure10,but
for the maximum dipole tilt ψ = 30°. The left and right plots correspond to opposite orientations of IMF:
B = +5nT(A)andB = − 5nT(B).AsinFigure10,duetothelackofhigh‐latitudemagnetosheathdata,both
z z
plotsarelimitedtothesameGSWlatituderangebetween∼− 70°and∼ +60°.Inbothcases,thepatternsare
stronglyasymmetricaboutequatorandrevealinterestingandsignificantchangesfromthecorrespondinguntilted
distributionsshowninFigure10.First,theflowmagnitudesaregenerallylargerinthecaseofsouthwardIMF.
TSYGANENKOETAL. 12of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure11. DiagramsoftheplasmaflowaroundthedaysidemagnetopauseinY − Zprojection(i.e.,asviewedfromSun).
PanelsA,B,andCcorrespondtointerplanetarymagneticfieldB =5nT,coneangle90°,andthreeclockanglesequalto0,
90,and180°,respectively.
Second, in both panels the subsolar flow stagnation areas are shifted southward from the equatorial plane, in
agreement with a similar tilt‐related shift of the reconnection site in an MHD simulation by Eggington
et al. (2020). Third, in the case of negative IMF B (right panel B) an even deeper stagnation area develops
z
poleward of the northern cusp throat. This can beinterpreted as a result of the flow braking against thelocal
TSYGANENKOETAL. 13of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Figure12. Flowdiagramsforpurelynorthward(a)andsouthward(b)interplanetarymagneticfield,correspondingtothe
tiltedgeodipole(redarrows)withψ =30°.
magnetic“wall”attheindentedmagnetopause(Sotirelis&Meng,1999;Tsyganenko&Russell,1999),thatforms
atthepolewardboundaryoftheoutercusp(notpresentintheaxisymmetricShue‐typemodelsurfaceusedinthis
study). A similar effect may be present in the southern hemispace; however, its detection is hardly possible
because,duetothepositivedipoletiltangle,thecuspthroatisshiftedtheretomuchhigherlatitudesandlarger
distances,farbeyondtheregionofthedatacoverageand,hence,ofthemodelvalidity.
Theabovediscussedtilteffectsaremoreclearlyvisibleinthediagramsoftheplasmaflowconfigurationinaclose
vicinityofthemagnetopause(atδ = 0),showninthenextFigure13inthesameformatasinFigure11.Forthe
purelynorthwardIMF(panelA),theflowpatternbecomesmuchwiderinlongitudethanthatintheuntiltedcase
inFigure11andshiftssouthwardby2–3R .InthecaseofpurelyazimuthalIMFwith90°clockangle(panelB),
E
the low‐latitude retardation area slightly shrinks in the Z direction, while at the top of the plot one sees the
emergingnortherncusp‐relatedflowstagnation.Finally,forthepurelysouthwardIMF(panelC)thelow‐latitude
depressionfurthershrinksinZ,whilethenortherncuspstagnationdeepensandbecomesevenmorepronounced
thaninthesubsolararea.
Wenotehereinpassingthat,bythemodel'sconstruction(seeFigure2andEquations8and9),thetilteffectsare
mirror‐symmetricwithrespecttothepolarityofthetiltangleψ.
Theexactnatureofthetilt‐andIMFB‐relatedrelocationofthestagnationareasstillremainsasubjectofdis-
z
cussion.InthecaseofnorthwardIMF,thelatitudinalshiftofthenear‐equatorialstagnationareacanbeexplained
byarelocationinthesamedirectionofthemagnetosphericfieldpeak,whichincreasestheplasmapile‐upeffect
anddeceleratestheflow.InthecaseofsouthwardIMF,thelow‐latitudesiteofthesubsolarflowdeceleration
followstheshiftofthefieldmergingsite,sincethisiswherethecancellationofantiparallelflowsfrominsideand
outsidethemagnetopauseisthemosteffective,asitisclearlyseeninthedivergingsubsolarflowsinpanelBof
Figure12.Thehigh‐latitudeflowdepressionismostlikelyduetothealreadymentionedmagnetic“wall,”formed
atthepolewardsideofthecuspthroat.ThiswalleffectdramaticallygrowsastheIMFturnssouthward,asaresult
oftheredistributionofthedaysidemagneticfluxduetoitserosionatlowlatitudesandconcurrentaccumulation
poleward from the cusps. Aside from the real physical factors at play, the effects may be partially due to the
simplicityofthereferencesurfaceδ = 0,basedontheShue‐typemodel.Beingaxiallysymmetric,itdoesnot
include the high‐latitude indentations associated with polar cusps, whose positions and depths depend on the
TSYGANENKOETAL. 14of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

 21699402, 2024, 11, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233 by Nasa Goddard, Wiley Online Library on [06/11/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical | Research: | Space Physics |
| ------- | -------------- | --------- | ------------- |
10.1029/2024JA033233
=30°.
| Figure13. | SameasinFigure11,butforthegeodipoletiltΨ |     |     |
| --------- | ---------------------------------------- | --- | --- |
dipoletilt(Boardsenetal.,2000;Linetal.,2010).Inthefuturework,amuchmoreinvolvedstudyofthisissueis
planned,basedonamoreaccuratereferenceboundary.
| 6.  | Summary and Outlook |     |     |
| --- | ------------------- | --- | --- |
Wepresentedfirstresultsofanattempttoquantitativelyreconstructanaveragelarge‐scalepictureoftheplasma
flow around the magnetosphere, using multi‐year sets of in situ spacecraft data combined with concurrent
TSYGANENKOETAL. 15of17

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
observationsintheinterplanetarymedium,andanadvancedmodelbasedonthetoroidal/poloidalformalismand
steadystateassumption.Theflowmodelisdrivenbythesolarwindprotonflow,IMFcomponents,andtheEarth's
dipole tilt angle, in such a way that the IMF parameterization is split into two separate groups with different
symmetryandparityproperties.Thefirstoneisduetothemagneticfieldcompression/tensioninsidethemag-
netosheathand,hence,isunrelatedtothemagneticfieldinsidethemagnetosphericboundary.Thesecondgroup
ofIMFeffectsisassociatedwiththereconnectionatthemagnetopauseand,hence,includesthedipoletiltangle.
Themodelingdemonstratedasatisfactoryleveloftheflowrepresentationintermsofthefittingmeritfunctionand
model‐datascatterplots,confirmedbytestingtheresultsobtainedforatrainingsubsetonanindependentvali-
dationsubset.Themodelingrevealedregularaveragepatternsofthemagnetosheathflow,withthemagnitudesof
thesameorderasintheincomingsolarwind,butstagnatedinthesubsolarareaandgraduallyincreasingaway
fromthenoonsector.TheflowsarefoundtobesignificantlymodifiedbytheIMF,reflectingboththemagnetic
effectsduetothepresenceofthemagnetosphereasahydromagneticobstacleandthoseduetothereconnection
with the geomagnetic field. Our data‐based study confirms quite a substantial impact of the seasonal/diurnal
changesofthedipoletiltonthemagnetosheathplasmaflowgeometry.Atthesametime,itshouldberealizedthat
themodelingresultsrepresentonlyanaveragepicture,derivedfromdatatakenatdifferenttimesandadditionally
blurredwithinaccuraciesintheinterplanetaryOMNIdataduetouncertaintiesofthepropagationtime/pathfrom
L1totheEarth'sbowshock(e.g.,Vokhmyaninetal.,2019).Moreadvancedfurtherstudiesaredefinitelyneeded,
includingmoreaccuratemagnetopausemodelsandmoreadvancedmethodsofdataselectionbetweendifferent
geospacedomains,usingautomatedAI‐basedselectionalgorithms.Also,thediversityofthesolarwindtypes
(Borovsky et al., 2019) should be taken into consideration, as well as a delayed/finite‐time response of the
magnetopauseshapeandsizetochangesinthestateofinterplanetarymedium.
Data Availability Statement
Cluster, THEMIS, and MMS magnetometer and plasma instrument data were downloaded from the NSSDC
CDAWEB interface at https://cdaweb.gsfc.nasa.gov/cdaweb/index.html. One‐minute resolution OMNI data
wereobtainedfromSPDFOMNIWEBathttps://omniweb.gsfc.nasa.gov.Alldatasetsandsoftwareusedtoobtain
theabovedescribedresultsarefreelyavailablefromtheFigSharerepositoryathttps://doi.org/10.6084/m9.fig-
share.27282336.v1.
Acknowledgments References
WeacknowledgetheteamsandPIsofall
Boardsen,S.A.,Eastman,T.E.,Sotirelis,T.,&Green,J.L.(2000).Anempiricalmodelofthehigh‐latitudemagnetopause.Journalof
experimentswhosedatacontributedtothis
study.Inparticular,ClusterandMMS GeophysicalResearch,105(A10),23–193.https://doi.org/10.1029/1998ja000143
Borovsky,J.E.,Denton,M.H.,&Smith,C.W.(2019).Somepropertiesofthesolarwindturbulenceat1AUstatisticallyexaminedinthedifferent
magnetometer/ephemerisdatawere
typesofsolarwindplasma.JournalofGeophysicalResearch:SpacePhysics,124(4),2406–2424.https://doi.org/10.1029/2019JA026580
obtainedfromtheNSSDCCDAWEB
Cowley,S.W.H.(1981).Magnetosphericasymmetriesassociatedwiththey‐componentoftheIMF.PlanetaryandSpaceScience,29(1),79–96.
onlinefacility,originallymadeavailable
https://doi.org/10.1016/0032‐0633(81)90141‐0
bythePIs:A.BaloghandM.Tatrallyay
Dimmock,A.P.,Hietala,H.,&Zou,Y.(2020).Compilingmagnetosheathstatisticaldatasetsunderspecificsolarwindconditions:Lessonslearnt
(Clusterdata),byJ.Burch,C.Russell,and
fromthedaysidekineticsouthwardIMFGEMchallenge.EarthandSpaceScience,7(6),e2020EA001095.https://doi.org/10.1029/
W.Magnus(MMSdata).V.
Angelopoulos,K.‐H.Glassmeier,U. 2020EA001095
Eggington,J.W.B.,Eastwood,J.P.,Mejnertsen,L.,Desai,R.T.,&Chittenden,J.P.(2020).Dipoletilteffectonmagnetopausereconnectionand Auster,W.Baumjohann,C.W.Carlson
thesteady‐statemagnetosphere‐ionospheresystem:GlobalMHDsimulations.JournalofGeophysicalResearch:SpacePhysics,125(7),
andJ.McFaddenareacknowledgedforthe
e2019JA027510.https://doi.org/10.1029/2019JA027510
useofTHEMISFGMandESAdata.High‐
Erkaev,N.V.,Farrugia,C.J.,&Biernat,H.K.(1998).ComparisonofgasdynamicsandMHDpredictionsformagnetosheathflow.InJ.Moen,A. resolutionOMNIinterplanetarydatawere
Egeland,&M.Lockwood(Eds.),Polarcapboundaryphenomena,NATOASIseries(Vol.509,pp.27–40).Springer.https://doi.org/10.1007/
obtainedfromtheSPDFOMNIWEB
interface(R.McGuire,N.Papitashvili). 978‐94‐011‐5214‐3_3
Erkaev,N.V.,Mezentsev,A.,&Biernat,H.(2006).Influenceoftheinterplanetarymagneticfieldonthesolarwindflowaboutplanetaryob- Theauthorsacknowledgefinancialsupport
stacles.SpaceScienceReviews,122(1–4),209–219.https://doi.org/10.1007/s11214‐006‐6059‐z fromtheRussianScienceFoundation
Fuselier,S.A.,Petrinec,S.M.,Reiff,P.H.,Birn,J.,Baker,D.N.,Cohen,I.J.,etal.(2024).Global‐scaleprocessesandeffectsofmagnetic
Grant23‐47‐00084“Magnetic
reconnectiononthegeospaceenvironment.SpaceScienceReviews,220(4),34.https://doi.org/10.1007/s11214‐024‐01067‐0
ReconnectioninSpaceandLaboratory
Gershenfeld,N.(2003).Thenatureofmathematicalmodeling.CambridgeUniversityPress.
Plasmas:ComputerSimulationsand
EmpiricalModeling.” Jelínek,K.,Němeček,Z.,&Šafránková,J.(2012).Anewapproachtomagnetopauseandbowshockmodelingbasedonautomatedregion
identification.JournalofGeophysicalResearch,117(A5),A05208.https://doi.org/10.1029/2011JA017252.1
Jung,J.,Connor,H.,Dimmock,A.,Sembay,S.,Read,A.,&Soucek,J.(2024).Mshpy23:Auser‐friendly,parameterizedmodelofmagnetosheath
conditions.EarthandPlanetaryPhysics,8(1),89–104.https://doi.org/10.26464/epp2023065
Kobel,E.,&Flückiger,E.O.(1994).Amodelofthesteadystatemagneticfieldinthemagnetosheath.JournalofGeophysicalResearch,99(A12),
23617–23622.https://doi.org/10.1029/94JA01778
Lin,R.L.,Zhang,X.X.,Liu,S.Q.,Wang,Y.L.,&Gong,J.C.(2010).Athree‐dimensionalasymmetricmagnetopausemodel.Journalof
GeophysicalResearch,115(A4),A04207.https://doi.org/10.1029/2009JA014235
Lu,J.Y.,Zhou,Y.,Ma,X.,Wang,M.,Kabin,K.,&Yuan,H.Z.(2019).Earth’sbowshock:Anewthree‐dimensionalasymmetricmodelwith
dipoletilteffects.JournalofGeophysicalResearch:SpacePhysics,124(7),5396–5407.https://doi.org/10.1029/2018JA026144
TSYGANENKOETAL. 16of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License

Journal of Geophysical Research: Space Physics 10.1029/2024JA033233
Mead,G.D.,&Fairfield,D.H.(1975).Aquantitativemagnetosphericmodelderivedfromspacecraftmagnetometerdata.JournalofGeophysical
Research,80(4),523–534.https://doi.org/10.1029/JA080i004p00523
MichottedeWelle,B.,Aunai,N.,Lavraud,B.,Génot,V.,Nguyen,G.,Ghisalberti,A.,etal.(2024).Globalenvironmentalconstraintsonmagnetic
reconnectionatthemagnetopausefrominsitumeasurements.JournalofGeophysicalResearch:SpacePhysics,129(8),e2023JA032098.
https://doi.org/10.1029/2023JA032098
MichottedeWelle,B.,Aunai,N.,Nguyen,G.,Lavraud,B.,Génot,V.,Jeandet,A.,&Smets,R.(2022).Globalthree‐dimensionaldrapingof
magneticfieldlinesinEarth’smagnetosheath fromin‐situspacecraftmeasurements.JournalofGeophysicalResearch:SpacePhysics,
127(12),e2022JA030996.https://doi.org/10.1029/2022JA030996
Narita,Y.,Töpfer,S.,&Schmid,D.(2023).Scalar‐potentialmappingofthesteady‐statemagnetosheathmodel.AnnalsofGeophysics,42,79–89.
https://doi.org/10.5194/angeo‐42‐79‐2024
Owen,C.J.,Slavin,J.A.,Richardson,I.G.,Murphy,N.,&Hynds,R.J.(1995).Averagemotion,structureandorientationofthedistant
magnetotaildeterminedfromremotesensingoftheedgeoftheplasmasheetboundarylayerwithE>35keVions.JournalofGeophysical
Research,100(A1),185–204.https://doi.org/10.1029/94ja02417
Phan,T.‐D.,Paschmann,G.,Baumjohann,W.,Sckopke,N.,&Lühr,H.(1994).Themagnetosheathregionadjacenttothedaysidemagnetopause:
AMPTE/IRMobservations.JournalofGeophysicalResearch,99(1),121–141.https://doi.org/10.1029/gm090p0115
Press,W.H.,Teukolsky,S.A.,Vetterling,W.T.,&Flannery,B.P.(1992).Numericalrecipes(2nded.).CambridgeUniversityPress.
Pudovkin,M.I.,Besser,B.P.,Zaitseva,S.A.,Lebedeva,V.V.,&Meister,C.‐V.(2001).Magneticbarrierincaseofasouthwardinterplanetary
magneticfield.JournalofAtmosphericandSolar‐TerrestrialPhysics,63(10),1075–1083.https://doi.org/10.1016/s1364‐6826(01)00023‐2
Pudovkin,M.I.,&Semenov,V.S.(1985).Magneticfieldreconnectiontheoryandthesolarwind‐Magnetosphereinteraction:Areview.Space
ScienceReviews,41(1–2),1–89.https://doi.org/10.1007/bf00241346
Russell,C.T.(1972).Theconfigurationofthemagnetosphere,in:Criticalproblemsofmagnetosphericphysics,(Eds.).C.R.Dyer,Inter‐union
committeeonsolar‐terrestrialphysics,NationalAcademyofSciences,
Samsonov,A.(2006).NumericalmodellingoftheEarth’smagnetosheathfordifferentIMForientations.AdvancesinSpaceResearch,38(8),
1652–1656.https://doi.org/10.1016/j.asr.2005.06.009
Shue,J.‐H.,Chao,J.K.,Fu,H.C.,Russell,C.T.,Song,P.,Khurana,K.K.,&Singer,H.J.(1997).Anewfunctionalformtostudythesolarwind
controlofthemagnetopausesizeandshape.JournalofGeophysicalResearch,102(5),9497–9511.https://doi.org/10.1029/97JA00196
Sibeck,D.G.,Siscoe,G.L.,Slavin,J.A.,Smith,E.J.,Tsurutani,B.T.,&Lepping,R.P.(1985).Thedistantmagnetotail’sresponsetoastrong
interplanetarymagneticfieldBy:Twisting,flattening,andfieldlinebending.JournalofGeophysicalResearch,90(A5),4011–4019.https://
doi.org/10.1029/ja090ia05p04011
Siscoe,G.L.,Crooker,N.U.,Erickson,G.M.,Sonnerup,B.U.Ö.,Maynard,N.C.,Schoendorf,J.A.,etal.(2002).MHDpropertiesof
magnetosheathflow.PlanetaryandSpaceScience,50(issues5–6),461–471.https://doi.org/10.1016/S0032‐0633(02)00026‐0
Sotirelis,T.,&Meng,C.‐I.(1999).Magnetopausefrompressurebalance.JournalofGeophysicalResearch,104(4),6889–6898.https://doi.org/
10.1029/1998ja900119
Soucek,J.,&Escoubet,C.P.(2012).PredictivemodelofmagnetosheathplasmaflowanditsvalidationagainstCLusterandTHEMISdata.
AnnalsofGeophysics,30(6),973–982.https://doi.org/10.5194/angeo‐30‐973‐2012
Tsyganenko,N.A.(1990).Quantitativemodelsofthemagnetosphericmagneticfield:MethodsandresultsSpaceSci.,Rev.SpaceScience
Reviews,54(1–2),75–186.https://doi.org/10.1007/bf00168021
Tsyganenko,N.A.,&Andreeva,V.A.(2015).Aforecastingmodelofthemagnetospheredrivenbyanoptimalsolarwindcouplingfunction.
JournalofGeophysicalResearch:SpacePhysics,120(10),8401–8425.https://doi.org/10.1002/2015JA021641
Tsyganenko,N.A.,Karlsson,S.B.P.,Kokubun,S.,Yamamoto,T.,Lazarus,A.J.,Ogilvie,K.W.,etal.(1998).Globalconfigurationofthe
magnetotailcurrentsheetasderivedfromGeotail,Wind,IMP8andISEE1/2data.JournalofGeophysicalResearch,102(A4),6827–6841.
https://doi.org/10.1029/97ja03621
Tsyganenko,N.A.,&Russell,C.T.(1999).Magneticsignaturesofthedistantpolarcusps:ObservationsbyPolarandquantitativemodeling.
JournalofGeophysicalResearch,104(A11),24–939.https://doi.org/10.1029/1999ja900279
Tsyganenko,N.A.,Semenov,V.S.,&Erkaev,N.V.(2023).Data‐basedmodelingofthemagnetosheathmagneticfield.JournalofGeophysical
Research:SpacePhysics,128(11),e2023JA031665.https://doi.org/10.1029/2023JA031665
Tsyganenko,N.A.,Semenov,V.S.,Erkaev,N.V.,&Gubaidulin,N.T.(2024).Magneticfieldsandelectriccurrentsaroundthedayside
magnetopauseasinferredfromdata‐constrainedmodeling.Front.Astron.SpaceSci.,11,1425165.https://doi.org/10.3389/fspas.2024.
1425165
Vokhmyanin,M.V.,Stepanov,N.A.,&Sergeev,V.A.(2019).OntheevaluationofdataqualityintheOMNIinterplanetarymagneticfield
database.SpaceWeather,17(3),476–486.https://doi.org/10.1029/2018SW002113
Walsh,B.M.,Sibeck,D.G.,Wang,Y.,&Fairfield,D.H.(2012).Dawn‐duskasymmetriesintheEarth’smagnetosheath.JournalofGeophysical
Research,117(A12),A12211.https://doi.org/10.1029/2012JA018240
Wang,Y.L.,Raeder,J.,&Russell,C.T.(2004).Plasmadepletionlayer:Magnetosheathflowstructureandforces.AnnalsofGeophysics,22(3),
1001–1017.https://doi.org/10.5194/angeo‐22‐1001‐2004
Zhang,H.,Fu,S.,Pu,Z.,Lu,J.,Zhong,J.,Zhu,C.,etal.(2019).Statisticsonthemagnetosheathpropertiesrelatedtomagnetopausemagnetic
reconnection.TheAstrophysicalJournal,880(2),122.https://doi.org/10.3847/1538–4357/ab290e
TSYGANENKOETAL. 17of17
21699402,
2024,
11,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JA033233
by
Nasa
Goddard,
Wiley
Online
Library
on
[06/11/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License