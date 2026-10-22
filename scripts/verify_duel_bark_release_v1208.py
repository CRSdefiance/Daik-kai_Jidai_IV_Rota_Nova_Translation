"""Verify full combined ancestry,exact16 records and reconstructable clean patch."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import duel_bark_editorial as owned
from dk4tool.patch.escape_direct_entries import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from scripts.duel_bark_layout_v1200 import IDS,compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_release_v1205')
ROM=Path('out/all_routes_combined_v1206_candidate.nds')
OLD=Path('out/all_routes_combined_v1189_candidate.nds')


def main():
    out=ROOT/'registered_release_verification.json';assert not out.exists()
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in (ROM,OLD)]
    assert manifest['profile']=='all-routes-unified-v1206' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json');assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored={**registry,'profiles':{k:v for k,v in registry['profiles'].items() if k!='all-routes-unified-v1206'}}
    assert restored==read(ROOT/'registry_before.json')
    assert manifest['batches']==prior['batches'] and len(manifest['batches'])==471 and len(registry['accepted_layers'])==114
    assert all(manifest['checks'].values())
    old,new=map(NdsImage.open,(OLD,ROM))
    assert [p for _,p,raw in old.iter_files() if new.read_file(p)!=raw]==['/COMMON/MESFILE.DK4']
    for p,raw in old.iter_components():
        if p!='/__arm9__.bin':assert new.read_file(p)==raw,p
    c,a=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    oc,oa=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    assert owned.apply_release(oc,oa,owned.CONFIG)[:2]==(c,a)
    before,after=previous_entries(oc,oa),owned.current_entries(c,a)
    doc=read(read(owned.CONFIG)['manuscript']);rows={r['message_id']:r for r in doc['records']}
    assert tuple(rows)==IDS and len(before)==len(after)==3668
    changes=[]
    for b,t in zip(before,after,strict=True):
        n=b.message_id;assert t.text==(compiled(rows[n]) if n in rows else b.text)
        if b.text!=t.text:changes.append(n)
    assert set(changes)<=set(IDS)
    proof=read(ROOT/'repack_plan.json');restored_arm=bytearray(a)
    for at,size in [*proof['metadata_fields'],*proof['owned_ARM9_fields']]:restored_arm[at:at+size]=oa[at:at+size]
    assert bytes(restored_arm)==oa
    builder=Path('scripts/build_integrated_release.py').read_bytes();block=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.replace(block,b'',1)==(ROOT/'builder_before.py').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
    assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not rebuilt.exists();make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt)
    assert rebuilt.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(out,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],
        'canonical_base':manifest['base_rom'],'canonical_sha256':manifest['base_sha256'],'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),
        'clean_input_sha256':clean_sha,'reconstruction':str(rebuilt),'complete_reconstruction_byte_exact':True,
        'all471_batches114_accepted_layers_and_prior_profiles_preserved':True,
        'all16_exact_compiled_reactions_and3652_unselected_texts_preserved':True,'actual_changed_message_IDs':changes,
        'all_routes_graphics_fonts_other_files_components_and_opaque_PREFIX_exact':True,
        'only_COMMON21_metadata_and_owned108_front_changed':True,
        'sections_BSS_cache_arena_ITCM_and123040_staged_payload_exact':True,
        'ordinary_startup_original_timed_feedback_and_completion_credit_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1206 combined ancestry and exact clean-input patch pass.',flush=True)
    print('ROM SHA256',sha(ROM.read_bytes()));print('Patch SHA256',sha(patch.read_bytes()))


if __name__=='__main__':main()
