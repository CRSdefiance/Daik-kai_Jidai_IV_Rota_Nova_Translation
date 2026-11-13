"""Meaningful changed-proof cases with dependency bypass and a zero-whole-NDS-commit trap."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_three_blocks_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_three_blocks_profile_v1 import contract
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_atomic_challenges_v8298')

if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();base_load=owned.load;conf=base_load(owned.CONFIG)
    extra=[base_load(paths['native_loader'])['load_proof'],base_load(paths['native_loader'])['parent_mode_proof']]
    actual=base_load(paths['actual_B137'])['groups'][0];extra += [actual['capture_report'],actual['observer']]
    extra += ['work/analysis/Hodram_scene_runs_v8280/route1_B137_clean_Japanese/identical_ordinary_A_inputs.json']
    inputs={str(Path(p).resolve()):base_load(p) for p in [owned.CONFIG,DOC,MAP,SEAL,*paths.values(),*extra]};cases=[]
    def add_many(label,edits,guard):
        changed={};descriptions=[]
        for path,keys,value in edits:
            canonical=str(Path(path).resolve());original=inputs[canonical]
            if canonical not in changed:changed[canonical]=deepcopy(original)
            cursor=changed[canonical];old=original
            for k in keys[:-1]:cursor=cursor[k];old=old[k]
            previous=deepcopy(old[keys[-1]]);assert previous!=value,(label,previous,value)
            cursor[keys[-1]]=deepcopy(value);descriptions.append(dict(path=canonical,keys=keys,before=previous,after=value))
        assert all(v!=inputs[p] for p,v in changed.items())
        cases.append(dict(case=label,edits=descriptions,changed=changed,expected_guard=guard))
    def add(label,path,keys,value,guard):add_many(label,[(path,keys,value)],guard)
    add('configuration-format',owned.CONFIG,['format'],'unreviewed','exact complete source-qualified configuration')
    add('missing-manuscript',owned.CONFIG,['manuscripts'],[],'exact complete source-qualified configuration')
    add('missing-proof-set',owned.CONFIG,['proofs'],{},'exact complete source-qualified configuration')
    add('archive-target',owned.CONFIG,['archives',0,'target_sha256'],'0'*64,'only one owned SC1 archive')
    add('invented-code-component',owned.CONFIG,['components'],[dict(file_path='/__arm9__.bin')],'only one owned SC1 archive')
    add('unregistered-name-dependency',owned.CONFIG,['required_registered_Gerhard_dependency','ARM9_sha256'],'0'*64,'explicit registered Adernkatz parent dependency')
    doc=base_load(DOC)
    for index in [0,21,23]:
        row=doc['records'][index]
        for gate in ['source','formatting']:add('individual-'+gate+'-'+row['id'],DOC,['records',index,'review',gate],False,'v2 requires per-record')
    add('unreviewed-prose',DOC,['records',0,'english'],doc['records'][0]['english']+'!','approved prose/source/context/waiver required')
    add('unreviewed-name-label',paths['names'],['records',0,'name'],'Admiral Hodram','frozen complete native andscoped-name approvals')
    add('altered-frozen-contract',paths['native_contract'],['source_macro_counts','FI'],1,'frozen complete native andscoped-name approvals')
    add('missing-map-scope',MAP,['external_references_complete'],False,'complete source/current/final reference flags')
    mapping=base_load(MAP)
    for index,g in enumerate(mapping['groups']):
        add('map-header-'+str(g['block']),MAP,['groups',index,'target_header_hex'],'ff'+g['target_header_hex'][2:],'every independent native reference/relative/header/tail/inverse map')
        add('map-reference-'+str(g['block']),MAP,['groups',index,'text_records',0,'new_offset'],g['text_records'][0]['new_offset']+2,'every independent native reference/relative/header/tail/inverse map')
        for fi,fix in enumerate(g['relative_fixups']):
            add(f'map-relative-{g["block"]}-{fi}',MAP,['groups',index,'relative_fixups',fi,'target_span'],fix['target_span']+2,'every independent native reference/relative/header/tail/inverse map')
    current=base_load(paths['current']);add('previous-header-literal',paths['current'],['groups',0,'current_header_hex'],'ff'+current['groups'][0]['current_header_hex'][2:],'complete stored source literals/headers')
    controls=base_load(paths['native_controls']);dispatch=controls['final_dispatches'][0]
    add('dispatch-actor',paths['native_controls'],['final_dispatches',0,'resolved_actor_ID'],2,'source-qualified final actor/voice/body offset')
    add('dispatch-voice',paths['native_controls'],['final_dispatches',0,'source_voice_class'],7,'source-qualified final actor/voice/body offset')
    add('dispatch-offset',paths['native_controls'],['final_dispatches',0,'final_offset'],dispatch['final_offset']+2,'source-qualified final actor/voice/body offset')
    add('dispatch-lost-final-glyph',paths['native_controls'],['final_dispatches',0,'boundaries',1,'text_hex'],dispatch['boundaries'][1]['text_hex'][:-2],'complete original progressive actor/text boundary')
    add('dispatch-FE-null-actor',paths['native_controls'],['final_dispatches',0,'FE_original_null_actor_calls'],[1],'complete static progressive dispatch andABI scope')
    add('catalogue-route-mask',paths['native_controls'],['registered_current_catalogue_binding','route_mask'],4,'all467 native catalogue keys/targets/routes/calls')
    add('raw-query-result',paths['native_controls'],['raw_predicates_andqueries',0,'cases',2,'native_result',1],1,'source-qualified complete raw evaluator result')
    q=controls['raw_predicates_andqueries'][0]['cases'][2]
    add('raw-query-offset',paths['native_controls'],['raw_predicates_andqueries',0,'cases',2,'offset'],q['offset']+2,'source-qualified complete raw evaluator result')
    add('raw-query-forced-flag',paths['native_controls'],['raw_predicates_andqueries',0,'cases',2,'no_predicate_or_event_flag_forced'],False,'raw evaluator original state/ABI/scratch guards')
    add_many('coherent-corrupt-end-value',[
        (paths['native_controls'],['normal_end_cases_exact_reused',0,'target_cases_exact_reuse',0,'native_result',1],1),
        (paths['relocation'],['groups',0,'target_seeded_normal_ends',0,'native_result',1],1)],'fourbyte normal end retains complete value word')
    add('relative-taken-result',paths['relocation'],['groups',0,'relocated_skip_cases',0,'cases',0,'taken'],False,'every original relative result/extent/endpoint/guard')
    add('wrong-item-layout',paths['native_controls'],['picture_andhide_boundary_cases',0,'original_picture_boundary_calls',0,'layout'],[2,0,1],'original4800 layout0 and4700 distinct')
    add('wrong-item-identity',paths['source_picture'],['item_ID'],180,'exact original item181 source/current identity')
    add('native-probe-false-full-resource-claim',paths['native_controls'],['full_opaque_A000_picture_resource_hide_UI_bodies_not_executed_bythis_native_boundary_probe'],False,'native probes do not claim fullscene oractivation')
    add('native-load-count',paths['native_loader'],['fresh_native_whole_loads_andcache_hits'],324,'complete original SC1 loader counts')
    add('native-parent-mode-count',paths['native_loader'],['fresh_initial_parent_modes'],649,'complete original SC1 loader counts')
    add('native-loader-cache-guards',paths['native_loader'],['all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact'],False,'loader declared guards andcontrolled-native scope')
    add('native-caller-scope',paths['native_caller'],['source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof'],False,'caller declared source andscope guards')
    add('native-loader-wrong-ROM',paths['native_loader'],['research_ROM_sha256'],'0'*64,'all loader/census proofs belong toexact approved reference ROM')
    add('native-action-wrong-block',extra[0],['routes',0,'actions',138,'native_selected_block'],136,'original index/whole native payload')
    modes=base_load(extra[1]);case=modes['native_handoff_and_first_read_cases'][0]
    add('native-first-read-address',extra[1],['native_handoff_and_first_read_cases',0,'original_source_reads',0,'address'],case['original_source_reads'][0]['address']+2,'original payload-plus8 firstread/mode guards')
    add('caller-unit-code-hash',paths['native_caller'],['native_call_census','units',0,'sha256'],'0'*64,'one fresh andexact reused complete-code census association')
    add('caller-interior-entry',paths['native_caller'],['groups',0,'original_entry_payload_offset'],10,'original blockindex entry,not interior offset')
    # These cases reach independent native/actual recomputation, rather than a checksum-only gate.
    model=base_load(paths['native_models']);adapter=model['source_owned_exact_target_page_adapter']
    add('native-page-adapter',paths['native_models'],['source_owned_exact_target_page_adapter'],adapter+'\n# unreviewed','source-locked native page adapter')
    add('native-body-input',paths['native_models'],['native_models','clean_Japanese',0,'input_hex'],model['native_models']['clean_Japanese'][0]['input_hex']+'20','literal source-qualified native input')
    add('native-body-events',paths['native_models'],['native_models','clean_Japanese',0,'pages',0,'events',0,'code'],model['native_models']['clean_Japanese'][0]['pages'][0]['events'][0]['code']^1,'native glyph/consumption/bounds metadata')
    add_many('coherent-corrupt-name-events',[
        (paths['native_models'],['name_planes',0,'native_glyph_events',0,'x'],6),
        (paths['native_names'],['name_planes',0,'native_glyph_events',0,'x'],6)],'complete name glyph order andfinal flush')
    st=base_load(paths['native_stored'])['records'][0]
    add('stored-parity-ownership',paths['native_stored'],['records',0,'compiler_owned_parity_space'],not st['compiler_owned_parity_space'],'compiler-only parity space')
    add('actual-command-result',paths['actual_B137'],['groups',0,'command_pairs',11,'native_result',1],99,'every recomputed selected/following command andspeech observation')
    add('actual-missing-complete-hold',paths['actual_B137'],['groups',0,'speeches',0,'complete_holds'],actual['speeches'][0]['complete_holds'][1:],'every recomputed selected/following command andspeech observation')
    add('actual-readonly-observer-flag',actual['observer'],['rows',0,'CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],False,'observed readonly original cache')
    add('actual-controller-retiming',extra[-1],[0,'start'],1001,'original unretimed ordinary input schedule')
    add('actual-PNG-integrity',actual['capture_report'],['frames_captured',0,'PNG_sha256'],'0'*64,'actual PNG integrity')
    comparison=base_load(paths['actual_comparison'])
    add('erased-command-differences',paths['actual_comparison'],['groups',0,'command_comparison_differences'],[],'all actual command/timing/RNG/UI differences retained')
    add('erased-duration-differences',paths['actual_comparison'],['groups',0,'duration_differences'],[],'all actual command/timing/RNG/UI differences retained')
    cash=comparison['groups'][0]['final_native_values'][0]['components']['state']['cash']
    add('final-native-state',paths['actual_comparison'],['groups',0,'final_native_values',0,'components','state','cash'],cash+1,'every recomputed final native component/actor/captain/RNG value')
    add('invented-normal-Hodram-tail',paths['actual_comparison'],['groups',0,'final_native_values',0,'captain_ID'],1,'every recomputed final native component/actor/captain/RNG value')
    add('later-RGB-difference',paths['actual_comparison'],['groups',0,'later_RGB_comparisons',0,'whole_RGB_equal'],False,'all complete later framebuffer comparisons retained')
    add('wrong-actual-item-layout',paths['actual_comparison'],['groups',2,'original4800_4700_actual','layout'],[2,0,1],'complete original item/hide observation andscope metadata')
    add('lost-fixture-scope',paths['display_approval'],['initialized_opening_not_original_event_activation_location_eligibility_orall_attainable_effect_paths'],False,'mandatory actual fixture/simulation scope limits')
    watched={Path(p) for p in conf['dependencies']}|{Path(owned.CONFIG),PARENT,ROM,DOC,MAP,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')}
    beforehashes={str(p):sha(p.read_bytes()) for p in watched};contract();baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');template=NdsImage.open(PARENT)
    before=bytes(template.rom.save());results=[];check=owned.check_dependencies;commit=owned.commit_image;ROOT.mkdir(parents=True)
    try:
        for index,c in enumerate(cases):
            image=NdsImage(PARENT,deepcopy(template.rom));original=image.rom;calls=[]
            def fake_load(path):
                canonical=str(Path(path).resolve());return deepcopy(c['changed'][canonical]) if canonical in c['changed'] else base_load(path)
            def no_commit(*args):calls.append('forbidden-commit');raise AssertionError('Rejected input reached a ROM commit')
            owned.load=fake_load;owned.check_dependencies=lambda conf:None;owned.commit_image=no_commit
            try:owned.apply_release(image,baseline)
            except ValueError as error:
                assert c['expected_guard'] in str(error),(c['case'],c['expected_guard'],str(error))
                record={k:v for k,v in c.items() if k!='changed'};record.update(rejected=True,error=str(error),dependency_digest_gate_deliberately_bypassed=True,
                    actual_input_changes_asserted=True,commit_calls=0,whole_input_identity_andall_ROM_bytes_unchanged=True)
                results.append(record)
            else:raise AssertionError('Unsafe changed input accepted:'+c['case'])
            assert not calls and image.rom is original and bytes(image.rom.save())==before and bytes(template.rom.save())==before
            save(ROOT/f'case_{index:03d}.json',record)
            print('PRECOMMIT_REJECTIONS',index+1,'of',len(cases),c['case'],flush=True)
    finally:owned.load=base_load;owned.check_dependencies=check;owned.commit_image=commit
    contract();assert beforehashes=={str(p):sha(p.read_bytes()) for p in watched}
    save(ROOT/'actual_changing_semantic_precommit_rejections.json',dict(cases=results,negative_count=len(results),all_expected_semantic_guards_match=True,
        dependency_gate_bypassed_buttrusted_frozen_andnative_source_guards_preserved=True,all_rejected_inputs_zero_whole_NDS_commits=True,
        complete_original_object_identity_andserialized_ROM_exact_for_every_failure=True,all_protected_files_hash_exact=True,
        no_new_ROM_capture_registration_promotion_orcredit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence=beforehashes|{str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('PASS',len(results),'actual-changing semantic precommit rejections,allzero commits/input bytes exact. No emulator replay orROM write.',flush=True)
