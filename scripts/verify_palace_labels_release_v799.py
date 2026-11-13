"""Registered menu-boundary release, unchanged prose and exact clean patch."""

from pathlib import Path

from dk4tool.patch import palace_label_boundaries as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
ROM=Path('out/all_routes_combined_v799_candidate.nds')


def main():
    registry=read('translations/release_stack.json');before=read(ROOT/'release_stack_before_v799.json')
    manifest=read(ROM.with_suffix('.manifest.json'));old_manifest=read('out/all_routes_combined_v797_candidate.manifest.json')
    assert manifest['candidate_sha256']==sha(ROM.read_bytes()) and manifest['profile']=='all-routes-unified-v799'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches']==old_manifest['batches'] and len(manifest['batches'])==470
    assert all(manifest['checks'].values()) and manifest['final_palace_menu_contract']['all_six_complete_labels_NUL_terminated_inside_owned_strings']
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    assert registry['canonical_baseline']==before['canonical_baseline']
    assert all(registry['profiles'][k]==v for k,v in before['profiles'].items())
    for p,h in read(ROOT/'frozen_prior_dependencies.json').items():assert sha(Path(p).read_bytes())==h,p
    old,new=[NdsImage.open(p) for p in ('out/all_routes_combined_v797_candidate.nds',str(ROM))]
    a,b=[{p:v for _,p,v in r.iter_files()}|dict(r.iter_components()) for r in (old,new)]
    assert set(a)==set(b) and {p for p in a if a[p]!=b[p]}=={'/__arm9__.bin'}
    arm=b['/__arm9__.bin'];assert owned.apply_release(a['/__arm9__.bin'],'translations/palace_label_boundaries_release_v1.json')[0]==arm
    assert arm==(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    owned.verify_final(arm)
    # Every Common record/block/metadata and the complete Palace dialogue
    # dispatcher remain identical to their previously verified V797 components.
    assert a['/COMMON/MESFILE.DK4']==b['/COMMON/MESFILE.DK4']
    assert arm[0x13E840:0x13E950]==a['/__arm9__.bin'][0x13E840:0x13E950]
    cfg=read('translations/palace_editorial_release_v1.json')
    assert cfg['target_common_sha256']==sha(b['/COMMON/MESFILE.DK4'])
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'clean_patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt);assert rebuilt.read_bytes()==ROM.read_bytes()
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'profile':manifest['profile'],'canonical_base':registry['canonical_baseline'],
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(b['/COMMON/MESFILE.DK4']),
        'all470_batches114_accepted_layers_prior_profiles_and_dependencies_preserved':True,
        'only_ARM9_six_label_pointers_and_source_owned_text_spans_change_from_V797':True,
        'entire_COMMON_and_all_route_graphics_and_other_components_identical':True,
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'clean_input_reconstruction_byte_exact':True,
        'actual_menu_and_startup_pending':True,'producer_sha256':sha(Path('scripts/verify_palace_labels_release_v799.py').read_bytes()),
        'full_goal_complete':False})
    print('V799 full stack,all unchanged prose/graphics and exact clean-input patch verified.',flush=True)


if __name__=='__main__':main()
