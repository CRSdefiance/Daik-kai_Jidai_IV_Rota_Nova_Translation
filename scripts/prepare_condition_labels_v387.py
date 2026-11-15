"""Review condition semantics and retain all neighboring source strings and code."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/condition_labels_v387')
ROM = Path('out/all_routes_combined_v383_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open(ROM)
    arm = parent.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    code = MainCodeFile(arm, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 3880
    confused = 0x01FFC000 + len(before[4])
    hurt = confused + 12
    code.sections[4].data.extend(b'Confused\0\0\0\0Hurt\0\0\0\0')
    rows = [
        (0x1483C4, 0x021482BC, confused, 'Mood', 5, '混乱', 'Dazed', 'Confused',
         'Mental confusion; Confused is clearer than a word which can suggest a physical daze.'),
        (0x1483D0, 0x021482E4, hurt, 'Health', 2, '軽傷', 'Wounded', 'Hurt',
         'Minor injury. Hurt gives the lighter condition a natural concise label.'),
        (0x1483D4, 0x021482A4, 0x021482E4, 'Health', 3, '重傷', 'Injured', 'Wounded',
         'Serious injury. Wounded distinguishes the stronger condition from Hurt in the health-state sequence.'),
    ]
    review = []
    for field, old, new, group, state, japanese, current, english, rationale in rows:
        assert struct.unpack_from('<I', clean, field)[0] == old
        assert clean[old - 0x02000000:].split(b'\0', 1)[0].decode('cp932') == japanese
        assert struct.unpack_from('<I', arm, field)[0] == old
        assert arm[old - 0x02000000:].split(b'\0', 1)[0].decode() == current
        struct.pack_into('<I', code.sections[0].data, field, new)
        review.append({'field': field, 'group': group, 'state': state, 'old_pointer': old,
                       'new_pointer': new, 'Japanese': japanese, 'old_English': current,
                       'English': english, 'rationale': rationale,
                       'review': dict.fromkeys(['source', 'context', 'localization', 'naturalness', 'formatting'], True)})
    assert len(code.sections[4].data) == 3900
    assert len(code.sections[4].data) <= 4096
    target = bytes(code.save())
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:3880]) == before[4]
    restored = bytearray(parsed.sections[0].data)
    for row in review:
        struct.pack_into('<I', restored, row['field'], row['old_pointer'])
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    parent.replace_file('/__arm9__.bin', target)
    parent.save(ROOT / 'research_only_conditions.nds')
    plan = {'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(target),
            'original_autoload_length': 3880, 'new_autoload_length': 3900,
            'autoload_suffix_hex': bytes(parsed.sections[4].data[3880:]).hex(),
            'pointer_changes': review, 'all_old_strings_including_Spirit_and_Luck_exact': True,
            'no_new_code_or_arenas_or_layout_changes': True,
            'actual_new_condition_states_gameplay_not_proven': True, 'research_only': True}
    (ROOT / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('translations/condition_labels_review_v1.json').write_text(
        json.dumps({'target_locale': 'en-US', 'records': review}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared Confused / Hurt / Wounded: three table pointers,20 bytes in existing reserved area; original strings/code intact.')


if __name__ == '__main__':
    main()
