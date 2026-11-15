import copy
import json
from pathlib import Path

import pytest

from dk4tool.patch.common_tribute_release import apply_release, runtime_component, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def inputs():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    document = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    component = json.loads(Path('translations/common_tribute_runtime_component_v1.json').read_text(encoding='utf-8'))
    return rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), document, component


def test_complete_tribute_repack_matches_output_locks():
    common, arm9, document, component = inputs()
    result = transform(common, arm9, document, component)
    config = json.loads(Path('translations/common_tribute_release_v1.json').read_text(encoding='utf-8'))
    assert sha(result.common) == config['target_common_sha256']
    assert sha(result.arm9) == config['target_arm9_sha256']
    assert len(result.entries) == 3668
    assert len(result.changed_records) == 22
    assert len(result.changed_offsets) == 83


def test_draft_release_cannot_bypass_review(tmp_path):
    common, arm9, _, _ = inputs()
    config = json.loads(Path('translations/common_tribute_release_v1.json').read_text(encoding='utf-8'))
    config['status'] = 'draft-review-incomplete'
    path = tmp_path / 'draft.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='review is incomplete'):
        apply_release(common, arm9, path)


def test_reviewed_experimental_release_matches_final_outputs():
    common, arm9, _, _ = inputs()
    changed_common, changed_arm9, report = apply_release(common, arm9, 'translations/common_tribute_release_v1.json')
    config = json.loads(Path('translations/common_tribute_release_v1.json').read_text(encoding='utf-8'))
    assert sha(changed_common) == config['target_common_sha256']
    assert sha(changed_arm9) == config['target_arm9_sha256']
    assert report['runtime_verified'] is False


def test_runtime_payload_mutation_is_rejected():
    _, arm9, _, component = inputs()
    broken = copy.deepcopy(component)
    broken['payload_hex'] = '00' + broken['payload_hex'][2:]
    with pytest.raises(ValueError, match='payload differs'):
        runtime_component(arm9, broken)


def test_missing_monthly_hook_is_rejected():
    _, arm9, _, component = inputs()
    component['static_patches'] = [r for r in component['static_patches'] if r['offset'] != 0x54160]
    with pytest.raises(ValueError, match='all three hooks'):
        runtime_component(arm9, component)
