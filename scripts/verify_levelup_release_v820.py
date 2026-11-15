"""Registered whole-stack preservation, exact tested ROM identity and clean patch."""

from pathlib import Path

from dk4tool.patch import levelup_stat_format as owned
from dk4tool.patch.ceremony_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.levelup_format_runtime_v819 import ROOT
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v820_candidate.nds')


def main():
    registry=read('translations/release_stack.json');prior=read(ROOT/'release_stack_before_v820.json')
    manifest=read(ROM.with_suffix('.manifest.json'));old_manifest=read('out/all_routes_combined_v809_candidate.manifest.json')
    assert manifest['profile']=='all-routes-unified-v820' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and manifest['batches']==old_manifest['batches']
    assert len(manifest['batches'])==470 and not manifest['required_batches']
    assert registry['accepted_layers']==prior['accepted_layers'] and len(registry['accepted_layers'])==114
    assert registry['canonical_baseline']==prior['canonical_baseline']
    assert all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    old,new=[NdsImage.open(p) for p in ('out/all_routes_combined_v809_candidate.nds',str(ROM))]
    a,b=[{p:v for _,p,v in r.iter_files()}|dict(r.iter_components()) for r in (old,new)]
    assert set(a)==set(b) and {p for p in a if a[p]!=b[p]}=={'/__arm9__.bin'}
    common,arm=b['/COMMON/MESFILE.DK4'],b['/__arm9__.bin']
    final,stage=owned.apply_release(common,a['/__arm9__.bin'],owned.CONFIG);assert final==arm
    before=previous_entries(common,a['/__arm9__.bin']);after=owned.current_entries(common,arm)
    assert len(before)==len(after)==3668 and all(x.text==y.text for x,y in zip(before,after,strict=True))
    assert all(phrase in arm for phrase in (b'Continue',b'New Game',b'Options',b'Grand Race',b'Extras',b'Gallery'))
    tested=ROOT/'levelup_v819_RESEARCH_ONLY.nds'
    assert ROM.read_bytes()==tested.read_bytes()
    fixture=read(ROOT/'six_stat_display_fixture_provenance.json')
    assert sha(arm)==fixture['repair_ARM9_sha256']!=fixture['fixture_ARM9_sha256']
    for row in fixture['fixture_only_patches']:
        at=row['address']-0x02000000;assert arm[at:at+4].hex()==row['before_hex']
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'v820_clean_patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt);assert rebuilt.read_bytes()==ROM.read_bytes()
    proof=dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),profile=manifest['profile'],
        canonical_base=registry['canonical_baseline'],COMMON_sha256=sha(common),ARM9_sha256=sha(arm),
        all470_batches114_accepted_layers_and_prior_profiles_unchanged=True,
        all3668_COMMON_strings_all_routes_graphics_help_and_ARM7_exact_to_V809=True,
        only_ARM9_owned160_code_bytes_may_change_from_V809=True,
        entire_registered_ROM_identical_to_completed_ordinary_gameplay_research_ROM=True,
        both_synthetic_growth_fixture_instructions_absent=True,stage_proof=stage,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_source_sha256=sha(clean.read_bytes()),
        clean_input_reconstruction_byte_exact=True,
        broader_ceremony_post_climb_world_state_issue_unresolved=True,
        source335_336_wording_retained_no_new_prose_completion_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'registered_release_verification_v820.json',proof);save(ROM.with_suffix('.verification.json'),proof)
    print('V820 exact tested-ROM identity, inherited470/114 stack,3668 unchanged COMMON entries and clean-input patch pass.',flush=True)
    print('ROM SHA256',proof['candidate_sha256'],flush=True)


if __name__=='__main__':main()
