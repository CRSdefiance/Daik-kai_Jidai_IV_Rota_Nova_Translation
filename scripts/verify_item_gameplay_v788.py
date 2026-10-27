"""Actual revised Guild prompt/cancel flow and exact ordinary startup controls."""

import struct
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import item_diplomacy_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_shared_newgame_v782 as startup
from scripts.record_navigation_v327 import dark_text
from scripts.verify_item_release_v788 import ROM, ROOT
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def capture(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 8400 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    ram, frames = {}, {}
    for row in report.get('read_only_capture_RAM_snapshots', [])+report.get('read_only_pause_RAM_snapshots', []):
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] == 0x400000 and row['read_only_export'] and sha(raw) == row['sha256']
        if row['frame'] in ram: assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    return path, report, frames, ram


def main():
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    FunctionType(startup.main.__code__, {**startup.__dict__, 'ROOT': ROOT,
        'REPORT': CAP/'item_v788_newgame/capture_report.json',
        'OLD': CAP/'shared_v782_newgame/capture_report.json', '__file__': str(Path(__file__).resolve())})()
    old_path, old, old_frames, old_ram = capture('item_guild_v786')
    new_path, new, new_frames, new_ram = capture('item_v788_guild')
    assert new['ROM_sha256'] == sha(ROM.read_bytes())
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = owned.current_entries(common, arm)
    blocks = IlnkContainer.parse(common).blocks
    raw_ptr, wrapped_ptr, owner = [struct.unpack_from('<I', arm, at)[0] for at in (0x5444C, 0x54450, 0x552A0)]
    entry = entries[1071]
    assert entry.text == b' Which one would you like?'
    raw = new_ram[7200]
    assert cstring(raw, owner+0x2030) == cstring(raw, raw_ptr) == entry.text
    assert raw.count(blocks[entry.block]) == 1
    assert struct.unpack_from('<I', raw, 0x279678)[0] == 5
    formatted = cstring(raw, wrapped_ptr)
    case = next(c for c in read(ROOT/'production_layout/verification.json')['cases'] if c['id'] == 1071)
    assert formatted.hex() == case['formatted_hex']
    image = Image.open(new_frames[7200]['path']).convert('RGB')
    glyph = dark_text(GameAsciiFont.from_arm9(arm), 'Which one would you like?', image, (12, 294, 250, 322))
    pairs = []
    frames = (1, 60, 180, 3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000, 6400, 6800, 7200, 7600, 8000, 8400)
    for f in frames:
        before, after = [Image.open(rows[f]['path']).convert('RGB') for rows in (old_frames, new_frames)]
        diff = ImageChops.difference(before, after)
        if f == 7200:
            ImageDraw.Draw(diff).rectangle((8, 294, 248, 322), fill=(0, 0, 0))
        assert diff.getbbox() is None, (f, diff.getbbox())
        pairs.append({'frame': f, 'whole_screen_exact': f != 7200,
            'only_reviewed_dialogue_ink_rectangle_excluded': f == 7200})
    states = []
    old_arm = NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
    for f in frames:
        if f < 3200: continue
        a, b = state(old_arm, old_ram[f]), state(arm, new_ram[f])
        assert a == b and b['cash'] == 38816
        assert models(old_arm, old_ram[f]) == models(arm, new_ram[f])
        assert persistent_objects(old_arm, old_ram[f]) == persistent_objects(arm, new_ram[f])
        states.append({'frame': f, 'state': b, 'company_fleet_ships_actors_towns_items_goods_match': True})
    assert state(arm, new_ram[3200]) == state(arm, new_ram[8400])
    assert models(arm, new_ram[3200]) == models(arm, new_ram[8400])
    assert persistent_objects(arm, new_ram[3200]) == persistent_objects(arm, new_ram[8400])
    save(ROOT/'Guild_gameplay_verification.json', {
        'candidate_sha256': new['ROM_sha256'], 'reports': [str(old_path), str(new_path)],
        'report_sha256': [sha(p.read_bytes()) for p in (old_path, new_path)],
        'actual_revised_COMMON1071_complete_hold': {'frame': 7200, 'template_hex': entry.text.hex(),
            'formatted_hex': formatted.hex(), 'resident_complete_block_sha256': sha(blocks[entry.block]),
            'complete_independent_native_glyph_mask': glyph},
        'actual_Guild_role': 5, 'all17_screen_controls': pairs, 'all14_persistent_state_model_object_controls': states,
        'normal_town_return': 8400, 'no_fixtures_dialogue_injection_or_savestates': True,
        'startup_seven_frames': str(ROOT/'newgame_regression.json'),
        'visual_review_prompt_margins_complete_words_letters_and_paper': True,
        'remaining_batch_gates': ['buy/sell/bargain economic outcomes', 'diplomacy entry and eligibility',
            'actual nominal-name SDK/GPU menus and remaining virtual consumers', 'document lifecycle and representative confirmation/drafting scenes'],
        'no_full_batch_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V788 revised Guild1071 full glyphs,17 frame controls,14 persistent-state controls,normal return and7 ordinary New Game pairs pass.', flush=True)


if __name__ == '__main__':
    main()
