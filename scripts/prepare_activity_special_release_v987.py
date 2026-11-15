"""Register17 guarded mixed-consumer comments after the complete V981 release stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import activity_special_editorial_v987b as owned,mood_comments_editorial_v981b as parent
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v987')
MANUSCRIPT=Path('translations/activity_special_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v981_candidate.nds')

def main():
    assert not Path(owned.CONFIG).exists() and not (ROOT/'registry_before.json').exists()
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert 'all-routes-unified-v987' not in registry['profiles']
    rom=NdsImage.open(OLD);doc=read(MANUSCRIPT);assert sha(OLD.read_bytes())==doc['current_ROM_sha256']
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    save(ROOT/'repack_plan.json',proof);(ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    rows=entries(c,a,proof['directory_sha256']);loader=Loader(a,c);cases=[]
    for mode in ('warm','cold'):
        for i,row in enumerate(rows):
            cases.append(loader.copy(row.message_id,row.text,mode))
            if (i+1)%1000==0:print(mode,i+1,'complete',flush=True)
    loader.reset();sequence=[]
    for block in list(range(41))+list(reversed(range(41)))+[0,18,0,18,40,0,40]:
        n=loader.directory[block][0]
        for _ in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert all(r['reads']==0 for r in sequence[1::2])
    copies=ROOT/'native_copy_proof.json'
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'complete_native_copies':len(cases),'cases':cases,
        'sequenced_cache_cases':sequence,'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,
        'callee_saved_ABI_and_stack_pass':True,'existing_single_cache_policy_bytes_unchanged':True,
        'host_open_read_contract_only_not_actual_ROM_or_hardware':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    previous=read(parent.CONFIG)
    for name,digest in previous['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    extra=['dk4tool/patch/activity_special_editorial_v987b.py','dk4tool/patch/activity_special_editorial.py',
        'dk4tool/patch/mood_comments_editorial_v981b.py',parent.CONFIG,'scripts/prepare_activity_special_release_v987.py',
        'scripts/activity_special_layout_v986.py','scripts/activity_special_layout_v986b.py',
        'translations/activity_special_native_modal_layout_v1.json','scripts/freeze_activity_modal_layout_v987.py',
        'scripts/research_next_comments_v983.py','scripts/prepare_activity_special_context_v984.py',
        'scripts/prepare_activity_special_prose_v985.py','scripts/probe_activity_special_fonts_v986.py',
        'scripts/prepare_activity_special_native_v986.py','scripts/audit_activity_special_native_v987.py',
        'translations/activity_special_editorial_manuscript_v1.json','work/analysis/next_comments_v983/source_selection_research.json',
        'work/analysis/activity_special_v984/source_context_packet.json',
        'work/analysis/activity_special_v985/source_context_and_faithfulness_review.json',
        'work/analysis/activity_special_v986/native_font_proof.json','work/analysis/activity_special_v986/visual_review.json',
        'work/analysis/activity_special_v987/native_generated_layout_provenance.json',
        'work/analysis/activity_special_v987/native_audit/audit.json',str(copies)]
    dependencies={name:sha(Path(name).read_bytes()) for name in [*previous['dependencies'],*extra]}
    config={'format':'dk4-activity-special-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_copy_proof':str(copies),
        'native_consumer_audit':'work/analysis/activity_special_v987/native_audit/audit.json','dependencies':dependencies}
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes();anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('activity_special_editorial')" not in before
    lo=before.index(b"    mood_comments_editorial = profile_config.get('mood_comments_editorial')");hi=before.index(anchor)
    block=before[lo:hi].replace(b'mood_comments',b'activity_special').replace(b'MOOD_COMMENTS',b'ACTIVITY_SPECIAL')
    block=block.replace(b'activity_special_editorial_v981b',b'activity_special_editorial_v987b')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert read(registry_path)==registry and builder.read_bytes()==before
    save(ROOT/'registry_before.json',registry);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block);builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v981'])
    profile.update(activity_special_editorial=owned.CONFIG,status='experimental',
        description='Complete V981 stack plus17 activity2,Chapel refusal and special-character comments1872-1888.',
        note='52 activity,16 special,12 legality and3 original refusal controls;20 Deck font cases and3 distinct popup font cases;7336 copies and178 cache sequences pass. Modal bytes are generated by the existing native balanced formatter and source-locked;no runtime code or membership change. Actual modal geometry,dismissal,representative Deck samples,startup and exact patch remain pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v987']=profile;save(registry_path,registry)
    save(ROOT/'registration_provenance.json',{'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'builder_prior_bytes_restored_by_removing_exact_optional_block':after.replace(block,b'',1)==before,
        'registry_before_sha256':sha((ROOT/'registry_before.json').read_bytes()),'registry_after_sha256':sha(registry_path.read_bytes()),
        'full_stage_replay_matches_native_repacked_targets':True,'producer_sha256':sha(Path(__file__).read_bytes()),'actual_RGB_and_exact_patch_pending':True})
    print('V987 registered;17 reviewed entries,7336 complete copies and178 cache sequences pass;actual samples remain.')

if __name__=='__main__':main()
