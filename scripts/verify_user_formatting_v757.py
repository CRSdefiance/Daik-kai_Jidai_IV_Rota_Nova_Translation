"""Recheck the user's cooking-pitch formatting against the completed correction."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_market_stock_v757 import ROOT
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_village_wrap_v608 import read, save


def main():
    common, arm = [(ROOT / f).read_bytes() for f in ('research_COMMON.bin', 'research_ARM9.bin')]
    entries = common_message_entries(common, arm, clean=False)
    previous_path = Path('work/analysis/dialogue_formatting_user_recheck_v754/COMMON676_677.json')
    previous = read(previous_path)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    rows = []
    for old in previous['entries']:
        number = old['id']
        assert entries[number].text == old['template'].encode('ascii')
        formatted, lines = native_layout(cpu, entries[number].text, number, ())
        assert formatted.hex() == old['native_formatted_hex'] and lines == old['lines']
        rows.append({'id': number, 'complete_text_and_native_layout_equal_repaired_V747_V754': True, 'lines': lines})
    capture_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/product_pitches_v747_new/frame_004200_cold_boot.png')
    assert sha(capture_path.read_bytes()) == 'eb5ef396a1eec18b1dedffe6ea688c71cb77b3ae9e0e4d71665c5a9aef4090d9'
    save(ROOT / 'user_formatting_reference.json', {'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'prior_recheck': str(previous_path), 'prior_recheck_sha256': sha(previous_path.read_bytes()),
        'entries': rows, 'earlier_actual_cooking_pitch_capture': str(capture_path),
        'actual_capture_sha256': sha(capture_path.read_bytes()),
        'scope': 'Current bytes/native formatting and inherited actual V747 screenshot; no new actual676 display claimed.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_game_formatting_complete': False})
    print('User676/677 example retains repaired text and complete native wrapping; earlier actual screenshot verified.', flush=True)


if __name__ == '__main__':
    main()
