"""Role-specific equipment retains full text and native allowed/denied colors."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_item_role_state import STATES
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.verify_item_interface_research import ATTRIBUTE_ROLES, verify_page
from scripts.verify_item_parent_layout import compose

TARGET = '642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf'


def verify_case(source, plan, common, font, item, state, mode, slot=2):
    captain = state == 'captain'
    native = verify_page(source, plan, 'main', (0, 2), font, mode, item_index=item, common=common,
                         crew_index=0 if captain else 170, player_name=b'ABCDEFGHIJKLMNOPQR' if captain else None,
                         role_state=state, equipment_slot=slot)
    eligible = state not in ('mismatching', 'unassigned')
    executed = set(native['executed_offsets'])
    required = {0x49A18, 0x49A84, 0x7F044, 0x7DAE4}
    if not captain:
        required |= {0x7DBC0, 0x7E958, 0x397D8}
    if state in ('matching', 'mismatching', 'unassigned', 'secondary-fleet-leader', 'other-fleet-leader'):
        required |= {0x7DB14, 0x2BDD8}
    if state in ('matching', 'mismatching', 'unassigned'):
        required |= {0x81F54, 0x820DC, 0x36C94}
    if state in ('matching', 'mismatching'):
        required |= {0x82E04, 0x132C0}
    if not required <= executed or native['item_provider_contracts'] != ['item_art_provider_not_rendered']:
        raise ValueError('Role-dependent equipment retained a getter callback or skipped a required native branch')
    if native['item_actual_role_eligibility'] != [{'state': state, 'eligible': eligible}]:
        raise ValueError('Actual main caller eligibility result is absent')
    owner = [g for g in native['glyph_events'] if g['y'] == 24 and g['x'] >= 88]
    if not owner or any(g['style'] != (1 if eligible else 4) for g in owner):
        raise ValueError('Complete owner name must retain native allowed/denied display color')
    return native


def main():
    source = Path('work/analysis/generated_item_advice_research_arm9.bin').read_bytes()
    if sha(source) != TARGET:
        raise ValueError('Exact complete item research target required')
    plan = json.loads(Path('work/analysis/generated_item_advice_plan.json').read_text(encoding='utf-8'))
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    common, font = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/GRP/KANJI.FNT')
    indices = []
    for index in range(188):
        record = source[0x11E210 + index * 24:0x11E210 + (index + 1) * 24]
        if record[16] == 4 and record[18] < 21 and record[20] == 115 and not record[21] & 20:
            indices.append(index)
    roles = {ATTRIBUTE_ROLES[source[0x11E210 + index * 24 + 18]] for index in indices}
    if roles != set(range(16)):
        raise ValueError('Actual resource inventory does not cover every private role label')
    parent = parent_crops(source)
    rows, panels = [], []
    destination = Path('work/qa/item_role_eligibility_native')
    destination.mkdir(parents=True, exist_ok=True)
    configurations = [(item, state, slot) for item in indices for state in STATES for slot in (2,)]
    configurations += [(item, state, slot) for item in (indices[0], indices[-1])
                       for state in ('matching', 'mismatching') for slot in (3, 4)]
    for item, state, slot in configurations:
        for mode in (4, 16):
            native = verify_case(source, plan, common, font, item, state, mode, slot)
            pixels, cells = compose(native, parent['requests'])
            row = {'index': item, 'state': state, 'equipment_slot': slot, 'mode': mode,
                   'eligible': native['item_actual_role_eligibility'][0]['eligible'],
                   'draws': native['item_draws'], 'owner_name_color': 1 if state not in ('mismatching', 'unassigned') else 4,
                   'classification': native['item_actual_owner_classifications'],
                   'native_executed_offsets': native['executed_offsets'],
                   'source_pixels_sha256': sha(native['pixels']), 'composed_pixels_sha256': sha(pixels),
                   'complete_owner_glyph_cells': len(cells), 'all_native_assignment_text_pixels_parent_and_style_pass': True}
            rows.append(row)
            if mode == 16 and ((item == indices[0] and slot == 2) or item == indices[-1] and slot == 2 and state == 'matching'):
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                               for c in struct.unpack('<49152H', pixels)])
                panel = panel.resize((768, 576), Image.Resampling.NEAREST)
                panel.save(destination / f'panel_{len(panels)}.png')
                panels.append((f'item {item}; {state}; native owner style {row["owner_name_color"]}', panel))
        if len(rows) % 56 == 0:
            print(f'{len(rows)} native role-specific equipment cases pass', flush=True)
            Path('work/analysis/item_role_eligibility_native_phase.json').write_text(json.dumps({
                'status': 'partial-native-role-equipment-phase', 'target_arm9_sha256': sha(source), 'cases': rows}, indent=2) + '\n', encoding='utf-8')
    sheet = Image.new('RGB', (1552, 604 * ((len(panels) + 1) // 2)), 'white')
    drawing = ImageDraw.Draw(sheet)
    for number, (label, panel) in enumerate(panels):
        x, y = 8 + number % 2 * 776, number // 2 * 604
        drawing.text((x, y + 2), label + '; native text/crops; physical palette/art pending', fill='black')
        sheet.paste(panel, (x, y + 24))
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'pass-native-role-specific-item-eligibility-and-complete-text', 'target_arm9_sha256': sha(source),
              'actual_item_indices': indices, 'actual_required_roles': sorted(roles), 'states': list(STATES), 'cases': rows,
              'visual_review': {'complete': False, 'panel_count': len(panels), 'sheet': str(destination / 'native_sheet.png')},
              'limitations': ['Actual crew/faction constructors and ship initialization execute; assignments/membership/active states are controlled inputs.',
                              'Native item search covers all three accessory slots, captain, faction membership, active fleet leaders, ship captains and assignment lookup.',
                              'Both allowed and denied states retain the complete owner name with original native styles1/4; palette appearance is a physical-display contract.',
                              'All sixteen role labels and every ordinary static role-required resource have complete glyph/pixel/native-parent coverage.',
                              'Outer tables and ship vtable are initialization contracts; artwork/bitmap origin/warm cache and physical controller/display remain unverified.',
                              'This verifies rendering and the mapped eligibility branches, not all recruitability or narrative combinations.',
                              'No ROM or registry changes; full goal remains incomplete.']}
    Path('work/analysis/item_role_eligibility_native_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: {len(rows)} native role equipment rasters, {len(indices)} resources, all16 roles and seven allowed/denied states.')


if __name__ == '__main__':
    main()
