RESEARCH ARTICLE Magnetosheath Proton Density and Temperature as Derived
10.1029/2025JA034343 From Data‐Constrained Modeling
KeyPoints: N.A.Tsyganenko1 ,N.T.Gubaidulin1 ,V.S.Semenov1 ,andN.V.Erkaev1,2,3
• Large‐scaledistributionsofmagneto-
sheathprotondensityandtemperature 1SaintPetersburgStateUniversity,SaintPetersburg,Russia,2InstituteofComputationalModellingofSiberianBranchof
arederivedfromspacecraftdatausing theRussianAcademyofSciences,Krasnoyarsk,RussianFederation,3AppliedMechanicsCathedra,SiberianFederal
aflexibleempiricalmodel
• SignificantIMFeffectsonplasma University,Krasnoyarsk,RussianFederation
parametersarerevealeddueto
magnetosheathfielddraping,
compression,andreconnectionat Abstract Globaldistributionsofthedaysidemagnetosheathprotondensityandtemperatureare
magnetopause reconstructed,usingamulti‐yearpoolofsatelliteobservationsandempiricaldata‐constrainedmodelswitha
• Remarkablesensitivitytogeodipole
flexiblearchitecture.ThemodelsarebasedondataofThemis,Cluster,andMMSsatellitesandaredrivenbythe
tilt,especiallyaroundpolarcusps,
pointsouttheimportanceofplasma/ upstreamsolarwinddensity,speed,protontemperature,andinterplanetarymagneticfield(IMF).Inthesimplest
fieldpile‐upandreconnection caseofzeroIMFanduntiltedgeodipole,themodelsrevealtheexpectedpeakofplasmadensityandtemperature
inthesubsolararea,withgradualdecreaseawayfromtheSun‐Earthline.Inmorecomplexsituationswith
Correspondenceto: nonzeroIMF,themagneticfielddrapingandassociatedelectromagnetictensions,combinedwiththe
N.A.Tsyganenko, reconnection‐inducedplasmaenergization,streaming,andpile‐upeffectsatthemagnetopause,resultindawn‐
n.tsyganenko@spbu.ru duskandnorth‐southasymmetries.Thenorth‐southasymmetryisdramaticallyenhancedduringperiodswith
largegeodipoletilttotheterminatorplane.Theasymmetryisespeciallypronouncedaroundthesunward(local
Citation: summer)polarcusp,moredirectlyexposedtothesolarwind.Inthiscase,thecusp'spolewardboundaryformsa
Tsyganenko,N.A.,Gubaidulin,N.T., localmagneticwallthatbrakestheparticleflowand,forparallelorientationbetweenthemagnetosheathand
Semenov,V.S.,&Erkaev,N.V.(2025).
magnetospheretaillobefield,formsapile‐upareawithenhanceddensity.Intheoppositecaseofantiparallel
Magnetosheathprotondensityand
temperatureasderivedfrom alignmentbetweenthemagnetosheathandlobefields,theinflowingplasmaiseffectivelydrainedawayby
data‐constrainedmodeling.Journalof reconnection.TheobtainedresultsarecomparedwiththoseofgasdynamictheoryandMHDsimulations.In
GeophysicalResearch:SpacePhysics,
particular,aremarkableagreementisfoundwiththeoreticallypredicteddensityandtemperaturejumpsacross
130,e2025JA034343.https://doi.org/10.
1029/2025JA034343 thesubsolarbowshock.
Received20JUN2025 PlainLanguageSummary Duetothesupersonicnatureofthesolarwind,itsflowaroundtheEarth's
Accepted25NOV2025
magnetosphereisnotlaminar,butresultsintheformationofabowshockandaturbulenttransitionzonebehind
thatboundary,calledthemagnetosheath(MS),wherethesolarwindplasmaissuddenlydecelerated,
AuthorContributions:
compressed,andheated.Inaddition,theinterplanetarymagneticfield(IMF),carriedbythesolarwindtothe
Conceptualization:N.A.Tsyganenko,
V.S.Semenov,N.V.Erkaev Earth'sorbit,penetratesinsidetheMS,drapesaroundthemagnetosphere,andreconnectswiththegeomagnetic
Datacuration:N.A.Tsyganenko, field.AlltheseeffectssignificantlyaffecttheMSplasmapropertiesandspaceweatherconditionsinthe
N.T.Gubaidulin
interfaceregionbetweenthesolarwindandmagnetosphere.Basedondataofthreesatellitemissionstaken
Formalanalysis:N.A.Tsyganenko,
N.V.Erkaev duringalmostthreedecades,inthisworkweconstructedamodelofMSprotondensityandtemperature,making
Fundingacquisition:V.S.Semenov itpossibletoquantitativelydescribetheMSplasmaenvironmentanditsresponsetochanginginterplanetary
Investigation:N.A.Tsyganenko,
conditions.
N.T.Gubaidulin,N.V.Erkaev
Methodology:N.A.Tsyganenko,
N.T.Gubaidulin,V.S.Semenov,
N.V.Erkaev
1. Introduction
Projectadministration:V.S.Semenov
Resources:N.A.Tsyganenko,
Inanalogytothewidelyusedmeteorologicalterm“weatherkitchen,”theEarth'smagnetosheath(henceforthMS)
V.S.Semenov
Software:N.A.Tsyganenko, canbedeservedlycalledthe“spaceweatherkitchen,”sincethisiswherethekeySun‐Earthinteractionprocesses
N.T.Gubaidulin,N.V.Erkaev are triggered and where the magnetosphere‐ionosphere system is fed and driven with the solar wind energy.
Supervision:V.S.Semenov
Exploringandmodelingthisregionusingvariousapproacheshasattractedmuchattentionsincelongago,starting
Validation:N.A.Tsyganenko,
N.V.Erkaev fromtheseminalcontributionsbySpreiteretal.(1966),SpreiterandAlksne(1969),followedbynumerouslater
Visualization:N.A.Tsyganenko, studies, including purely theoretical works (Kobel & Flückiger, 1994; Zwan & Wolf, 1976), data‐based case
N.T.Gubaidulin,N.V.Erkaev
studies and statistical surveys (Dimmock et al., 2016, 2020; Dimmock & Nykyri, 2013; Phan et al., 1994; Pi
Writing–originaldraft:
N.A.Tsyganenko etal.,2024;Soucek&Escoubet,2012;Zhangetal.,2019),MHDsimulations(Jungetal.,2024;Samsonov,2006;
Samsonovetal.,2012,2016;Siscoeetal.,2002;Wangetal.,2004),and,finally,thepurelydata‐constrained
models, based on large sets of multi‐year/multi‐probe data (Michotte de Welle et al., 2022; O’Brien
etal.,2024;Tsyganenkoetal.,2023,2024a,2024b).BycontrasttotheoreticalstudiesandMHDsimulations,the
©2025.AmericanGeophysicalUnion.All
RightsReserved. data‐basedmodelingseekstoquantitativelyreconstructtheactuallyobservedMSanditsresponseto external
TSYGANENKOETAL. 1of17

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Writing–review&editing: drivers by extracting maximum available information from in situ data. The latter approach, in turn, was
N.A.Tsyganenko,N.T.Gubaidulin, developedbydifferentauthorsusingdifferenttechniques.MichottedeWelleetal.(2022)employedasophis-
V.S.Semenov,N.V.Erkaev
ticatedmachinelearningmethodbasedonaK‐Nearest‐Neighboralgorithmtooptimallybinthedataandderive
thedrapedmagneticfieldstructures.O’Brienetal.(2024)developedarecurrentneuralnetworkalgorithmand
demonstrateditsabilitytoreconstructtheMSplasmaparametersandmagneticfielddrapingbasedontheMMS
missiondata.
Thispaperisthefourthinaseriesofourrecentpublications(Tsyganenkoetal.,2023,2024a,2024b,referred
henceforthasTSE23andTSEG24ab),inwhichamoretraditionalapproachisemployedtoempiricallymodelthe
Earth'sMSusinglargesetsofspacecraftdata.Theessenceofthemethodistoformulateamathematicalmodel,
representingthequantitiesofinterestasflexibleexpansionswithunknowncoefficientsandnonlinearparameters,
derivedbyminimizingther.m.s.deviationofthemodelfromtheentirebodyofdata.Whilethemainfocusofour
previouspaperswasonthevectorMScharacteristics,suchasthemagneticfield(TSE23,TSEG24a)orplasma
bulkflow(TSEG24b),hereweconcentrateonthebasicscalarparameters,namely,ontheprotondensityDand
theirtemperature(thermalenergy)W.Accuratemodelingofthesefundamentalplasmaparametersisbecoming
especially important nowadays in view of the upcoming launch of the SMILE mission, whose remote X‐ray
observations made from a distance will need an independent benchmarking tool, based on direct in situ
measurements.
The structure of the paper is as follows: in Section 2 we describe the mathematical framework of the model,
Section 3 addresses the data set used in the generation of the model parameters and intercalibration issues,
Section4presentsthemainresultsanddiscussesthemostinterestingfindings,andSection5concludesthepaper
withasuccinctsynopsisofmainresults.Inaddition,acomprehensivetableoftermsenteringinthemodelex-
pansionsisprovidedinAppendixA,withadetailedlistoftheirparitypropertiesandanexplanationofhowthey
arederived.
2. Formulation and Architecture of the Model
In the case of the magnetic field and bulk flow modeling addressed in TSE23 and TSEG24a,b, an essential
requirementwastokeepthevectorfieldsdivergence‐free,whichwasachievedbyrepresentingthemasasumof
toroidalandpoloidalcomponents,whosegeneratingfunctionswereeachexpandedintotriplesumsoftheform
L N n
∑δl(r,θ)∑ ∑Y(lnm)(θ,ϕ) (1)
l=0 n=1 m=0
whereY(lnm) arestandardsphericalfunctionswithfreeunknowncoefficientsg andh :
lnm lnm
Y(lnm)(θ,ϕ)=Pm(cosθ)(g cosmϕ+h sinmϕ). (2)
n lnm lnm
Thedimensionlessvariable
δ(r,θ)=1− rcos2α(θ/2)/R , (3)
S
derivedfromequationbyShueetal.(1997),staysconstantonnestedaxisymmetricsurfaceswithnosepointsat
r = R andservesasaconvenientquantifierofpositionofanarbitrarypoint{r,θ,ϕ}withrespecttomagneto- S
pauseandbowshock,asillustratedinFigure1(adoptedfromTSE23andTSEG24a,b.)
As noted above, in this work we model scalar quantities and, therefore, no longer have to care about the
divergenceissues.Thisgreatlysimplifiestheproblem,sinceboththedensityDandthermalenergyWcannowbe
directlyrepresentedbytheexpansions(1),withnoneedtocomplicatethemodelmathematicalstructurewithfirst
andsecondderivatives,aswasthecaseinthetoro/poloidalformalism.Anotherthingthatshouldbeclearlystated
from the outset is that our model expansions are continuous functions of δ, without any abrupt jumps at the
magnetopauseandbowshock.Outsidethemagnetosheath,themodelvaluesofDandWshouldbeviewedasonly
aresultofsmoothextrapolationfrominsidethemodelingregion.
TSYGANENKOETAL. 2of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

 21699402, 2025, 12, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343 by Sang-Yun Lee - Nasa Goddard , Wiley Online Library on [30/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical | Research: |     | Space | Physics |     |     |     |     |     |     |
| ------- | -------------- | --------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
10.1029/2025JA034343
Thenexttaskistoconsistentlyestablishthehierarchyofthemodeldrivers.In
thecaseofmodelingtheMSmagneticfield(TSE23/TSEG24a),theprincipal
|     |     |     | driver        | was the | interplanetary | magnetic  |              | field (IMF), | directly    | responsible | for |
| --- | --- | --- | ------------- | ------- | -------------- | --------- | ------------ | ------------ | ----------- | ----------- | --- |
|     |     |     | the MS        | field   | formation,     | strength, | and          | geometry of  | its draping | around      | the |
|     |     |     | magnetopause. |         | Accordingly,   | the       | coefficients | in the       | generating  | function    | ex- |
pansionswererepresentedaslinearcombinationsofIMFcomponents,while
theeffectofsolarwindflowpressurewasaccountedforby(a)appropriate
overallscalingofcoordinatesand(b)viaacommonempiricalfactorbythe
|     |     |     | field magnitude. |     | In the | present | analysis, | we use a similar | approach, |     | except |
| --- | --- | --- | ---------------- | --- | ------ | ------- | --------- | ---------------- | --------- | --- | ------ |
thatnowtheIMFandsolarwindplasmaparameterschangetheirroles:the
|     |     |     | density | D , | speed V , | and thermal | energy | W come | to  | the foreground, |     |
| --- | --- | --- | ------- | --- | --------- | ----------- | ------ | ------ | --- | --------------- | --- |
|     |     |     |         | sw  | sw        |             |        | sw     |     |                 |     |
whiletheIMFeffectsareviewedasthenext‐orderperturbationsthatmodify
thezero‐approximationspatialdistributionoftheMSplasmaparametersD
andW.Withallthatsaid,belowisthefinalformulationoftheMSdensity
model:
D(δ,θ,ϕ)=D(1)+D(2)Ψ+D(3)Ψ2+D(4)B∗+D(5)B∗
|     |     |     |     |     |     |     |     |     | x   | y   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure1. (Corrected/adoptedfromTSE23/TSEG24a,b).Cartesian +D(6)B∗+D(7)B∗2+D(8)B∗2+D(9)B∗2
coordinates:GSWsystemwithx‐axisagainstthesolarwind.Spherical: z x y z
(4)
radialdistancer,coneandclockanglesθ = arccos(x/r)and D(10)B∗B∗+D(11)B∗B∗+D(12)B∗B∗
+
ϕ = arctan(y/z),resp.Thegray‐shadedreferencesurfacesδ(r,θ) = constare x y x z y z
nearlysimilarinshapetothemagnetopauseandbowshock.
+D(13)B∗Ψ+D(14)B∗Ψ+D(15)B∗Ψ
|     |     |     |     |     |     |     | x   | y   | z   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
whereΨisthegeodipoletiltangleandB∗,B∗,B∗arenormalizedIMFcomponents(dividedby5nT).Thepartial
x y z
termsD(i)includeexpansions(1)inthecoordinates{δ,θ,ϕ}(eachwithitsownpairofcoefficientsg(i) andh(i)
|     |     |     |     |     |     |     |     |     |     | lnm | lnm ), |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
multiplied by normalized solar wind proton density D∗ = D /5cm−3, speed V∗ = V /400km/s, and
|     |     |     |     |     | sw  | sw  |     | sw  | sw  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
thermalenergyW∗
|     | =   | W sw /10eV,raisedtotheexponentsα |     |     |     | d ,α v ,andα | w ,respectively,asfollows: |     |     |     |     |
| --- | --- | -------------------------------- | --- | --- | --- | ------------ | -------------------------- | --- | --- | --- | --- |
sw
|     |     |     |     |     |     | L N | n   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∑Y(lnm)(θ,ϕ)
|     |     | D(i)=(D∗ | )αd(V∗ | )αv(W∗ | )αw∑δl∑ |         |     |     |     |     | (5) |
| --- | --- | -------- | ------ | ------ | ------- | ------- | --- | --- | --- | --- | --- |
|     |     |          | sw     | sw     | sw      |         | i   |     |     |     |     |
|     |     |          |        |        |         | l=0 n=1 | m=0 |     |     |     |     |
ThermalenergyW oftheMSprotonswasmodeledusingequationsfullyidenticaltoEquation4–5,exceptthe
notationchange:D(i) → W(i);tosavepagespace,theyarenotreproducedhere.Intheexpansion(Equation4),
weretainedcontributionsfromthegeodipoletiltangleandIMFcomponentsuptoquadraticterms,inorderto
keepanoptimaltradeoffbetweenthemodelcomplexity,dataunevenness/noise,andcomputationalfeasibility.
ThesamereasoningwasusedtodefinetheupperlimitsL,N oftheindicesl,nintheexpansion(Equation5).
Namely,inviewofarelativelynarrowseparationbetweenthedaysidemagnetopauseandbowshock(aswellas
sparsity of high‐latitude data), the quadratic Taylor expansion in δ with L = 2 was found to be sufficient.
Likewise,theangularresolutionsinθandϕwererestrictedto∼18°and36°,respectively,bysettingN =
10.
WiththeabovedefinedlimitsonLandN,thetotaltheoreticalnumberofunknownexpansioncoefficientsg and
lnm
h wouldbeaslargeas5,400.Althoughstillcomputationallydoable,retainingallthetermswouldmakelittle
lnm
senseduetosignificantlynon‐uniformdistributionofdata,bothingeometricandparametricspace.Inparticular,
onewouldexpectasignificantinterplaybetweentheseasonallongitudinalshiftofthesatelliteorbitalcoverage
andtheEarth'sdipoletiltangle,potentiallyresultinginanindistinguishablemixtureofrealfeaturesandmodel
artifacts.Anaturalwaytoovercomethatdifficultyistoimposefromtheoutsetappropriatenorth‐southanddawn‐
dusksymmetry/antisymmetryrestrictionsontheindividualtermsin(Equation4),basedontheoreticallyexpected
geometry of the plasma flow around the magnetosphere. In doing so, it is instructive to rank the symmetry
propertiesaccordingtotheprincipalphysicalfactorsatplayandtheirrelativeimportance.Firstofall,forzero
(Ψ = 0),
IMF, untilted geodipole and viewing the magnetosphere as a blunt impenetrable and unmagnetized
obstaclesymmetricinyandzdirections,itisnaturaltoassumethefirstandthirdtermsD(1)in(Equation4)toalso
bemirrorsymmetricwithrespecttobothequatorialandnoon‐midnightmeridianplanes.Thesecondterm,D(2)Ψ,
TSYGANENKOETAL. 3of17

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
takesintoaccountapossibilityofnorth‐southasymmetryofthemagnetopauseduetonon‐zerodipoletiltand,
hence,mustbeantisymmetric(odd)withrespecttoZcoordinate.
Theotherremaining12termsin(Equation4)includeIMFcomponentsandmustreflecttwophysicallydifferent
effects.Thefirstoneisassociatedwiththemagneticfielddrapingaroundthemagnetopauseandrelatedelec-
tromagnetictensionsduetotheIMFcompressionandfieldlinebendinginthemagnetosheath.Inthiscase,the
magnetosphere is still assumed as a rigid unmagnetized obstacle, not interacting electromagnetically with the
magnetosheath field; this uniquely defines what specific restrictions should be placed on symmetries/anti-
symmetriesofthecorrespondingterms.Thesecondtypeofinteractionisassociatedwiththemagneticrecon-
nectionbetweenthemagnetosheathandmagnetosphericfields,whichinsomecasesmayresultinconfigurations
withdifferentsymmetryproperties,evenforthesameIMForientations.Forexample,considerthefourthtermin
(Equation4)representingtheeffectofapurelyradialIMF.InthecaseofIMFB ≠0,B = B = 0,Ψ = 0,and
x y z
assumingnoreconnectionatthemagnetopause,oneshouldexpecttheplasmaparameterstobemirrorsymmetric
inbothyandzdirectionsacrosstheSun‐Earthline.However,includingthereconnectiondestroysthenorth‐south
symmetry, due to different mutual orientation of the magnetospheric and draped magnetosheath B vectors
northwardandsouthwardfromtheequatorialplane,whichmakesitnecessarytosplitthetermD(4)B∗ intotwo x
separatesubterms,symmetricandantisymmetricwithrespecttoz.Thesymmetriesorantisymmetriesalongyand
zaxestransformintocorrespondingrestrictionsontheallowedparitiesoftheazimuthalindexmintheexpansions
(Equation5).Acomprehensivelistofm‐indexparitiesforeachtermin(Equation4)isgivenbelowinAppen-
dixA.Upontakingintoaccountallthelimitationsimposedbythesymmetryrequirements,thefinalnumberof
unknowncoefficientstobederivedfromdatadramaticallydropsfromtheoriginal5,400to1,605.Inadditionto
thecoefficients,themodelincludesfournonlinearparameters,quantifyingtherelativesensitivityofDorW to
principalsolarwinddrivers;thesearethreeexponentsα ,α ,α in(Equation5)andtheexponentε,enteringin
d v w
thecoordinatescalingrelationr ʹ = r(P/〈P 〉)εwhichquantifiestheeffectofoverallcompression/expansionof
d d
themagnetosheathinresponsetochangesofthesolarwindrampressureP .
d
The basic procedure to calculate the model parameters was an iterative minimization of a target function Q,
defined as the r.m.s. residual difference between the modeled quantities and those from a training set of data
(described in detail in the next section). The minimization algorithm was based on an iterative Nelder‐Mead
simplexsearch(Pressetal.,1992),suchthateachstepinthefour‐dimensionalnonlinearparametricspacewas
followed by the derivation of a corresponding set of 1,605 linear coefficients by means of the singular value
decomposition(SVD,Pressetal.,1992),fromwhichacurrentvalueofthetargetfunctionwasobtained.Inamore
overallperspective,thebest‐fitmodelparameterswerederivedinthreestages.Firstofall,atentativecalculation
ofnonlinearparameterswasmadewithatruncatedversionoftheexpansion(Equation4),inwhichonlythefirst
termD(1) wasretained,whileallIMFanddipoletilteffectsweretemporarilyignored.Thatmadeitpossibleto
reducethenumberofunknowncoefficientsto105,quicklyassessstartingvaluesofthefournonlinears,andmove
ontothesecondstage,atwhichthefullexpansion(Equation4)withallIMF‐relatedtermswasbroughtintoplay.
At this step, in order to keep the computation within a reasonable timeframe, the training data subset was
decimated,suchthatonlyevery10thconsecutivedatarecordwasincludedinthefitting.Asaresult,arefinedset
ofnonlinears wasobtained,whichallowedto proceedto thelast,third stage,atwhich theobtained nonlinear
parameterswerefrozen,andthefinalvaluesofmodelcoefficientswerederivedinanone‐timeSVDcalculation,
usingafullsetoftrainingdata(around∼600,000one‐minutedatarecords).Havingthusfinalizedthemodelon
thebasisofthetrainingsubset,itsvalidationwascarriedout,usingacompletelyindependentdatasubsetofa
comparablesize.FurtherdetailsareprovidedbelowintheDataandResultssections.
3. Data
Theoriginaldatausedinthisstudywerevirtuallythesameasthose,exhaustivelydescribedinourpreviousmost
recentworks(TSEG24a,b).Tokeepthispaperreasonablyself‐contained,weprovidehereabriefsurveyofthe
mostimportantissues.Thegranddatasetisbasedonobservationsbythreemagnetosphericmissions:Cluster
(− 1,− 3,and− 4)CIS/FGMdatafrom2001through2022,Themis(− A,− B,− C,− D,and− E)ESA/FGMdata
from2007through2024,andMMS‐1FPI/FGMdatafrom2015through2024.Allthedatahave1‐minresolution
andeachrecordincludesprincipalplasmaparametersandmagneticfieldcomponents,aswellasconcurrent1‐min
averagevaluesofthesolarwindprotondensity,speed,thermalenergy,andtheIMFcomponentsfromtheOMNI
definitive database (Papitashvili & King, 2020). An important problem in the grand file compilation was to
TSYGANENKOETAL. 4of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure2. (a)Equatorialdistributionoftheprotondensityinanearlyversionofthemodelwithsecondarypeaksaroundthe
terminator,obtainedfornominalinterplanetaryparameters(V =400km/s,N =5cm−3,IMFB = B =0,B =5nT).
x y z
(b)AresultofanMHD‐simulationinthesameformat(seetextfordetails);(c)distributionoftherelativeshareofnear‐
equatorialMMSrecordswithrespecttoalldata.
accuratelyselecttheMSdatarecordsand,atthesametime,mosteffectivelyremovethosebelongingtothesolar
windandmagnetosphere.Tothatend,atwo‐stepfiltrationprocedurewasused,basedonthemethodproposedby
Jelineketal.(2012)(seeFigures4–7andrelevanttextinSection3ofTSEG24b).Theessenceofthemethod,in
short, is to generate a 2D diagram of the measured proton densities D and magnetic field magnitude B, each
quantitynormalizedbythecorrespondingsolarwindparameters,D andB ,basedondataofinterplanetary sw sw
monitorsandpropagatedfromL1pointtothesubsolarbowshock.Asaresult,threedistinctareasofenhanced
datapointconcentrationcanbeidentifiedintheplots,correspondingtothedatataken(a)inthesolarwind(low
D/D ,lowB/B ),(b)inthemagnetosheath(highD/D ,higherB/B ),and(c)inthemagnetosphere(low
sw sw sw sw
D/D ,muchhigherB/B ).Themagnetosheathdata“cloud”isthenencircledwithanisointensitycontourof
sw sw
datadensity,andawindingalgorithmisappliedtoselecttheMSdataintoanintermediatesubset.Toimprovethe
filtration accuracy, the second selection round is applied, differing from the first one in that now the plotting
parametersarethenormalizedbulkvelocityandiontemperature,whicharealsolargelydifferentinthedifferent
regionsand,hence,canalsobeusedasefficientMSidentifiers.
Inaddition,toremoveoutliersandavoideventswithextremeinterplanetaryconditions,theMSdatasubsetwas
furtherrefinedbyexcludingobservationswithboththeMSplasmaandsolarwind/IMFparametersoutsidetheir
5%–95%intervals.Afterhavingimposedalltheaboverestrictions,weendedupwithatotalof1,155,012records
for the modeling, of which 579,736 and 575,276 were placed into a training (T) and validation (V) subsets,
respectively. To ensure the mutual independence of the T and V subsets, we used the same method as in
TSEG24a,b,namely,thedatawereselectedalternatelyfromadjacentcontinuous10‐dayintervals,forexample,
from01/01− 01/10totheTsubset,thenfrom01/11− 01/20toV,thenagainfrom01/21− 01/30toT,andsoon.
A common obstacle in the plasma data interpretation is the difference in the construction and capabilities of
instrumentsonboardindividualmissions,suchastheirenergyresolution,spectrumrange,pitchanglecoverage,
etc. Being manufactured at different times and institutions, using different designs and technologies, they are
unlikelytoensurethesameuniformityofmeasurements,whichshouldinevitablyresultinsystematicdatabiases
between different missions and calls for some kind of intercalibration. The need for such a procedure was
eventually realized when analyzing equatorial distributions of the proton density in early trial versions of the
model.
AtypicalexampleisdisplayedintheleftpanelaofFigure2withanequatorialmodeldistributionoftheMS
particle density, obtained for a nominal interplanetary input with V = 400 km/s, N = 5 cm−3, IMF
B = B = 0,B = 5nT.TheplotrevealsstrongsecondarypeaksofDaroundthedawnandduskterminator,
x y z
clearlyinconsistentwithnumericalMHDresults,startingfromanearlysimulationbySpreiteretal.(1966,see
TSYGANENKOETAL. 5of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure3. ComparingconjunctiondataofThemispanels(a,c)andCluster(b,d)withMMS.Topandbottompanelscompare
protondensityandthermalenergyvalues,respectively.Datatakenatdifferentorbitsarehighlightedwithdifferentcolors.
Bestfitlines,theirslopes,Pearsoncorrelations,andnumberofdatapoints,includingtotalsandthosefromdifferentorbits(in
parentheses)areshowninlegends.
theirFigure6).ThecenterpanelbofFigure2displaysaresultofourownMHDrun,usingnearlythesamesolar
windconditions(V = 500,N = 5cm−3,IMFB = B = 0,B = 5nTandbasedonaconservativeGodunov‐
x y z
type scheme on a spherical grid, similar to that described in Erkaev et al. (2017). The plot indicates a steady
decreaseoftheMSplasmadensityawayfromthesubsolarpointofthebowshock,inobviousdisagreementwith
thestrangetriple‐peakedpatternintheleftpanel.Inordertolocatethesourceoftheproblemandruleoutthe
modelasapossibleculprit,wecloselyinspectedthedatathatmightcontributetotheunphysicaldensitysurge.To
thatend,allnear‐equatorialdatawith|Z |≤2.5 R wereselectedintoΔX = ΔY = 1.5 R slidingboxesand
GSW E E
theobtainedaveragevaluesoftherelativeshareofMMSdatawerebinnedinto0.25 × 0.25 R intervalsofXand
E
Y.TherightpanelcinFigure2representstheresultinthesameformatanddemonstratesthat100%ofnear‐
terminatorlow‐latitudedatacamefromMMSobservationsnearthedawnandduskapogeesofthespacecraft.
The commonly recognized high quality of the most modern MMS plasma instrument (FPI), with a wide and
detailed coverageof theenergyspectrum (e.g.,Bakeretal., 2016),motivatedus to adopttheMMSdataas a
referencebenchmark,findawaytocomparethemwithdataoftheothertwomissions,andcarryouttheirre‐
calibration on the basis of average ratios between the quantities in question. A possible and, probably, the
onlyfeasiblemethodtodirectlycomparethedataistobrowsethroughtheMMSdatabases,ontheonehand,and
thoseofCluster/Themis,ontheother,andselectrecordscorrespondingtospacecraftconjunctions,sufficiently
close in space and time. More quantitatively, the essence of the procedure was to collect data records taken
onboardtheconjoiningsatellites,suchthatthey(a)fallwithinfixedrestrictedintervalsoftheirspatialseparation
δR≤ΔR,(b)aresufficientlycloseintime,thatis,fallwithinlimitedtimeintervalsδT≤ΔT betweenthemea-
surements,and(c)provideareasonablenumberofrecordstocompare.Noteinpassingthatasimilarmethodwas
usedinthepasttodetermineasystematicoffsetinmagnetometerdataofGOES‐8,basedonitsconjunctionswith
themagneticallycleanPolarsatellite(Tsyganenkoetal.,2003).
TSYGANENKOETAL. 6of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure4. DistributionofthemodelvaluesoftheMSprotondensity(a,b)andthermalenergy(c,d)againsttheirobserved
1‐minaveragevaluesinthetraining(left)andvalidation(right)datasubsets.Best‐fitregressionlinesarealsoshown,aswell
astheirslopes,datapointnumbers,andPearsoncorrelationcoefficientsR.Thecolorindicatesthedatarelativedensityin
termsoflogarithmofnumberofrecordsfallingintofixedintervalsofthequantitiesinquestion.
TheselectedsetofThemis—MMSconjunctionsincluded346recordswithΔR = 3R andΔT = 5min,allof
E
whichwerenearlyequallyrepresentedbyThemisAandThemisD.Notethatallthoserecordsbelonged,infact,
toonlythreedifferentThemis—MMSconjunctioneventsthatoccurredon12/1/2021and2/13/2022forThemis
D,andon2/17/2022forThemisA.
ThesearchforCluster—MMSconjunctionsresultedinsomewhatlesstotalnumberofrecords(246),butprovided
alargernumberofseparateconjunctionevents(9)atdifferentorbitsegments,allofwhichoccurredin2019–2021
andwererepresentedbyCluster4,theonlysatelliteoftheoriginalfourprobeswhoseplasmainstrumentsurvived
inoperatingconditionbythattime.Duetomuchlargerorbitalinclinationdifference,theCluster—MMScon-
junctions lasted much shorter (δT = 1min) than Themis—MMS events (δT = 5min), for the same spatial
separationlimitΔR = 3R .
E
Figure3displaystheresultsofcomparisonoftheprotondensityandtemperaturemeasuredbyThemis/Cluster
andMMSplasmainstruments.ToppanelsshowscatterplotsoftheprotondensityvaluesobtainedbyThemisand
ClusterinstrumentsagainstthenearlysimultaneousandfairlycospatialobservationsbyMMS.Whatimmediately
attractstheattentionisthefactthatinbothcasestheslopesofbest‐fitregressionlinesarenotablylessthanunity,
whichimpliesthattheplasmainstrumentsonboardbothsatellitessignificantlyunderestimatedtheactualdensity
values.Onecansurmiseagraduallong‐termdegradationoftheplasmainstrumentsasapossiblecause,butthe
factthatthethermalenergybest‐fitslopesinbottompanelsarestillclosetounity(evenbyafewpercentlarger)
testifiesagainstthatconjectureandsuggeststhattheobtaineddifferencedidnotchangetoomuchovertheentire
TSYGANENKOETAL. 7of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure5. Equatorialdiagramsofthemagnetosheathprotondensityfornominalsolarwindconditions:V =400km/s, sw
D =5cm−3,W =10eV,IMFB = B =0,andthreeB values:B =0(a),B = +5nT(b),andB = − 5nT(c).
sw sw x y z z z z
MagnetopauseandbowshockcontourscorrespondtoLinetal.(2010)andLuetal.(2019)models.
durationofbothmissions.Theinversevaluesoftheobtainedslopeswereusedascorrectionfactorsforthedensity
D(1.42and1.96)andenergyW(0.92and0.94)intheThemisandClusterdatapools,respectively.Asaresult,the
r.m.s.value〈D〉oftherecalibrateddensityoverthenewgranddatasetsignificantlyincreased(from∼19cm−3to
∼24cm−3but,atthesametime,therelativeresidualr.m.s.mismatchQ/〈D〉betweenthemodelanddatatangibly
decreased.Theoverallredistributionofthedensityvaluesresultedinacompletedisappearanceoftheunphysical
densitypeaksaroundtheterminator(Figure2a).Beforegoingtothemodelingresultsinthenextsection,wenote
that,duetotheinevitablescarcityofthesatelliteconjunctiondata,theemployedcorrectionmethodisnotperfect
and,hence,thefinalmodeledquantitiesarenotfullyindependentontheassumedselectionprocedure.
4. Results and Discussion
Figure4demonstratestheoverallperformanceofthemodelsbymeansof2Dcoloredhistogramsofthepredicted
valuesofMSprotondensity(toppanels)andthermalenergy(bottom)againstthecorrespondingobservedvalues.
Leftandrightpanelsinbothrowsarebasedontheindependenttrainingandvalidationsubsets,respectively.The
firstthingworthmentioningistheratherhighvaluesofthemodel–datacorrelations(showninthelegends),both
fortheTandVsubsets.Thismayappearsomewhatunusual,giventhelargeamountofdata,generallyhighlevel
ofnoiseintheturbulentMSmedium,andtherathersimplemathematicalform(Equation5)oftheadoptedmodel
dependenceonthesolarwindplasmaparameters.Thedistributionslopesareby∼11 − 15%lowerthanunity,
which reflects the inevitable residual imperfection of the approximations, in particular, at the high end of the
diagrams, where the model somewhat undershoots observations due to unaccounted nonlinear effects at large
valuesoftheinputparameters.However,therelativelysmalldecreaseofthecorrelationandslopevaluesinthe
validationplotsdemonstratestheoverallstabilityofthemodelingresultsandaclose‐to‐optimalbalancebetween
theunderfittingandoverfitting(seeGershenfeld,2003,Ch.12.4).
Toprovideamorecomprehensiveassessmentofthemodel'sperformanceanditspredictiveaccuracy,additional
quantificationmetricswerecalculated,suchastheRootMeanSquareError(RMSE),themeanabsoluteerror
(MAE), the average error (AE), and the prediction efficiency (PE; e.g., McCollough et al., 2008; Vassilia-
dis,2007).Specifically,fortheprotondensitymodelbasedonthetrainingset,thefollowingvalueswereob-
tained:RMSE=5.11cm−3,MAE=3.64cm−3,AE=0.05cm−3,andPE=0.95.Thecorrespondingvaluesbased
on the validation set were found equal to RMSE = 5.48 cm−3, MAE = 3.84 cm−3, AE = 0.02 cm−3, and
PE = 0.94, respectively. For the proton thermal energy, the corresponding results are as follows:
RMSE = 45.9 eV, MAE = 29.5 eV, AE = 0.14 eV, PE = 0.95 (training set) and RMSE = 53.0 eV,
MAE=34.0eV,AE=− 1.08eV,PE=0.94(validationset).
TSYGANENKOETAL. 8of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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
by the
applicable
Creative
Commons
License

 21699402, 2025, 12, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343 by Sang-Yun Lee - Nasa Goddard , Wiley Online Library on [30/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical |     | Research: | Space | Physics |     |     |     |
| ------- | -------------- | --- | --------- | ----- | ------- | --- | --- | --- |
10.1029/2025JA034343
Figure6. SameasinFigure5,butforaspiral‐likeIMForientationwithB = − 4,B = +5,andthreeIMFB values:
|     |             |            |                                                        |     |     | x y | z   |     |
| --- | ----------- | ---------- | ------------------------------------------------------ | --- | --- | --- | --- | --- |
|     | B = +5(a),B | =0(b),andB | = − 5nT(c).TheinclinedIMForientationisshownwitharrows. |     |     |     |     |     |
|     | z           | z          | z                                                      |     |     |     |     |     |
Itisinstructivetoanalyzetheobtainedbest‐fitvaluesofexponentsα d ,α v ,andα w in(Equation5),forboththeMS
protondensityandenergy,andcomparethemwiththeoreticalvalues.FortheMSdensityD,thefittingreturned
the following values: α = 0.939, α = − 0.073, and α = − 0.008, indicating an almost linear relationship
|     |     |     | d v |     | w   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
betweenDandD sw ,aweakinversedependenceonthesolarwindspeedV sw ,andvirtuallynosensitivitytothe
interplanetaryprotontemperature.Forcomparison,thegasdynamictheory(Spreiteretal.,1966;Equation29)
predictsthatthedensityjumpatthesubsolarbowshockisasimplefunctionoftheMachnumberM:
(γ+1)M2
|     |     |     |     | D=D |     |     |     | (6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
sw(γ−
1)M2+2
Assuming the solar wind polytrope index γ = 5/3 and M ∼ 10, one obtains D≈4D and extremely weak
sw
dependenceonthesolarwindbulkspeedandtemperature(enteringviatheMachnumberM).Thisisingood
agreementwithourresults,asevidencedbytheobtainedvaluesofexponentsα d ,α v ,andα w ,aswellasbythe
model values of the subsolardensity jump across the bow shock shown in the diagrams that follow below in
Section4.1.
Turning now to the proton thermal energy, the modeling yielded α = 0.094, α = 2.13, and α = 0.073,
|     |     |     |     |     |     | d v | w   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
indicatingweaksensitivitytothesolarwinddensityandtemperature,butadramaticnearlyquadraticdependence
onthesolarwindspeed. Accordingto thesame gasdynamictheory (Spreiter etal.,Equation28),thethermal
|     | energyW | behindthebowshockequals |      |     |       |     |     |     |
| --- | ------- | ----------------------- | ---- | --- | ----- | --- | --- | --- |
|     |         |                         |      | (γ− | 1)    | v2  |     |     |
|     |         |                         | W =W | {1+ | M2(1− | )}, |     | (7) |
|     |         |                         |      | sw  | 2     | V2  |     |     |
sw
wherevistheplasmabulkspeedintheMS.Forthesamevaluesofthepolytropicindexγ,MachnumberM,and
√̅̅̅̅̅̅̅̅̅
assumingthebulkspeedv≪V insidetheMS,oneobtainsW ≈W (M2/3).SinceM∝V / W ,thefinal
|     |     |     | sw  |     |     | sw  | sw sw |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- |
resultisthatW∝V2 andisvirtuallyindependentontheothertwodrivers:again,inalmostperfectagreement
sw
withthemodelingresult.Inthefollowingsections,wepresentanddiscussourgraphicalresultsofthedensityand
thermalenergymodeling.
|     | 4.1. ProtonDensity |     |     |     |     |     |     |     |
| --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
Figure 5 shows equatorial distributions of the proton density D for nominal values of external drivers,
V = 400km/s,D = 5cm−3,W = 10eV,IMFB = B = 0andthreevaluesofB = 0,B = +5nT,
|     | sw  | sw  | sw  |     | x y |     | z z |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
TSYGANENKOETAL. 9of17

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
andB = − 5nT.ThemagnetopauseandbowshockcontourscorrespondtoLinetal.(2010)andLuetal.(2019)
z
models,respectively,forthesameinterplanetaryconditions.AsalreadynotedinSection2,wereiteratehereagain
thatboththemodeldensityandthermalenergyarecontinuousfunctionsofthecoordinateδ,thatis,neitherofthe
modeloutputparametersincludeabruptjumpsatthebowshockandmagnetopause.TheLuetal.(2019)andLin
etal.(2010)boundariesshowninthisandfollowingfiguresareprovidedonlyforthepurposeofevaluatingthe
rangeofthedensityandenergyvariationacrosstheMSandforthereader'sorientation.
Ingeneral,thethreeplotsaremostlysimilartoeachother,withthesubsolardensitypeakingatD≈24cm−3and
decreasingtowardtheterminator.Themaindifferencebetweenthecasesofnorthward(B)andsouthward(C)
IMFB issomewhathigher/lowerdensitiesintheformer/lattercase,whichmaybeinterpretedasaconsequence
z
oftheplasmapileupforB >0anditseffectivereconnection‐relateddrainingfromthesubsolarareaforB <0.
z z
The next Figure 6 corresponds to a more common case of a Parker‐type spiral IMF orientation with IMF
B = − 4, B = +5, and three values of B = +5 (A), B = 0 (B), and B = − 5 (C). Here one can see a
x y z z z
significantdawn‐duskasymmetrywiththepeakdensityareasshiftedtopre‐noonMLThours,wheretheIMF
fieldlinesareorientedatlargeranglestothebowshockandmagnetopause.Asinthepreviouscase,oneobserves
the same effect of IMF B polarity with clearly higher (lower) densities at the magnetopause for IMF B >0
z z
(B <0).Theoriginofthebifurcationswithsecondarylocalpeaksintheazimuthaldensitydistributionisnot
z
quiteclear;oneofpossiblecausesmaybeanunevenazimuthaldistributionofdata,combinedwiththeoscillating
natureofsphericalfunctions(Equation2)intheindividualexpansionterms(Equation5).
ThenextsetofplotsinFigure7showsmeridionaldistributionsofthemagnetosheathprotondensityforthree
orientations of IMF and two dipole tilt angles. The left (A, C, E) and right (B, D, F) columns correspond,
respectively,tothecasesofuntiltedandtilteddipolewithΨ = 0andΨ = 25°.Threepanelsineachcolumn
display,fromtoptobottom,themodeldensitydistributionsfornorthward(A,B),southward(C,D),andpurely
radial(E,F)IMFwith{B ,B ,B} = {0,0, +5},{0,0, − 5},and{+5,0,0}.TheIMFdirection,magnetospheric
x y z
fieldorientationnearthemagnetopause,andthegeodipolemomentvectorareshownbyarrows.Severalinter-
estingfeaturesareimmediatelyapparent.Intheleftcolumn,thetoppanelarevealsasignificantplasmapile‐upin
thesubsolararea,wheretheIMFandmagnetosphericfieldarenorthward.Bycontrast,thedensityissignificantly
lower around and above the polar cusps, where the magnetosheath and high‐latitude tail lobe fields are anti-
parallel,suchthattheparticlesareeffectivelydrainedoutbyreconnection.IntheoppositecaseofsouthwardIMF
(panelc),thesubsolardensitygetslower,butincreaseswithinlocal“tongues”thatemergefromthecusps.The
lattermaybeinterpretedasaneffectofreconnection‐relatednorthwardandsouthwardplasmastreamsthatblow
fromthesubsolarareaandimpingeagainsttheplasmapile‐upregionsathigherlatitudes.
These effects become more dramatic in the case of tilted dipole: for IMF B >0 (panel b), the subsolar peak
z
increasesinmagnitudeandshiftssouthward,whilethenorthernhigh‐latitudedensitydepressionexpandsinsize,
withthelowestvaluesfoundinthecenterofthecuspindentation.FortheoppositecaseofIMFB <0(paneld),
z
thecontrastbetweentheareaspolewardandequatorwardfromthenortherncuspbecomesevengreater;herewe
noteinpassingthat,duetothedipoletilt,thenortherncuspshiftstolowerlatitudeswherethedatacoverageis
muchbetterthanathigherZ,whichdismissesthedatascarcityasanuncertaintyfactorandapossiblesourceof
artifacts.
Thepile‐upeffectonthenorthernsidedramaticallyincreasesnotonlyduetotheparallelfieldsorientation,but
alsobecauseofmuchlargerincidenceangleoftheplasmaflowagainstthelocalmagnetopausearea.Itshouldbe
remindedherethattheplasmacompressioninthatregionisaccompaniedbythelocalincreaseoftheinternal
magnetospheric magnetic field, persistently revealed in the Polar magnetometer data (Tsyganenko & Rus-
sell,1999;Figure2).Maintainingtheforcebalanceacrossthislocalmagnetic“wall”necessarilycallsforthe
increaseoftheexternalmagnetosheathplasmapressure.Immediatelysouthwardfromthenortherncusp,onesees
alocalizedareawithmuchlowerdensities,causedmostlikelybyacombinationofreconnection‐relateddraining
andlowflowincidenceangle.Atevenlowerlatitudesandfurthersouthwardfromtheequatorialplane,awide
region of enhanced density is formed, bifurcated into two islands, most likely due to two antiparallel jets
spreadingfromthereconnectionlineatZ ∼ − 3R . E
Theaboveinterpretationintermsofthereconnection/pile‐upisconfirmedbywhatoneseesintwobottompanels,
for the case of purely radial IMF. For the untilted dipole (panel e), one sees generally larger densities in the
southernhemisphere,withalocalpeakatZ ∼ − 2R ,extendingintothenorthernhemispaceasatongue‐like
E
TSYGANENKOETAL. 10of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on [30/10/2026].
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

 21699402, 2025, 12, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343 by Sang-Yun Lee - Nasa Goddard , Wiley Online Library on [30/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical |     | Research: | Space Physics |     |     |     |
| ------- | -------------- | --- | --------- | ------------- | --- | --- | --- |
10.1029/2025JA034343
Figure7. MeridionaldistributionsofthemagnetosheathprotondensityfordifferentIMForientations(toptobottom)andtwo
geodipoletiltangles(leftandrightcolumns).SpecificvaluesofIMFcomponentsandthedipoletiltanglesareshowninthe
=0,B =0,
legendsoneachpanel.Magneticfieldorientationinsidethemagnetosphereisshownwithyellowarrows.(a)B x y
=5,Y=0;(b)B =0,B =0,B =5,Y=25;(c)B =0,B =0,B =− 5,Y=0;(d)B =0,B =0,B =− 5,Y=25;
|     | B z      | x                | y z  | x y           | z   | x y | z   |
| --- | -------- | ---------------- | ---- | ------------- | --- | --- | --- |
|     | =5,B     | =0,B =0,Y=0;(f)B | =5,B | =0,B =0,Y=25. |     |     |     |
|     | (e)B x y | z                | x    | y z           |     |     |     |
strip.Again,thedistributiondramaticallychangesforthecaseoftilteddipole:thepile‐upeffectincreasesand
expandsovermuchlargerareasouthwardfromtheequator,whilethedensitiesaroundthenortherncuspforma
strikingly antisymmetric pattern with enhanced/depressed areas northward/southward from the cusp center,
correspondingtothepile‐up/reconnectionregionsontheoppositesidesofthecusp.
TSYGANENKOETAL. 11of17

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure8. ThermalprotonenergyWdistributionsintheequatorialplane,fordifferentcombinationsofIMFcomponentsand
nominalsolarwindplasmaparameters:(a)B =0,B =0;B =0;(b)B =0,B =0;B =+5;(c)B =0,B =0;B =− 5.
x y z x y z x y z
Ageneralnoteshouldbemadehereinregardoftheso‐calledplasmadepletionlayer(PDL)thatformsnearthe
magnetopauseundernorthwardIMFconditions(e.g.,Anderson&Fuselier,1993;MichottedeWelleetal.,2024;
Phanetal.,1994;Pudovkinetal.,2001).IdentifyingthePDLwasoneofourtopprioritiessincetheveryinception
ofthisproject.Tothatend,amultitudeofmodelingexperimentshavebeencarriedoutwith(a)differentradialand
angular flexibility degrees (quantified by the upper limits of L,M,N indices), (b) different stringency of the
magnetosheath data selection criteria (from the Jelinek‐type diagrams), (c) different numbers of the model
expansionterms,and(d)differentvaluesoftheSVDtoleranceparameter(ratioofmintomaxeigenvalues).Asa
result,itwaseventuallyconcludedthat,dueto(a)theextremelydynamicalnatureofthemagnetosheathmedium
anditsinner/outerboundaries,(b)smallthicknessofthePDLrelativetothemagnetosheathcrosssection,(c)
inevitableinaccuracyofpropagatingthesolarwindparametersfromL1pointtothebowshock,and(d)thelargely
approximatenatureoftheadoptedmagnetopausemodelbyLinetal.,thistaskstillremainsbeyondthereachof
thepresentapproach.
4.2. ProtonThermalEnergies
Figure8showsequatorialdistributionsoftheprotonthermalenergiesineVforthesamethreeIMForientations
andcomponentvaluesasinFigure5andthesamenominalsolarwindplasmaparameters.Asexpected,theenergy
peaksatthesubsolarpointandsteadilyfallsoffawaytowardtheterminator,asaresultoftheplasmacoolingand
conversionofitsthermalenergyintothekineticenergyofthedirectedbulkflow.Theleftpanelcorrespondstothe
rarecaseofunmagnetizedsolarwindwiththesubsolarenergypeakofnearly220–230eV,whichis22–23times
greaterthanthenominalsolarwindinputvalueofW =10eVand,hence,wellintheballparkoftheoretically
sw
predictedvaluesW ≈W (M2/3) ∼ 210− 230.Thesubsolarenergytangiblydecreasesinthecaseofnorthward sw
IMF (center panel b) downto ∼200eV, as aresult of theconcurrent pile‐up‐related density increaseand the
requirementtokeeptheplasmapressureatnearlythesameleveltomaintaintheforcebalanceacrossthebow
shock.
The situation changes for the southward IMF B (panel c): due to the plasma heating by reconnection, the
z
temperaturerisesbackto210–220eV,whilethedensityfallsdown(Figure5).
Figure9displaysequatorialdistributionsofthethermalenergyforthesamethreecombinationsoftheinputIMF
components as in Figure 6, corresponding to the Parker spiral with B = − 4, B = +5, and B = +5 (A),
x y z
B = 0(B),andB = − 5(C).Asopposedtothedensity(Figure6),herethedawn‐duskasymmetryrevealsitself
z z
mostlyinthepost‐dawnandpre‐dusksectors,ratherthanaroundthesubsolararea:thetemperaturesaregenerally
higheratthemorningside,whichmaybeattributedtotheforeshock‐relatedplasmaheating.
TSYGANENKOETAL. 12of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure9. SameasinFigure8,butfortheinclinedspiral‐typeorientationoftheIMF.(a)B =− 4,B =5;B =5;(b) x y z
B =− 4,B =5;B =0;(c)B =− 4,B =5;B =− 5.
x y z x y z
ThenextFigure10isanalogousinformattoFigure7,andshowsthemeridionaltemperaturedistributionsforthe
sameinputvaluesoftheIMFcomponentsandgeodipoletiltangle.Ingeneral,byvisuallycomparingthetwo
figures,oneclearlyseesaone‐to‐oneanticorrelationbetweenthedensityminima/maximainFigure7andthe
correspondingtemperaturepatterns,asitshouldbeinviewofthepressurebalancerequirement.Thetemperatures
aregenerallyhigherintheareas,whereonecanexpectthereconnectionjetstoimpingeupontheflowstagnation
regionswithpiled‐upplasma.Thisisespeciallypronouncedintherightcolumnforthecaseoftiltedgeodipole:in
thepanelsbandd,correspondingtonorthwardandsouthwardIMFB,respectively,thetemperaturepeaksare
z
locatedontheoppositesidesfromthenortherncusp.Asomewhatdifferentinterpretationcanbesuggestedforthe
caseofpurelyradialIMF(panelf):thereconnectionjetblowingnorthwardfromlowlatitudesbrakesagainstthe
stagnated/piled‐up plasma above the cusp, resulting in plasma compression (Figure 7, the same panel f) and
heating. The same arguments hold for interpreting the temperature distributions around the southern cusp in
panelseandf:thebroadareasofdepressedtemperaturesouthward/sunwardfromthemagnetopauseindentation
match the corresponding regions of elevated density in the same panels in Figure 7, in line with the pressure
balancerequirement.Theoriginoftheenhancedtemperatureareaatthesouthernterminatoredgeoftheplotin
panel f is not yet clear; it may be a model artifact due to lack of data in the poorly populated corner of the
parametricspace.
5. Conclusions
Empirical models have been constructed of the proton density and temperature (thermal energy) in the
terrestrial magnetosheath, based on data of plasma instruments onboard spacecraft missions Cluster, Themis,
andMMS.Theone‐minuteresolutiondatawerethesameasthoseusedinourpreviousmodelingstudiesofthe
magnetosheath magnetic field and plasma flows, separately selected for each mission by means of a 2D‐
histogram technique originally proposed by Jelinek et al. (2012). In addition, the data were intercalibrated
usingseveraleventsofcloseClusterandThemisconjunctionswiththeMMSsatellite.Themodeloutputswere
foundingoodagreementwithgasdynamic/MHDresultsinregardtothedensityandtemperaturejumpsacross
the bow shock. The modeling revealed a significant influence of the IMF orientation and magnitude on the
plasmadensityandtemperaturedistributionsinsidethemagnetosheath,duetoboththemagneticpressureand
tensionofthedrapedmagnetosheathfieldlines,ontheonehand,andthereconnection/pile‐upeffects, onthe
other. The latter effects were shown to be quite sensitive to the geodipole tilt, especially pronounced in the
vicinityof thedaysidepolarcusps duringthe periodsoftheir maximalexposure to thesolarwindatsummer
time.
TSYGANENKOETAL. 13of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Figure10. SameasinFigure7,butforthemagnetosheathplasmatemperature(thermalenergy)ineV.Magneticfield
componentsareinnT,geodipoleangle(Y)isindegrees:(a)B =0,B =0,B =5,Y=0;(b)B =0,B =0,B =5,Y=25;
x y z x y z
(c)B =0,B =0,B =− 5,Y=0;(d)B =0,B =0,B =− 5,Y=25;(e)B =5,B =0,B =0,ψ=0;(f)B =5,B =0,
x y z x y z x y z x y
B =0,Y=25.
z
Asafinalnote,thisstudyshouldbeviewedasonlythefirststep,intendedtotouchtheboundarybetweendoable
andundoableandtoexplorethefeasibilitylimitsofthedata‐basedapproach.Developmentofmoreadvancedand
accuratemethodsofplasmadomainidentification,dataselection,andintercalibrationofmeasurementsmadeby
individualspacecraftisoneoftheproblemsstillawaitingtobeaddressedinthefuture.
TSYGANENKOETAL. 14of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

 21699402, 2025, 12, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343 by Sang-Yun Lee - Nasa Goddard , Wiley Online Library on [30/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| Journal | of Geophysical |     | Research: | Space | Physics |     |     |     |
| ------- | -------------- | --- | --------- | ----- | ------- | --- | --- | --- |
10.1029/2025JA034343
|     | Appendix | A: Parity | Properties | of Individual | Model Expansion | Terms |     |     |
| --- | -------- | --------- | ---------- | ------------- | --------------- | ----- | --- | --- |
TableA1presentsanexplicitstructureofalltermsenteringinEquation4withtheirdetailedbreakdownintopairs
of terms proportional to cosmϕ and sinmϕ, as well as their parities in Y, Z, and m‐index. The word “none”
denotestermsthatshouldbeskippedintheexpansionsasincompatiblewiththerequiredsymmetry/antisymmetry
conditions.ThefactorsF(i) = g(i) Dαd Vαv WαwPm(cosθ)andF(i) = h(i) Dαd Vαv WαwPm(cosθ).
|     |     |     | c lnm | sw sw sw n | s lnm | sw sw | sw n |     |
| --- | --- | --- | ----- | ---------- | ----- | ----- | ---- | --- |
TableA1
FullListofEquation4TermsWithTheirDawn‐Dusk(y)andNorth‐South(z)Parities
|     |               |      | Parities |           |                 |      | Parities |           |
| --- | ------------- | ---- | -------- | --------- | --------------- | ---- | -------- | --------- |
|     | Terms         | iny  | inz      | m         | Terms           | iny  | inz      | m         |
|     | F(1)cosmϕ     |      |          |           | F(9)B2cosmϕ     | Even |          |           |
|     | c             | Even | Even     | Even      | c z             |      | Even     | Even      |
|     | F(1)sinmϕ     | –    | –        |           | F(9)B2sinmϕ     | –    | –        |           |
|     | s             |      |          | None      | s z             |      |          | None      |
|     | (2)Ψcosmϕ     |      |          |           | (10)BxBycosmϕ   |      |          |           |
|     | F             | Even | Odd      | odd       | F               | Even | Even     | Even      |
|     | c             |      |          |           | c               |      |          |           |
|     | F (2)Ψsinmϕ   | –    | –        | None      | F (10)BxBysinmϕ | Odd  | Even     | Odd       |
|     | s             |      |          |           | s               |      |          |           |
|     | F (3)Ψ2cosmϕ  | Even | Even     | Even      | F (11)BxBzcosmϕ | Even | Odd      | Odd       |
|     | c             |      |          |           | c               |      |          |           |
|     | F (3)Ψ2sinmϕ  | –    | –        | None      | F (11)BxBzsinmϕ | –    | –        | None      |
|     | s             |      |          |           | s               |      |          |           |
|     | F (4)Bxcosmϕ  | Even | Odd      | Odd       | F (12)ByBzcosmϕ | Even | Even     | Even      |
|     | c             |      |          |           | c               |      |          |           |
|     | F (4)Bxsinmϕ  | –    | –        | None      | F (12)ByBzsinmϕ | Even | Even     | Even(m>0) |
|     | s             |      |          |           | s               |      |          |           |
|     | F (5)Bycosmϕ  | –    | –        |           | F (13)BxΨcosmϕ  | Even | Even     | Even      |
|     | c             |      |          | None      | c               |      |          |           |
|     | (5)Bysinmϕ    |      |          |           | (13)BxΨsinmϕ    | –    | –        |           |
|     | F s           | Odd  | Odd      | Even(m>0) | F s             |      |          | None      |
|     | (6)Bzcosmϕ    |      | Even     |           | (14)ByΨcosmϕ    | –    | –        |           |
|     | F c           | Even |          | Even      | F c             |      |          | None      |
|     | (6)Bzsinmϕ    |      |          |           | (14)ByΨsinmϕ    |      |          |           |
|     | F             | –    | –        | None      | F               | Odd  | Even     | Even(m>0) |
|     | s             |      |          |           | s               |      |          |           |
|     | F (7)B2 cosmϕ | Even | Even     | Even      | F (15)BzΨcosmϕ  | Even | Odd      | Odd       |
|     | c x           |      |          |           | c               |      |          |           |
|     | F (7)B2 sinmϕ | –    | –        | None      | F (15)BzΨsinmϕ  | –    | –        | None      |
|     | s x           |      |          |           | s               |      |          |           |
|     | F(8)B2cosmϕ   | Even | Even     | Even      |                 |      |          |           |
c y
|     | F(8)B2sinmϕ | –   | –   |      |     |     |     |     |
| --- | ----------- | --- | --- | ---- | --- | --- | --- | --- |
|     | s y         |     |     | None |     |     |     |     |
As explainedin Section2, theexpansiontermsin (Equation 4)areclassifiedintoafew groups, basedonthe
expectedsymmetryofthemagnetosheathplasmaflowandmagneticfieldreconnectiongeometrywithrespectto
YandZaxeswhich,inturn,followfromtheassumptionsof(a)themagnetopausesymmetryalongYandZand(b)
thecorrespondingsymmetrypropertiesoftheunderlyingmagnetosphericfield.Morespecifically,itisassumed
thattheboundarycoordinatesandplasmaparametersareevenfunctionsofY;asconcernstheirdependenceonZ,
itisalittlemoreinvolvedduetotheeffectsofthegeodipoletiltΨ.Namely,theparametersremaininvariantwith
respecttosimultaneouschange:Z → − Z andΨ → − Ψ.Thisuniquelydefinesthem‐indexselectionforthe
termsindependentofIMF(lines1–6intheleftcolumnofTableA1).Theselectionprocedureismorecomplexfor
the rest of the terms that depend onthe IMF components. The terms linear with respect to B x (lines 7–8) are
exclusivelyassociatedwithreconnectionand,duetoitsNorth‐Southantisymmetry,mustbeoddinZ.Thesame
holdsforthetermslinearinIMFB andB;tosingleoutthosewithallowedm‐indexparities,thebasicprocedure
|     |     |     | y   | z   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
istodrawcorrespondingpatternsoftheIMFdrapingaroundthemagnetopauseandvisuallycheckthedrapedfield
orientationwithrespecttotheunderlyingfieldlinesofuntiltedmagnetosphericfield.Thenext12linesofthetable
includetermsquadraticinIMFcomponents;someofthemareexclusivelyassociatedwiththeIMFdraping(blue
font),orreconnection(red),orboth(black).Thelast6linesincludeproductsoftheIMFcomponentsandthe
dipoletiltΨ,whichnaturallyassociatesthemwithreconnectioneffects. Here,inorderto correctlydefinethe
allowedparities,itisinstructivetokeepinmindthatthemagneticeffectofthedipoletiltcanberepresentedtothe
firstorderasaproperlyweightedaxisymmetricfieldofashieldedparalleldipole(withΨ = 90°),whosefield
TSYGANENKOETAL. 15of17

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
linesextendradiallyfromthesubsolarpointalongthemagnetopause(e.g.,bottompanelofFigure3;Tsyganenko
&Andreeva,2014).
Conflict of Interest
Theauthorsdeclarenoconflictsofinterestrelevanttothisstudy.
Data Availability Statement
Cluster,THEMIS,andMMSmagnetometerandplasmainstrumentoriginaldataforthisstudyweredownloaded
fromtheNSSDCCDAWEBinterfaceathttps://cdaweb.gsfc.nasa.gov/cdaweb/index.html.One‐minuteresolu-
tionOMNIdatawereobtainedfromSPDFOMNIWEBathttps://omniweb.gsfc.nasa.gov.Allthetrainingand
validationdatasetsusedtoconstructtheabovedescribedmodels,basedonthedataoftheabovemissions,andthe
employed software are freely available from Zenodo public repository at: https://doi.org/10.5281/zenodo.
17330908(Tsyganenko,2025).
Acknowledgments References
WeacknowledgetheteamsandPIsofall
Anderson,B.J.,&Fuselier,S.A.(1993).Magnetosphericpulsationsfrom0.1to4.0HzandassociatedplasmapropertiesintheEarth’ssubsolar
experimentswhosedatacontributedtothis
magnetosheathandplasmadepletionlayer.JournalofGeophysicalResearch,98(A2),1461–1479.https://doi.org/10.1029/92ja02197 study.Inparticular,ClusterandMMS
Baker,D.N.,Riesberg,L.,Pankratz,C.K.,Panneton,R.S.,Giles,B.L.,Wilder,F.D.,&Ergun,R.E.(2016).Magnetosphericmultiscale
plasma/magnetometer/ephemerisdata
instrumentsuiteoperationsanddataSystem.SpaceScienceReviews,199(1–4),545–575.https://doi.org/10.1007/s11214‐014‐0128‐5
wereobtainedfromtheNSSDCCDAWEB
Dimmock,A.P.,Hietala,H.,&Zou,Y.(2020).Compilingmagnetosheathstatisticaldatasetsunderspecificsolarwindconditions:Lessonslearnt
onlinefacility,originallymadeavailable
bythePIs:H.Reme(ClusterCIS/CODIF fromthedaysidekineticsouthwardIMFGEMchallenge.EarthandSpaceScience,7(6),e2020EA001095.https://doi.org/10.1029/
plasmadata)A.BaloghandM.Tatrallyay 2020EA001095
Dimmock,A.P.,&Nykyri,K.(2013).ThestatisticalmappingofmagnetosheathplasmapropertiesbasedonTHEMISmeasurementsinthe
(Clustermagnetometerandephemeris
magnetosheathinterplanetarymediumreferenceframe.JournalofGeophysicalResearch:SpacePhysics,118(8),4963–4976.https://doi.org/
data),byJ.Burch,C.Russell,W.Magnus,
10.1002/jgra.50465
C.Pollock,andB.Giles(MMS
Dimmock,A.P.,Pulkkinen,T.J.,Osmane,A.,&Nykyri,K.(2016).Thedawn‐duskasymmetryofiondensityinthedaysidemagnetosheathand
magnetometerdata).V.Angelopoulos,
itsannualvariabilitymeasuredbyTHEMIS.AnnalsofGeophysics,34(5),511–528.https://doi.org/10.5194/angeo‐34‐511‐2016
K.‐H.Glassmeier,U.Auster,W.
Baumjohann,C.W.Carlsonand Erkaev,N.V.,Odert,P.,Lammer,H.,Kislyakova,K.G.,Fossati,L.,Mezentsev,A.,etal.(2017).Effectofstellarwind‐inducedmagneticfields
onplanetaryobstaclesofnon‐magnetizedhotJupiter.MonthlyNoticesoftheRoyalAstronomicalSociety,470(4),4330–4336.https://doi.org/ J.McFaddenareacknowledgedfortheuse
10.1093/mnras/stx1471 ofTHEMISFGMandESAdata.High‐
Gershenfeld,N.(2003).Thenatureofmathematicalmodeling.CambridgeUniversityPress.
resolutionOMNIinterplanetarydatawere
Jelínek,K.,Němeček,Z.,&Šafránková,J.(2012).Anewapproachtomagnetopauseandbowshockmodelingbasedonautomatedregion
obtainedfromtheSPDFOMNIWEB
identification.JournalofGeophysicalResearch,117,A05208.https://doi.org/10.1029/2011JA017252.1
interface(R.McGuire,N.Papitashvili).
SpecialthanksareduetoArcadiUsmanov Jung,J.,Connor,H.,Dimmock,A.,Sembay,S.,Read,A.,&Soucek,J.(2024).Mshpy23:Auser‐friendly,parameterizedmodelofmagnetosheath
whonoticedandinformedusonanerrorin conditions.EarthandPlanetaryPhysics,8(1),89–104.https://doi.org/10.26464/epp2023065
Kobel,E.,&Flückiger,E.O.(1994).Amodelofthesteadystatemagneticfieldinthemagnetosheath.JournalofGeophysicalResearch,99(A12),
theoriginalversionofFigure1,which
23617–23622.https://doi.org/10.1029/94JA01778
creptin,unnoticed,inourthreeprevious
Lin,R.L.,Zhang,X.X.,Liu,S.Q.,Wang,Y.L.,&Gong,J.C.(2010).Athree‐dimensionalasymmetricmagnetopausemodel.Journalof
publications(TSE23,TSEG24aandb).
GeophysicalResearch,115(A4),A04207.https://doi.org/10.1029/2009JA014235
Theauthorsacknowledgefinancialsupport
Lu,J.Y.,Zhou,Y.,Ma,X.,Wang,M.,Kabin,K.,&Yuan,H.Z.(2019).Earth’sbowshock:Anewthree‐dimensionalasymmetricmodelwith
fromtheRussianScienceFoundation
Grant23‐47‐00084“Magnetic dipoletilteffects.JournalofGeophysicalResearch:SpacePhysics,124(7),5396–5407.https://doi.org/10.1029/2018JA026144
Ma,X.,Nykyri,K.,Dimmock,A.,&Chu,C.(2020).Statisticalstudyofsolarwind,magnetosheath,andmagnetotailplasmaandfieldproperties:
ReconnectioninSpaceandLaboratory
12+yearsofTHEMISobservationsandMHDsimulations.JournalofGeophysicalResearch:SpacePhysics,125(10),e2020JA028209.
Plasmas:ComputerSimulationsand
https://doi.org/10.1029/2020JA028209
EmpiricalModeling.”
McCollough,J.P.,Gannon,J.L.,Baker,D.N.,&Gehmeyr,M.(2008).Astatisticalcomparisonofcommonlyusedexternalmagneticfield
models.SpaceWeather,6(10),S10001.https://doi.org/10.1029/2008SW000391
MichottedeWelle,B.,Aunai,N.,Nguyen,G.,Lavraud,B.,Génot,V.,Jeandet,A.,&Smets,R.(2022).Globalthree‐dimensionaldrapingof
magneticfieldlinesinEarth’smagnetosheath fromin‐situspacecraftmeasurements.JournalofGeophysicalResearch:SpacePhysics,
127(12),e2022JA030996.https://doi.org/10.1029/2022JA030996
MichottedeWelle,B.,Aunai,N.,Lavraud,B.,Génot,V.,Jeandet,A.,Nguyen,G.,etal.(2024).Spatialdistributionofplasmadensityand
magneticfieldamplitudeinthedaysidemagnetosheathasafunctionoftheIMForientation.FrontiersinAstronomyandSpaceSciences,11,
1427791.https://doi.org/10.3389/fspas.2024.1427791
O’Brien,C.,Walsh,B.M.,Zou,Y.,Qudsi,R.,Tasnim,S.,Zhang,H.,&Sibeck,D.G.(2024).PRIME‐SH:Adata‐drivenprobabilisticmodelof
Earth’smagnetosheath.JournalofGeophysicalResearch:MachineLearningandComputation,1(3),e2024JH000235.https://doi.org/10.
1029/2024JH000235
Papitashvili,N.E.,&King,J.H.(2020).OMNI1‐mindataset[Dataset].NASASpacePhysicsDataFacility.https://doi.org/10.48322/45bb‐8792
Phan,T.‐D.,Paschmann,G.,Baumjohann,W.,Sckopke,N.,&Lühr,H.(1994).Themagnetosheathregionadjacenttothedaysidemagnetopause:
AMPTE/IRMobservations.JournalofGeophysicalResearch,99(A1),121–141.https://doi.org/10.1029/93JA02444
Pi,G.,Nemecek,Z.,Safrankova,J.,&Grygorov,K.(2024).SpatialprofilesofmagnetosheathparametersunderdifferentIMForientations:
THEMISobservations.FrontiersinAstronomyandSpaceSciences,11,1401078.https://doi.org/10.3389/fspas.2024.1401078
Press,W.H.,Teukolsky,S.A.,Vetterling,W.T.,&Flannery,B.P.(1992).NumericalRecipes(2nded).CambridgeUniversityPress.
Pudovkin,M.I.,Besser,B.P.,Zaitseva,S.A.,Lebedeva,V.V.,&Meister,C.‐V.(2001).Magneticbarrierincaseofasouthwardinterplanetary
magneticfield.JournalofAtmosphericandSolar‐TerrestrialPhysics,63(10),1075–1083.https://doi.org/10.1016/s1364‐6826(01)00023‐2
Samsonov,A.(2006).NumericalmodellingoftheEarth’smagnetosheathfordifferentIMForientations.AdvancesinSpaceResearch,38(8),
1652–1656.https://doi.org/10.1016/j.asr.2005.06.009
TSYGANENKOETAL. 16of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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

Journal of Geophysical Research: Space Physics 10.1029/2025JA034343
Samsonov,A.A.,Gordeev,E.,Tsyganenko,N.A.,Safrankova,J.,Nemecek,Z.,Simunek,J.,etal.(2016).Doweknowtheactualmagnetopause
positionfortypicalsolarwindconditions?JournalofGeophysicalResearch:SpacePhysics,121(7),6493–6508.https://doi.org/10.1002/
2016JA022471
Samsonov,A.A.,Nemecek,Z.,Safrankova,J.,&Jelinek,K.(2012).Whydoesthesubsolarmagnetopausemovesunwardforradialinterplanetary
magneticfield?JournalofGeophysicalResearch,117,A05221.https://doi.org/10.1029/2011JA017429
Shue,J.‐H.,Chao,J.K.,Fu,H.C.,Russell,C.T.,Song,P.,Khurana,K.K.,&Singer,H.J.(1997).Anewfunctionalformtostudythesolarwind
controlofthemagnetopausesizeandshape.JournalofGeophysicalResearch,102(5),9497–9511.https://doi.org/10.1029/97JA00196
Siscoe,G.L.,Crooker,N.U.,Erickson,G.M.,Sonnerup,B.U.Ö.,Maynard,N.C.,Schoendorf,J.A.,etal.(2002).MHDpropertiesof
magnetosheathflow.PlanetaryandSpaceScience,50(5–6),461–471.https://doi.org/10.1016/s0032‐0633(02)00026‐0
Soucek,J.,&Escoubet,C.P.(2012).PredictivemodelofmagnetosheathplasmaflowanditsvalidationagainstclusterandTHEMISdata.Annals
ofGeophysics,30(6),973–982.https://doi.org/10.5194/angeo‐30‐973‐2012
Spreiter,J.R.,&Alksne,A.Y.(1969).Plasmaflowaroundthemagnetosphere.ReviewsofGeophysics,7(1–2),11–50.https://doi.org/10.1029/
rg007i001p00011
Spreiter,J.R.,Summers,A.L.,&Alksne,A.Y.(1966).Hydromagneticflowaroundthemagnetosphere.PlanetaryandSpaceScience,14(3),
223–250.https://doi.org/10.1016/0032‐0633(66)90124‐3
Tsyganenko,N.A.,Semenov,V.S.,Erkaev,N.V.,&Gubaidulin,N.T.(2024a).MagnetosheathplasmaflowanditsresponsetoIMFand
geodipoletiltasobtainedfromthedata‐basedmodeling.JournalofGeophysicalResearch:SpacePhysics,129(11),e2024JA033233.https://
doi.org/10.1029/2024JA033233
Tsyganenko,N.A.(2025).Magnetosheathprotondensityandtemperatureasderivedfromdata‐constrainedmodeling[DatasetsandSoftware].
https://doi.org/10.5281/zenodo.17330908
Tsyganenko,N.A.,&Andreeva,V.A.(2014).Onthe“bowl‐shaped”deformationofplanetaryequatorialcurrentsheets.GeophysicalResearch
Letters,41(4),1079–1084.https://doi.org/10.1002/2014GL059295
Tsyganenko,N.A.,&Russell,C.T.(1999).Magneticsignaturesofthedistantpolarcusps:Observationsbypolarandquantitativemodeling.
JournalofGeophysicalResearch,104(A11),24939–24955.https://doi.org/10.1029/1999ja900279
Tsyganenko,N.A.,Semenov,V.S.,&Erkaev,N.V.(2023).Data‐basedmodelingofthemagnetosheathmagneticfield.JournalofGeophysical
Research:SpacePhysics,128(11),e2023JA031665.https://doi.org/10.1029/2023JA031665
Tsyganenko,N.A.,Semenov,V.S.,Erkaev,N.V.,&Gubaidulin,N.T.(2024b).Magneticfieldsandelectriccurrentsaroundthedayside
magnetopauseasinferredfromdata‐constrainedmodeling.Front.Astron.SpaceSci.,11,1425165.https://doi.org/10.3389/fspas.2024.
1425165
Tsyganenko,N.A.,Singer,H.J.,&Kasper,J.C.(2003).Storm‐timedistortionoftheinnermagnetosphere:Howseverecanitget?Journalof
GeophysicalResearch,108(A5),1209.https://doi.org/10.1029/2002JA009808
Vassiliadis,D.(2007).Forecastingspaceweather.InSpaceweather—Physicsandeffects.SpringerPraxisBooks.Springer.https://doi.org/10.
1007/978‐3‐540‐34578‐7_14
Wang,Y.L.,Raeder,J.,&Russell,C.T.(2004).Plasmadepletionlayer:Magnetosheathflowstructureandforces.AnnalsofGeophysics,22(3),
1001–1017.https://doi.org/10.5194/angeo‐22‐1001‐2004
Zhang,H.,Fu,S.,Pu,Z.,Lu,J.,Zhong,J.,Zhu,C.,etal.(2019).Statisticsonthemagnetosheathpropertiesrelatedtomagnetopausemagnetic
reconnection.TheAstrophysicalJournal,880(2),122.https://doi.org/10.3847/1538‐4357/ab290e
Zwan,B.J.,&Wolf,R.A.(1976).Depletionofsolarwindplasmanearaplanetaryboundary.JournalofGeophysicalResearch,81(10),1636–
1648.https://doi.org/10.1029/ja081i010p01636
TSYGANENKOETAL. 17of17
21699402,
2025,
12,
Downloaded
from
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JA034343
by
Sang-Yun
Lee
- Nasa
Goddard
, Wiley
Online
Library
on
[30/10/2026].
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