"""Actual-changing in-memory proof corruptions with dependency bypass and a whole-NDS commit trap."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import gerhard_surname_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract
from dk4tool.patch.gerhard_surname_evidence_v1 import MODEL
from scripts.Gerhard_surname_release_paths_v8238 import proofs,APPROVED,MAP,SEAL,FLAGS,PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_atomic_challenges_v8257')

if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();base_load=owned.load;configuration=base_load(owned.CONFIG)
    inputs={str(Path(p).resolve()):base_load(p) for p in [owned.CONFIG,APPROVED,MAP,SEAL,MODEL,*paths.values()]}
    cases=[]
    def add(label,path,keys,value,guard):
        canonical=str(Path(path).resolve());original=inputs[canonical];changed=deepcopy(original);cursor=changed;old=original
        for k in keys[:-1]:cursor=cursor[k];old=old[k]
        previous=deepcopy(old[keys[-1]]);assert previous!=value,(label,previous,value)
        cursor[keys[-1]]=deepcopy(value);assert changed!=original
        cases.append(dict(case=label,path=canonical,keys=keys,before=previous,after=value,changed=changed,expected_guard=guard))
    add('configuration-format',owned.CONFIG,['format'],'unreviewed-format','exact complete source-bound configuration')
    add('configuration-missing-manuscript',owned.CONFIG,['manuscripts'],[],'exact complete source-bound configuration')
    add('configuration-missing-proof',owned.CONFIG,['proofs'],{},'exact complete source-bound configuration')
    add('configuration-archive-target',owned.CONFIG,['archives',0,'target_sha256'],'0'*64,'exact two owned configuration output entries')
    for i,row in enumerate(base_load(APPROVED)['records']):
        for gate in ['source','context','localization','naturalness','formatting']:
            add('individual-'+gate+'-'+row['id'],APPROVED,['records',i,'review',gate],False,'v2 requires per-record')
        for key,value in [('english',row['english']+'!'),('source_meaning',row['source_meaning']+' New unreviewed rank.'),('compiled_hex',row['compiled_hex']+'20')]:
            add('individual-'+key+'-'+row['id'],APPROVED,['records',i,key],value,'approved prose/source/context/waiver required')
    for gate in ['source','context','localization','naturalness','formatting']:
        add('owned-name-'+gate,APPROVED,['name_records',0,'review',gate],False,'All five individual Gerhard name gates required')
    add('owned-name-original20-byte-allocation',APPROVED,['name_records',0,'bytes'],20,'Exact approved surname source/context/owned12-byte span required')
    for flag in FLAGS:add('missing-scope-'+flag,MAP,[flag],False,'all independently frozen source/scope flags')
    mapping=base_load(MAP)
    add('map-name-span',MAP,['name_record','bytes'],20,'exact name field independent inverse/pointers/Blades')
    for index,g in enumerate(mapping['blocks']):
        add('map-header-'+str(g['block']),MAP,['blocks',index,'target_header_hex'],'ff'+g['target_header_hex'][2:],'every sparse reference/header/tail/command/relative/inverse map')
        add('map-relative-'+str(g['block']),MAP,['blocks',index,'relative_fixups',0,'target_span'],g['relative_fixups'][0]['target_span']+2,'every sparse reference/header/tail/command/relative/inverse map')
        add('map-speech-reference-'+str(g['block']),MAP,['blocks',index,'text_records',0,'new_offset'],g['text_records'][0]['new_offset']+2,'every sparse reference/header/tail/command/relative/inverse map')
    controls=base_load(paths['native_controls'])
    add('dispatch-wrong-voice',paths['native_controls'],['final_dispatches',0,'source_voice_class'],7,'original final dispatch actor andvoice')
    add('dispatch-wrong-actor',paths['native_controls'],['final_dispatches',0,'resolved_actor_ID'],2,'original final dispatch actor andvoice')
    add('dispatch-wrong-offset',paths['native_controls'],['final_dispatches',0,'final_offset'],controls['final_dispatches'][0]['final_offset']+2,'final stored dispatch physical reference')
    add('dispatch-truncated-body',paths['native_controls'],['final_dispatches',0,'boundaries',1,'text_hex'],controls['final_dispatches'][0]['boundaries'][1]['text_hex'][:-2],'all original final dispatch boundaries/body/macro/actor references')
    add('raw-query-result',paths['native_controls'],['raw_predicates_andqueries',0,'cases',2,'native_result',1],1,'exact raw original results preserved')
    add('raw-query-offset',paths['native_controls'],['raw_predicates_andqueries',0,'cases',2,'offset'],controls['raw_predicates_andqueries'][0]['cases'][2]['offset']+2,'each exact original raw operand association')
    add('seeded-normal-value',paths['native_controls'],['normal_seeded_ends',0,'cases',0,'native_result',1],1,'normal end retains entire value word')
    add('normal-phase-duplicate',paths['native_controls'],['normal_seeded_ends',1,'version'],'clean','all six unique original terminal phases')
    add('normal-terminal-offset',paths['native_controls'],['normal_seeded_ends',0,'terminal','offset'],controls['normal_seeded_ends'][0]['terminal']['offset']+2,'complete terminal binds exact independent command map')
    add('normal-extra-read',paths['native_controls'],['normal_seeded_ends',0,'cases',0,'no_leading_or_post_four_byte_payload_read'],False,'native terminal read/ABI guards')
    add('native-load-omitted',paths['native_loader'],['fresh_native_whole_loads_andcache_hits'],335,'complete native whole loads andparent modes')
    add('native-parent-mode-omitted',paths['native_loader'],['fresh_initial_parent_modes'],671,'complete native whole loads andparent modes')
    add('native-loader-cache-guard',paths['native_loader'],['all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact'],False,'original index/cache/entry ABI guards')
    add('caller-interior-alias',paths['native_caller'],['only_original24070_interpreter_call_no_literal_alias'],False,'complete shipped caller census/entry scope')
    add('caller-map-offset',paths['native_caller'],['groups',0,'all_command_maps',0,'new_offset'],10,'all independently rebuilt caller command maps')
    add('native-compiled-alignment-count',paths['native_fonts'],['fresh_compiled_alignment_cases'],19,'five native pages/twenty alignments')
    add('stored-alignment-count',paths['native_stored'],['fresh_native_alignment_cases'],3,'one fresh parity tail/four exact native bodies')
    add('native-compiled-body',paths['native_fonts'],['records',0,'compiled_hex'],'00','compiled/stored individual bodies')
    add('stored-body-parity',paths['native_stored'],['records',3,'compiler_owned_parity_space'],False,'individual stored parity ownership')
    add('stored-expansion',paths['native_stored'],['records',0,'expanded_stored_hex'],'00','stored native macro expansion')
    add('native-name-model',MODEL,['name_planes','revised_English',2,'text'],'Gerhard Pirateking','exact full original progressive name andflush')
    add('native-model-source-actor',MODEL,['native_models','parent_English',0,'source_selector'],2,'native source-bound model body')
    actual=base_load(paths['actual'])
    add('actual-body-hold-count',paths['actual'],['complete_body_holds'],29,'30 body and262 name holds')
    add('actual-name-hold-count',paths['actual'],['relevant_name_holds'],261,'30 body and262 name holds')
    add('actual-false-natural-intro',paths['actual'],['additional_B27_intro_display8_of8_is_not_full_branch_controlflow_ornatural_activation'],False,'actual initial frame/intro scope')
    add('actual-option1-claim',paths['actual'],['original_Hamburg_choice_selected_option0_only_option1_individual_actual_coverage_not_claimed'],False,'only original menu option0 observed')
    add('actual-frozen-individual-capture',paths['actual'],['groups',2,'speeches',0,'start'],actual['groups'][2]['speeches'][0]['start']+1,'frozen individual actual observations') if actual['groups'][2]['speeches'][0]['changed_body'] else None
    add('actual-duration-source-association',paths['actual'],['groups',0,'command_pairs',0,'duration'],actual['groups'][0]['command_pairs'][0]['duration']+1,'actual original command timing')
    add('actual-raw-result-association',paths['actual'],['groups',0,'command_pairs',0,'native_result',1],actual['groups'][0]['command_pairs'][0]['native_result'][1]^1,'actual raw command result/length')
    add('actual-source-ROM-membership',paths['actual'],['groups',0,'fixture','source_block_sha256'],'0'*64,'actual source route/block identity')
    add('actual-focused-bypass-hidden',paths['actual'],['groups',4,'fixture','original_full_B27_conditions_andremaining_effects_NOT_executed_bythis_display_fixture'],False,'focused original outer condition unexecuted')
    comparison=base_load(paths['actual_comparison'])
    add('comparison-duration-value',paths['actual_comparison'],['groups',1,'duration_differences',0,'revised'],comparison['groups'][1]['duration_differences'][0]['revised']+1,'every original command/timing/RNG/UI difference retained')
    add('comparison-final-RNG',paths['actual_comparison'],['groups',2,'final_native_values',1,'PRNG_seed'],comparison['groups'][2]['final_native_values'][1]['PRNG_seed']^1,'every recomputed final native component/actor/captain/RNG value')
    add('comparison-later-RGB-value',paths['actual_comparison'],['groups',2,'later_full_RGB_comparisons',0,'parent_RGB_sha256'],'0'*64,'every later full RGB measurement')
    add('comparison-captain0-tail-hidden',paths['actual_comparison'],['whole_B27_tail_NOT_normal_Lil_route_continuity_ororiginal_optional_event_context_proof'],False,'captain0 wholeB27 fixture limitation')
    focus=base_load(paths['actual_focus'])
    add('focused-raw-RNG-value',paths['actual_focus'],['sampled_comparisons',0,'parent_PRNG_seed'],focus['sampled_comparisons'][0]['parent_PRNG_seed']^1,'computed raw phase RNG states')
    add('focused-final-byte-count',paths['actual_focus'],['sampled_comparisons',7,'bounded_native_model_andpersistent_byte_differences','fleet','changed_bytes'],3,'independently recomputed every bounded byte difference')
    add('focused-replay-obligation',paths['actual_focus'],['all_same_ROM_input_horizon_observer_rows_selected_framebuffers_andfinal_RAM_reproduce_exactly_perversion'],False,'exact same-input replay obligation')
    add('sealed-actual-scope-count',MAP,['actual_scope','complete_body_holds'],29,'every independently measured actual scope/limit field')
    watched={Path(p) for p in configuration['dependencies']}|{Path(owned.CONFIG),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),PARENT,ROM,Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds')}
    beforehashes={str(p):sha(p.read_bytes()) for p in watched};contract()
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');template=NdsImage.open(PARENT);before=bytes(template.rom.save());results=[]
    check=owned.check_dependencies;commit=owned.commit_image
    ROOT.mkdir(parents=True)
    try:
        for index,case in enumerate(cases):
            image=NdsImage(PARENT,deepcopy(template.rom));original=image.rom;calls=[]
            def fake_load(path):
                canonical=str(Path(path).resolve())
                return deepcopy(case['changed']) if canonical==case['path'] else base_load(path)
            def no_commit(*args):calls.append('forbidden-commit');raise AssertionError('Rejected input reached a ROM commit')
            owned.load=fake_load;owned.check_dependencies=lambda conf:None;owned.commit_image=no_commit
            try:owned.apply_release(image,baseline)
            except ValueError as error:
                assert case['expected_guard'] in str(error),(case['case'],case['expected_guard'],str(error))
                result={k:v for k,v in case.items() if k!='changed'};result.update(rejected=True,error=str(error),dependency_digest_gate_deliberately_bypassed=True,actual_input_change_asserted=True,commit_calls=0,complete_input_object_identity_andROM_bytes_unchanged=True)
                results.append(result)
            else:raise AssertionError('Unsafe changed input accepted:'+case['case'])
            assert not calls and image.rom is original and bytes(image.rom.save())==before and bytes(template.rom.save())==before
            if index%5==4 or index+1==len(cases):print('PRECOMMIT_REJECTIONS',index+1,'of',len(cases),flush=True)
    finally:owned.load=base_load;owned.check_dependencies=check;owned.commit_image=commit
    contract();assert beforehashes=={str(p):sha(p.read_bytes()) for p in watched}
    save(ROOT/'actual_changing_semantic_precommit_rejections.json',dict(cases=results,negative_count=len(results),all_expected_semantic_guards_match=True,
        dependency_gate_bypassed_buttrusted_frozen_contract_andnative_source_guards_not_weakened=True,
        zero_wholeNDS_commit_calls_forall_failed_inputs=True,whole_input_object_identity_andall_ROM_bytes_exact_forall_failures=True,
        all_watched_sources_ROMs_configs_proofs_registry_ledger_andpins_hash_exact=True,trusted_frozen_contract_revalidated_before_andafter=True,
        new_credit=0,new_emulator_runs=0,new_ROMs=0,full_goal_complete=False,evidence=beforehashes|{str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('PASS',len(results),'actual-changing independent semantic rejections;all zero commits/input bytes exact;no replay orROM write.',flush=True)
