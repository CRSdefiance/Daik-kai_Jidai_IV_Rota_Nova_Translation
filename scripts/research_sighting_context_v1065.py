"""Source-bound sighting voices and bearing arguments; no prose/completion credit."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reinforcement_sniping_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_editorial_v1065')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1049_1034_regional')
BASE=0x02000000


def main():
    assert not ROOT.exists()
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    arm,source=[r.read_file('/__arm9__.bin') for r in (rom,clean)]
    common=rom.read_file('/COMMON/MESFILE.DK4')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    current=current_entries(common,arm)
    report=read(CAP/'capture_report.json');raw_path=CAP/'frame_005210_arm9_ram.bin';raw=raw_path.read_bytes()
    assert report['cold_boot'] and not report['savestate_loaded'] and report['ROM_sha256']==sha(ROM.read_bytes())
    receipt=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==5210)
    assert sha(raw)==receipt['sha256'] and len(raw)==0x400000
    spans=((0x53F4C,0x53FE4),(0x6567C,0x65794),(0x774BC,0x77770),(0x7777C,0x77A40),(0x77A58,0x77EC4))
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);code=[]
    for lo,hi in spans:
        assert arm[lo:hi]==source[lo:hi]
        code.append({'address':BASE+lo,'end':BASE+hi,'source_sha256':sha(source[lo:hi]),
            'instructions':[f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in md.disasm(source[lo:hi],BASE+lo)]})
    table=0x02118560
    assert arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
    assert struct.unpack_from('<8i',source,table-BASE)==tuple(range(614,622))
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);hero=get(0x7F244);voices=[]
    for actor in range(208):
        obj=actors+0x19E4 if actor==hero else actors+4+actor*32
        voice=get(0x7E988,obj);number=get(0x53F4C,obj,table)
        assert 0<=voice<8 and number==614+voice
        voices.append({'actor_ID':actor,'original_voice_class':voice,'message_ID':number})
    directions=[]
    for x,y in ((0,0),(100,0),(-100,0),(0,100),(0,-100),(100,100),(-100,100),(100,-100),(-100,-100)):
        at=get(0x6567C,x&0xFFFFFFFF,y&0xFFFFFFFF)
        value=bytes(cpu.mem_read(at,64)).split(b'\0')[0]
        directions.append({'source_relative_vector':[x,y],'argument_address':at,'hex':value.hex(),'text':value.decode('cp932')})
    assert directions[0]['text']=='至近距離'
    assert {d['text'] for d in directions[1:]}=={'N','NE','E','SE','S','SW','W','NW'}
    # Original arrival handler stores actual role-one direction then faction arguments.
    assert struct.unpack_from('<I',source,0x77770)[0]==table
    assert struct.unpack_from('<I',source,0x77A4C)[0]==table
    assert struct.unpack_from('<I',source,0x77ED4)[0]==table
    rows=[]
    for n in range(606,630):
        rows.append({'message_ID':n,'selected_sighting_family':614<=n<=621,
            'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_hex':current[n].text.hex(),'current_English':current[n].text.decode('cp932'),
            'source_block':jp[n].block,'current_block':current[n].block})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_context_packet.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_snapshot':str(raw_path),
        'source_snapshot_sha256':sha(raw),'terminal_report':str(CAP/'capture_report.json'),
        'terminal_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'original_source_fragments':code,'table':table,'source_voice_IDs':list(range(614,622)),
        'all208_original_actor_voice_selections':voices,'original_bearing_getter_cases':directions,
        'native_speaker_role':1,'native_argument_order':['relative-bearing-label','complete-faction-label'],
        'original_callers':[0x020775E8,0x020778D0,0x02077DDC],
        'source_neighbors_and_eight_independent_voice_alternatives':rows,
        'previous_actual614_capture':str(CAP/'frame_005210_navigation.png'),
        'new_finding':'Current6567C still returns Japanese 至近距離 for close-range sightings. Its eight compass abbreviations are already Latin. Future English must handle this real argument as well as complete faction labels;do not assume every argument can follow to the.',
        'close_range_source_gloss':'at very close range; close by',
        'no_new_ROM_or_live_RAM_change':True,'no_source_prose_or_completion_credit':True,
        'no_new_actual_scene_claim':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight original sighting voices,208 actor selections,nine bearing arguments and source neighbors bound. Close-range Japanese provider remains an explicit repair item.',flush=True)


if __name__=='__main__':main()
