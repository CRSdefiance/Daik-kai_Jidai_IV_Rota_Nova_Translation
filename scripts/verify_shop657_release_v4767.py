"""Verify complete cumulative ancestry, exact narrow diff and clean-input patch."""
from copy import deepcopy
from pathlib import Path
import json

from dk4tool.patch import shop_657_reflow as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_release_v4767')
ROM=Path('out/all_routes_combined_v4766_candidate.nds')
OLD=Path('out/all_routes_combined_font_and_square_fixed_20261027.nds')
CONFIG=Path('translations/shop657_full_width_reflow_release_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    terminal=read('work/analysis/shop657_build_v4766/terminal.json')
    assert terminal['terminal'] and terminal['returncode']==0
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]]
    digest=sha(ROM.read_bytes());stack=read('translations/release_stack.json')
    reg=read('work/analysis/shop657_registration_v4765/registration_receipt.json')
    assert manifest['candidate_sha256']==digest and manifest['profile']==reg['profile']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==reg['registry_after_sha256']
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert all(manifest['checks'].values()) and len(manifest['checks'])==18
    assert sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    assert len(stack['accepted_layers'])==114 and stack['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    restored=deepcopy(stack);restored['profiles'].pop(manifest['profile'])
    assert restored==read('work/analysis/shop657_registration_v4765/registry_before.json')
    normal=lambda s:str(s).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+['translations/shop657_full_width_reflow_manuscript_v1.json']
    assert len(manifest['batches'])==561
    parent,current=NdsImage.open(OLD),NdsImage.open(ROM)
    files=[p for _,p,data in parent.iter_files() if current.read_file(p)!=data]
    components=[p for p,data in parent.iter_components() if current.read_file(p)!=data]
    assert files==['/COMMON/MESFILE.DK4'] and components==[]
    expected=ROOT/'expected_by_registered_layer.nds'
    baseline=NdsImage.open(manifest['base_rom']);report=owned.apply_release(parent,baseline,CONFIG)
    ROOT.mkdir(parents=True);parent.save(expected)
    assert expected.read_bytes()==ROM.read_bytes()
    bound=manifest['relocations']['/COMMON/MESFILE.DK4']['shop657_full_width_reflow']
    assert bound['proof']==report and bound['release_config_sha256']==sha(CONFIG.read_bytes())
    patch=ROM.with_suffix('.xdelta');reconstruction=ROOT/'clean_patch_reconstruction.nds'
    assert not patch.exists() and not reconstruction.exists()
    clean=Path('work/clean.nds');clean_hash=sha(clean.read_bytes())
    assert clean_hash=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_hash
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    for p in [ROM,expected,reconstruction]:
        assert all(Path(v['path']).resolve()!=p.resolve() for v in values)
        values.append(dict(path=str(p.resolve()),reason='Shop657 full-width reflow cumulative build/proof; preserve for continuing editorial goal. SHA256 '+sha(p.read_bytes())))
    newline='\r\n' if b'\r\n' in before else '\n'
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n',newline).encode('utf-8')
    assert pins.read_bytes()==before;pins.write_bytes(encoded)
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,
        manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=manifest['profile'],batch_count=561,accepted_layers=114,checks=manifest['checks'],
        parent=str(OLD),parent_sha256=sha(OLD.read_bytes()),files_changed=files,components_changed=components,
        all_four_story_files_fonts_graphics_ARM9_ARM7_tables_and_every_other_file_exact=True,
        expected_whole_ROM_by_scoped_layer=str(expected),expected_whole_ROM_equal=True,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_hash,
        clean_patch_reconstruction=str(reconstruction),exact_clean_input_reconstruction=True,
        preserved_promoted_main='all-routes-unified-v4701',native_copies=7336,atomic_negatives=16,
        regression_tests=dict(passed=94,elapsed_seconds=5.35,source='completed terminal run',
            includes_78_existing_release_dialogue_cases_and16_unregistered_planner_research_cases=True),
        actual_new_gameplay_pending=True,no_added_editorial_credit=True,
        pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),all_existing_ROMs_preserved=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),batches=561,
               changed_files=files,clean_patch_exact=True),flush=True)
