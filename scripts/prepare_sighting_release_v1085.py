"""Register source/native-reviewed sighting paragraphs after the fullV1034 stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import reinforcement_sniping_editorial as parent
from dk4tool.patch import sighting_editorial as owned
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sighting_layout_v1069 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_release_v1085')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v7.json')
OLD=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry,registry_raw,before=read(rp),rp.read_bytes(),builder.read_bytes()
    assert 'all-routes-unified-v1086' not in registry['profiles']
    assert 'sighting_editorial' not in registry['profiles']['all-routes-unified-v1034']
    rom=NdsImage.open(OLD);doc=read(MANUSCRIPT);font=read(doc['native_font_proof']);visual=read(doc['visual_review'])
    assert sha(OLD.read_bytes())==doc['current_ROM_sha256'] and not visual['visual_review_pending']
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    assert all(compiled(r).hex()==r['compiled_hex'] for r in doc['records'])
    previous=read(parent.CONFIG)
    for name,digest in previous['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('sighting_editorial')" not in before
    lo=before.index(b"    reinforcement_sniping_editorial = profile_config.get('reinforcement_sniping_editorial')")
    hi=before.index(anchor)
    block=before[lo:hi].replace(b'reinforcement_sniping',b'sighting').replace(b'REINFORCEMENT_SNIPING',b'SIGHTING')
    old=b"changed_records.setdefault(arm_path, []).append('SIGHTING_NATIVE_SELECTION_METADATA')"
    new=b"changed_records.setdefault(arm_path, []).extend(['SIGHTING_NATIVE_SELECTION_METADATA', 'CLOSE_RANGE_BEARING_LABEL', 'ARMED_LATINA_DEFAULT_SHIP_LABEL'])"
    assert block.count(old)==1;block=block.replace(old,new)
    after=before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    audit=ROOT/'native_audit/audit.json';audit.parent.mkdir()
    save(audit,{'batch':str(MANUSCRIPT),'batch_sha256':sha(MANUSCRIPT.read_bytes()),'records':doc['records'],
        'native_label_records':doc['native_label_records'],'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),
        'native_repack_plan':proof,'complete_native_font_cases':2700,'reviewed_native_boundary_warnings':[],
        'all15_current_paragraphs_and_representative2700_case_font_sheets_visually_reviewed':True,
        'all2700_complete_font_planes_independently_match':True,'two_label_native_font_previews_reviewed':True,
        'blocking_errors':0,'unwaived_warnings':0,'standard_story_audit_format_unsupported_COMMON_native_consumer_audit_used':True,
        'actual_registered_ROM_scene_eligibility_UI_and_transitions_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    rows=entries(c,a,proof['directory_sha256']);loader,cases=Loader(a,c),[]
    for mode in ('warm','cold'):
        for i,row in enumerate(rows):
            cases.append(loader.copy(row.message_id,row.text,mode))
            if (i+1)%1000==0:print(mode,i+1,'complete native copies',flush=True)
    loader.reset();sequence=[]
    for block_id in list(range(41))+list(reversed(range(41)))+[0,7,0,7,40,0,40]:
        n=loader.directory[block_id][0]
        for _ in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert len(cases)==7336 and len(sequence)==178 and all(r['reads']==0 for r in sequence[1::2])
    copies=ROOT/'native_copy_proof.json'
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'complete_native_copies':len(cases),'cases':cases,
        'sequenced_cache_cases':sequence,'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,
        'callee_saved_ABI_and_stack_pass':True,'source_and_target_cache_CODE_LOCKS_and_single8KiB_policy_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_actual_gameplay_or_editorial_completion_credit':True})
    extras=[str(Path(__file__)),str(MANUSCRIPT),str(audit),str(copies),parent.CONFIG,
        'dk4tool/patch/sighting_editorial.py','scripts/sighting_layout_v1069.py','scripts/sighting_runtime_v1071.py',
        'scripts/sighting_labels_v1083b.py','scripts/probe_sighting_labels_v1083b.py','scripts/prepare_sighting_manuscript_v1084.py',
        'scripts/verify_sighting_runtime_v1076.py','scripts/probe_sighting_layout_v1070.py',
        'scripts/probe_sighting_balanced_layout_v1072.py','scripts/prepare_sighting_readiness_v1073.py',
        'scripts/prepare_sighting_sentence_v1074.py','scripts/probe_sighting_fonts_v1075.py',
        'scripts/prepare_sighting_readaloud_v1079.py','scripts/probe_sighting_font_delta_v1080.py',
        'scripts/record_sighting_native_checkpoint_v1082.py']
    keys=('reviewed_research_manuscript','native_context_proof','source_context_supplement','native_font_proof','visual_review','native_runtime_proof','native_provider_proof','native_label_proof')
    extras += [doc[k] for k in keys]
    extras += [font['matrix'],font['source_font_proof'],read(font['source_font_proof'])['matrix'],
        'work/analysis/sighting_runtime_v1076/internal_reference_changes.json',
        *read(doc['native_runtime_proof'])['all_completed_source_proofs']]
    old_visual=read(doc['visual_review'])['reviewed_dialogue_visual_proof'];extras.append(old_visual)
    extras += [r['path'] for r in read(old_visual)['all_six_native_review_sheets_visually_inspected']]
    extras += [r['preview'] for r in read(doc['native_label_proof'])['native_font_previews']]
    deps={name:sha(Path(name).read_bytes()) for name in dict.fromkeys([*previous['dependencies'],*extras])}
    config={'format':'dk4-sighting-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'native_copy_proof':str(copies),'native_consumer_audit':str(audit),'dependencies':deps}
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
    save(ROOT/'registry_before.json',registry);(ROOT/'registry_before_raw.json').write_bytes(registry_raw)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1034'])
    profile.update(sighting_editorial=owned.CONFIG,status='experimental',
        description='FullV1034 stack plus15 reviewed fleet-sighting paragraphs614-628 and two bounded native label repairs.',
        note='Natural-dialogue-v2 one-paragraph inputs;416 actor selections,nine bearings20 factions,2700 complete fonts,7336 copies178 cache sequences. Two exact native labels preserve allocations. Fixed212/128-byte runtime and123040 staged bytes. Actual scenes,startup,exact patch and inherited successful-shot gate pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v1086']=profile;save(rp,registry)
    save(ROOT/'registration_provenance.json',{'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'prior_builder_bytes_restored_by_removing_exact_added_block':after.replace(block,b'',1)==before,
        'registry_before_raw_sha256':sha(registry_raw),'registry_after_sha256':sha(rp.read_bytes()),
        'accepted_layers_and_canonical_baseline_preserved':True,'full_stage_replay_matches_native_targets':True,
        'source_and_target_candidate_profiles':['all-routes-unified-v1034','all-routes-unified-v1086'],
        'producer_sha256':sha(Path(__file__).read_bytes()),'registered_ROM_actual_scenes_and_exact_patch_pending':True})
    print('V1086 experimental profile registered;7336 native copies178 cache sequences pass. Build and actual scenes pending.',flush=True)


if __name__=='__main__':main()
