"""Source review, exact native selectors and full condition-label rasters."""

import json
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sailing_condition_names import BASE, LABELS, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.verify_modal_cursor_native_v272 import verify_ascii
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/analysis/sailing_conditions_v309')
CONFIG = Path('translations/sailing_condition_names_release_v1.json')


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source, clean, canonical = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
                               ('out/all_routes_combined_v307_candidate.nds', 'work/clean.nds',
                                'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(source, clean, canonical)
    (ROOT / 'research_arm9.bin').write_bytes(target)
    assert target[0x82E74:0x82E98] == source[0x82E74:0x82E98]
    before, after = initialized(source), initialized(target)
    selectors = []
    for index in (*range(26), -1, 26, 255, 0x7FFFFFFF):
        outputs = []
        for u in (before, after):
            u.reg_write(UC_ARM_REG_R0, index & 0xFFFFFFFF)
            u.reg_write(UC_ARM_REG_R1, 0x02460000)
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.emu_start(BASE + 0x82E74, STOP, count=100)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
            pointer = u.reg_read(UC_ARM_REG_R0)
            if 0 <= index < 26:
                value = bytes(u.mem_read(pointer, 64)).split(b'\0')[0]
            else:
                assert pointer == 0x02460000
                value = None
            outputs.append(value)
        if 0 <= index < 26:
            assert outputs == [LABELS[index][0].encode('cp932'), LABELS[index][1].encode('ascii')]
        selectors.append({'index': index, 'original_Japanese_and_full_English_selector_returns_exact': True,
                          'native_return_stack_and_invalid_fallback_preserved': True})
    rasters = []
    for japanese, english in LABELS:
        rasters.append({'Japanese': japanese, 'English': english, **verify_ascii(target, english.encode('ascii'))})
    # Actual warning template is reviewed separately from the label-only cases.
    warning = verify_ascii(target, b'Admiral! Reefs!')
    report_path = Path('work/emulation_v193/weapon_acquisition_v309/capture_report.json')
    capture = json.loads(report_path.read_text(encoding='utf-8'))
    assert capture['cold_boot'] and not capture['savestate_loaded'] and not capture['callback_errors']
    assert capture['frames'] == 32800 and capture['ROM_sha256'] == sha(Path('out/all_routes_combined_v307_candidate.nds').read_bytes())
    for row in capture['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    inputs = [r for r in capture['scripted_input_schedule'] if r['start'] <= 28800]
    save(ROOT / 'reef_replay_inputs.json', inputs)
    proof = {**plan, 'native_selector_cases': selectors, 'complete_native_label_rasters': rasters,
             'complete_native_reef_warning_raster': warning,
             'actual_Japanese_reef_warning_frame': 28800, 'source_capture_report': str(report_path),
             'source_capture_report_sha256': sha(report_path.read_bytes()),
             'full_staged_pool_copy_cache_boot_and_arena_checks_pass': True,
             'actual_English_warning_replay_pending': True, 'full_goal_complete': False}
    save(ROOT / 'native_proof.json', proof)
    save(CONFIG, {'format': 'dk4-sailing-condition-names-release-v1',
                  'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
                  'source_review': 'All26 original table terms reviewed in their sailing weather/creature/crew/hull context. Complete natural English names; shared warning substitutions retain original templates.',
                  'localization_notes': {'雷': 'Lightning is the visible dangerous weather phenomenon rather than its sound.',
                                         '流氷': 'Drift Ice means floating sea ice, without inventing icebergs.',
                                         '水漏れ': 'Leaks retains water ingress without overstating flooding.',
                                         '謎の泡': 'Strange Bubbles preserves the unexplained phenomenon.',
                                         '化け魚': 'Monster Fish preserves the fantastic creature rather than a named real species.'},
                  'verification_evidence_sha256': {str(ROOT / 'native_proof.json'): sha((ROOT / 'native_proof.json').read_bytes())},
                  'status': 'experimental-native-verified-actual-English-warning-pending'})
    print(json.dumps({'full_names': len(rasters), 'native_selector_cases': len(selectors),
                      'pool_remaining_bytes': plan['owned_pool_remaining_bytes'], 'target_arm9_sha256': sha(target)}))


if __name__ == '__main__':
    main()
