"""Prepare once-only disjoint completion, preserving a deep inverse of every ledger change."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read

INTRO="Rafael B48 is complete in current registered experimental cumulative V8066:91 speeches,42 revisions and49 individually justified retentions credited once. Totals are7,082 completed/7,085 source-prose records anddrafts/4,411 integrated revisions/2,671 retentions;SC0 279 androute subset5,482. All637 manifest batches/114 accepted layers/18 release checks/110 regressions,whole-reference equality andexact clean-input patch reconstruction pass. MainV4701 remains unchanged. The full editorial goal is active."
DETAILS="""Whole clean Japanese,nine clean identities,full B128 sailing-errand callback andpreviously read B37 context preceded current English. All91 source/current/effective/logical/compiled/stored/actual/integrated references,42 revisions and49 individual justified retentions are in translations/rafael_B48_contextual_final_review_v1.json. Preserve Athens learning banter,Julio's errand,refused free passage,Hans's passion for natural history,Claudio's reversal,assistant Arcadius's introduction,Julio/Hans acquaintance,the seven regional treasures/ancient Seven Sages/maps,reported destiny andRafael's ambition,optional Hayreddin challenge,andthe uncertain recent southern African rumor. Preserve the four system panels:complete Hans Letzel joining text,not a navigator/Deck restriction,item information andX instruction. Do not invent kinship,rank,romance,concealed identity,biography orguaranteed treasure location. R38 stays unnamed secondperson;shared surnames do not prove relationships. R370 retains effective catalogue-selected wording andone original FI.

All91 native paragraphs/92 pages pass. Final compiled binding hasfour fresh R140 alignments/360 exact reused cases;stored proof has192 fresh parity-tail alignments for48records/172 reused for43. Source00 has28objects/27unique bodies;selectors00/04/05/06/07/08/0D/4B/71/FE andcomplete preambles remain. Global216px/four-row profile,body NUL guard andfonts areunchanged;private FI6/FA6/FO10 usesexact source/current measurements. Four FE consumers preserve216pxusable text inside228x48logical/228x64physical paper. R171 retains its source CP932ellipsis.163commands/28relative sites/five raw predicates/two completion queries/threeA000effects/allscene controls/fullend survive.140relocated native branch cases,25seeded value-carry ends,343loads/686parent modes andfreshshippedcaller census pass.500source-result compositions yield32paths. Complete clean/predecessor block andarchive inverses areexact;342otherblocks andeveryotherfile/component matchV8013.

Two disclosed original B44entry fixtures retain the complete163-command B48 exchange afterthe ten-command initialization;they run80,002ordinary-input coldboot frames.78speeches perlanguage/156occurrences/157complete page observations/486complete body holds areactual coverage,includingfourFEpanels andsix progressive headers.13conditional speeches andJanus/Cesare/Cristina headers remainnative-only;fullcatalogue UI/customnames/all207review staysopen.31final actual sheets weredirectly viewed,plusone preserved focus-caption predecessor. EnglishR347usesfive fuller rows/two pages;ordinaryA18400turns between18370/18430withinthe same command,thenR350appears. Page2startswithcomplete sealed at[6,0] andendswithshapes. SourceR129'squestionmark iscompletein the nineteenth12pxcell at[216,16];one source-only native228pxglyphspan matchesbothblack/CP932shadow masks. Thisdoesnotwiden English rules. Preserve bothR129andolderB35R65findingsforlatertechnicalre-audit. The fixtures do notprove naturalAthens activation,earned prerequisites,originalscene location,fullroute orhardware coverage.

All146selected initialization/exchange results andUIrequests match;all78upper-scene/portrait/header pairs match. Normal[0,0] returnsat22735Japanese/22973English,+238frames. Preserve129comparisonrows/34durationdifferences. The first RNGphase difference isR832sourceoffset,173versus177frames;R347duration241versus481advances58additionalgeneratorsteps,Englishphase4before/62after. Exitphase+63/final-393,seeds1328542105/448695880. All285laterRGBsamples differ;state/models/tasks/calendar match,persistentobjects/wholeactors differ. Rawcalendarsbothticks0/[0,0,0] areuninterpretedoriginalfields. Continuedinputsre-enterthefixtureat35462/35702andendduringthatlatervisit;distinguishitfromthecompletefirstexchange. No controller retiming,state/seed/resultforcing,every-call causal trace,future-state orfullsimulation equivalence isclaimed. Keepallrawdifferences andincidentalB127/Sailor/resourceprosewithoutneweditorialcredit.

Automatic wrapping keepsR140aren't you? togetherandavoidsfourshortR347rows merelytoendapageatasentenceboundary.37original row-countinfos andtwoexactweak-endingwarnings remain:R86line1the/Proof;R406line2of/Conquest. Eachhasanid/source/logicalEnglish/compiled/line/issue-bound reason;no diagnosticsare removed orglobalweakrule relaxed. Frozenpolicypasses91positives/1454actual-changingguardrejections. Whole-ROMatomicpositivecommitsonefileslistonlyafterallchecks;455independentrealproofcorruptionsrejectprecommitwithconfigurationdigestsbypassed. Trustedfrozencontractisreadonceandrevalidatedafterallnegativecases;semanticchecksandcommittrapsstayactive. Registrationreceiptaccuratelybinds455negatives/637batches/one91-objectmanifest;noinheritedstalediagnosticcounts.

Freshordinaryown-V8066Rafaelstartupruns4,001frames:sixwholeRGBpairs/captain0/wholeactorcontrols matchV8013;strict2b6/COMMON/directory/123264payloadguards passandthesheetisdirectlyviewed. Owncurrentinputiswork/analysis/current_V8066_Rafael_native_v8069/current_native_input.json. Reuse priorverifiedchecks byexactreferenceequality. Preserve all earlier ROMs,translations,drafts,failures,executedproducers andproofs. Graphics/all18plaques andlaterolder-recordtechnicalre-audit remainseparate. No separateunifiedpackage,promotion,pruning,commit orpush."""
NEXT="""Continue the full editorial goal from verifiedV8072/current registeredV8066. B48's91 speeches are complete andcredited once;reuse verified source/context/names/32paths/native/stored/representative-actual/policy/atomic/release/patch/startup checks without needless replay. Use own-current Rafael input work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json. Other-route contexts remain historical until rebound orrecaptured.

Select the next untouched complete clean exchange using exact EV/caller/conditional/prerequisite context before current English;block orderaloneisnotchronology. B128/B37contextandincidentalB127/Sailor/resourcecaptures arepreviouslyexposedleads,not newlyunreadsource. Preserve fullcoverageacrossallfourstorylines,earliertranslateddialogue,sharedshops/towns/random/Help/remainingprose,all207names/roles/aliases andretrospectiveprematurewrapping. Preserve allpriorunfinishedinventories,twelvecontraction/question-tagleads,unscannedrecords beyond558plans,inheritedweak-before-rowandpage-boundary-before-readabilityleads. Do not mechanicallyminimizerows orreversejustifiedphrasing.

KeepPasardistinctfromPashaandpreservehistoricalcounterpartqueueswithoutglobalreplacement. Retain allolderitem/counterpart/displayleads,Cristina/Christina,HansRetzel/Letzelconsistency,Trader/PortWorker/Guildmaster,Sailor151-159versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andallotherrecordedopenwork. Keepgraphics/all18plaques andlaterolder-recordtechnicalre-auditseparate,includingnormal-endvaluecarry,source-onlyB35R65/B48R129nineteenthcells,andallmeasuredtiming/highlight/RNG/component/calendar/RGB/fixture-reentrylimits. PreserveeveryROM,translation,draft,failure,executedproducerandproof. MainV4701unchanged;fullgoalactive,noseparateunifiedpackage,promotion,pruning,commit orpush."""

if __name__=='__main__':
    source=Path('scripts/complete_Rafael_B47_v8018.py').read_text(encoding='utf8')
    start=source.index('INTRO=');end=source.index('\ndef digest(',start)
    actual=read('work/analysis/Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json')
    changes={
        source[start:end]:'INTRO='+repr(INTRO)+'\nDETAILS='+repr(DETAILS)+'\nNEXT='+repr(NEXT)+'\n',
        'B47':'B48','R53':'R347','v8018':'v8071','v8019':'v8072','V8018':'V8071','V8019':'V8072',
        'Rafael_B47_release_paths_v8006':'Rafael_B48_release_paths_v8060',
        'editorial_handoff_verification_v8008':'editorial_handoff_verification_v8045',
        'Rafael_B47_release_v8014':'Rafael_B48_release_v8067',
        'Rafael_B47_context_binding_v8016':'Rafael_B48_context_binding_v8069',
        'Rafael_B47_startup_view_v8017':'Rafael_B48_startup_view_v8070',
        'Rafael_B47_atomic_challenges_v8011':'Rafael_B48_atomic_challenges_v8064',
        'Rafael_B47_registration_v8012/registration_receipt_corrected.json':'Rafael_B48_registration_v8065/registration_receipt.json',
        'Rafael_B47_atomic_positive_v8010':'Rafael_B48_atomic_positive_v8063',
        'contextual_Mediterranean_advice':'contextual_Athens_naturalist_Proof_exchange',
        'BEFORE=(6976,6979,6979,4361,2615)':'BEFORE=(6991,6994,6994,4369,2622)',
        'AFTER=(6991,6994,6994,4369,2622)':'AFTER=(7082,7085,7085,4411,2671)',
        "UNVISITED=['DK4_MES_B47_R0017','DK4_MES_B47_R0063','DK4_MES_B47_R0092','DK4_MES_B47_R0122']":'UNVISITED='+repr(actual['native_only_unvisited_speech_IDs']),
        'all-routes-unified-v8013':'all-routes-unified-v8066','==636':'==637','manifest_batches=636':'manifest_batches=637',
        "atomic['positive_records']==15":"atomic['positive_records']==91",'==202':'==455',
        'all15_five_gates':'all91_five_gates',"len(doc['records'])==15":"len(doc['records'])==91",
        'len(oldkeys)==6976 and len(keys)==15':'len(oldkeys)==6991 and len(keys)==91',
        '[47]':'[48]','block=47':'block=48','blocks=[47]':'blocks=[48]',
        "{'revision':8,'retention':7}":"{'revision':42,'retention':49}",
        'revised=8,retained=7':'revised=42,retained=49',
        'source_prose_and_completion_credit_added_once=15':'source_prose_and_completion_credit_added_once=91',
        'actual_unique_speeches_each_language=11,actual_speech_occurrences=22,actual_total_complete_page_occurrences=23':'actual_unique_speeches_each_language=78,actual_speech_occurrences=156,actual_total_complete_page_occurrences=157',
        'actual_unique_pages_both_languages=23':'actual_unique_pages_both_languages=157',
        'complete_body_andheader_holds=88':'complete_body_andheader_holds=486',
        'native_all15_paragraphs16_pages_andR53_only_two_pages':'native_all91_paragraphs92_pages_fourFE_andR347_only_two_pages',
        'all48_commands24_relatives15_preambles_six_predicates_zero_macros_andcomplete_ends_preserved':'all163_commands28_relatives91_preambles_five_predicates_two_queries_oneFI_fourFE_andcomplete_ends_preserved',
        'three_actual_names_Janus_native_only_full207_broader_consumers_open':'six_actual_names_three_native_only_full207_broader_consumers_open',
        'policy15_positives302_negatives_atomic15_positive202_negatives':'policy91_positives1454_negatives_atomic91_positive455_negatives',
        'original_QA_six_infos':'original_QA_37_infos',
        "new[key][file]==173;put([key,file],188)":"new[key][file]==188;put([key,file],279)",
        'revised_count=8,retained_count=7,fresh_revisions=8,fresh_retentions=7':'revised_count=42,retained_count=49,fresh_revisions=42,fresh_retentions=49',
        'fresh_pass_records_explicitly_reread=6991,fresh_pass_records_integrated=6991':'fresh_pass_records_explicitly_reread=7082,fresh_pass_records_integrated=7082',
        'records=15,final_review=str(FINAL),new_revisions=8,justified_retentions=7,new_completed_records=15':'records=91,final_review=str(FINAL),new_revisions=42,justified_retentions=49,new_completed_records=91',
        'actual_initialized_fixture_speeches=11':'actual_initialized_fixture_speeches=78',
        'actual_pages=12,offline_only_objects=4':'actual_pages=79,offline_only_objects=13',
        '==5376':'==5391','reviewed_route_records=5391,completed_route_records=5391':'reviewed_route_records=5482,completed_route_records=5482',
        'completion_credit_added=15':'completion_credit_added=91','actual_objects=11':'actual_objects=78',
        '15-source-prose-native-stored-reference':'91-source-prose-native-stored-reference',
        'native_pages16_R53_only_two_pages=True,row_infos6':'native_pages92_R347_only_two_pages_fourFE=True,row_infos37',
        'completed_objects=15,revisions=8,retentions=7':'completed_objects=91,revisions=42,retentions=49',
        'new_source_prose_reviews=15,new_completed_records=15':'new_source_prose_reviews=91,new_completed_records=91',
        'Rafael B47 Mediterranean advice integrated in cumulative V8013':'Rafael B48 Athens naturalist exchange integrated in cumulative V8066',
        'V8013 current':'V8066 current','V8013':'V8066',
        'all15_records_integrated_once':'all91_records_integrated_once',
        '15 disjoint Rafael decisions/8 revisions/7 retentions':'91 disjoint Rafael decisions/42 revisions/49 retentions',
        'exactly15_disjoint_new_records':'exactly91_disjoint_new_records','exactly15_decisions_credited_once':'exactly91_decisions_credited_once',
        '6991 completed/4369 revisions/2622 retentions':'7082 completed/4411 revisions/2671 retentions',
        'len(completed)==6991':'len(completed)==7082',
        'records_editorially_completed=6991,records_with_source_and_prose_pass=6994,records_with_source_prose_drafts=6994':'records_editorially_completed=7082,records_with_source_and_prose_pass=7085,records_with_source_prose_drafts=7085',
        'records_revised_and_integrated=4369,retained_wordings_editorially_completed=2622':'records_revised_and_integrated=4411,retained_wordings_editorially_completed=2671',
        'completed=6991,source_prose=6994,revised=4369,retained=2622,SC0=188':'completed=7082,source_prose=7085,revised=4411,retained=2671,SC0=279',
        'reviewed_routes=5391,completed_routes=5391':'reviewed_routes=5482,completed_routes=5482',
        'actual_speech_occurrences=22,actual_complete_body_andheader_holds=88':'actual_speech_occurrences=156,actual_complete_body_andheader_holds=486',
        '6991completed/6994source-prose/4369revisions/2622retentions;15credited once':'7082completed/7085source-prose/4411revisions/2671retentions;91credited once',
    }
    absent=[k for k in changes if k not in source];assert not absent,absent
    print(derive('scripts/complete_Rafael_B47_v8018.py','scripts/complete_Rafael_B48_v8071.py',changes))
