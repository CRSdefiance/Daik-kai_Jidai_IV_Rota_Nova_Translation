"""Bind an actually displayed mixed ship name to current and clean ROM source."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/armed_latina_v1078')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1063_1034_regional')


def main():
    assert not ROOT.exists()
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    arm,source=[r.read_file('/__arm9__.bin') for r in (rom,clean)]
    at=0x15E0A4;size=16
    before=arm[at:at+size];original=source[at:at+size]
    assert before.split(b'\0')[0].decode('cp932')=='武装Latina'
    assert original.split(b'\0')[0].decode('cp932')=='武装ラティーナ'
    replacement=b'Armed Latina\0'.ljust(size,b'\0');assert len(replacement)==size
    raw_path=CAP/'frame_008504_arm9_ram.bin';raw=raw_path.read_bytes()
    assert raw[at:at+size]==before
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    actual=raw[wrapped-0x02000000:wrapped-0x02000000+256].split(b'\0')[0]
    assert actual==b'Enemy ship '+before.split(b'\0')[0]+b' captured!'
    screenshot=CAP/'frame_008504_navigation.png'
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_actual_name_inventory.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'file':'/__arm9__.bin','offset':at,'allocation_bytes':size,
        'source_hex':original.hex(),'source_Japanese':'武装ラティーナ','current_hex':before.hex(),'current_mixed_label':'武装Latina',
        'proposed_English':'Armed Latina','proposed_equal_allocation_hex':replacement.hex(),
        'source_meaning':'Armed version of the established Latina ship class.',
        'localization_note':'Use Armed consistently with neighboring Armed HanseCog/Armed Carrack labels;retain established Latina. The complete English fits16 owned bytes with its NUL and no growth.',
        'actual_capture':str(screenshot),'actual_capture_sha256':sha(screenshot.read_bytes()),
        'actual_RAM':str(raw_path),'actual_RAM_sha256':sha(raw),'actual_complete_native_notice_hex':actual.hex(),
        'same_mixed_label_confirmed_in_current_ROM_not_only_a_legacy_save':True,
        'constructor_provider_all_copies_native_display_and_registered_integration_pending':True,
        'review':{'source':True,'context':False,'localization':True,'naturalness':True,'formatting':False},
        'no_ROM_live_RAM_or_save_changed':True,'inventory_only_no_source_prose_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    ledger['newly_observed_armed_latina_followup']={'inventory':str(ROOT/'source_and_actual_name_inventory.json'),
        'status':'current-ROM-source-and-actual-mixed-label-bound;constructor-copy-release-and-new-display-pending',
        'source_prose_reviews_added':0,'completed_entries_added':0}
    save(ledger_path,ledger)
    print('Actual mixed ship name is present in the current ARM9 source;equal16-byte Armed Latina draft recorded. No ROM edit or completion credit.',flush=True)


if __name__=='__main__':main()
