"""Bind the two live description representations and exact active/dead pointer tables."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script import common_message_table as common_parser
from dk4tool.script.common_entry_tables import B32_TABLE_OFFSET
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_description_consumers_v6092')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6091/verified_handoff.json')
DESC=Path('work/analysis/shachihoko_description_v6085/clean_description_neighbor_context_current_COMMON_and_staged_copy_lead.json')
BASE,POOL=0x02000000,0x02387A20

def collect(arm,common,raw,plan,helper):
    cpu,get,provider=machine(arm,common,raw,plan);cases=[]
    for ident in range(218):
        key=0xAFF+ident;pointer=get(helper-BASE,key);parts=[];at=pointer
        for line in range(4):
            value=bytes(cpu.mem_read(at,512)).split(b'\0',1)[0]
            if not value:break
            parts.append(value);at+=len(value)+1
        assert 1<=len(parts)<=3 and all(all(32<=c<127 for c in value) for value in parts)
        cases.append(dict(item_ID=ident,message_ID=key,pointer=pointer,terminated_rows_hex=[v.hex() for v in parts],paragraph=' '.join(v.decode('ascii') for v in parts)))
    return dict(cases=cases,file_opens=provider.opens,file_reads=provider.reads,executed_current_instruction_addresses=len(provider.executed_current),
        actual_native_COMMON_lookup_then_private_override_executed=True,native_file_open_read_host_contracts_disclosed=True)

if __name__=='__main__':
    assert not ROOT.exists();prior,desc=map(read,[PRIOR,DESC]);assert prior['goal_turn_classification']=='progress' and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'];reg=read('translations/release_stack.json');assert len(reg['accepted_layers'])==114 and reg['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    image=NdsImage.open(prior['candidate']);arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4');payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123040 and arm.count(payload)==1
    legacy_plan=read('work/analysis/item_interface_plan.json');helper=next(r['start'] for r in legacy_plan['main_pool_helpers'] if r['kind']=='advice_lookup');at=helper-POOL
    code=payload[at:at+48];assert struct.unpack_from('<I',code,20)[0]==0xE35400DA
    active=struct.unpack_from('<I',code,44)[0];table=list(struct.unpack_from('<218I',payload,active-POOL));old=legacy_plan['advice_table']
    assert active!=old and list(struct.unpack_from('<198I',payload,old-POOL))==table[:198]
    pointer=table[116];next_pointer=table[117];assert pointer==desc['staged_literal']['deployed_address']
    field=active-POOL+116*4;allaliases=[i for i in range(len(arm)-3) if arm[i:i+4]==struct.pack('<I',pointer)]
    expected=[arm.index(payload)+t-POOL+116*4 for t in [old,active]];assert sorted(allaliases)==sorted(expected)
    old_table_refs=[i for i in range(len(arm)-3) if arm[i:i+4]==struct.pack('<I',old)];assert old_table_refs==[]
    calls=[];disassembler=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for site in [0x4D834,0x4E50C]:
        instruction=next(disassembler.disasm(arm[site:site+4],BASE+site));assert instruction.mnemonic=='bl' and instruction.op_str==hex(helper).replace('0x','#0x')
        calls.append(dict(address=BASE+site,whole_instruction_hex=arm[site:site+4].hex(),target=helper))
    directory=read('translations/shop657_full_width_reflow_release_v1.json')['directory_sha256'];entries=owned_entries(common,arm,directory);e=entries[2931]
    assert e.table_offset==B32_TABLE_OFFSET+116*2 and e.block==32 and e.text.hex()==desc['current_description']['text_hex']
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B204_voices_v6063/current_native_input.json','unused-no-historical-ROM',ROOT/'current_context')
    native=ctx.execute(collect,helper);ctx.machines.pop();assert not ctx.machines and len(native['cases'])==218
    assert [r['pointer'] for r in native['cases']]==table and native['cases'][116]['paragraph']==' '.join(e.text.decode('ascii').split())
    save(ROOT/'current218_live_description_getters_two_item_callers_and_exact_owned_representations.json',dict(
        candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),native=native,
        advice_helper=helper,advice_helper48_hex=code.hex(),active218_table=active,active218_pointers=table,
        item116_active_pointer_field_file_offset=arm.index(payload)+field,item116_active_pointer_field_payload_offset=field,
        item116_old_compiled_pointer=pointer,item116_old_compiled_payload_span=[pointer-POOL,next_pointer-POOL],item116_old_compiled_hex=payload[pointer-POOL:next_pointer-POOL].hex(),
        duplicate_legacy198_table=old,duplicate_legacy198_table_has_no_literal_owner=True,all_literal_old116_pointer_fields=allaliases,
        duplicate_old198_table_is_historical_data_not_active_helper_table=True,only_active218_field_to_change_when_relocating=True,
        original_item_detail_callers=calls,COMMON_and_B32_item_table_share_exact_field=e.table_offset,
        COMMON_directory_offset=common_parser.DIRECTORY_OFFSET,COMMON_table_offset=common_parser.TABLE_OFFSET,COMMON_directory_sha256=directory,
        actual_detail_UI_drawing_and_future_replacement_still_pending=True,no_ROM_or_registry_ledger_change=True,
        previous_goal_turn_classification='progress',new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,DESC,Path(__file__),Path('work/analysis/item_interface_plan.json')]}))
    print('218 live COMMON/private-description getters pass;two detail callers bind active218 table. Old198 table has no literal owner. Both live representations bound;no mutation or credit.')
