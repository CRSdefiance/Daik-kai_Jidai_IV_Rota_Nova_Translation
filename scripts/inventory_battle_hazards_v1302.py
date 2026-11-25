"""Clean/current battle hazard inventory prompted by an actual powder-fire notice."""
import struct
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_hazards_inventory_v1302')
IDS = tuple(range(2052,2114))


def main():
    assert not ROOT.exists()
    rom_path = Path('out/all_routes_combined_v1266_candidate.nds')
    clean,rom = NdsImage.open('work/clean.nds'),NdsImage.open(rom_path)
    source,arm = clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en = current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    ledger = read('translations/editorial_review_current_v1.json')
    completed = {n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])}
    reviewed = completed|set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    rows = []
    for number in IDS:
        rows.append({'message_id':number,'source_reference':{k:v for k,v in asdict(jp[number]).items() if k != 'text'},
            'source_hex':jp[number].text.hex(),'source_Japanese':jp[number].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[number]).items() if k != 'text'},
            'current_text_hex':en[number].text.hex(),'current_English':en[number].text.decode('cp932'),
            'already_source_reviewed':number in reviewed,'already_complete':number in completed})
    words = []
    for offset in range(0x117900,0x117D00,4):
        value = struct.unpack_from('<I',source,offset)[0]
        if value in IDS:
            assert arm[offset:offset+4] == source[offset:offset+4]
            words.append({'address':0x02000000+offset,'native_message_ID':value})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_current_packet.json',{'candidate':str(rom_path),'candidate_sha256':sha(rom_path.read_bytes()),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'records':rows,
        'original_native_table_words':words,'actual_new_lead':'Gerhard powder-fire notice in town_gunnery_v1300 frame7210/7310',
        'source_or_prose_or_formatting_approval_not_granted_by_inventory':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    for row in rows:
        print(row['message_id'],repr(row['source_Japanese']),'=>',repr(row['current_English']))


if __name__ == '__main__':
    main()
