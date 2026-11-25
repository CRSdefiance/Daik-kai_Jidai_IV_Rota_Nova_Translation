"""Classify the duplicated Maria region using source boundaries and native VM."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B115_tail_classification_v3216')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json')
COPIES=[(0,123,730),(1,123,398),(2,115,440),(3,97,16)]
BASE=0x02000000
ACTIVE=0x02279668+0x54

def graph(commands,start,logical_end):
    byat={c['offset']:c for c in commands};queue=[start];seen=set();edges=[];terminals=[]
    while queue:
        at=queue.pop()
        if at in seen:continue
        assert at in byat
        seen.add(at);c=byat[at];word=c['word']
        state=struct.unpack_from('<I',bytes.fromhex(c['native_result_hex']))[0]
        if state==0:
            assert word==0 and c['whole_command_hex']=='00000000'
            terminals.append(at);continue
        if word in [0x100,0x200,0x300,0x400]:
            matched=at+4+struct.unpack_from('<H',bytes.fromhex(c['whole_command_hex']),2)[0]
            targets=[matched] if word==0x100 else sorted({at+4,matched})
        else:
            targets=[at+c['native_extent']]
        for target in targets:
            assert target in byat or target==logical_end
            edges.append(dict(source_offset=at,target_offset=target))
            if target<logical_end:queue.append(target)
    return dict(entry=start,reachable_commands=sorted(seen),reachable_return0_commands=sorted(terminals),
        conservative_both_conditional_results_explored=True,edges=edges)

if __name__=='__main__':
    assert not ROOT.exists()
    source=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',source['current_ROM']]]
    blocks=[[IlnkContainer.parse(im.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)] for im in images]
    arms=[im.read_file('/__arm9__.bin') for im in images]
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256']
    for a,b in [(0x23FFC,0x24118),(0x2A414,0x2A510),(0x2A510,0x2A5BC)]:
        assert arms[0][a:b]==arms[1][a:b]
    src=blocks[0][2][115];tail=src[440:8+struct.unpack_from('<I',src,4)[0]]
    assert len(tail)==1886
    inventory,_,_=scoped_inventory();copies=[];VMcases=[]
    for route,n,at in COPIES:
        versions=[]
        for label,bb,arm in zip(['clean','current'],blocks,arms,strict=True):
            block=bb[route][n];logical=8+struct.unpack_from('<I',block,4)[0]
            commands,_=inventory(arm,block);cfg=graph(commands,8,logical)
            if label=='clean':assert block[at:logical]==tail and at+len(tail)==logical
            canonical=at==16
            assert (at in cfg['reachable_commands'])==canonical
            if canonical:
                assert not any(p<at for p in cfg['reachable_return0_commands'])
            else:
                assert cfg['reachable_return0_commands']==[at-4]
                assert not any(p>=at for p in cfg['reachable_commands'])
                assert block[at-4:at]==bytes(4)
                for mode in [0,1]:
                    cpu=machine(arm);stream,owner=0x02660000,0x02662000
                    cpu.mem_write(stream-16,b'\xa5'*(len(block)+32));cpu.mem_write(stream,block)
                    cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<2I',0,stream+at-4))
                    owner_before=bytes(cpu.mem_read(owner-16,64))
                    cpu.mem_write(ACTIVE,struct.pack('<I',1));before=bytes(cpu.mem_read(BASE,0x400000))
                    executed=[];reads=[]
                    def observe(u,pc,size,unused):
                        executed.append(pc)
                        if pc==BASE+0x2A524:reads.append(pc)
                    hook=cpu.hook_add(UC_HOOK_CODE,observe)
                    try:call(cpu,0x23FFC,(0,owner,0,mode),instruction_limit=20000)
                    finally:cpu.hook_del(hook)
                    assert reads==[BASE+0x2A524]
                    assert BASE+0x24098 in executed and BASE+0x240EC not in executed
                    assert bytes(cpu.mem_read(BASE,0x400000))==before
                    assert bytes(cpu.mem_read(owner-16,64))==owner_before
                    assert bytes(cpu.mem_read(stream,len(block)))==block
                    assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(block),16))==b'\xa5'*16
                    VMcases.append(dict(route=route,block=n,version=label,mode=mode,return_word_offset=at-4,
                        sole_native_decoder_call_reads_return0=True,original_VM_returns_before_cursor_advance=True,
                        ABI_all4MiB_owner_stream_and_boundary_guards_exact=True,
                        source_owned_ACTIVE1_is_isolated_VM_input_not_a_gameplay_fixture=True))
            versions.append(dict(version=label,block_sha256=sha(block),logical_end=logical,tail_offset=at,
                tail_bytes=logical-at,tail_sha256=sha(block[at:logical]),native_control_graph=cfg))
        copies.append(dict(route=route,block=n,source_tail_offset=at,versions=versions,
            clean_tail_exact_to_SC3_B97=True,ordinary_entry_reaches_tail=at==16))
    assert len(VMcases)==12
    packet_rows=[r for r in source['records'] if r['block']==115 and r['source_reference']['offset']>=440]
    assert len(packet_rows)==32
    canonical=blocks[0][3][97];canonical_current=blocks[1][3][97]
    aliases=[]
    for r in packet_rows:
        old=r['source_reference']['offset'];at=old-440+16
        raw=bytes.fromhex(r['source_hex'])
        assert canonical[at:at+len(raw)]==raw and canonical[at+len(raw)]==0
        current_at=at;value=canonical_current[current_at:canonical_current.index(b'\0',current_at)]
        aliases.append(dict(lil_copy_id=r['id'],lil_copy_source_reference=r['source_reference'],
            canonical_file_path='/data/SC3.DK4',canonical_block=97,
            canonical_id=f'DK4_MES_B97_R{canonical[:at].count(bytes([0])):04d}',
            canonical_source_reference=dict(offset=at,bytes=len(raw),header_offset=at-5),
            canonical_current_reference=dict(offset=current_at,bytes=len(value),header_offset=current_at-5),
            source_hex=raw.hex(),canonical_current_hex=value.hex(),
            canonical_Maria_context_already_clean_read_but_current_binding_and_English_review_pending=True))
    code_censuses=[dict(version=label,**census(im)) for label,im in zip(['clean','current'],images,strict=True)]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_return0_graph_and_canonical_Maria_copy_classification.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        ARM9_sha256=sha(arms[1]),source_tail_sha256=sha(tail),tail_bytes=1886,copies=copies,
        original_VM_return_cases=VMcases,shipped_interpreter_call_censuses=code_censuses,
        all12_original_VM_return0_cases_stop_before_cursor_advance=True,
        all_original_prefix_branch_results_cannot_reach_appended_SC0_SC1_SC2_copies=True,
        ordinary_SC3_B97_entry8_reaches_canonical_region_at16=True,
        canonical_Maria_source_record_aliases=aliases,
        no_new_entrypoint_route_role_or_macro_fixture=True,no_selected_scene_or_gameplay_claim=True,
        source_lil_scope182_includes32_ordinary_entry_unreachable_Maria_copy_records=True,
        remaining_Lil_player_facing_objects=150,remaining_Lil_speeches=116,remaining_Lil_actor_style_alternatives=34,
        preserve_appended_copies_as_unowned_current_bytes_during_Lil_relocation=True,
        canonical32_Maria_SC3_B97_records_remain_in_full_editorial_goal=True,
        no_global_source_universe_reaudit_or_older_record_technical_reaudit=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Four exact1886byte Japanese copies classified.12nativeVMreturn0 cases andbranchgraphs excludeappended SC0/SC1/SC2 tails;ordinarySC3B97entry reachescanonical32Maria speeches.150Lil targets+32canonicalMaria leads;zero editorialcredit.')
