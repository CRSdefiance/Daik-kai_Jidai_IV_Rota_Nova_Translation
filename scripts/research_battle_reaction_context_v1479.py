"""Original actor-speech contracts and contextual branches for32 reactions."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.ship_loss_surrender_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_context_v1479')
INVENTORY=Path('work/analysis/battle_reactions_source_v1478/source_inventory.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    inventory=read(INVENTORY);rom=NdsImage.open(inventory['candidate']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(inventory['candidate']).read_bytes())==inventory['candidate_sha256']
    arm,original=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    raw=Path(inventory['snapshot']['path']).read_bytes();assert sha(raw)==inventory['snapshot']['sha256']
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata=True
    spans=[(0x65968,0x65A00),(0x65B08,0x65B90),(0x70FA0,0x71088),
        (0x74094,0x74328),(0x751E0,0x756FC),(0x7E0AC,0x7E158),(0x53F0C,0x53F4C)]
    code=[]
    for lo,hi in spans:
        assert arm[lo:hi]==original[lo:hi]
        code.append({'span':[BASE+lo,BASE+hi],'sha256':sha(original[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(original[lo:hi],BASE+lo)]})
    def operands(at):return next(md.disasm(original[at-BASE:at-BASE+4],at)).op_str
    assert struct.unpack_from('<I',original,0x71084)[0]==0x02065968
    assert operands(0x02071020)=='r0, [pc, #0x5c]' and operands(0x02071024)=='#0x2065b08'
    assert operands(0x020659D4)==operands(0x020659F0)==operands(0x02074260)==operands(0x020742C8)=='#0x2053f0c'
    assert operands(0x0207564C)=='#0x2074094'
    assert operands(0x0207E0AC)=='r1, [r0, #7]' and operands(0x0207E0F8)=='r1, [r0, #6]'
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);families=[]
    for f in inventory['families']:
        cases=[]
        for voice in range(8):
            existing=next(r for r in f['all206_existing_actor_choices'] if r['voice']==voice)
            actor=actors+4+32*existing['existing_actor_ID'];n=f['first_ID']+voice
            result=consumer(arm,common,raw,{'patches':[]},0x53F0C,actor,f['table'])
            assert result['input_hex']==entries[n].text.hex()
            assert result['parent']==0x02053F40 and result['selector_offset']==0x274 and result['selector']==f['table']
            cases.append({'message_ID':n,'existing_actor_ID':existing['existing_actor_ID'],
                'actor_object':actor,'native_speech_probe':result,
                'CPU_direct_table_probe_not_original_reaction_or_health_event':True})
        contexts={
            2147:'Optional battle-setup crew callback65968,registered through71020/71024. Original RNG100 must return0;voice2/3 use this table after mood0;actor24 is excluded from this callback branch. All eight stored alternatives remain source text;other voices are not individually claimed reachable through this one caller.',
            2155:'Same optional battle-setup callback65968;voice4/6 use this table after mood1. Preserve confident/eager reactions. Other stored voices have native table proof,not an assertion of original callback reachability.',
            2163:'Original own-ship projectile-hit path7564C calls74094. It chooses an existing own crew member through original role/RNG selection. First incident flag plus the original level/probability branch can set mood5 and reduce actor HP by10-14 before the surprise remark. Do not describe this as an unrelated town surprise or assume this is the persistent-injury branch.',
            2171:'Same original own-ship hit handler74094. Its later original stat/probability branch reduces actor HP by10-14,shows the wound reaction,then updates health-state0->2 or2->3. Wound language and frustrated exclamations are contextual;do not invent tactical failure,cause,attacker,death or healing.'}
        families.append({**f,'original_entry':0x02053F0C,'original_parent':0x02053F40,
            'selector_stack_offset':0x274,'source_native_macros':[],'native_argument_count':0,
            'original_context':contexts[f['first_ID']],'all8_original_actor_speech_contract_probes':cases})
    for row in inventory['records']:
        if row['selected']:
            body=bytes.fromhex(row['source_hex']);assert b'%' not in body
            assert not any(m in body for m in [b'FA',b'FI',b'FO',b'FU',b'IC'])
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_original_reaction_context.json',{**inventory,'source_inventory':str(INVENTORY),
        'source_inventory_sha256':sha(INVENTORY.read_bytes()),'families':families,'original_code_spans':code,
        'all32_current_original_actor_selection_file_copy_printf_macro_entry_contracts_executed':True,
        'no_RNG_injury_eligibility_or_result_override_or_live_event':True,
        'source_context_approved_prose_layout_release_and_actual_events_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('32 original actor-speech contracts pass;setup callback and own-ship surprise/injury branches mapped. No forced RNG/health/event or completion credit.')
