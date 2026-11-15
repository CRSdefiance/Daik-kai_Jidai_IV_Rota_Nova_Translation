"""Stage, apply and verify additive editorial progress without completion credit."""
import json
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_checkpoint_v8806')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B54_B60_82_contextual_prose_native_display_pending_storage_actual_release_v8806'
SCOPE='unfinished_editorial_scope_v8806'
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
VIEW=Path('work/analysis/Hodram_B54_B60_native_view_v8805/all82_native_English_direct_view_andboundary_review.json')
EVIDENCE=[
 'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
 'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json',
 'work/analysis/Hodram_B54_B60_clean_names_v8793/twenty_clean_full_andprogressive_compositions_current_binding.json',
 'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json',
 'work/analysis/Hodram_B54_B60_clean_context_v8795/complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json',
 'work/analysis/Hodram_B58_source_paths_v8796/all64_structural_paths_49utterance_memberships_unforced_opening_reference.json',
 'work/analysis/Hodram_B54_B60_source_macros_v8797b/FI_given_FA_surname_original_virtual_getter_trace.json',
 'work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json',
 'work/analysis/Hodram_B54_B60_source_review_v8798b/Geronimo_de_particle_field_andshared_pointer_inventory.json',
 'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json',
 'work/analysis/Hodram_B54_B60_prose_v8800/contextual_review.json',
 'work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json',
 'work/analysis/Hodram_B54_B60_layout_v8802d/automatic_plans.json',
 'work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json',
 str(DOC),str(VIEW),'translations/hodram_B54_B60_speaker_name_review_v1.json',
]
TEXT="""V8806 continues from verified V8790/current registered experimental cumulative V8778. Hodram SC1 B54-B60 now has 82 individual contextual prose decisions:46 revisions and36 justified retentions. All82 clean Japanese utterances,160 linked context utterances/two source choices,source names/roles and complete alternate paths preceded current English comparison. Source/current references,raw predecessors,individual findings,reasons and mapped neighbor pairs are preserved in translations/hodram_B54_B60_editorial_manuscript_v1.json. Four prose gates pass individually;formatting remains false pending stored andactual validation. No new completion/source-prose counter credit,ROM,registered build,emulator capture,promotion,separate package,pruning,commitorpush. Counts remain7,237 completed/7,240 credited source-prose anddrafts/4,492 integrated revisions/2,745 retentions. The previous status-answer-only turn was no progress;this continuation produces new manuscript/native evidence and a preserved checkpoint. Full goal remains active.

Clean-first source8791 proves152commands/82complete preambles,24relative sites120cases,six unforced queries,33paired nonprose structural decodes and175seeded ends. These are offline original-code tests,not plot/roster/item semantics or source-event activation. Names8792/8793 bind10identities,20clean and20current progressive/full getters,voices and11native name planes. Source display8794 covers82complete pages/328alignments,all11sheets viewed before currentEnglish. Linked37/15/142/128/65 context supplies the release,full introduction,language learning and later departure without inventing a romance;B128 hasno spoken text. B37 actual first choice is prepare to attack,not the stopped review's mistaken phrase. B58 atlas8796 has31unconditional/18conditional utterances and64structural models. Repeated descriptors neednot stay constant across opaque effects;composed paths are not native eligibility or actual scene reachability. FI/FA8797b are proved by actual captain virtual calls as given name/surname,Hodram6/Bergstrom9;they are not inferred faction names. FO haszero occurrences andnonew semantic orcustom-name coverage. Original two literal guard branches remain executed and unchanged.

Current comparison8799 binds all82 English predecessors,152complete command mappings,24relative targets andsix unforced queries in own V8778/captain1 context. Prose8800 restores fraud/farmland/missing family,reporting corruption back home/staged accident,villagers' dispersal/hunger,Sera's younger brother/companions and the incriminating admission,Westerners' abuses and the captain's individual self-doubt. It restores the rumored singular demon king/weapon,conditional worthiness,Iceland as a suggestion,map/Proof distinction,peace andprosperity,andManuel's carpenter role,Portuguese fleet,India,circulating illness,reported mistreatment,neighbor-love andpersonal vow. FE caption is Foreign Girl: ... rather than Strange girl. Retentions are justified individually in the complete exchange. Sera's learner speech remains respectful;no invented romance,ranks,gender for the unnamed friend,nationality,weapon identity,completed sale,homecoming,execution or disease is added.

English logical8801 passes328fresh original native default-name alignments. Automatic full216px plans8802d preserve every word andFI3/FA4/FO0,withzero original QAerrors orwarnings andno waivers. Earlier plans andstopped producers remain. Coherent phrase costs keep good luck andmilitary man,right? together;direct native view led to keeping We'd been praying together across the Proof explanation's page transition. No ordinary prose linebreak,padding,viewport narrowing,font change orfit-driven shortening is authored. Three records span two pages:B59R23/B59R26/B60R12. The FE consumer keeps its distinct228bitmap/216usable/48logical-height/288stride/6x12glyph/16physical-pitch contract.

Complete English native display8803b/8804 proves82utterances/85pages,including84progressive pages andoneFEpanel;all11latest sheets and79automatic word boundaries were directly reviewed in8805. Complete leading/internal/final codes,independent pixels,bounds,consumption,pagination andno blank/overlap pages pass. These are offline native CPU checks,not new gameplay. Preserve original8803 failure:an overstrict assertion wrongly required first visible originzero on every page. The actual existing page-continuation guard draws space atx0 andfirst glyph atx6;qualified8803b binds that exact prefix/event/origin while retaining every glyph/bitmap/bounds/canary check. Completed65records were reused exactly,only17remaining records were run;8804 rerenders only the later improved B59R23 andbinds81unchanged records/83pages. Original8802 syntax failure andactual six source-bound reactions are qualified in8802b;all original files/partials/failures remain.

Ten scoped progressive names/roles are editorally retained with individual source/context reasons,not credited as dialogue or approved globally. Full-name lead remains open:source Geronimo de Espinosa currently renders Geronimo デ Espinosa. The two-byte デ field is shared with actor49 Alonso;static pointer inventory is not exhaustive runtime-consumer coverage. Qualify all affected full-name consumers,field ownership,deployment andregistered guards before a scoped asset change. Preserve approved Rafael,Hodram,Joakim,Maria,Camille andcurrent mixed-width storage. All207names/fullcatalogue/customnames andwider role contexts remain in scope.

Next:reuse allcompleted source/context/names/prose/logical/plans/native pages/direct views;perform complete stored-block relocation maps,source/current/archive/whole-ROM inverses andindependent references/controls;representative initialized ornatural gameplay for FE/progressive transitions,learner exchange andmultipage behavior plus concrete risks;source-bound production/atomic checks andregistered cumulative integration/exactclean-input patch/ownstartup. No exhaustive natural playthrough orforced conditional roster/plot is required. Keep offline,initialized-fixture,inherited-save,natural activation,unvisited conditional content andhardware claims distinct. Credit these82 once only after necessary registered integration checks pass.

Current verified experimental V8778 andits exact clean-input patch,647manifestbatches/114acceptedlayers/18releasechecks/110regressions andownstartup remain unchanged. Reuse all completed B31/B53/B52 checks;do not rerun unchanged historical work. MainV4701/canonicalbaseline remain unchanged. Allfourstorylines/earlier translated dialogue/sharedtown-shop/random/Help/restprose/all207names-roles-aliases-customnames/retrospectiveprematurebreaks remain active. Every earlier unfinished-scope key/value/lead anddocument byte is preserved by inverse checks,including contractions/questiontags/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wider104-105-113-147/JanusPasar-versusPasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159versusRetainer/oldernormalends/nineteenthcells/B47-B48-B50metadata. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stay separate. Roughly20,000 remaining is a planning estimate,not an audited denominator. Preserve every ROM,translation,draft,producer,proof andfailure;the full objective is not complete.
"""

def protected_paths(old):
    return [Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py'),Path(old['current_integrated_candidate']['path']),Path(old['current_integrated_candidate']['patch']),Path('out/raphael_natural_v2_accepted_base.nds'),Path('work/clean.nds')]

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='stage':
        assert not ROOT.exists();old=read(LEDGER);view=read(VIEW);doc=read(DOC)
        assert old['goal_status']=='active' and not old['full_goal_complete'] and old['records_editorially_completed']==7237
        assert view['all11_sheets85pages82utterances_directly_viewed'] and doc['revised']==46 and doc['retained']==36
        assert KEY not in old and SCOPE not in old
        ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
        proofs={p:sha(Path(p).read_bytes()) for p in EVIDENCE}
        new=deepcopy(old);new['latest_checkpoint']=TEXT
        pending=dict(status='82-prose-reviewed-native-English-pages-viewed-storage-actual-production-registered-release-pending',
            records=[{k:r[k] for k in ['id','file_path','block','source_record_index','source_reference','source_hex','current_reference','current_hex','english','speaker','source_meaning','context','finding','decision','localization_note','retention_reason','review']} for r in doc['records']],
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_view=str(VIEW),native_view_sha256=sha(VIEW.read_bytes()),
            revisions=46,retentions=36,total=82,new_credit=0,new_emulator_runs=0,new_ROM=False,full_goal_complete=False,evidence=proofs,
            supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_clean_glosses_pending_native_andcurrent_English_v8783',
            next_required=['complete stored relocation and inverses','independent references and control flow','representative gameplay/focused risks','production/atomic guards','registered cumulative ROM/exact clean patch/own startup','once-only82 credit'],
            Geronimo_Alonso_shared_de_field_open=True)
        new[KEY]=pending
        scope_before=Path(old['unfinished_editorial_scope_v8783']['path']);scope=read(scope_before)
        (ROOT/'scope_before.json').write_bytes(scope_before.read_bytes());scope_new=deepcopy(scope);scope_new[KEY]=deepcopy(pending)
        save(ROOT/'unfinished_editorial_scope_inventory.json',scope_new)
        new[SCOPE]=dict(path=str(ROOT/'unfinished_editorial_scope_inventory.json'),sha256=sha((ROOT/'unfinished_editorial_scope_inventory.json').read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_completion_credit=0,full_goal_complete=False)
        new['research_checkpoints'].append(dict(id='V8806-Hodram-B54-B60-82-prose-native-pages',documentation='docs/editorial_Hodram_B54_B60_v8806.md',
            manuscript=str(DOC),native_view=str(VIEW),new_editorially_completed=0,new_ROM=False,source_prose_records=82,draft_revisions=46,retained_wordings=36))
        save(ROOT/'ledger_staged.json',new)
        changes=[]
        for path,header in [('docs/editorial_handoff_current.md','# Current editorial handoff - V8806; V8778 current\n\n## B54-B60:82 prose decisions and85 native English pages;storage/actual/release pending\n\n'),('docs/known_issues.md','## V8806: Hodram B54-B60 prose/native display checkpoint\n\n'),('docs/todo.md','## V8806 active editorial continuation\n\n')]:
            p=Path(path);before=p.read_bytes();backup=ROOT/(p.name+'.before');backup.write_bytes(before)
            staged=ROOT/(p.name+'.staged');prefix=(header+TEXT+'\n').encode('utf-8');staged.write_bytes(prefix+before)
            changes.append(dict(path=path,before=str(backup),before_sha256=sha(before),staged=str(staged),staged_sha256=sha(staged.read_bytes()),prefix_bytes=len(prefix)))
        p=ROOT/'editorial_Hodram_B54_B60_v8806.md';p.write_text('# Hodram B54-B60 editorial checkpoint V8806\n\n'+TEXT,encoding='utf-8')
        save(ROOT/'stage_manifest.json',dict(ledger_before_sha256=sha(LEDGER.read_bytes()),ledger_staged_sha256=sha((ROOT/'ledger_staged.json').read_bytes()),
            scope_before_path=str(scope_before),scope_before_sha256=sha(scope_before.read_bytes()),documents=changes,checkpoint_doc=str(p),checkpoint_doc_sha256=sha(p.read_bytes()),
            protected_files={str(p):sha(p.read_bytes()) for p in protected_paths(old)},evidence=proofs,
            previous_status_answer_turn_was_no_progress_revalidated_by_new82_decisions_native_tests_andcheckpoint=True,
            new_credit=0,full_goal_complete=False))
        print('Staged additive checkpoint; all counters andrelease artifacts unchanged; independent audit required.')
    elif mode=='apply':
        manifest=read(ROOT/'stage_manifest.json');audit=read(ROOT/'independent_staged_audit.json')
        assert audit['pass'] and audit['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
        assert sha(LEDGER.read_bytes())==manifest['ledger_before_sha256']
        for r in manifest['documents']:assert sha(Path(r['path']).read_bytes())==r['before_sha256'] and sha(Path(r['staged']).read_bytes())==r['staged_sha256']
        for path,digest in {**manifest['protected_files'],**manifest['evidence']}.items():assert sha(Path(path).read_bytes())==digest
        target=Path('docs/editorial_Hodram_B54_B60_v8806.md');assert not target.exists()
        LEDGER.write_bytes((ROOT/'ledger_staged.json').read_bytes())
        for r in manifest['documents']:Path(r['path']).write_bytes(Path(r['staged']).read_bytes())
        target.write_bytes(Path(manifest['checkpoint_doc']).read_bytes())
        save(ROOT/'applied.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),new_credit=0,full_goal_complete=False))
        print('Applied audited checkpoint; verification still required.')
    else:raise ValueError(mode)
