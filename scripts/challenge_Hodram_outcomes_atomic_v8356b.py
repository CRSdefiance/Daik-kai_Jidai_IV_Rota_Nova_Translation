"""Actual-changing semantic challenges with only release dependency digests bypassed; zero commits."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v1 import contract
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM,DOC,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b')

if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();base_load=owned.load;conf=base_load(owned.CONFIG);data={k:base_load(p) for k,p in paths.items()}
    extra=[data['loaders']['load_proof'],data['loaders']['parent_mode_proof'],data['actual48']['groups'][0]['observer'],data['actual48']['groups'][0]['capture_report']]
    FEterminal=base_load('work/analysis/Hodram_outcome_FE_geometry_runs_v8336/clean_Japanese/terminal.json');extra.append(FEterminal['observer'])
    inputs={str(Path(p).resolve()):base_load(p) for p in [owned.CONFIG,DOC,MAP,SEAL,*paths.values(),*extra]};cases=[]
    def many(label,edits,guard):
        changed={};descriptions=[]
        for path,keys,value in edits:
            canonical=str(Path(path).resolve());original=inputs[canonical]
            if canonical not in changed:changed[canonical]=deepcopy(original)
            cursor=changed[canonical];old=original
            for k in keys[:-1]:cursor=cursor[k];old=old[k]
            previous=deepcopy(old[keys[-1]]);assert previous!=value,(label,keys)
            cursor[keys[-1]]=deepcopy(value);descriptions.append(dict(path=canonical,keys=keys,before=previous,after=value))
        assert all(v!=inputs[p] for p,v in changed.items());cases.append(dict(case=label,edits=descriptions,changed=changed,expected_guard=guard))
    def add(label,path,keys,value,guard):many(label,[(path,keys,value)],guard)
    add('configuration-format',owned.CONFIG,['format'],'unreviewed','exact complete source-qualified configuration')
    add('missing-proof-set',owned.CONFIG,['proofs'],{},'exact complete source-qualified configuration')
    add('foreign-code-edit',owned.CONFIG,['components'],[dict(file_path='/__arm9__.bin')],'only one owned SC1 archive')
    add('wrong-name-dependency',owned.CONFIG,['required_registered_Gerhard_dependency','ARM9_sha256'],'0'*64,'explicit registered Adernkatz parent dependency')
    doc=base_load(DOC)
    for i,row in enumerate(doc['records']):add('individual-formatting-'+row['id'],DOC,['records',i,'review','formatting'],False,'v2 requires per-record')
    add('lost-qualified-discovery',DOC,['records',3,'english'],'Lil Argot found Ullr\'s Bow!','approved prose/source/context/waiver required')
    add('reversed-Amsterdam-instruction',DOC,['records',5,'english'],"I'll be waiting in Amsterdam.",'approved prose/source/context/waiver required')
    add('invented-personal-FE-speaker',paths['names'],['FE_is_not_actor254_orpersonal_name'],False,'frozen complete native andscoped-name approvals')
    add('missing-source-reference-completeness',MAP,['external_references_complete'],False,'complete source/current/final reference flags')
    mapping=base_load(MAP)
    for i,g in enumerate(mapping['groups']):
        add('map-header-'+str(g['block']),MAP,['groups',i,'target_header_hex'],'ff'+g['target_header_hex'][2:],'every independent native reference/header/tail/inverse map')
        add('map-interior-reference-'+str(g['block']),MAP,['groups',i,'text_records',0,'new_offset'],g['text_records'][0]['new_offset']+2,'every independent native reference/header/tail/inverse map')
    add('mixed-consumer-map',MAP,['records',3,'consumer'],'progressive','all six exact source/current/final records andconsumers')
    current=data['current'];add('current-header',paths['current'],['groups',0,'current_header_hex'],'ff'+current['groups'][0]['current_header_hex'][2:],'complete stored source literals/headers')
    # Corrupt executable adapter semantics coherently; the trusted frozen original must still reject before exec.
    adapter=data['pages']['source_owned_target_page_adapter'];evil='raise RuntimeError("untrusted native page adapter executed")\n'+adapter
    many('coherent-untrusted-page-code',[(paths[k],['source_owned_target_page_adapter'],evil) for k in ['pages','source_display','stored']],'exact trusted source-owned adapter required:pages')
    add('source-glyph-order',paths['models'],['native_models','clean_Japanese',0,'pages',0,'events',0,'code'],data['models']['native_models']['clean_Japanese'][0]['pages'][0]['events'][0]['code']^1,'independent progressive glyph/geometry/consumption metadata')
    add('FE-lost-final-byte',paths['models'],['native_models','clean_Japanese',3,'expanded_native_hex'],data['models']['native_models']['clean_Japanese'][3]['expanded_native_hex'][:-2],'complete expanded native model body/page count')
    name=data['models']['name_planes'][0];event=deepcopy(name['native_glyph_events']);event[0]['x']+=6
    many('coherent-shifted-Lil-name',[(paths['models'],['name_planes',0,'native_glyph_events'],event),(paths['source_display'],['reused_original_Lil_style11_plane','native_glyph_events'],event)],'source-qualified complete Lil nameplane/events/flushes')
    for label,keys,value in [('FE-as-actor254',['resolved_actor_ID'],254),('FE-invented-voice',['source_voice_class'],3),('FE-missing-null-call',['FE_original_null_actor_calls'],[])]:
        add(label,paths['controls'],['final_dispatches',3,*keys],value,'independent full final dispatch fields andABI guards')
    add('FI-expanded-as-old-name',paths['controls'],['final_dispatches',4,'boundaries',1,'text_hex'],'00','independent full final dispatch fields andABI guards')
    add('invented-event-exclusion',paths['source_controls'],['source_event_records',1,'must_not_be_completed'],[47],'two original EV1 outcomes and asymmetric exclusions')
    add('source-end-dropped-value',paths['source_controls'],['groups',0,'normal_seeded_ends',0,'native_result',1],1,'all independently executed complete end/ABI/value-carry fields')
    add('final-end-dropped-value',paths['relocation'],['groups',1,'target_seeded_normal_ends',0,'native_result',1],1,'all independently executed complete end/ABI/value-carry fields')
    add('changed-opaque-effect',paths['controls'],['nontext_commands',0,'complete_source_current_target_hex'],'0000','all nine nontext commands/100 source-target ends')
    add('native-load-count',paths['loaders'],['fresh_native_whole_loads_andcache_hits'],324,'complete original SC1 loader counts')
    add('native-cache-guard',paths['loaders'],['all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact'],False,'original loader scope')
    modes=base_load(extra[1]);add('native-first-read-address',extra[1],['native_handoff_and_first_read_cases',0,'original_source_reads',0,'address'],modes['native_handoff_and_first_read_cases'][0]['original_source_reads'][0]['address']+2,'original payload-plus8 firstread/mode guards')
    add('caller-interior-entry',paths['callers'],['groups',0,'original_entry_payload_offset'],10,'original blockindex entry,not interior offset')
    add('fixture-shortened-script',paths['fixtures'],['fixtures',0,'constant_shift_bytes'],32,'exact source prelude andwhole native command census')
    actual=data['actual48']['groups'][0]
    add('actual-lost-FE-complete-hold',paths['actual48'],['groups',0,'speeches',0,'complete_holds'],actual['speeches'][0]['complete_holds'][1:],'independent every actual trace/hold/header/return andlater-command field')
    add('actual-wrong-end-value',paths['actual48'],['groups',0,'command_pairs',-1,'native_result',1],99,'independent every actual trace/hold/header/return andlater-command field')
    add('actual-not-readonly',extra[2],['rows',0,'CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],False,'every original callback readonly')
    # Live FE objects have original VRAM-relative descriptors and palette15 ink, never the synthetic RAM layout.
    FE=data['FE_geometry'];g=FE['groups'][0]
    add('FE-synthetic-relative-offset20',paths['FE_geometry'],['groups',0,'captured_original_header',4],20,'every independently recomputed original FE descriptor/palette/VRAM/hold/scope field')
    add('FE-normalized-ink1-palette',paths['FE_geometry'],['groups',0,'palette15_RGB'],[0,0,0],'every independently recomputed original FE descriptor/palette/VRAM/hold/scope field')
    add('FE-stack-context-falsely-persistent',paths['FE_geometry'],['groups',0,'complete_actual_holds',0,'original_paint_context_stack_storage_reused_after_paint'],False,'every independently recomputed original FE descriptor/palette/VRAM/hold/scope field')
    add('FE-wrong-VRAM-bank-offset',paths['FE_geometry'],['groups',0,'complete_actual_holds',0,'actual_bitmap_VRAM_binding','physical_LCDM_offset'],20,'every independently recomputed original FE descriptor/palette/VRAM/hold/scope field')
    observer=base_load(extra[4]);ri=next(i for i,r in enumerate(observer['rows']) if 'complete_readonly_snapshots' in r)
    add('FE-original-R1-snapshot-mismatch',extra[4],['rows',ri,'R1'],observer['rows'][ri]['R1']+2,'original modal paint PC/arguments/full input andNUL')
    c=data['comparison']['groups'][1]
    add('erased-B48-duration-difference',paths['comparison'],['groups',1,'duration_differences'],[],'all actual command/timing/RNG/UI differences retained')
    add('invented-final-B48-PRNG-equality',paths['comparison'],['groups',1,'final_PRNG_seeds'],[3110383956,3110383956],'exact raw RNG/calendar scope')
    add('erased-B48-13-RGB-differences',paths['comparison'],['groups',1,'later_RGB_difference_count'],0,'all complete later framebuffer comparisons retained')
    add('later-changed-pixel-count',paths['later'],['groups',1,'later_RGB_differences',0,'changed_pixels'],1,'every recomputed later pixel/PRNG/duration/native-state scope field')
    add('false-future-random-outcome-equivalence',paths['later'],['matching_selected_final_components_not_full_simulation_orfuture_outcome_equivalence'],False,'explicit later comparison limits')
    watched={Path(p) for p in conf['dependencies']}|{Path(owned.CONFIG),PARENT,ROM,DOC,MAP,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')}
    beforehashes={str(p):sha(p.read_bytes()) for p in watched};contract();baseline=NdsImage.open(owned.CANONICAL);template=NdsImage.open(PARENT);before=bytes(template.rom.save());results=[];check,commit=owned.check_dependencies,owned.commit_image;ROOT.mkdir(parents=True)
    try:
        for i,c in enumerate(cases):
            if i<23:
                priorpath=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356')/f'case_{i:03d}.json';record=base_load(priorpath)
                assert all(record[k]==c[k] for k in ['case','edits','expected_guard']) and record['rejected'] and record['commit_calls']==0
                assert record['dependency_digest_gate_deliberately_bypassed'] and record['whole_input_identity_andall_ROM_bytes_unchanged']
                record.update(exact_completed_case_reused=str(priorpath),exact_completed_case_sha256=sha(priorpath.read_bytes()))
                results.append(record);save(ROOT/f'case_{i:03d}.json',record)
                continue
            image=NdsImage(PARENT,deepcopy(template.rom));original=image.rom;calls=[]
            def fake_load(path):
                canonical=str(Path(path).resolve());return deepcopy(c['changed'][canonical]) if canonical in c['changed'] else base_load(path)
            def no_commit(*args):calls.append('forbidden');raise AssertionError('Rejected input reached a ROM commit')
            owned.load=fake_load;owned.check_dependencies=lambda conf:None;owned.commit_image=no_commit
            try:owned.apply_release(image,baseline)
            except ValueError as error:
                assert c['expected_guard'] in str(error),(c['case'],c['expected_guard'],str(error))
                record={k:v for k,v in c.items() if k!='changed'};record.update(rejected=True,error=str(error),dependency_digest_gate_deliberately_bypassed=True,actual_input_changes_asserted=True,commit_calls=0,whole_input_identity_andall_ROM_bytes_unchanged=True);results.append(record)
            else:raise AssertionError('Unsafe changed input accepted:'+c['case'])
            assert not calls and image.rom is original and bytes(image.rom.save())==before and bytes(template.rom.save())==before
            save(ROOT/f'case_{i:03d}.json',record);print('PRECOMMIT_REJECTIONS',i+1,'of',len(cases),c['case'],flush=True)
    finally:owned.load=base_load;owned.check_dependencies=check;owned.commit_image=commit
    contract();assert beforehashes=={str(p):sha(p.read_bytes()) for p in watched}
    save(ROOT/'actual_changing_semantic_precommit_rejections.json',dict(cases=results,negative_count=len(results),all_expected_semantic_guards_match=True,dependency_gate_bypassed_buttrusted_frozen_andnative_source_guards_preserved=True,all_rejected_inputs_zero_whole_NDS_commits=True,complete_original_object_identity_andserialized_ROM_exact_for_every_failure=True,all_protected_files_hash_exact=True,no_new_ROM_capture_registration_promotion_orcredit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence=beforehashes|{str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('PASS',len(results),'actual-changing semantic precommit rejections;zero commits/input bytes exact.No emulator replay orROMwrite.',flush=True)
