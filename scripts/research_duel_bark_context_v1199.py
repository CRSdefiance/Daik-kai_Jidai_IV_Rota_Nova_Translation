"""Source-bound context for16 timed duel-action reactions, not an approval."""
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.escape_direct_entries import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_context_v1199')
ROM=Path('out/all_routes_combined_v1189_candidate.nds')
IDS=tuple(range(1957,1973))


def main():
    assert not ROOT.exists()
    clean,current,canonical=map(NdsImage.open,('work/clean.nds',ROM,'out/raphael_natural_v2_accepted_base.nds'))
    a,b=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())=='a7b7799052a83703dc5a2bf84e946e43b31d5e1f795f9f3371417412f60c7df4'
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),a)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),b)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    spans=((0x1042C,0x106E0),(0x106E0,0x10824),(0xD458,0xD540),(0x7E988,0x7E9B0),
        (0x117560,0x117580),(0x1175C0,0x1175E0))
    for lo,hi in spans:assert a[lo:hi]==b[lo:hi]
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    instructions=lambda lo,hi:[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
        for at in range(lo,hi,4) for i in decoder.disasm(a[at:at+4],0x02000000+at)]
    call_bindings=[]
    for at,literal,table,kind,flag in ((0x104FC,0x106CC,0x021175C0,'negative_action_reaction',0),
                                      (0x105F4,0x106D4,0x02117560,'positive_action_reaction',1)):
        assert struct.unpack_from('<I',a,literal)[0]==table
        assert next(decoder.disasm(a[at:at+4],0x02000000+at)).op_str=='#0x200d458'
        call_bindings.append({'call':0x02000000+at,'voice_table_literal':0x02000000+literal,'voice_table':table,
            'family':kind,'original_side':0,'original_duration':60,'result_written_to_caller_pointer':flag,
            'source_window':instructions(at-32,at+8)})
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189/frame_006202_arm9_ram.bin')
    raw=snapshot.read_bytes();cpu,get=get_machine(b,raw)
    widget,controller,header,h=actual_widget(raw);main_controller=controller-0x40
    objects=list(struct.unpack('<2I',cpu.mem_read(controller+0x34,8)))
    source_ids=[get(0x7EE08,obj) for obj in objects]
    assert source_ids==[1,32]
    assert struct.unpack('<I',cpu.mem_read(main_controller+0x4E8,4))[0]==1
    actors=get(0xCB184);choices=[]
    for table,first in ((0x02117560,1957),(0x021175C0,1965)):
        assert struct.unpack_from('<8I',a,table-0x02000000)==tuple(range(first,first+8))
        for slot in range(208):
            obj=actors+4+slot*32 if slot<207 else actors+0x19E4
            voice=get(0x7E988,obj);number=get(0x53F4C,obj,table)
            assert number==first+voice
            choices.append({'actor_slot':slot,'actor_ID':get(0x7EE08,obj),'actor_object':obj,
                'voice_class':voice,'table':table,'message_ID':number})
    rows=[]
    ref=lambda r:{k:v for k,v in asdict(r).items() if k!='text'}
    for n in IDS:
        rows.append({'message_ID':n,'source_reference':ref(jp[n]),'source_hex':jp[n].text.hex(),
            'source_Japanese':jp[n].text.decode('cp932'),'canonical_source_hex':accepted[n].text.hex(),
            'current_reference':ref(en[n]),'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
            'voice_class':(n-1957)%8,'family':'positive_action_reaction' if n<1965 else 'negative_action_reaction',
            'native_argument_count':0,'source_native_macros':[],
            'context':'Independent voice alternative in a timed duel action. Original1042C selects the positive/negative feedback table and calls D458 with native side0/duration60. Alternatives are not sequential conversation. The source actor is the nested duel controller side0; input timing, combat result and identity are not changed by translation.'})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_context_packet.json',{'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),
        'current_ARM9_sha256':sha(b),'records':rows,'source_callable_code_spans':[{'lo':lo,'hi':hi,'sha256':sha(a[lo:hi])} for lo,hi in spans],
        'original_timed_action_function':instructions(0x1042C,0x106E0),'original_caller':instructions(0x107AC,0x10824),
        'two_original_voice_call_bindings':call_bindings,'all416_unchanged_native_voice_selections':choices,
        'actual_snapshot':str(snapshot),'actual_snapshot_sha256':sha(raw),
        'source_bound_nested_controller':controller,'main_controller':main_controller,'source_actor_IDs':source_ids,
        'actual_input_mode_flag4E8_is1_in_this_frame':True,
        'input_polling_CF534_CF55C_conditions_are_source_evidence_not_actual_bark_activation':True,
        'native_D458_font_consumer_has_same24x3_visible_contract_as_static_duel':True,
        'native_front_currently_excludes_both_new_tables':True,'formatting_and_actual_activation_pending':True,
        'fourteen_additional_special_move_lines1980_1993_remain_separate_unreviewed_work':True,
        'no_prose_or_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('16 timed-action reactions mapped:416 original voice selections,two exact D458 calls; no prose credit.',flush=True)


if __name__=='__main__':main()
