"""Refresh the complete inherited V158 native paths on the final item target."""

import json
import struct
from pathlib import Path

from dk4tool.patch.gallery_description_release import PAGES
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_promised_words_release import PREFIX, SUFFIX
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_common_copy_arm946_alignment import matrix
from scripts.probe_common_monthly_tribute_preparation import execute as monthly
from scripts.probe_movement_notice_callers import caller as movement_caller
from scripts.verify_gallery_descriptions_research import verify_page as gallery_page
from scripts.verify_ordinary_name_fidelity_research import initialized
from scripts.verify_village_promised_words_research import caller as village_caller


def main():
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    source = Path('work/analysis/generated_item_advice_research_arm9.bin').read_bytes()
    font, common = image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4')
    previous = json.loads(Path('work/analysis/gallery_descriptions_native_proof.json').read_text(encoding='utf-8'))
    plan = json.loads(Path('work/analysis/gallery_description_plan.json').read_text(encoding='utf-8'))
    gallery = []
    for row, (page, mode) in zip(previous['native_pixel_cases'], [(p, m) for p in PAGES for m in (4, 16)], strict=True):
        native = gallery_page(source, plan, page, font, mode)
        if sha(native['pixels']) != row['pixels_sha256']:
            raise ValueError('Item extension changes inherited Gallery pixels')
        gallery.append({'page': page, 'mode': mode, 'pixels_sha256': sha(native['pixels'])})
    duel_previous = json.loads(Path('work/analysis/swordsmanship_status_native_proof.json').read_text(encoding='utf-8'))
    duel = []
    for row in duel_previous['native_pixel_cases']:
        native = raster(source, row['complete_formatted_text'], sword_stats=(row['effective_skill'], row['hp'], row['state']),
                        duel_actor_index=row['duel_actor_index'], surface_size=(156, 12), mode=row['mode'], kanji_font=font)
        if sha(native['pixels']) != row['pixels_sha256']:
            raise ValueError('Item extension changes inherited duel pixels')
        duel.append({k: row[k] for k in ('duel_actor_index', 'mode', 'effective_skill', 'hp', 'state', 'pixels_sha256')})
    entries = common_message_entries(common, source, clean=False)
    if entries != common_message_entries(common, original, clean=False):
        raise ValueError('Item extension changes inherited COMMON selectors/text')
    movement = [movement_caller(source, common, variant, supply_selector=supply)
                for supply in (None, 0, 1) for variant in range(8)]
    village_plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    messages = {r['index']: r for r in village_plan['records'] if r['kind'] == 'MESSAGE'}
    village = []
    for captain in (4, 19):
        for index, start in ((0, 0x78ADC), (2, 0x78BA0), (3, 0x78BB0)):
            village.append(village_caller(source, start, 0, captain, bytes.fromhex(messages[index]['compiled_hex']).decode('ascii')))
        for row in village_plan['records']:
            if row['kind'] == 'CLUE':
                clue = bytes.fromhex(row['compiled_hex']).decode('ascii')
                village.append(village_caller(source, 0x78B8C, row['index'], captain, PREFIX + clue + SUFFIX, clue=clue))
    monthly_rows = []
    for parent_return, table in ((0x02053F40, 0x021189C0), (0x02053EAC, 0), (0x02053F40, 0x021189C4)):
        for amount in (0, 999999, 42949672):
            options = {'word_wrapped': parent_return == 0x02053F40 and table == 0x021189C0,
                       'parent_return': parent_return, 'selector_table': table}
            if monthly(original, 'Payment: %s gold coins.', amount, 0x02428000, **options) != monthly(
                    source, 'Payment: %s gold coins.', amount, 0x02428000, **options):
                raise ValueError('Item extension changes inherited monthly/unrelated scope')
            monthly_rows.append({'parent_return': parent_return, 'selector_table': table, 'amount': amount})
    old_machine, new_machine = initialized(original), initialized(source)
    names = []
    for index in range(207):
        old, new = ordinary_getter(original, index, old_machine), ordinary_getter(source, index, new_machine)
        if old != new or bytes(old_machine.mem_read(old, 128)) != bytes(new_machine.mem_read(new, 128)):
            raise ValueError('Item extension changes inherited ordinary name output')
        names.append({'index': index, 'pointer': new, 'complete_name_preserved': True})
    name_plan = json.loads(Path('work/analysis/ordinary_name_fidelity_plan.json').read_text(encoding='utf-8'))
    owners = []
    for row in name_plan['inherited_pointer_moves']:
        old, new = [struct.unpack_from('<I', raw, row['field'])[0] for raw in (original, source)]
        if old != new or bytes(old_machine.mem_read(old, 128)) != bytes(new_machine.mem_read(new, 128)):
            raise ValueError('Item extension changes inherited shared-name pointer/output')
        owners.append({'field': row['field'], 'pointer': new})
    sailing = []
    for mode in (4, 16):
        old, new = [raster(raw, 'Auto Sail', sailing_status=True, surface_size=(256, 32), kanji_font=font, mode=mode)
                    for raw in (original, source)]
        if any(old[k] != new[k] for k in ('pixels', 'glyph_events', 'sailing_status_draws')):
            raise ValueError('Item extension changes sailing status pixels')
        sailing.append({'mode': mode, 'complete_native_status_pixels_preserved': True})
    result = {'status': 'pass-item-target-inherited-v158-native-paths', 'source_arm9_sha256': sha(original),
              'target_arm9_sha256': sha(source), 'Gallery_pixels': gallery, 'duel_pixels': duel,
              'movement_callers': movement, 'village_callers': village, 'monthly_scope_cases': monthly_rows,
              'ordinary_names': names, 'shared_name_owners': owners, 'sailing_status_pixels': sailing,
              'common_selected_entries_preserved': len(entries), 'shared_copy_alignment_cases': matrix(source),
              'physical_gameplay_verified': False,
              'limitations': ['Fresh native execution on the final target; prior identical Gallery/duel pixel sheets retain their reviewed evidence.',
                              'Complete source/font/pointer/COMMON bytes are inherited; this does not cover every gameplay path.',
                              'Physical cold boot, input, artwork/palette/output and downloaded-save states remain unverified.']}
    Path('work/analysis/item_release_inherited_native_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Pass: inherited14 Gallery/64 duel rasters,24 movement/54 village/9 monthly,207 names/239 owners,3668 COMMON selections and704 alignment cases.')


if __name__ == '__main__':
    main()
