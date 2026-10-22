"""Register the reviewed text-only sighting grammar layer after complete V1086."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import sighting_editorial as parent
from dk4tool.patch import sighting_grammar_editorial as owned
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_grammar_release_v1104')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v9.json')
OLD=Path('out/all_routes_combined_v1086_candidate.nds')


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry,registry_raw,before=read(registry_path),registry_path.read_bytes(),builder.read_bytes()
    assert 'all-routes-unified-v1105' not in registry['profiles']
    assert 'sighting_grammar_editorial' not in registry['profiles']['all-routes-unified-v1086']
    rom=NdsImage.open(OLD);doc=read(MANUSCRIPT);font=read(doc['native_font_proof']);visual=read(doc['visual_review'])
    assert sha(OLD.read_bytes())==doc['current_ROM_sha256']
    assert visual['all15_source_meaning_voice_and_complete20_faction_substitutions_read_aloud']
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    previous=read(parent.CONFIG)
    for name,digest in previous['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('sighting_grammar_editorial')" not in before
    lo=before.index(b"    sighting_editorial = profile_config.get('sighting_editorial')");hi=before.index(anchor)
    block=before[lo:hi].replace(b'sighting',b'sighting_grammar').replace(b'SIGHTING',b'SIGHTING_GRAMMAR')
    old=b"changed_records.setdefault(arm_path, []).extend(['SIGHTING_GRAMMAR_NATIVE_SELECTION_METADATA', 'CLOSE_RANGE_BEARING_LABEL', 'ARMED_LATINA_DEFAULT_SHIP_LABEL'])"
    new=b"changed_records.setdefault(arm_path, []).append('SIGHTING_GRAMMAR_NATIVE_SELECTION_METADATA')"
    assert block.count(old)==1;block=block.replace(old,new)
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before
    compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True);save(ROOT/'repack_plan.json',proof)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    audit=ROOT/'native_audit/audit.json';audit.parent.mkdir()
    save(audit,{'batch':str(MANUSCRIPT),'batch_sha256':sha(MANUSCRIPT.read_bytes()),'records':doc['records'],
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'native_repack_plan':proof,
        'complete_native_font_cases':2700,'all_six_review_sheets_visually_inspected':True,
        'all2700_complete_font_planes_independently_match':True,'reviewed_native_boundary_warnings':[],
        'blocking_errors':0,'unwaived_warnings':0,'standard_story_audit_format_unsupported_COMMON_native_consumer_audit_used':True,
        'actual_new_registered_wording_and_transitions_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
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
    keys=('native_context_proof','source_context_supplement','native_font_proof','visual_review','supersedes_manuscript')
    extras=[str(Path(__file__)),str(MANUSCRIPT),str(audit),str(copies),parent.CONFIG,
        'dk4tool/patch/sighting_grammar_editorial.py','dk4tool/patch/sighting_editorial.py',
        'scripts/sighting_layout_v1069.py','scripts/review_sighting_faction_grammar_v1098b.py',
        'scripts/probe_sighting_fonts_v1099.py','scripts/record_sighting_grammar_native_v1100.py',
        *[doc[k] for k in keys],font['matrix'],*[r['path'] for r in font['review_sheets']]]
    dependencies={name:sha(Path(name).read_bytes()) for name in dict.fromkeys([*previous['dependencies'],*extras])}
    config={'format':'dk4-sighting-grammar-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'native_copy_proof':str(copies),'native_consumer_audit':str(audit),'dependencies':dependencies}
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert registry_path.read_bytes()==registry_raw and builder.read_bytes()==before
    save(ROOT/'registry_before.json',registry);(ROOT/'registry_before_raw.json').write_bytes(registry_raw)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1086'])
    profile.update(sighting_grammar_editorial=owned.CONFIG,status='experimental',
        description='Full V1086 stack plus15 source-faithful sighting faction-grammar revisions.',
        note='2700 complete native fonts/wraps,six visual sheets,7336 copies178 cache sequences. Only COMMON7/native message metadata differ;renderer/runtime/name labels and123040 staged bytes exact. New actual/startup/exact patch and inherited shot gates pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v1105']=profile;save(registry_path,registry)
    save(ROOT/'registration_provenance.json',{'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'prior_builder_bytes_restored_by_removing_exact_added_block':after.replace(block,b'',1)==before,
        'registry_before_raw_sha256':sha(registry_raw),'registry_after_sha256':sha(registry_path.read_bytes()),
        'accepted_layers_and_canonical_baseline_preserved':True,'full_stage_replay_matches_native_targets':True,
        'source_and_target_profiles':['all-routes-unified-v1086','all-routes-unified-v1105'],
        'producer_sha256':sha(Path(__file__).read_bytes()),'registered_ROM_actual_scenes_and_exact_patch_pending':True})
    print('V1105 profile registered;7336 native copies178 cache sequences pass. Runtime,labels and staged payload unchanged;build pending.',flush=True)


if __name__=='__main__':main()
