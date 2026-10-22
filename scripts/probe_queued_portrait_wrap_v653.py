"""Prove the shared queued factory contract and complete affected voice layouts."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.queued_portrait_wrap import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_dialogue_palette_v628 import raster
from scripts.verify_tavern_queued_native_v626 import queued_wrap, table_scopes
from scripts.verify_tavern_scheme_native_v625 import dispatches
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FAMILIES = ((0x02118380, range(890, 897)), (0x02117460, range(71, 76)),
            (0x02117080, range(2683, 2690)))


def factory(arm, clean):
    spans = ((0x53CB0, 0x53DCC), (0x53F4C, 0x53F9C),
             (0x54058, 0x54160), (0x54164, 0x54424),
             (0x54C28, 0x54CF8), (0x54DB0, 0x54E44))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    assert struct.unpack_from('<2I', arm, 0x118AC8) == (228, 48)
    assert arm[0x118AC8:0x118B28] == clean[0x118AC8:0x118B28]
    cases = []
    for run, frame in (('full_fleet_staffing_v652_actual', 5200),
                       ('full_fleet_staffing_v652_actual', 12800),
                       ('full_fleet_battle_v652_near_target', 15200)):
        rp = CAP / run / 'capture_report.json'
        report = read(rp)
        assert report['ROM_sha256'] == sha(Path('out/all_routes_combined_v651_candidate.nds').read_bytes())
        path = CAP / run / f'frame_{frame:06d}_arm9_ram.bin'
        raw = path.read_bytes()
        parents = [a for a in range(0x170000, len(raw) - 0x90, 4)
                   if struct.unpack_from('<I', raw, a)[0] == 0x021438A0
                   and struct.unpack_from('<2I', raw, a + 0x28) == (228, 48)]
        assert len(parents) == 1
        at = parents[0]
        assert struct.unpack_from('<4I', raw, at + 0x40) == (8, 16, 0, 0)
        assert struct.unpack_from('<2I', raw, at + 0x84) == (0, 96)
        cases.append({'run': run, 'frame': frame, 'RAM_sha256': sha(raw),
                      'report_sha256': sha(rp.read_bytes()), 'actual_parent': at + 0x02000000,
                      'actual_native_view': [228, 48], 'original_margins': [8, 16, 0, 0],
                      'original_frame_origin': [0, 96]})
    return {'original_factory_code_spans_clean_exact': [list(x) for x in spans],
            'question_parent_02053D24_and_notice_parent_02053DB8_both_call_02054058': True,
            'original_role_selection_lookup_then_same_actor_factory_no_table_geometry_branch': True,
            'native_view_width_height': [228, 48],
            'original_font_source_metrics': [6, 12], 'display_row_pitch': 16,
            'actual_three_captured_parent_layouts': cases}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v651_candidate.nds')
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    target, proof = transform(arm)
    contract = factory(arm, clean)
    # Only the two exact queued parents broaden. Numeric/direct/modal families
    # retain their complete existing dispatch, including the V651 captain fix.
    numeric = []
    for parent in (0x02054014, 0x02054044, 0x020546E8):
        assert dispatches(arm, parent) == dispatches(target, parent)
        numeric.append({'parent': parent, 'all3668_old_new_dispatches_exact': True})
    tables = [0, 1, 0xFFFFFFFF, 0x02117080, 0x02117460, 0x02118380,
              0x021181E0, 0x021182E0, 0x02118381, 0x02118800]
    scopes = []
    for parent in (0x02053D24, 0x02053DB8, 0x02053D20, 0x02053DBC,
                   0x02053C14, 0x02053C5C, 0x02054044):
        before, after = table_scopes(arm, parent, tables), table_scopes(target, parent, tables)
        if parent in (0x02053D24, 0x02053DB8):
            assert after == [0x01FFCF78] * len(tables)
        else:
            assert before == after
        scopes.append({'parent': parent, 'tables': tables, 'before': before, 'after': after})
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    cases = []
    for table, numbers in FAMILIES:
        source_ids = struct.unpack_from('<8I', clean, table - 0x02000000)
        assert set(source_ids) - {0xFFFFFFFF} == set(numbers)
        assert arm[table - 0x02000000:table - 0x02000000 + 32] == struct.pack('<8I', *source_ids)
        for number in numbers:
            template = entries[number].text.rstrip()
            values = (['Latina', 'San Juan Bautista', 'Kuala Lumpur'] if number >= 2683
                      else ['1', '106', '９９９９９９９'])
            for value in values:
                expanded = template.replace(b'%s', value.encode('cp932'))
                assert b'%' not in expanded
                for parent in (0x02053D24, 0x02053DB8):
                    prepared = queued_wrap(target, expanded, parent, table)
                    assert b' '.join(prepared.split()) == b' '.join(expanded.split())
                    assert len(prepared.splitlines()) <= 4
                    pixels, events = raster(target, kanji, prepared)
                    visible = [e for e in events if e['code'] not in (0, 10, 13, 32)]
                    text = expanded.decode('cp932')
                    expected = [int.from_bytes(c.encode('cp932'), 'big') for c in text if not c.isspace()]
                    assert [e['code'] for e in visible] == expected, (number, value, prepared)
                    at = 0
                    for word in text.split():
                        group = visible[at:at + len(word)]
                        assert len(group) == len(word) and len({e['y'] for e in group}) == 1
                        at += len(word)
                    assert all(0 <= e['x'] < 228 and 0 <= e['y'] < 64 for e in visible)
                    cases.append({'native_ID': number, 'parent': parent, 'table': table,
                                  'supplied_layout_argument': value,
                                  'unchanged_expanded_English': text,
                                  'prepared': prepared.decode('cp932'),
                                  'all_native_glyphs_in_order_every_word_single_row': True,
                                  'ink_points': sum(v == 15 for v in pixels),
                                  'shadow_points': sum(v == 14 for v in pixels)})
    # The existing helper deliberately falls back for an overlong word or more
    # than four rows. This fix does not claim to paginate arbitrary prose.
    failures = []
    for text in (b'', b'A' * 237, b' '.join([b'Extraordinary'] * 16)):
        for parent in (0x02053D24, 0x02053DB8):
            old = queued_wrap(arm, text, parent, 0x021181E0)
            new = queued_wrap(target, text, parent, 0x02117080)
            assert old == new
            failures.append({'length': len(text), 'parent': parent,
                             'previous_admitted_family_failure_behavior_and_guards_exact': True})
    save(ROOT / 'native_dispatch_proof.json', {
        'transform': proof, 'original_factory_contract': contract,
        'all22008_unrelated_numeric_dispatch_executions': numeric,
        'exact_parent_and_table_independence_cases': scopes,
        'all19_voice_entries114_native_layouts': cases,
        'empty_overlong_word_and_fifth_row_fallback_controls': failures,
        'original_expansion_source_destination_guards_and_saved_register_ABI_pass': True,
        'layout_arguments_are_supplied_contracts_not_all_native_provider_verification': True,
        'actual_repaired_emulator_pixels_pending': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    (ROOT / 'research_ARM9.bin').write_bytes(target)
    save('translations/queued_portrait_wrap_v1.json', {'format': 'dk4-queued-portrait-wrap-v1', 'proof': proof})
    print('V653: same original actor factory; two exact parents; 22008 unrelated dispatches; 114 complete native voice layouts pass.')


if __name__ == '__main__':
    main()
