"""Register20 source/native-reviewed paragraphs after the full V997 stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import battle_declaration_editorial as parent
from dk4tool.patch import reinforcement_sniping_editorial as owned
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1033')
MANUSCRIPT=Path('translations/reinforcement_sniping_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v997_candidate.nds')


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry,registry_raw,before=read(rp),rp.read_bytes(),builder.read_bytes()
    assert 'all-routes-unified-v1034' not in registry['profiles']
    assert 'reinforcement_sniping_editorial' not in registry['profiles']['all-routes-unified-v997']
    rom=NdsImage.open(OLD);doc=read(MANUSCRIPT);font=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    assert sha(OLD.read_bytes())==doc['current_ROM_sha256']
    assert not visual['visual_review_pending']
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    assert all(compiled(r).hex()==r['compiled_hex'] for r in doc['records'])
    previous=read(parent.CONFIG)
    for name,digest in previous['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('reinforcement_sniping_editorial')" not in before
    lo=before.index(b"    battle_declaration_editorial = profile_config.get('battle_declaration_editorial')")
    hi=before.index(anchor)
    block=before[lo:hi].replace(b'battle_declaration',b'reinforcement_sniping').replace(b'BATTLE_DECLARATION',b'REINFORCEMENT_SNIPING')
    after=before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    audit=ROOT/'native_audit/audit.json';audit.parent.mkdir()
    save(audit,{'batch':str(MANUSCRIPT),'batch_sha256':sha(MANUSCRIPT.read_bytes()),'records':doc['records'],
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'native_repack_plan':proof,
        'complete_native_font_cases':694,'reviewed_native_boundary_warnings':[],
        'all20_templates_and_representative_extreme_name_canvases_visually_reviewed':True,
        'all694_complete_font_planes_independently_match':True,'blocking_errors':0,'unwaived_warnings':0,
        'standard_story_audit_format_unsupported_COMMON_native_consumer_audit_used':True,
        'actual_registered_ROM_scene_eligibility_UI_and_transitions_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    rows=entries(c,a,proof['directory_sha256']);loader,cases=Loader(a,c),[]
    for mode in ('warm','cold'):
        for i,row in enumerate(rows):
            cases.append(loader.copy(row.message_id,row.text,mode))
            if (i+1)%1000==0:print(mode,i+1,'complete native copies',flush=True)
    loader.reset();sequence=[]
    for block_id in list(range(41))+list(reversed(range(41)))+[0,20,0,20,40,0,40]:
        n=loader.directory[block_id][0]
        for _ in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert len(cases)==7336 and len(sequence)==178 and all(r['reads']==0 for r in sequence[1::2])
    copies=ROOT/'native_copy_proof.json'
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'complete_native_copies':len(cases),'cases':cases,
        'sequenced_cache_cases':sequence,'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,
        'callee_saved_ABI_and_stack_pass':True,'existing_single_cache_policy_bytes_unchanged':True,
        'host_open_read_contract_only_not_actual_ROM_or_hardware':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    extra=[str(Path(__file__)),str(MANUSCRIPT),str(audit),str(copies),owned.CONFIG.replace('_release_v1.json','_manuscript_v1.json'),
        'dk4tool/patch/reinforcement_sniping_editorial.py',parent.CONFIG,
        'scripts/reinforcement_sniping_layout_v1024.py','scripts/reinforcement_sniping_runtime_v1025.py',
        'scripts/research_reinforcement_sniping_v1022b.py','scripts/prepare_reinforcement_sniping_prose_v1023.py',
        'scripts/verify_reinforcement_sniping_runtime_v1029.py','scripts/probe_reinforcement_sniping_layout_v1030.py',
        'scripts/probe_reinforcement_sniping_fonts_v1031.py','scripts/prepare_reinforcement_sniping_native_v1032.py',
        'work/analysis/reinforcement_sniping_v1022b/original_source_fragments.json',
        'work/analysis/reinforcement_sniping_v1029/internal_reference_changes.json']
    extra += [doc[k] for k in ('native_context_proof','source_context_supplement','native_font_proof','visual_review_proof','native_runtime_proof')]
    extra += [font['matrix'],*read(doc['native_runtime_proof'])['all_completed_source_proofs']]
    dependencies={name:sha(Path(name).read_bytes()) for name in dict.fromkeys([*previous['dependencies'],*extra])}
    config={'format':'dk4-reinforcement-sniping-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'native_copy_proof':str(copies),'native_consumer_audit':str(audit),'dependencies':dependencies}
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
    save(ROOT/'registry_before.json',registry);(ROOT/'registry_before_raw.json').write_bytes(registry_raw)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v997'])
    profile.update(reinforcement_sniping_editorial=owned.CONFIG,status='experimental',
        description='Full V997 stack plus20 reviewed reinforcement,covering-fire and Lookout-shot announcements1911-1930.',
        note='Natural-dialogue-v2 one-paragraph inputs;624 voice selections24 wrappers40 faction and57 compact-name fragments;694 complete fonts;7336 copies178 cache sequences. Fixed212/128-byte runtime allocations;actual event eligibility/UI,dismissal/return,startup and exact patch pending. Canonical unchanged.')
    registry['profiles']['all-routes-unified-v1034']=profile;save(rp,registry)
    save(ROOT/'registration_provenance.json',{'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'prior_builder_bytes_restored_by_removing_exact_added_block':after.replace(block,b'',1)==before,
        'registry_before_raw_sha256':sha(registry_raw),'registry_after_sha256':sha(rp.read_bytes()),
        'accepted_layers_and_canonical_baseline_preserved':True,'full_stage_replay_matches_native_targets':True,
        'source_and_target_candidate_profiles':['all-routes-unified-v997','all-routes-unified-v1034'],
        'producer_sha256':sha(Path(__file__).read_bytes()),'registered_ROM_actual_scenes_and_exact_patch_pending':True})
    print('V1034 experimental profile registered;7336 complete copies178 cache sequences pass. Build and actual scenes pending.',flush=True)


if __name__=='__main__':main()
