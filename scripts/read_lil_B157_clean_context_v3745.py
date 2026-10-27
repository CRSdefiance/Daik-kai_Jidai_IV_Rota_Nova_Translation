"""Record all75 fresh clean-source glosses before comparing any older B157 English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B157_clean_context_v3745')
SOURCE=Path('work/analysis/lil_B157_B160_source_v3744/all157_clean_current_complete_context.json')
TRANSCRIPT=Path('work/analysis/lil_B152_B160_next_source_v3614/SC2_B157_complete_clean_exchange.txt')
CONTEXT='''Carlo orders his usual quantity ofcinnamon fromthe Trader addressed inJapanese asAdil. They know one another:Carlo challenges theprice,knows his purchasing cost,cites thisyear's yield andlocal demand,andthreatens tobuy elsewhere. The Trader yields. Carlo thennotices his fever/pallor;the Trader first mistakes this foranother bargaining complaint,thenfeels chills. Carlo postpones his ownpurchase andurges him toclose/rest;the Trader apologizes tothe other waiting customers. Lil asks howCarlo knew he wasill. Carlo cites his poorcolor. Optional Fernando boasts thatCarlo's insight isasgood ashis. Lil's uncertain inner reply isoutside thatoptional branch,so retain its ability torefer tothe pallor explanation without Fernando present. Carlo says he issensitive topeople's health andoffers tomake up thedelay bymeeting Lil atthe trading post tomorrow morning. Lil eagerly treats itasrepaying afavor,not a monetary debt.
The nextday,the woman whose native catalogue role isInnkeeper thanks Carlo andsays Adil isathome resting asa precaution. She complains thathe doesnot listen toher;do notinvent an explicit marriage label forthis woman ortranslate familiar address asCarlo's wife. Carlo's later ownwife/daughter are explicit andmust remain distinct. The woman calls Carlo alifesaver andoffers thanks;this isher grateful characterization,not independent proof ofa fatal illness ormedical cure. Carlo redirects thethanks tothe travelers whowaited overnight. She apologizes fortheir delay andoffers an unnamed modest gift. Preserve theoffer without inventing money,itemidentity or an earned inventory effect. Carlo thanks her asan older woman/proprietress andoffers thetravelers priority because they areinahurry. Adil thenappears,claiming he isfit andcannot stay inbed ona fine dayforbusiness. The woman scolds him;Carlo isrelieved butstillurges moderation andsays he willreturn anotherday. He entrusts their trade tothe shopkeeper andadvises thetravelers totreasure family andhealth.
Lil pauses,thenasks Carlo togo tosea withher. Her familiar oji-san address establishes no uncle relationship. She feels they wouldgetalong andhasanintuition. Carlo protests thathe isamerchant,not asailor;Lil isdelighted thathe isaprofessional,exempts himfromoperating theship andpoints out thatshe isamerchant too. She asks whether he hasareason tostay,withMalacca notbeing hishometown asarhetorical question,not evidence ofan invented birthplace oraccent. Carlo reveals his family died ayearago. His nexttwo sourceFE panels arehis first-person recollection,not omniscient narration or a newunnamed speaker. Firsthis daughter caught theillness goingaround;he wasabsorbed inwork anddidnot adequately care forher. Treatment wasdelayed,his wife caught ittoo,andhelost both. Preserve his personal regret without naming a pathogen,age,doctor,medical specialty orjudgment beyond hissource words. Thework hebought attheneglect ofhis family felt empty. Since thenotherpeople's health concerns himmore thanwork. Lil understands whyhe noticed Adil's illness andasks whether heconsidered returning home. Carlo namesVenice;itcontains toomany happy memories forhimtolivethere alone. Do noterase thelove inthose memories orconvert his grief intohatred ofVenice.
Lil renews theinvitation tothegroup andexplicitly promises thatthey willbecome his family. This source-supported chosen-family offer doesnot invent biological parenthood,adoption paperwork,romance or a shipdoctor position. Optional Emilio encourages shared meals;gohan meansfood/meals,not necessarily rice. Camille enthusiastically praises FI's compassionate remark. Lil deflects withher habitual claim thatshe always saysgood things,andseeks Carlo's agreement. Carlo thanks themandaccepts;Lil celebrates. Camille says FI hasrisen somewhat inhis estimation. Keep theheartfelt gratitude andhis unusual respect alongside Lil's comic self-regard. Carlo gives his fullname;the bound native approved catalogue spelling isCarlo Sinat. SourceFI occurs twice;itmust stay a runtime macro rather thanan authored Lil string. Whole-source condition/reward/recruitment/FE/presentation ownership andactual event timing/eligibility remain separate obligations.'''
MEANINGS={
5:'Carlo asks forthe usual quantity ofcinnamon. Preserve the established repeat-customer transaction,not a newquantity orprice.',
9:'Lil privately wonders whether there isa customer ahead ofthem. This isher tentative observation,not narrated certainty.',
13:'The Trader agrees andquotes theamount due witha deictic thismuch. No number orcurrency isspoken.',
17:'Carlo notices thattheprice hasgone up. This challenges thequoted charge rather thanannouncing an external market fact.',
21:'The Trader denies an increase andclaims itisabout theusual price. Preserve his defensive reply tothechallenge.',
24:'Carlo laughs,addresses Adil byname andcalls theclaim nonsense:doeshe think Carlo doesnot know his purchasing cost? Preserve familiar bargaining without inventing fraud orkinship.',
27:'The Trader protests witha familiar Hey,comeon response. Keep itshort anddefensive.',
31:'Carlo cites thisyear\'s yield andlocal demand asreasons theTrader coulddo alittle better onprice. Preserve his argument andqualified demand,not a guaranteed profit theorem.',
35:'Carlo says he cantryanother seller;no lawrequires himtobuy fromthesame shop everytime. The mock-legal line isbargaining humor.',
39:'The Trader falters andagrees,admitting he cannotget thebetter ofCarlo. Preserve theconcession andfamiliar exasperation.',
43:'Carlo notices something andasks Adil whether he hasafever. Theexchange nowturns frombargaining toconcern.',
46:'Adil addresses Carlo andasks whether he isstill finding fault withhis business. He mistakes thehealth concern forcontinued haggling.',
49:'Carlo denies that,intells himhe hasafever andurges himtogotobed early today. Preserve Carlo\'s direct concern,not an invented physician title.',
52:'Adil initially dismisses it,thennotices he really doesfeel chills. The change ofmind completes thehealth exchange.',
55:'Carlo says Seethat;he willmake his purchase tomorrow,sothe shopshould close today. Preserve both postponement andrest.',
58:'Adil agrees tofollow Carlo\'s advice,thenapologizes tothe other customer(s) andasks themtoreturn tomorrow too.',
64:'Carlo apologizes tothe travelers andrecognizes they cametodobusiness too. The apology concerns thedelay he caused.',
67:'Lil asks theolder manhowhe knew. Her familiar address isnot Uncle andthequestion\'s missing object isclarified inthenextturn.',
71:'Carlo asks whatshe means. This brief puzzled reply setsup herclarification.',
75:'Lil clarifies thatshe meanshowhe knew themanwasill. Preserve theconnection toher preceding question.',
79:'Carlo says itwasbecause themanlooked pale/unwell. This ishis observation,not an invented medical test.',
91:'Optional Fernando boasts thatCarlo seemsabout asobservant ashe is. Preserve thecomic self-comparison without inventing medical credentials.',
97:'Lil isquiet andprivately uncertain whether thatwasreally so. This rowalso occurswithout Fernando,so donot makeitsreferent depend solely onhis optional boast.',
101:'Carlo says mostpeople wouldnot notice;he isparticularly sensitive topeople\'s health. Preserve hisself-description andthe latergrief explanation.',
105:'Lil responds witha drawn-out interested Oh/really. Keep hercuriosity beforehis invitation.',
109:'Carlo asks hertocome withhim tothetrading post tomorrow morning;he thinks he canmake up fortoday\'s inconvenience. Preserve thetime andqualified offer.',
112:'Lil checks thathe isrepaying thefavor andeagerly agrees tocome. This isnot an explicit loan orcash repayment.',
115:'The woman thanks Carlo foryesterday. Preserve herfamiliar gratitude without inventing a specific kinship.',
119:'Carlo asks where Adil is/howhe is. Thefollowing response concernshis absence/resting,not death.',
123:'The woman says he isathome inbed today,taking no chances. Preserve restasa precaution.',
126:'Carlo acknowledges thisandhopes he recovers soon. Keep thesimple goodwish.',
130:'The woman says he neverlistens toher;without Carlo\'s intervention yesterday... Preserve herunfinished complaint without asserting an unspoken marriage label.',
134:'She interrupts herownlongtalk,callshim alifesaver andsays she wantedtothank him. Thelifesaver claim isher grateful speech.',
138:'Carlo thanks herandisglad,butasks hertothank these travelers instead:they waited overnight todo business. Preserve whomhe redirects thereward toandwhy.',
142:'The woman apologizes fortheir being heldup andoffers something modest,asking whetherthey willaccept it. No itemidentity oramount isspoken.',
148:'Carlo thanks thewoman witha familiar respectful address,thenlets thetravelers buyfirst because they areinahurry. This creates neither a wife relationship nor an unspoken noble title.',
152:'Adil greets Carlo andapologizes foryesterday. His sudden appearance reverses thepreceding report thathe wasresting athome.',
155:'The woman exclaims atAdil inrecognition/reproach. Preserve thesurprised admonition,not an invented name orrelationship.',
159:'Carlo calls Adil byname andsays he shouldbe inbed. This continues hisconcern.',
162:'Adil insists he isfit ascanbe andcannot stay lazily inbed ona daylike thisforbusiness. Preserve his ownclaim,not proof thathe iscured.',
166:'The woman exasperatedly calls himhopeless/incorrigible. Keep thefamiliar scolding.',
170:'Carlo laughs andisreassured byhis energy,butwarns himnottooverdo ittoday. Preserve relief plusrestraint.',
174:'Carlo willcome back tomorrow/anotherday andasks Adil tohandle thesetravelers\' business. Preserve thehand-off oftrade priority.',
177:'Carlo advises thetravelers tocherish family andhealth,thenbids themfarewell. This setsthe theme ofhislater confession.',
180:'Lil pauses silently afterCarlo\'s parting advice. Retain wordless acting beforeher impulse tocall himback.',
185:'Lil calls out totheolder man. Preserve herattention-getting familiar address without inventing uncle kinship.',
189:'Carlo turns/responds witha brief questioning Hm? Keep thereply aspart oftheir renewed conversation.',
193:'Lil invites himtogo tosea withher. Preserve herdirect enthusiastic first-person invitation.',
197:'Carlo reacts insurprise,asking whatshe issuddenly talking about. He hasnot yetaccepted.',
201:'Lil feels they wouldgetalong andhasasudden intuition aboutit. Preserve personal instinct,not prophecy or an invented prior friendship.',
204:'Carlo says he isnot asailor,just amerchant. Do notinvent a doctor,shipcaptain ormilitary role.',
207:'Lil exclaims thatshe knewitandsurely thought he wasaprofessional. This playful response embraces hismerchant identity rather thanhis objection.',
210:'Lil says he neednot operate theship;she isamerchant too. Preserve herreply tothe sailor/merchant distinction.',
213:'Carlo falls silent. Preserve his hesitation beforeLil asksabout attachments toMalacca.',
217:'Lil asks whether he hasareason nottoleave;Malacca isnot hishometown,is it? Preserve thequestion withoutinventing a birthplace oraccent clue.',
221:'Carlo says he hasno family now;they died ayearago. Thenexttwo panels identify hiswife anddaughter;do notinvent other relatives\' deaths.',
224:'Lil isquiet onhearing this. Preserve hersubdued reaction beforehis explanation.',
229:'Inafirst-person FE recollection,Carlo says hisdaughter firstcaught theillness goingaround. He wasabsorbed inwork thenanddidnot properly care forher. Preserve hispersonal regret without naming a pathogen orherage.',
232:'Inthenextfirst-person FE panel,he says treatment came toolate,hiswife caught ittoo,andhelost both. Preserve thedaughter-to-wife progression andtwo deaths,without inventing medical procedures.',
236:'Lil addresses himsoftly inresponse tohis loss. Oji-san doesnot establish kinship.',
240:'Carlo says thework heobtained atthecost ofneglecting hisfamily wasempty. Since thenpeople\'s health weighs onhimmore thanwork. Preserve regret andthecause ofhisattentiveness.',
243:'Lil realizes thatthisiswhyhe noticed theman\'s illness. Preserve herunderstanding oftheearlier incident.',
246:'Lil gently asks whether heeverthought ofreturning home. Keep herhesitation andquestion.',
249:'Carlo namesVenice. There aretoomany happy memories there;he cannot livetherealone. Preserve thehappy memories madepainful byloss,not hatred ordanger.',
253:'Lil pauses,absorbing hisanswer. Preserve thesilence beforeher renewed invitation.',
257:'Lil asks himtocome withthem afterall. Theinvitation nowexplicitly concernsthegroup.',
260:'Carlo responds witha questioning pause. Keep thiswordless request forexplanation.',
264:'Lil says being alone isnofun andpromises thatfromnowon they willbe hisfamily. Preserve theexplicit chosen-family promise without inventing biological parenthood orromance.',
276:'Optional Emilio agrees:meals tastebetter wheneveryone eats together. Preserve hiswarm food-centered voice;gohan neednot meanrice.',
282:'Camille enthusiastically tells FI shehassaid something wonderful. Preserve thesincere praise andruntimeFI name.',
285:'Lil objects thatshe always saysgood thingsandseeks theolder man\'s agreement. Preserve hercomic self-regard amidthe genuine kindness.',
289:'Carlo thanks themandaccepts,asking fortheir kindness/help goingforward. Preserve hissoftened gratitude andspoken agreement,not an earned recruitment effect.',
292:'Lil celebrates withan exuberant Yes/Yay. Keep theshort successful-invitation reaction.',
296:'Camille tells FI hethinks alittle better ofher now. Preserve theunusual respect/softening andruntimeFI substitution.',
299:'Carlo introduces himself byhisfullname andoffers a cordial closing. Use thebound approved native spelling Carlo Sinat,not a newly guessed surname.'
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);rows=deepcopy([r for r in source['records'] if r['block']==157]);assert len(rows)==len(MEANINGS)==75 and {r['source_record_index'] for r in rows}==set(MEANINGS);assert sum(r['source_selector']==254 for r in rows)==2;macros={k:sum(bytes.fromhex(r['source_hex']).count(k.encode()) for r in rows) for k in ['FI','FA','FO']};assert macros=={'FI':2,'FA':0,'FO':0}
    for r in rows:r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,clean_source_complete_exchange_read_before_older_English=True,source_FЕ_remembers_Carlo_first_person_not_a_new_narrator=r['source_selector']==254)
    assert next(r for r in rows if r['source_record_index']==91)['ancestor_0100_offsets'] and not next(r for r in rows if r['source_record_index']==97)['ancestor_0100_offsets'];ROOT.mkdir(parents=True);save(ROOT/'all75_complete_B157_exchange_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_transcript=str(TRANSCRIPT),clean_transcript_sha256=sha(TRANSCRIPT.read_bytes()),whole_exchange_context=CONTEXT,records=rows,all75_clean_source_speeches_and_optional_Fernando_Emilio_branches_read=True,all75_glosses_before_older_English=True,source_first_person_FE_panels=2,source_macro_counts=macros,approved_native_name='Carlo Sinat',Adil_Japanese_address='アディール',Adil_Romanization_to_reconcile_with_approved_name_references_before_authoring=True,other_woman_native_catalogue_Innkeeper_doesnot_authorize_an_explicit_Adil_wife_label=True,source_explicit_Carlo_wife_daughter_loss_andchosen_family_offer_preserved=True,source_Lil97_outside_optional_Fernando91_guard_referent_kept_open=True,other82_B158_B160_objects_still_not_fully_read_or_gloss_approved=True,oldEnglish_comparison_localization_native_controls_FE_formatting_actual_and_release_pending=True,new_native_calls=0,new_emulator_runs=0,source_prose_orcompletion_credit_added=0,no_ROM_registry_ledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('All75 B157 clean speeches/glosses,including2 first-personFE panels,recorded beforeolder English;FI2. No credit.')
