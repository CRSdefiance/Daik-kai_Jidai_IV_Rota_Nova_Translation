"""Actual Lil context, complete original53914 execution and whole-memory checks."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.codec import parse_markup,tokens_to_bytes
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_macro_v1698d')
ROM=Path('out/all_routes_combined_v1676_candidate.nds')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676/frame_006000_arm9_ram.bin')
INPUT,OUTPUT=0x02660000,0x02662000


if __name__=='__main__':
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');raw=SNAP.read_bytes()
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    restored=bytearray(arm[0x2425C:0x24344])
    for at in (0x242C8,0x24310,0x24330):
        word=struct.unpack_from('<I',arm,at)[0];rel=word&0xFFFFFF;rel=rel-(1<<24) if rel&(1<<23) else rel
        assert word>>24==0xEB and 0x02000000+at+8+4*rel==0x023A4DC4
        restored[at-0x2425C:at-0x2425C+4]=original[at:at+4]
    assert bytes(restored)==original[0x2425C:0x24344]
    assert arm[0x5397C:0x53980]!=original[0x5397C:0x53980] and arm[0x53A44:0x53A48]!=original[0x53A44:0x53A48]
    cpu,get=get_machine(arm,raw);assert get(0x7F244)==2
    actors=get(0xCB184);captain=actors+0x19E4;vt=struct.unpack('<I',cpu.mem_read(captain,4))[0]
    name=get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-0x02000000,captain)
    assert cstring(raw,name)==b'Lil'
    doc=read('translations/lil_opening_editorial_manuscript_v1.json');cases=[];writes=[]
    def on_write(u,access,address,size,value,_):
        # ABI helper uses an isolated high stack; original live4MiB must remain exact.
        writes.append((address,size))
    hook=cpu.hook_add(UC_HOOK_MEM_WRITE,on_write)
    boundary=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    def expand(value,actor,alignment):
        assert b'\0' not in value and len(value)<2048
        cpu.mem_write(INPUT-16,b'\xA5'*2080);cpu.mem_write(INPUT+alignment,value+b'\0')
        input_before=bytes(cpu.mem_read(INPUT-16,2080))
        cpu.mem_write(OUTPUT-16,b'\xA5'*4128)
        writes.clear();call(cpu,0x242C8,(OUTPUT,INPUT+alignment,actor),instruction_limit=200000)
        result=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
        assert bytes(cpu.mem_read(INPUT-16,2080))==input_before
        assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(OUTPUT+len(result)+1,4096-len(result)-1))==b'\xA5'*(4096-len(result)-1)
        assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
        assert all(OUTPUT<=a<a+n<=OUTPUT+len(result)+1 or 0x027EF000<=a<a+n<=0x027F0000 for a,n in writes)
        return result
    try:
        for r in doc['records']:
            speaker=int(r['source_presentation_prefix_hex'],16);actor_ID=get(0x2434C,speaker)
            actor=captain if actor_ID==2 else actors+4+actor_ID*32
            text=r['english'].replace('{PAD}','')
            paragraph=tokens_to_bytes(parse_markup(text),guard_linebreaks=True,pair_phase_safe_breaks=True,macro_ascii_lengths={'FI':3,'FA':5,'FO':9})[1:]
            assert b'\n' not in paragraph
            expected=paragraph.replace(b'FI',b'Lil')
            for alignment in range(4):
                result=expand(paragraph,actor,alignment)
                assert result==expected,(r['id'],alignment,result,expected)
                cases.append({'id':r['id'],'source_speaker_byte':speaker,'original_2434C_actor_ID':actor_ID,'actor_object':actor,
                    'input_alignment':alignment,'input_hex':paragraph.hex(),'output_hex':result.hex(),
                    'entire4MiB_input_guards_output_guards_and_ABI_preserved':True})
        controls=[]
        for token in (b'FI',b'FA',b'FO',b'IC',b'I\n',b'ICARUS',b'FIRE'):
            result=expand(token,captain,0)
            controls.append({'input_hex':token.hex(),'output_hex':result.hex(),'output_CP932':result.decode('cp932')})
        assert controls[0]['output_hex']==b'Lil'.hex()
        assert all(r['output_hex']!=r['input_hex'] for r in controls)
    finally:cpu.hook_del(hook);cpu.hook_del(boundary)
    ROOT.mkdir(parents=True)
    save(ROOT/'original_story_macro_proof.json',{'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'snapshot':str(SNAP),'snapshot_sha256':sha(raw),'actual_Lil_captain_ID':2,'actual_default_FI_hex':b'Lil'.hex(),
        'original_story_dispatch_span_except_three_registered_catalog_calls':[0x0202425C,0x02024344],
        'original_story_calls53914_at':[0x020242C8,0x02024310,0x02024330],
        'current_existing_V255_F_I_prefix_guards_executed_not_modified':True,'actual_current_story_catalog_wrapper':0x023A4DC4,'original_caller_LR':0x020242CC,'registered_catalog_calls_only_differences_in_source_dispatch_span':True,
        'all196_paragraph_alignment_cases':cases,'genuine_macro_and_collision_controls':controls,
        'ordinary_ASCII_I_F_and_default_FI_preserved_in_all49_drafts':True,
        'I_followed_by_LF_and_literal_IC_or_FI_remain_unsafe_and_must_be_rejected':True,
        'FU_not_used_in_this_opening_and_not_in_readonly_control_scope':True,'FU_observation_in_aborted_predecessor':'Original7EA8C builds Lil Argot in native cache022A47F8 and updates022A44F4;it is not a readonly getter. No FU replacement or runtime change is proposed.','aborted_predecessors':['scripts/probe_lil_opening_macro_v1698.py','scripts/probe_lil_opening_macro_v1698b.py','scripts/probe_lil_opening_macro_v1698c.py'],'proof_does_not_approve_wrapped_bytes_font_pages_relocation_or_new_draft_gameplay':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('49 complete paragraphs x4 alignments execute original53914 with actual Lil state:196 exact outputs,whole4MiB/ABI/guards preserved. Genuine macros and I-LF collisions remain active.')
