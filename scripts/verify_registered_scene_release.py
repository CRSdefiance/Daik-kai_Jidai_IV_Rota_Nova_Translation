"""Verify a cumulative scene successor and reconstruct it exactly from clean input."""
import argparse
from collections import Counter
from pathlib import Path
import sys
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as verify_baseline

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('candidate','parent','reconstruction','preparation','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    manifest_path=args.candidate.with_suffix('.manifest.json');manifest=load(manifest_path)
    preparation=load(args.preparation);rebuilt=load(args.reconstruction)
    registry_path=Path(manifest['release_stack']);registry=load(registry_path)
    assert sha(registry_path.read_bytes())==manifest['release_stack_sha256']
    assert manifest['profile']==preparation['profile']
    assert sha(args.candidate.read_bytes())==manifest['candidate_sha256']==preparation['target_ROM_sha256']==rebuilt['research_ROM_sha256']
    assert all(manifest['checks'].values()) and manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    profile=registry['profiles'][manifest['profile']]
    config_path=Path(profile['late_editorial_extensions'][-1]['config']);config=load(config_path)
    assert str(config_path)==preparation['config'] and sha(config_path.read_bytes())==preparation['config_sha256']
    parent_manifest=load(args.parent.with_suffix('.manifest.json'))
    assert sha(args.parent.read_bytes())==parent_manifest['candidate_sha256']==rebuilt['parent_sha256']
    assert manifest['batches'][:-2]==parent_manifest['batches'][:-1]
    assert manifest['batches'][-2:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds']))]
    assert len(manifest['batches'])==len(parent_manifest['batches'])+1
    present={str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert len(registry['accepted_layers'])==preparation['accepted_layers']==114
    assert all(row.get('baked_into_baseline') is True or str(Path(row['batch']).resolve()).casefold() in present for row in registry['accepted_layers'])
    old_registry=load(Path(args.preparation).parent/'release_stack_before.json')
    assert registry['accepted_layers']==old_registry['accepted_layers']
    assert all(registry['profiles'][key]==value for key,value in old_registry['profiles'].items())
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']==sha(Path(registry['canonical_baseline']['path']).read_bytes())
    candidate,parent=NdsImage.open(args.candidate),NdsImage.open(args.parent)
    changed=[path for _,path,data in parent.iter_files() if candidate.read_file(path)!=data]
    approved=load(config['manuscript']);path=approved['file_path']
    assert changed==[path] and all(candidate.read_file(p)==data for p,data in parent.iter_components())
    old,new=[IlnkContainer.parse(image.read_file(path)).blocks for image in (parent,candidate)]
    assert len(old)==len(new)
    changed_blocks=[n for n,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]
    assert changed_blocks==config['blocks']
    for group in rebuilt['groups']:
        assert new[group['block']]==Path(group['target_block']).read_bytes()
    for internal in set(manifest['changed_records'])|set(parent_manifest['changed_records']):
        added=Counter(manifest['changed_records'].get(internal,[]))-Counter(parent_manifest['changed_records'].get(internal,[]))
        removed=Counter(parent_manifest['changed_records'].get(internal,[]))-Counter(manifest['changed_records'].get(internal,[]))
        assert not removed
        assert added==(Counter(row['id'] for row in approved['records']) if internal==path else Counter())
    assert args.candidate.read_bytes()==Path(rebuilt['research_ROM']).read_bytes()
    old_argv=sys.argv
    try:
        sys.argv=['verify_release_baseline',str(registry['canonical_baseline']['path']),str(args.candidate)]
        for internal in manifest['changed_paths']:sys.argv+=['--allow-path',internal]
        verify_baseline()
    finally:sys.argv=old_argv
    clean=Path(config['clean_ROM']);assert sha(clean.read_bytes())==config['clean_ROM_sha256']
    patch=args.candidate.with_suffix('.xdelta');assert not patch.exists()
    args.out.mkdir(parents=True)
    reconstructed=args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,args.candidate,patch);apply_xdelta(clean,patch,reconstructed)
    assert reconstructed.read_bytes()==args.candidate.read_bytes()
    save(args.out/'registered_release_verification.json',dict(
        candidate=str(args.candidate),candidate_sha256=manifest['candidate_sha256'],
        manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),
        profile=manifest['profile'],registry_sha256=manifest['release_stack_sha256'],
        canonical_base=manifest['base_rom'],canonical_sha256=manifest['base_sha256'],
        parent=str(args.parent),parent_sha256=parent_manifest['candidate_sha256'],
        changed_internal_files=changed,changed_blocks={path:changed_blocks},
        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,
        complete_stack_entries=len(manifest['batches']),accepted_layers=len(registry['accepted_layers']),
        passing_release_checks=len(manifest['checks']),new_contextual_records=len(approved['records']),
        byte_exact_to_checked_research_image=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),
        clean_input_sha256=sha(clean.read_bytes()),exact_clean_reconstruction=str(reconstructed),
        reconstructed_sha256=sha(reconstructed.read_bytes()),clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True,experimental_not_promoted=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    pinpath=Path('translations/rom_retention_pins.json');pins=load(pinpath)
    for rom in [args.candidate,reconstructed]:
        resolved=str(rom.resolve())
        if not any(row['path']==resolved for row in pins):
            pins.append(dict(path=resolved,reason='Preserve registered cumulative editorial candidate and exact clean-input reconstruction;main promotion pending user acceptance.'))
    save(pinpath,pins)
    print('Registered cumulative stack and exact clean-input patch verified;own startup pending.')

if __name__=='__main__':
    main()
