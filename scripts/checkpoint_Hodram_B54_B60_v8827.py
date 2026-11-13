"""Additive verified handoff:82 five-gate decisions,14 captures;production/release pending."""
import json,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_checkpoint_v8827')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B54_B60_82_fivegate_reviewed_stored_actual_pending_production_registered_v8827'
SCOPE='unfinished_editorial_scope_v8827'
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v3.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v2.json')
FORMAT=Path('work/analysis/Hodram_B54_B60_format_v8826/formatting_approval.json')
REVIEW=Path('work/analysis/Hodram_B54_B60_actual_review_v8825/qualified_actual_review.json')
EVIDENCE=[str(DOC),str(NAMES),str(FORMAT),str(REVIEW),
 'work/analysis/Hodram_B54_B60_compiled_v8808/compiled_body_bindings.json',
 'work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json',
 'work/analysis/Hodram_B54_B60_independent_v8810/independent_reconstruction.json',
 'work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json',
 'work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json',
 'work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json',
 'work/analysis/Hodram_B54_B60_references_v8814/references.json',
 'work/analysis/Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
 'work/analysis/Hodram_B54_B60_models_v8817/native_models.json',
 'work/analysis/Hodram_B56_FE_binding_v8819b/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
 'work/analysis/Hodram_B54_B60_comparison_v8821/paired_selected_path_comparison.json',
 'work/analysis/Hodram_B60_focus_actual_v8823/B60/paired_actual_dialogue_headers_flow_returns.json',
 'work/analysis/Hodram_B60_focus_comparison_v8824/paired_selected_path_comparison.json',
]
TEXT="""V8827 continues from verified V8807/current registered experimental cumulative V8778. Hodram SC1 B54-B60 has82 individual five-gate natural-dialogue-v2 approvals:46 revisions/36 justified retentions. Latest manuscript translations/hodram_B54_B60_editorial_manuscript_v3.json and10scoped progressive-name reviews v2 preserve every approved word,source/current reference,compiled byte,individual finding andretention reason. Complete final stored references andformatting reasons are added. Standardv2 passes;original QAinfos remain,withzero errors,warnings orwaivers. These82 decisions are still unintegrated/uncredited. Counts remain7,237 completed/7,240 credited source-prose anddrafts/4,492 integrated revisions/2,745 retentions;SC0 368/SC1 157/SC2 4,915/SC3 197/COMMON1,600 completed. No registered build,promotion,separate userpackage,pruning,commitorpush. Preserve every ROM,translation,draft,producer,proof andfailure. Full objective remainsactive.

Reuse completed clean-first8791-8805 source/context/names/branch/macro/prose/logical/full-width plans and85native English pages. New compiled binding8808 preservesall82original manuscript values. Sparse reconstruction8809 andindependent152-command-atom reconstruction8810 agree exactly on allseven targetblocks andthewhole SC1archive. Source/current/target six-byte preambles,all152commands,24relative sites120nativecases,six queries,33nonprose controls,seven complete normalends andseparate source tails are bound. Blocks54-60 become128/116/224/240/2880/612/804storedbytes. All318otherblocks/every other file/component andcomplete clean/currentblock,archive andwhole in-memoryROM inverses pass. No original opaque effect is assigned invented semantics.

Stored8811 checks all82dispatches,original actors/voices,FE null actor andFI3/FA4/FO0 expansions. Forty compiler-owned parity spaces require160fresh alignment cases/43native pages;42byte-identical bodies/pages and168alignment cases are reused. All85stored visible planes equal the already viewed complete models,including every first/internal/final glyph,bounds,consumption andpagination;no blank oradditional page. Research reference8812 derivesonlysevenSC1blocks from completeV8778;all318otherblocks/every other file/component/wholeROMinverse pass. Reference and12whole-scene fixtures are pinned without removing any prior pin orROM. The reference is research-only,not a handoff,candidate ornewparent.

Fresh loader8813 runs325whole native loads/cache hits and326originalEV1actions because archive offsets moved. It runs14parent cases for the7changedpayloads andbinds636unchanged parent cases byexact318payloads/whole currentARM9 andpriorproof,650total. Headers,payload-plus8 entries,metadata,neighbors,first reads,SP/PC/ABI andoriginal instructions pass. References8814 binds all152complete source/current/final command maps,82final NULindices andseven unchangedEV1entries. The complete original caller census is reused only afterall decodedsection/overlay names,bases,lengths andpayload hashes match exactly. This is scoped external-reference proof,not arbitrary dynamic pointer,outer scheduler,eligibility,location orall-attainable-path proof.

Representative fixtures8815 retainall commands from B54/B56/B57/B58/B59/B60 after8original opening initializers34bytes. B55 remains offline. Twelve initial paired cold boots8816 total116,012frames;source Japanese bodies use current English names/UI,not all-Japanese UI. Complete masks/native flow audits8818/8820 prove63unique utterances/129page occurrences/580complete body-name orFE-absent-header holds. The English two-page B59R23/B59R26/B60R12 records each have complete captures ofeverypage. Both B58runs naturally select31utterances;18conditional utterances are unvisited/offline-only. Together with B55,19of82remain offline-only,withcomplete source/branch/default-macro/stored-native evidence andrepresentative same-consumer actualcoverage. No conditions,roster,flags,funds,RNG,results orper-language timing are forced. No natural optional-event activation,original location,earned progress,fullroute orhardware claim.

B56 FE live binding8819b proves2original paint snapshots and6same-run complete logical bitmap/palette/VRAM/RGB holds at4090/4150/4210. The actual typed228x48/288stride/6x12/16physical-pitch context,current vtables andabsentnameplate agree withoffline models;progressive->FE->progressive returns4493inbothlanguages. Preserve stopped8819:its assumed4030complete hold was not in the actual mask-audited hold set;8819b binds onlythe3proven holds perlanguage. No scene recapture orweakened geometry/palette/RGB checks. B59's original4810/4700/4800/4700 sequence is observed at source offsets44/104/154/458,andall7corresponding upper scene/portrait/resource views are RGB-equal atmatching dialogue stages. Existing WeparHalberd/LowerStoneTablet labels are currentUI observations,not new source-item identity ornew item-editorial approval.

All20main dialogue sheets and6long transition sheets are directly viewed,includingall continuationpages andthecomplete Sera language-learning exchange. Main returnsJP/English:54 4733/4736;56 4493/4493;57 5696/5696;58 11457/11455;59 5696/6176;60 6176/6415. B58 returns[0,1];others[0,0]. Normalend's persistent resultword remains distinct from interpreterr3. Selected command signatures/results andUIrequests match;all measured duration/decoded-length/boundaryRNG/following-command differences are retained. LaterRGB differences:54 3/22;56 0/43;57 0/56;58 3/77;59 65/65;60 61/61. Long finalfive components/wholeactors matchfor54/56/57/58/59;B60 differs in persistent actor data/wholeactors. B59 finalseeds3723713416/827389248;B60 longseeds654172275/654172275. Do not call these long runs fully equivalent orsilently attribute the differences to one cause.

Focused B60pair8822 adds14,002frames,endingat7,001withthe same ordinary inputprefix throughA6400,no laterA6640/6880suffix. Audit8823 confirms complete dialogue andsame6176/6415returns. Beforethe long run's nextA6640,41Japanese and40English callbacks matchtheir respective longrun frame/kind/fullWRAM/DTCM/ITCM/CPU hashes exactly. Focus comparison8824 shows all5sampled components,wholeactors,captain1 andrawcalendar equal at7001. Its seeds3736791874/459828772 andall11laterRGBpairs still differ. This supports a bounded post-exchange interval,not full future equivalence orcausal diagnosis;the long B60actor divergence remains. Requested6176/6415native exports saveCPU/TCM/VRAM butnot mainWRAM,so no immediate-return actor snapshot claim is made. The focused4dialogue sheets are byte-identical toalready viewedlong sheets;its transition sheet is directly viewed. Total14terminal/reaped runs130,014frames/676holds. Qualified review8825 records27viewedmain/transition sheets andall scope limits. Reuse every completed capture/model/audit;no unconditional replay.

Formatting8826 approvesall82individual formats and10scoped progressive labels understandardnatural-dialogue-v2,withno word/byte/source/control change. Eight actor headers are actual:{1,23,24,36,84,114,119,141};20and113remain offline here. Fullnames/all207roles-aliases/customnames/widercontexts remainopen. In particular Geronimo デ Espinosa's sharedデmiddle field alsoaffectsAlonso;allaffectedfull-nativeconsumers,ownership,deployment andregistered guards need qualification beforeanyasset change. This progressive-format approval doesnot close that full-name lead. Approved Rafael/Hodram/Joakim/Maria/Camille andcurrent mixed-width storage remain.

Next:freeze source-qualified prose/compiler/native/reference/control/loaders/actual/comparison evidence;enforce actual production readers andmeaningful changed-input rejections;verifywhole-NDS atomic application/shared hook;integrate throughregistered cumulative builder;exactclean-input patch reconstruction/ownstartup;thencredit82sourcepositions exactly once. Keep full scope intact. CurrentV8778's647manifestbatches/114acceptedlayers/18releasechecks/110regressions/exactpatch/ownstartup remainunchanged;reuse all previous B31/B53/B52 checks. MainV4701/canonicalbaseline unchanged. No new playable candidate untilregisteredworkflow passes.

Allfourstorylines,earliertranslatedstorydialogue,sharedtown-shop,random,Help/restprose,all207names-roles-aliases-customnames andretrospectiveprematurebreaks remainactive. Every prior unfinished-scope key/value/lead anddocument byte ispreserved,including contractions/questiontags/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wider104-105-113-147/JanusPasar-versusPasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159versusRetainer/oldernormalends/nineteenthcells/B47-B48-B50metadata. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stay separate. Roughly20,000remaining isonlyaplanningestimate,notanauditeddenominator. Full goal isnotcomplete.
"""

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='stage':
        assert not ROOT.exists();old=read(LEDGER);doc,names,approval,review=map(read,[DOC,NAMES,FORMAT,REVIEW])
        assert old['records_editorially_completed']==7237 and old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old
        assert approval['all82_five_gates_true'] and approval['standard_natural_dialogue_v2_validation_pass'] and len(names['records'])==10
        assert (review['total_runs'],review['total_frames'],review['total_holds'])==(14,130014,676)
        ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
        pending=dict(status='82-fivegate-reviewed-production-atomic-registered-cleanpatch-startup-andonceonly-credit-pending',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),formatting=str(FORMAT),formatting_sha256=sha(FORMAT.read_bytes()),
            actual_review=str(REVIEW),actual_review_sha256=sha(REVIEW.read_bytes()),records=[{k:r[k] for k in ['id','file_path','block','source_record_index','source_reference','source_hex','current_reference','current_hex','final_reference','final_hex','english','compiled_hex','decision','finding','localization_note','retention_reason','review','actual_observation_status','formatting_approval_reason']} for r in doc['records']],
            total=82,revisions=46,retentions=36,actual_unique=63,offline_only=19,actual_runs=14,actual_frames=130014,actual_holds=676,
            supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_contextual_prose_native_display_pending_storage_actual_release_v8806',
            all_long_andfocused_scope_limits_preserved=True,Geronimo_Alonso_shared_de_fullname_lead_open=True,
            new_credit=0,new_registered_ROM=False,research_ROMs_preserved=13,full_goal_complete=False,
            evidence={p:sha(Path(p).read_bytes()) for p in EVIDENCE})
        new=deepcopy(old);new['latest_checkpoint']=TEXT;new[KEY]=pending
        scope_before=Path(old['unfinished_editorial_scope_v8806']['path']);scope=read(scope_before);(ROOT/'scope_before.json').write_bytes(scope_before.read_bytes())
        scope[KEY]=deepcopy(pending);save(ROOT/'unfinished_editorial_scope_inventory.json',scope)
        new[SCOPE]=dict(path=str(ROOT/'unfinished_editorial_scope_inventory.json'),sha256=sha((ROOT/'unfinished_editorial_scope_inventory.json').read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_completion_credit=0,full_goal_complete=False)
        new['research_checkpoints'].append(dict(id='V8827-Hodram-B54-B60-82-fivegates-stored-actual',documentation='docs/editorial_Hodram_B54_B60_v8827.md',manuscript=str(DOC),
            actual_review=str(REVIEW),new_editorially_completed=0,new_registered_ROM=False,research_ROMs=13,actual_runs=14,actual_frames=130014))
        save(ROOT/'ledger_staged.json',new);changes=[]
        for path,header in [('docs/editorial_handoff_current.md','# Current editorial handoff - V8827; V8778 current\n\n## B54-B60:82 five-gate reviews/storage/actual pass;production andregisteredintegration pending\n\n'),('docs/known_issues.md','## V8827: Hodram B54-B60 stored/actual/format checkpoint\n\n'),('docs/todo.md','## V8827 active editorial continuation\n\n')]:
            p=Path(path);before=p.read_bytes();backup=ROOT/(p.name+'.before');backup.write_bytes(before);staged=ROOT/(p.name+'.staged');prefix=(header+TEXT+'\n').encode('utf-8');staged.write_bytes(prefix+before)
            changes.append(dict(path=path,before=str(backup),before_sha256=sha(before),staged=str(staged),staged_sha256=sha(staged.read_bytes()),prefix_bytes=len(prefix)))
        checkpoint=ROOT/'editorial_Hodram_B54_B60_v8827.md';checkpoint.write_text('# Hodram B54-B60 stored andactual checkpoint V8827\n\n'+TEXT,encoding='utf-8')
        protected=[Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py'),Path(old['current_integrated_candidate']['path']),Path(old['current_integrated_candidate']['patch']),Path('out/raphael_natural_v2_accepted_base.nds'),Path('work/clean.nds'),Path('translations/rom_retention_pins.json')]
        save(ROOT/'stage_manifest.json',dict(ledger_before_sha256=sha(LEDGER.read_bytes()),ledger_staged_sha256=sha((ROOT/'ledger_staged.json').read_bytes()),scope_before_path=str(scope_before),scope_before_sha256=sha(scope_before.read_bytes()),
            documents=changes,checkpoint_doc=str(checkpoint),checkpoint_doc_sha256=sha(checkpoint.read_bytes()),protected_files={str(p):sha(p.read_bytes()) for p in protected},evidence=pending['evidence'],
            previous_goal_turn_was_progress_verified_by_V8807=True,new_credit=0,full_goal_complete=False))
        print('Staged V8827:82fivegate reviews/14actualruns;all counts andregistered artifacts unchanged.Independent audit required.')
    elif mode=='apply':
        m=read(ROOT/'stage_manifest.json');a=read(ROOT/'independent_staged_audit.json');assert a['pass'] and a['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
        assert sha(LEDGER.read_bytes())==m['ledger_before_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['before_sha256'] and sha(Path(r['staged']).read_bytes())==r['staged_sha256']
        for p,h in {**m['protected_files'],**m['evidence']}.items():assert sha(Path(p).read_bytes())==h
        checkpoint=Path('docs/editorial_Hodram_B54_B60_v8827.md');assert not checkpoint.exists()
        LEDGER.write_bytes((ROOT/'ledger_staged.json').read_bytes())
        for r in m['documents']:Path(r['path']).write_bytes(Path(r['staged']).read_bytes())
        checkpoint.write_bytes(Path(m['checkpoint_doc']).read_bytes())
        save(ROOT/'applied.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),new_credit=0,full_goal_complete=False));print('Applied audited checkpoint;verification required.')
    else:raise ValueError(mode)
