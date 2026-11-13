"""Classify eight actor-style alternatives per native4100 object;zero prose credit."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from unicorn.arm_const import UC_ARM_REG_R0
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_4100_alternatives_v3156')
ROM=Path('out/all_routes_combined_v3144_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);prior=Path('work/analysis/editorial_handoff_verification_v3155/verified_handoff.json');assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    paths=[Path('work/clean.nds'),ROM];images=[NdsImage.open(p)for p in paths];arms=[i.read_file('/__arm9__.bin')for i in images];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in images];scope=read('work/analysis/lil_after_Crew_Items_clean_scope_v3152/complete_clean_next_exchange_inventory.json');inventory,_,_=scoped_inventory()
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256'];ranges=[(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x2434C,0x243A0),(0x7E988,0x7E9A0)]
    for a,b in ranges:assert arms[0][a:b]==arms[1][a:b]
    results=[];allrows=[];native_cases=0
    for spec in scope['blocks']:
        n=spec['block']
        if n==120:continue
        commands,_=inventory(arms[1],blocks[1][n]);current={c['offset']:c for c in commands}
        for command in spec['commands']:
            if command['word']!=0x4100:continue
            at=command['offset'];now=current[at];assert now['word']==0x4100;versions=[]
            for label,arm,bb,c in zip(['clean','current'],arms,blocks,[command,now],strict=True):
                block=bb[n];value=block[at:at+c['native_extent']];assert value[:2]==bytes.fromhex('0041') and len(value)>=20 and value[18]==0
                offsets=list(struct.unpack_from('<8H',value,2));prefix=value[19];cpu=machine(arm);STREAM,OBJECT=0x02660000,0x02662000
                cpu.mem_write(STREAM-16,b'\xA5'*(len(value)+32));cpu.mem_write(STREAM,value);cpu.mem_write(OBJECT-16,b'\xA5'*64);cpu.mem_write(OBJECT,struct.pack('<4I',0,STREAM,0,0));guard=bytes(cpu.mem_read(OBJECT-16,64));main=bytes(cpu.mem_read(0x02000000,0x400000));slots=[]
                for style in range(8):
                    call(cpu,0x2A154,(OBJECT,style));pointer=cpu.reg_read(UC_ARM_REG_R0);relative=20+offsets[style];assert pointer==STREAM+relative and relative<len(value)
                    text=bytes(cpu.mem_read(pointer,len(value)-relative)).split(bytes([0]))[0];assert text
                    assert bytes(cpu.mem_read(OBJECT-16,64))==guard and bytes(cpu.mem_read(STREAM,len(value)))==value and bytes(cpu.mem_read(0x02000000,0x400000))==main
                    for p in [STREAM-16,STREAM+len(value)]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
                    slots.append(dict(style_index=style,relative_offset=relative,offset=at+relative,hex=text.hex(),text=text.decode('cp932'),native_inline_getter_ABI_all4MiB_input_owner_and_stream_guards_exact=True));native_cases+=1
                versions.append(dict(version=label,command_offset=at,command_hex=value.hex(),command_bytes=len(value),offsets=offsets,source_selector=prefix,low_byte_flags=0,style_slots=slots))
            assert versions[0]['offsets']==versions[1]['offsets'] and versions[0]['source_selector']==versions[1]['source_selector']
            aliases={offset:[r['style_index']for r in versions[0]['style_slots']if r['relative_offset']==offset]for offset in sorted({r['relative_offset']for r in versions[0]['style_slots']})};rows=[]
            for offset,styles in aliases.items():
                jp,en=[next(r for r in v['style_slots']if r['relative_offset']==offset)for v in versions];ident=f'DK4_VOICE_B{n}_C{at}_T{offset}'
                row=dict(id=ident,file_path='/data/SC2.DK4',block=n,command_offset=at,kind='typed-4100-actor-style-alternative',style_indices=styles,source_reference=dict(offset=jp['offset'],bytes=len(bytes.fromhex(jp['hex'])),command_offset=at),current_reference=dict(offset=en['offset'],bytes=len(bytes.fromhex(en['hex'])),command_offset=at),source_hex=jp['hex'],current_hex=en['hex'],source_Japanese=jp['text'],current_English=en['text'],source_selector=versions[0]['source_selector'],source_legacy_NUL_ID=f'DK4_MES_B{n}_R{blocks[0][n][:jp["offset"]].count(bytes([0])):04d}',source_prose_or_completion_credit_added=0,actor_style_consumer_and_full_native_display_approval_pending=True)
                rows.append(row);allrows.append(row)
            results.append(dict(block=n,command_offset=at,source_command=command,current_command=now,versions=versions,source_alias_groups={str(k):v for k,v in aliases.items()},records=rows,not_a_player_menu=True,eight_slots_selected_by_original_actor_record_byte1C=True))
    assert len(results)==14 and native_cases==224 and len(allrows)==len({r['id']for r in allrows})
    known={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert not known&{(r['file_path'],r['id'])for r in allrows}
    ROOT.mkdir(parents=True);save(ROOT/'all14_clean_current_eight_style_alternatives.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_ROM=str(paths[0]),source_ROM_sha256=sha(paths[0].read_bytes()),objects=results,records=allrows,native_inline_getter_cases=native_cases,source_exact_ranges=[dict(start=a,end=b,sha256=sha(arms[0][a:b]))for a,b in ranges],original_4100_handler_uses_7E988_actor_record_byte1C_then_2A154_style_pointer_and_2425C_dispatch=True,source_low_byte_masks_all_zero_and_all8_slots_inline=True,source_command_18byte_table_plus2byte_selector_and_relative_text_base20=True,player_choice_count_pointer_VM_and_choice_renderer_must_not_be_applied=True,alias_groups_preserved_in_exact_clean_current_pointer_tables=True,source_dynamic_selector_context_macro_pipeline_voice_mapping_complete_display_reference_proofs_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes())for p in [lp,prior,Path(__file__)]},full_goal_complete=False))
    first=[r for r in allrows if r['block']<=110];print('14actor-style objects,112source slots,',len(allrows),'unique storedalternatives,224clean/currentgetter cases. First10exchanges:',len(first),'alternatives plus164speeches. No choices or editorialcredit.')
