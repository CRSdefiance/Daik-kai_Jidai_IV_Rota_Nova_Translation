"""Exact full centered stack,hot-spring12 changes and clean-input reconstruction."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import hot_spring_editorial as owned
from dk4tool.patch.ship_advice_choice_centering import apply_release as center_choices
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.hot_spring_native_plan_v1615 import current_entries as previous_entries,IDS,compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_release_v1621')
ROM=Path('out/all_routes_combined_v1622_candidate.nds')
OLD=Path('out/screenshot_text_repairs_20261022_candidate.nds')
if __name__=='__main__':
    output=ROOT/'registered_release_verification.json';assert not output.exists()
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]]
    assert manifest['profile']=='all-routes-unified-v1622' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(OLD.read_bytes())=='ba0c910644725ef54a3d817b1754a861244c11fe7c95a06974f32440773bbf54'
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json');assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);restored['profiles'].pop(manifest['profile']);assert restored==read(ROOT/'registry_before_raw.json')
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    expected=prior['batches']+[str(Path('translations/ship_advice_choice_centering_20261022_manuscript_v1.json'))]
    assert manifest['batches']==expected and len(expected)==473
    old,new=NdsImage.open(OLD),NdsImage.open(ROM)
    center=center_choices(old,NdsImage.open('work/clean.nds'),'translations/ship_advice_choice_centering_20261022_release_v1.json')
    assert center['last_terminator_and_following_command_positions_exact']
    assert [p for _,p,data in old.iter_files() if new.read_file(p)!=data]==['/COMMON/MESFILE.DK4']
    for p,data in old.iter_components():
        if p!='/__arm9__.bin':assert new.read_file(p)==data,p
    c,a=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin');oc,oa=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    assert owned.apply_release(oc,oa,owned.CONFIG)[:2]==(c,a)
    before,after=previous_entries(oc,oa),owned.current_entries(c,a);doc=read(read(owned.CONFIG)['manuscript']);rows={r['message_id']:r for r in doc['records']}
    assert tuple(rows)==IDS and len(before)==len(after)==3668
    changed=[]
    for b,t in zip(before,after,strict=True):
        assert t.text==(compiled(rows[b.message_id]) if b.message_id in rows else b.text)
        if b.text!=t.text:changed.append(b.message_id)
    assert changed==[n for n in IDS if n!=2282]
    blocks,target=IlnkContainer.parse(oc).blocks,IlnkContainer.parse(c).blocks
    assert [b for b in range(41) if blocks[b]!=target[b]]==[24]
    proof=read(ROOT/'repack_plan.json');restored_arm=bytearray(a)
    for p in proof['patches']:
        at=p['address']-0x02000000;value=bytes.fromhex(p['source_hex']);assert a[at:at+len(value)].hex()==p['target_hex'];restored_arm[at:at+len(value)]=value
    assert bytes(restored_arm)==oa
    old_code,new_code=[MainCodeFile(v,0x02000000) for v in [oa,a]];shape=lambda o:[(s.ramAddress,len(s.data),s.bssSize) for s in o.sections]
    assert shape(old_code)==shape(new_code) and cache_plan(oa)==cache_plan(a)
    assert all(old_code.sections[i].data==new_code.sections[i].data for i in [1,2,3,4]) and len(new_code.sections[3].data)-48==123040
    builder=Path('scripts/build_integrated_release.py').read_bytes();block=(ROOT/'builder_added_optional_stage.bin').read_bytes();assert builder.replace(block,b'',1)==(ROOT/'builder_before.py').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists() and not rebuilt.exists()
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt);assert rebuilt.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(output,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],'canonical_base':manifest['base_rom'],'canonical_sha256':manifest['base_sha256'],
        'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),
        'clean_input_sha256':clean_sha,'reconstruction':str(rebuilt),'complete_reconstruction_byte_exact':True,'all473_batches114_accepted_layers_and_prior_profiles_preserved':True,
        'all13_compiled_hot_spring_paragraphs_and3656_unselected_or_retained_copies_preserved':True,'actual_changed_message_IDs':changed,
        'all_routes_graphics_fonts_later_screenshot_centering_and_other_components_preserved':True,
        'only_COMMON24_native_metadata_and_existing188_172_selector_spans_changed_from_centered_parent':True,
        'centering_is_exact_source_locked_parent_layer_not_hot_spring_change':center,
        'sections_BSS_cache_arena_ITCM_and123040_staged_payload_exact':True,'ordinary_startup_original_scenes_and_completion_credit_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1622 full centered stack and exact clean-input patch pass. ROM',sha(ROM.read_bytes()),'patch',sha(patch.read_bytes()))
