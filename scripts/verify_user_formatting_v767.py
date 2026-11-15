"""Recheck the user's photographed cooking pitch in the current combined ROM."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_village_wrap_v608 import read, save


def main():
    latest = read('out/editorial_review_latest.json')
    path = Path(latest['path'])
    assert latest['profile'] == 'all-routes-unified-v767'
    assert sha(path.read_bytes()) == latest['sha256']
    rom = NdsImage.open(path)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    assert sha(common) == latest['MESFILE_sha256']
    assert sha(arm) == latest['ARM9_sha256']
    entries = common_message_entries(common, arm, clean=False)
    reference = Path('work/analysis/dialogue_formatting_user_recheck_v762/COMMON676_677.json')
    prior = read(reference)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    rows = []
    for old in prior['entries']:
        number = old['id']
        assert entries[number].text == old['template'].encode('ascii')
        formatted, lines = native_layout(cpu, entries[number].text, number, ())
        assert formatted.hex() == old['native_formatted_hex']
        assert lines == old['lines']
        assert 'Discover' not in ' '.join(lines)
        rows.append({'id': number, 'template': old['template'], 'lines': lines,
                     'native_formatted_hex': formatted.hex(),
                     'exact_repaired_text_and_native_formatting_preserved': True})
    capture = Path(prior['earlier_actual_capture'])
    assert sha(capture.read_bytes()) == prior['earlier_actual_capture_sha256']
    root = Path('work/analysis/dialogue_formatting_user_recheck_v767')
    root.mkdir(parents=True, exist_ok=True)
    proof = root / 'COMMON676_677.json'
    save(proof, {'candidate': str(path), 'sha256': latest['sha256'],
                 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'entries': rows,
                 'prior_reference': str(reference), 'prior_reference_sha256': sha(reference.read_bytes()),
                 'earlier_actual_capture': str(capture),
                 'earlier_actual_capture_sha256': sha(capture.read_bytes()),
                 'scope': 'Current V767 bytes and native formatter rechecked. Earlier V747 actual cooking-pitch capture visually reviewed; no new V767 gameplay activation claimed.',
                 'producer_sha256': sha(Path(__file__).read_bytes()),
                 'full_game_formatting_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    watch = ledger['formatting_watchlist']
    watch['latest_reference_proof'] = str(proof)
    watch['reference_case'] += ' V767 exact ROM bytes and native formatting now rechecked against V762; both repaired entries remain exact, and the earlier V747 actual capture was visually reviewed again. No new V767 gameplay activation is claimed.'
    save(ledger_path, ledger)
    print('V767: cooking/fashion text and native wrapping remain exact; persistent formatting watchlist updated.', flush=True)
    for row in rows:
        print(row['id'], row['lines'], flush=True)


if __name__ == '__main__':
    main()
