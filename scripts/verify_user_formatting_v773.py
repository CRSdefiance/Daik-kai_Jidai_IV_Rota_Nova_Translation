"""Recheck the photographed shop pitch without changing the current ROM."""

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
    assert latest['profile'] == 'all-routes-unified-v773'
    assert sha(path.read_bytes()) == latest['sha256']
    rom = NdsImage.open(path)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    assert sha(common) == latest['MESFILE_sha256']
    assert sha(arm) == latest['ARM9_sha256']
    entries = common_message_entries(common, arm, clean=False)
    reference = Path('work/analysis/dialogue_formatting_user_recheck_v767/COMMON676_677.json')
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
        rows.append({'id': number, 'lines': lines,
                     'native_formatted_hex': formatted.hex(),
                     'exact_repaired_text_and_native_formatting_preserved': True})
    capture = Path(prior['earlier_actual_capture'])
    assert sha(capture.read_bytes()) == prior['earlier_actual_capture_sha256']
    proof = Path('work/analysis/dialogue_formatting_user_recheck_v773/COMMON676_677.json')
    proof.parent.mkdir(parents=True, exist_ok=True)
    save(proof, {'candidate': str(path), 'sha256': latest['sha256'],
                 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'entries': rows,
                 'prior_reference': str(reference), 'prior_reference_sha256': sha(reference.read_bytes()),
                 'earlier_actual_capture': str(capture),
                 'earlier_actual_capture_sha256': sha(capture.read_bytes()),
                 'scope': 'V773 ROM bytes and native wrapping rechecked. Earlier V747 actual shop-pitch capture visually reviewed; no fresh V773 activation of this scene claimed.',
                 'producer_sha256': sha(Path(__file__).read_bytes()),
                 'full_game_formatting_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    watch = ledger['formatting_watchlist']
    watch['latest_reference_proof'] = str(proof)
    note = ' V773 user screenshot recheck confirms exact repaired676/677 ROM bytes and native wrapping; earlier V747 actual cooking scene visually reviewed. No fresh V773 shop-scene activation claimed.'
    if note not in watch['reference_case']:
        watch['reference_case'] += note
    save(ledger_path, ledger)
    for row in rows:
        print(row['id'], row['lines'], flush=True)
    print('Current V773 formatting preserved; ongoing formatting watchlist retained.', flush=True)


if __name__ == '__main__':
    main()
