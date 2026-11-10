"""Prepare once-only six-record ledger credit, preserving every earlier value through a deep inverse."""
import ast,re
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

INTRO="""Hodram SC1B47/B48 are complete in registered experimental cumulative V8362:6records,3revisions and3individually justified retentions credited once. Totals7205completed/7208source-prose-and-drafts/4474integrated revisions/2731retentions. SC0368,SC1125,SC24915,SC3197,COMMON1600complete1603source-prose;route subset5605 isnot a full-goal denominator. All642manifest batches/114accepted layers/18release checks/110regressions,whole tested-reference equality,exact clean-input patch andown registered Hodramstartup pass. MainV4701/canonicalbaseline unchanged;preserve every ROM,translation,draft,executed producer,proof andfailure. No separate requestedtestpackage,promotion,pruning,commit orpush. Fullobjective active."""
DETAILS="""Whole clean Japanese outcomes andindividual first glosses precede priorEnglish. Remove invented unfairness,restore Lil's prospective best-in-the-world insistence,andkeep the addressee's instruction towait inAmsterdam. Retain the rueful concession,qualified Lil Argot/Ullr's Bow discovery andplayful chuckle/taunt withone real FI;source musicalnote expresses playful intent without inventing singing,romance orrank. Scoped Lil Argot identity is retained;FE isnot actor254 orpersonalname. No present worldsupremacy,territorialconquest,player award orpromised handover isadded.

Six complete automatic paragraphs preserve usable216px progressive/FE widths,original FE228x48/288stride/6x12/16pitch geometry,allfirst/internal/finalglyphs,completeconsumption,bounds andsinglepages. Zero warnings/waivers andsix source line-count infos remain. Full15commands/six preambles/seven opaque effects/oneFE/oneFI/two fourbyte ends andseparate tails survive bothclean source/fullparentarchive/wholeROMinverses. All323otherSC1blocks/allotherfiles/components/names/fonts/123264payload remainexact;325loads-cache/650modes/326actions andcaller census pass.

Four complete initialized source/revised fixtures40004frames cover12pages/100body-name orFE-absentheader holds,alloriginalcommands/returns andFE-to-Lil transition. TwofocusedFE runs8002frames bindoriginalpaint CPU/WRAM/TCM objects,temporary stackcontext,persistentview/palette andbankDVRAM/everyRGBinkpixel. B47 returns4495both;B48source4495/English4494 returns[0,0]. B47later93of93RGBpairs andfinalPRNGmatch. B48later80of93RGBpairs match;13differ(Aprompt/menu highlights/lower sailingclouds),andfinalPRNG3450714279 versus3110383956 differs. Alloriginalscript-boundaryPRNGpairs match;fivecheckednativecomponents/actors/captain1match. Rawcalendar remainsuninterpreted. This isdisclosed opening-fixture coverage,not naturaloptionalactivation,originaleventlocation/outereligibility/earnedprogress/everyframecausality/future-random-outcome/broadsimulation/fullroute/hardwareproof.

Frozenpolicy6positives/357changed-inputrejections andindependent native/actual/FE/control/comparison checks pass. Atomicone-whole-objectpositive preservesoriginalinput untilcommit. Fiftysemanticprecommitrejections makezerocommits withrelease dependencydigestsbypassed. Preserve stoppedreaders/harnesses;onlyCPUindex/JSONrepresentation/expectederrorwording werecorrected. Builderguard successors retainall417frozenentries and481otheroldproductiondependencies;exactsingleownedstage removalmustrecoverwholeoldbuilder. Eightalteredbuildercases reject. Prior50semanticcases bind byexactsevenmodule sourceequivalence andarenot claimed asrerun;currentproductionv2 hasfresh fullpositive. Newownregistered4001frameordinaryHodramstartup/sixcompletePNGpairs/wholeactors/name12/Blades8/runtimefontCOMMONdirectoryand123264payload pass withoutreplayingoptional scenes.

Allfour stories,earliertranslations,sharedtowns/shops/randomscenes,Help/remainingprose,all207names/roles/aliases andretrospectiveprematurewraps remainopen. Keepallpriorfamilies/leads andGerhard/Rafael/Hodram timing/RNG/component/calendar/RGB/fixture-entry limits. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stayseparate."""
NEXT="""Continue from verifiedV8368/currentregisteredV8362. These6Hodramoutcomes areintegrated/creditedonce;reusecompleted source/context/native/stored/actual/policy/atomic/release/startup proofs withoutunchangedreplays. UseownV8362captain1 input8365;otherroutecontexts needproperrebind/recapture,no historicalRAMoverlay orcaptain2 borrowing.

Continue completeclean SC1B49 from8357/first14speech+twochoiceglosses8358/itemidentity8360a. CurrentEnglishdialogue remainsunread. Established item84isHeavenlyWristband/item148Ullr'sBow;completeclean/currentnativepointers/NULnames/20unownedmetadata fieldsbound. Preserve Lil'sexcitedbargaining,regionalproof/hearsayNewWorldlocation/conditionaltrade,Hodram'ssilence andqualifiednegateddenial,andoutgoingwristband FEnotice. Keeprepeatedenthusiasticopeningsdistinct. Bindall14source/current/effective refs/twochoices,36commands/fullpreambles/relatives/query/itemdisplay-hide/opaqueeffects/fullend/tails;reviewwholeexchangepaths beforeindividualnatural-dialogue-v2 revisions/retentions. Originalevent49requires48;outereligibility/location/activation/fullchronology unproven. These14firstglosses addzerocreditedcounts. Nativechoice/control/FE/display/representativeactualrisk tests andregisteredintegration remainpending. Exhaustivenaturalplaythroughs/individualconditionalvisits arenotrequired.

Preserve allprior scopeleads:12contraction/questiontags,unscanned beyond558plans,weak-before-row/page-before-readability,COMMON750-752/preLF6435,item/counterpart/nameconsistency/all207labels/customnames;normalendcarry/B35R65/B48R129nineteenthcells/correctedoldB47receipt/B48/B50labels;allGerhard/Rafael/Hodram timing/RNG/component/calendar/RGB/fixture-entrylimits. Maintainbroadpractical town/randomcapture andhonest offline/gameplay scope. Keepfullgoalactive,main4701/canonicalbaseline unchanged andeveryartifact;no separatepackage/promotion/pruning/commit/push. Graphics/latertechnicalaudit separate."""

if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_completion_tools_v8367');assert not root.exists();source=Path('scripts/complete_Hodram_three_blocks_v8305.py').read_text('utf8');tree=ast.parse(source)
    start=source.index('ROOT=');end=source.index('def restore');constants='''ROOT=Path('work/analysis/Hodram_outcomes_completion_v8367')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8368')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8360/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
RELEASE=Path('work/analysis/Hodram_outcomes_release_v8363/registered_release_verification.json')
START=Path('work/analysis/Hodram_outcomes_registered_binding_v8365/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_outcomes_registered_startup_view_v8366/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8359e/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b/actual_changing_semantic_precommit_rejections.json')
REG=Path('work/analysis/Hodram_outcomes_registration_v8361/registration_receipt.json')
FINAL=Path('translations/hodram_outcomes_contextual_final_review_v1.json')
KEY='Hodram_SC1B47_B48_completion_v8367'
FAMILY='Hodram_SC1B47_B48_treasure_outcomes_v8367'
SCOPE='unfinished_editorial_scope_v8367'
NEXT_KEY='Hodram_SC1B49_fourteen_clean_glosses_two_choices_items_pending_controls_current_andrelease_v8367'
BEFORE=(7199,7202,7202,4471,2728)
AFTER=(7205,7208,7208,4474,2731)
NEXT_SOURCE={'49':'work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json'}
NEXT_GLOSS='work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json'
NEXT_ARTIFACT='work/analysis/Hodram_B49_item_identity_v8360a/clean_trade_item84_Heavenly_Wristband_item148_Ullr_Bow_exact_native_name_fields.json'
'''+ 'INTRO='+repr(INTRO)+'\nDETAILS='+repr(DETAILS)+'\nNEXT='+repr(NEXT)+'\n\n'
    replacements={source[start:end]:constants,'scripts.Hodram_three_blocks_release_paths_v8290':'scripts.Hodram_outcomes_release_paths_v8347'}
    nums={28:6,16:3,12:3,56:12,262:100,579:357,71:50,641:642,7171:7199,7199:7205,7202:7208,4471:4474,2728:2731,5571:5599,5599:5605}
    def transform(text):
        # Match complete numeric tokens, never address fragments, arbitrary substrings or inserted values.
        text=re.sub(r'\b(?:'+ '|'.join(map(str,sorted(nums,reverse=True)))+r')\b',lambda m:str(nums[int(m.group())]),text)
        changes={
            'all-routes-unified-v8300':'all-routes-unified-v8362','V8305':'V8367','V8306':'V8368','V8300':'V8362','Hodram28':'Hodram6',
            '[137,45,46]':'[47,48]',"proofs()[f'actual_B{row[\"block\"]}']":"proofs()[f'actual{row[\"block\"]}']",
            'comparedwith V8259':'comparedwith V8300',
            "new[k]['/data/SC1.DK4']==91;put([k,'/data/SC1.DK4'],119)":"new[k]['/data/SC1.DK4']==119;put([k,'/data/SC1.DK4'],125)",
            'SC1=119':'SC1=125',
            'current_native_macro_English=body,current_native_macro_output_hex=raw[1:].hex()':"current_native_macro_English=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').decode('cp932'),current_native_macro_output_hex=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').hex()",
            'body/name holds':'body/name-orFE-absent-header holds',
            'all60commands28preambles8relatives2queries_4800layout0_4700_andcomplete_ends_preserved':'all15commands6preambles_zero_relatives_queries_one_FE_one_FI_andcomplete_ends_preserved',
            'all_three_clean_source_andfull_predecessor_inverses_exact':'both_clean_source_andfull_predecessor_inverses_exact',
            'original_five_infos_two_exact_warning_waivers_preserved':'six_original_infos_zero_warnings_orwaivers_preserved',
            '28complete-singlepages-six-scopednames-registered-release-pass':'six-complete-singlepages-originalFE-one-scopedLil-name-registered-release-pass',
            'row_infos5_two_exact_warning_waivers':'six_original_row_infos_zero_warnings_orwaivers',
            'exactly28':'exactly6','all28_records':'all6_records','28disjoint decisions/16revisions/12retentions':'6disjoint decisions/3revisions/3retentions',
            'next six clean source glosses prepared':'next14clean utterances/twochoices glossed',
            'new_uncredited_Hodram_source_positions=6':'new_uncredited_Hodram_source_positions=14','new_uncredited_source_positions=6':'new_uncredited_source_positions=14',
            'nextHodram6sourceglosses':'nextHodram14utterances/twochoices glossed',
        }
        for a,b in sorted(changes.items(),key=lambda p:len(p[0]),reverse=True):text=text.replace(a,b)
        return text
    for name in ['gates','stage']:
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name);old=ast.get_source_segment(source,node);new=transform(old)
        if name=='stage':
            a=new.index('    pending=dict(');b=new.index('    evidence=',a)
            new=new[:a]+'''    pending=dict(status='fourteen-clean-source-glosses-two-choice-labels-item84and148-identity-bound-current-dialogue-unconsulted-controls-native-prose-formatting-release-pending',source_packets=NEXT_SOURCE,first_gloss=NEXT_GLOSS,artifact_identity=NEXT_ARTIFACT,file_path='/data/SC1.DK4',blocks=[49],physical_source_positions=14,typed_choice_labels=2,original_commands=36,current_English_dialogue_bodies_unconsulted=True,established_artifact_names=['Heavenly Wristband',"Ullr's Bow"],source_notice_outgoing_wristband=True,no_new_name_asset_mechanics_ororiginal_activation_claim=True,source_native_controls_choice_predicates_relatives_items_FE_current_editorial_andrelease_pending=True,source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False)
'''+new[b:]
        replacements[old]=new
    main=source[source.index("if __name__=='__main__':"):];newmain=transform(main)
    marker="            verified['Hodram_source_native_checkpoint'].update("
    assert marker in newmain;newmain=newmain.replace(marker,"            verified['Hodram_outcomes_production_checkpoint']=dict(")
    replacements[main]=newmain
    d=derive('scripts/complete_Hodram_three_blocks_v8305.py','scripts/complete_Hodram_outcomes_v8367.py',replacements)
    root.mkdir(parents=True);save(root/'once_only_six_record_full_inverse_completion_derivation.json',dict(derivation=d,before=[7199,7202,7202,4471,2728],after=[7205,7208,7208,4474,2731],exact_source_current_final_andFI_expansion_references_required=True,new14sourceglosses_andtwochoices_uncredited=True,no_credit_until_registered_release_ownstartup_andview_gates=True,all_prior_scope_andhistory_preserved=True,full_goal_complete=False))
