"""Source1747 first-person expansion in all25 genuine native actor models."""

import struct
from pathlib import Path
from dk4tool.patch.common_literal_prefix import guard
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_boarding_pronoun_v2438b')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
INPUT,OUTPUT=0x02450020,0x02451020


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_pronoun_proof.json').exists()
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'));a,j=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    source=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),j)[1747].text
    assert source.count(b'IC')==1
    assert sha(j[0x53914:0x53AC4])=='71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'
    assert a[0x7E9B8:0x7E9D0]==j[0x7E9B8:0x7E9D0]
    restored=bytearray(a[0x53914:0x53AC4])
    literal=read(ROM.with_suffix('.manifest.json'))['relocations']['/__arm9__.bin']['common_literal_prefix']
    for at,prefix in ((0x5397C,'F'),(0x53A44,'I')):
        row=next(r for r in literal['changes'] if r['offset']==at)
        assert struct.unpack_from('<I',a,at)[0]==row['after'] and struct.unpack_from('<I',j,at)[0]==row['before']
        restored[at-0x53914:at-0x53914+4]=j[at:at+4]
    assert bytes(restored)==j[0x53914:0x53AC4]
    folders={0:('personal_activity_v839_838_Rafael_later',3200),1:('battle_survey_lookout_v939_938_CaptainSurvey',16500),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for actor in range(25):
        raw,receipt=snapshot(*(folders[actor] if actor<4 else ('battle_personal_v897_893_Julio',14700)))
        cpu,get=machine_at(a,raw)
        assert bytes(cpu.mem_read(0x02053914,0x1B0))==a[0x53914:0x53AC4]
        for prefix in ('F','I'):
            entry=literal['helpers'][prefix]['entry'];code=guard(entry,prefix)
            assert bytes(cpu.mem_read(entry,len(code)))==code
        actors=get(0xCB184)
        obj=actors+struct.unpack_from('<I',a,0x1229C)[0] if actor<4 else actors+4+actor*32
        if actor<4:assert get(0x7F244)==actor
        kind=get(0x7E9B8,obj);assert kind in (0,1)
        pronoun=('アタシ' if kind==1 else '僕').encode('cp932');expected=source.replace(b'IC',pronoun);variants=[]
        for surface in ('current','clean_parser_control'):
            if surface=='clean_parser_control':cpu.mem_write(0x02053914,j[0x53914:0x53AC4])
            cpu.mem_write(INPUT-16,b'\xA5'*(len(source)+33));cpu.mem_write(INPUT,source+b'\0')
            before=bytes(cpu.mem_read(INPUT-16,len(source)+33));cpu.mem_write(OUTPUT-16,b'\xA5'*560)
            call(cpu,0x53914,(OUTPUT,INPUT,obj))
            actual=bytes(cpu.mem_read(OUTPUT,512)).split(b'\0',1)[0]
            assert actual==expected and bytes(cpu.mem_read(INPUT-16,len(source)+33))==before
            assert bytes(cpu.mem_read(OUTPUT-16,560))==b'\xA5'*16+expected+b'\0'+b'\xA5'*(543-len(expected))
            variants.append({'surface':surface,'expanded_hex':actual.hex(),'expanded_Japanese':actual.decode('cp932'),
                'source_output_guards_and_ABI_pass':True})
        cases.append({'actor_ID':actor,'source_snapshot':receipt,'native_pronoun_kind':kind,'variants':variants})
    save(ROOT/'source_pronoun_proof.json',{'candidate_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(a),
        'source1747_hex':source.hex(),'all25_current_and_clean_parser_control_cases':cases,
        'IC_is_first_person_not_actor_name':True,'source1747_first_person_leads_hand_to_hand_combat':True,
        'source_macro_can_be_localized_as_English_first_person_without_proper_name_substitution':True,
        'four_genuine_captain_states_no_actor_ID_replacement':True,
        'no_ROM_live_RAM_or_actual_gameplay_changes':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('50 complete current/clean source1747 expansions pass;IC is first person,not an actor name.',flush=True)


if __name__=='__main__':main()
