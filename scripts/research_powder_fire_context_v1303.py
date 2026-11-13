"""Bind six powder-fire alternatives to their original caller and actual Gunner."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_context_v1303')
BASE, TABLE = 0x02000000, 0x02117980
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266')


def main():
    assert not ROOT.exists()
    rom = NdsImage.open('out/all_routes_combined_v1266_candidate.nds')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    values = list(struct.unpack_from('<8I',source,TABLE-BASE))
    assert values == [2052,2053,2054,2054,2054,2055,2056,2057]
    assert arm[TABLE-BASE:TABLE-BASE+32] == source[TABLE-BASE:TABLE-BASE+32]
    literals = {BASE+offset for offset in range(0,0x130000,4) if struct.unpack_from('<I',source,offset)[0] == TABLE}
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    callers = []
    for offset in range(0,0x130000,4):
        word = struct.unpack_from('<I',source,offset)[0]
        if word & 0x0F7F0000 != 0x051F0000:
            continue
        literal = BASE+offset+8+(word & 4095)*(1 if word & 0x00800000 else -1)
        if literal not in literals:
            continue
        lo,hi = offset-64,offset+64
        assert arm[lo:hi] == source[lo:hi]
        callers.append({'literal':literal,'load_instruction':BASE+offset,
            'original_caller_span':[BASE+lo,BASE+hi],
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(source[lo:hi],BASE+lo)]})
    assert callers
    entries = current_entries(common,arm)
    cache_owner = struct.unpack_from('<I',arm,0x552A0)[0]
    report = read(CAP/'capture_report.json')
    assert report['frames'] == 7510 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    snapshots = {row['frame']:row for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
    holds = []
    for frame in [7210,7310]:
        snapshot = snapshots[frame]
        raw = Path(snapshot['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
        cpu,get = get_machine(arm,raw)
        fleets,actors = get(0xCB1A8),get(0xCB184)
        actor = get(0x82428,fleets+0x2090,9)
        assert actor == actors+4+16*32 and get(0x7EE08,actor) == 16
        voice,number = get(0x7E988,actor),get(0x53F4C,actor,TABLE)
        assert number == values[voice] and number in range(2052,2058)
        template = raw[cache_owner-BASE+0x2030:cache_owner-BASE+0x2230].split(b'\0')[0]
        assert template == entries[number].text
        block = IlnkContainer.parse(common).blocks[entries[number].block]
        assert raw.count(block) == 1
        image = CAP/f'frame_{frame:06d}_navigation.png'
        holds.append({'frame':frame,'native_Gunnery_role':9,'actual_actor_ID':16,'source_voice':voice,
            'source_selected_message_ID':number,'stored_current_template_exact':True,'unique_complete_resident_block_exact':True,
            'RAM_sha256':sha(raw),'capture':str(image),'capture_sha256':sha(image.read_bytes()),
            'current_English':template.decode('cp932'),'new_English_not_yet_integrated_or_tested':True})
    packet_path = Path('work/analysis/battle_hazards_inventory_v1302/source_current_packet.json')
    packet = read(packet_path)
    selected = [row for row in packet['records'] if 2052 <= row['message_id'] <= 2057]
    assert len(selected) == 6 and all(not row['already_source_reviewed'] and not row['already_complete'] for row in selected)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_actual_binding.json',{'original_table':TABLE,'all8_voice_selections':values,
        'original_table_and_caller_code_equal_clean':True,'original_literal_caller_windows':callers,
        'records':selected,'actual_old_wording_holds':holds,'source_current_packet':str(packet_path),
        'source_current_packet_sha256':sha(packet_path.read_bytes()),'terminal_report':str(CAP/'capture_report.json'),
        'terminal_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'source_and_disposable_saves_unchanged':read('work/analysis/town_gunnery_v1300/terminal_preservation.json')['source_and_disposable_donors_unchanged'],
        'new_translation_or_formatting_or_family_completion_not_claimed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original powder-fire table',hex(TABLE),'callers:',callers,'actual old-wording holds:',holds)


if __name__ == '__main__':
    main()
