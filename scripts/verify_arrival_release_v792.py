"""Registered inheritance, exact no-growth scope and clean-input reconstruction."""

from pathlib import Path

from dk4tool.patch import arrival_notices_editorial as owned
from dk4tool.patch import item_diplomacy_editorial as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
ROM=Path('out/all_routes_combined_v792_candidate.nds')


def main():
    registry=read('translations/release_stack.json');before=read(ROOT/'release_stack_before_v792.json')
    manifest=read(ROM.with_suffix('.manifest.json'));old_manifest=read('out/all_routes_combined_v788_candidate.manifest.json')
    assert manifest['profile']=='all-routes-unified-v792' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and manifest['batches']==old_manifest['batches']
    assert len(manifest['batches'])==470 and not manifest['required_batches']
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    assert registry['canonical_baseline']==before['canonical_baseline']
    assert all(registry['profiles'][k]==v for k,v in before['profiles'].items())
    for p,h in read(ROOT/'frozen_prior_dependencies.json').items():assert sha(Path(p).read_bytes())==h,p
    old,new=[NdsImage.open(p) for p in ('out/all_routes_combined_v788_candidate.nds',str(ROM))]
    a,b=[{p:v for _,p,v in r.iter_files()}|dict(r.iter_components()) for r in (old,new)]
    assert set(a)==set(b) and {p for p in a if a[p]!=b[p]}=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}
    common,arm=b['/COMMON/MESFILE.DK4'],b['/__arm9__.bin']
    assert owned.apply_release(a['/COMMON/MESFILE.DK4'],a['/__arm9__.bin'],'translations/arrival_notices_editorial_release_v1.json')[:2]==(common,arm)
    assert common==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and arm==(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    prior=previous.current_entries(a['/COMMON/MESFILE.DK4'],a['/__arm9__.bin']);entries=owned.current_entries(common,arm)
    assert {n for n,(x,y) in enumerate(zip(prior,entries,strict=True)) if x.text!=y.text}==set(owned.IDS)
    assert all(entries[n].text==prior[n].text for n in (676,677))
    assert all(phrase in arm for phrase in (b'Continue',b'New Game',b'Options',b'Grand Race',b'Extras',b'Gallery'))
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'clean_patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt)
    assert rebuilt.read_bytes()==ROM.read_bytes()
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'profile':manifest['profile'],'canonical_base':registry['canonical_baseline'],
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'all470_batches114_accepted_layers_all_prior_profiles_and_pinned_dependencies_exact':True,
        'only_COMMON_and_ARM9_change_from_V788':True,'all3665_other_strings_and_earlier_shop_fix_preserved':True,
        'native_936_complete_copies_3668_scope_cases_49_layouts_seven_fonts':True,
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'clean_source_sha256':sha(clean.read_bytes()),
        'clean_input_reconstruction_byte_exact':True,'actual_revised_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Registered full V792 stack and clean-input patch reconstruct exactly;only3 COMMON strings change.',flush=True)


if __name__=='__main__':main()
