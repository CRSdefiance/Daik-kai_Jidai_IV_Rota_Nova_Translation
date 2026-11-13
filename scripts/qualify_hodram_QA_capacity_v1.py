"""Bind the oversized synthetic script to observed saved-register corruption."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B301_B310_clean_20261107')
OUT=ROOT/'native_QA_capacity_v1.json'

def main():
    assert not OUT.exists()
    rebuilt=load(ROOT/'reconstruction_v1/reconstruction.json')
    registered=NdsImage.open(rebuilt['parent']);arm=registered.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    locks={0x23E04:'0f002de9',0x23E08:'f04f2de9',0x23E0C:'d0c19fe5',0x23E10:'0cd04de0',
        0x23E90:'10408de2',0x23F3C:'0400a0e1',0x23F40:'b30000eb',0x23F44:'0710a0e1',
        0x23F48:'0400a0e1',0x23F4C:'780000eb',0x24188:'081086e2',0x24190:'56b702eb',
        0x23FFC:'0f002de9',0x24000:'f04f2de9',0x24004:'14d04de2'}
    for offset,expected in locks.items():assert arm[offset:offset+4]==clean[offset:offset+4]==bytes.fromhex(expected)
    literal=0x23E0C+8+0x1D0
    assert literal==0x23FE4 and arm[literal:literal+4]==clean[literal:literal+4]
    allocation=struct.unpack_from('<I',arm,literal)[0];assert allocation==0x241C
    buffer_offset=0x10+8
    before_saved_registers=allocation-buffer_offset;assert before_saved_registers==0x2404
    limit=before_saved_registers//16*16;assert limit==0x2400
    terminal=ROOT/'return_trace_run_v8/terminal.json';t=load(terminal);observer=Path(t['observer'])
    assert digest(observer)==t['observer_sha256']
    traced=load(observer);assert not traced['errors'] and not traced['mismatches'] and traced['all_host_slots_restored_and_core_file_exact']
    entries=[r for r in traced['rows'] if r['kind']=='vm_command']
    assert entries[-2]['command_32_hex'].startswith('00c200000000') and entries[-1]['command_32_hex'].startswith('00000000')
    assert (entries[-2]['frame'],entries[-1]['frame'])==(28015,28016)
    # Source prologue: pushed r0-r3, nine saved registers, and20 local bytes.
    caller_SP=entries[-1]['SP']+16+36+20
    assert caller_SP==0x0218F298
    buffer=caller_SP+buffer_offset
    fixture=ROOT/'focused_fixtures_exit_v2/hodram_desert_temple_wolf_and_offer_fixture.json';f=load(fixture)
    image=NdsImage.open(f['research_ROM']);assert digest(f['research_ROM'])==f['research_ROM_sha256']
    block=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks[42]
    assert len(block)==10540 and len(block)>before_saved_registers
    snap=next(r['complete_readonly_snapshots']['WRAM'] for r in reversed(traced['rows']) if 'complete_readonly_snapshots' in r)
    raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256'] and len(raw)==0x400000
    assert raw[buffer-0x02000000:buffer-0x02000000+len(block)]==block
    saved=[]
    for index in range(9):
        address=caller_SP+allocation+4*index
        offset=address-buffer
        value=raw[address-0x02000000:address-0x02000000+4]
        assert value==block[offset:offset+4]
        saved.append(dict(register=['r4','r5','r6','r7','r8','r9','r10','r11','lr'][index],address=address,
            fixture_offset=offset,overwritten_hex=value.hex()))
    assert saved[-1]['fixture_offset']==0x2424 and saved[-1]['overwritten_hex']=='61792120'
    assert all(g['current_bytes']<=limit and g['target_bytes']<=limit for g in rebuilt['groups'])
    old=load('work/Hodram_B281_B300_clean_20261107/focused_fixtures_v1/hodram_royal_ruins_beasts_and_gunpowder_fixture.json')
    old_block=IlnkContainer.parse(NdsImage.open(old['research_ROM']).read_file('/data/SC1.DK4')).blocks[42]
    assert len(old_block)==9008 and len(old_block)<=limit
    save(OUT,dict(registered_ARM9_sha256=sha(arm),source_ARM9_sha256=sha(clean),
        source_current_consumer_code_exact=True,locked_native_instructions={hex(k):v for k,v in locks.items()},
        source_consumer_allocation=allocation,buffer_offset_from_frame_SP=buffer_offset,
        bytes_before_saved_registers=before_saved_registers,safe_QA_block_limit=limit,
        conservative_limit_rounds_hard_boundary_down_to16_bytes=True,
        oversized_fixture_bytes=len(block),observed_buffer_address=buffer,
        all10540_fixture_bytes_exact_in_native_stack_buffer=True,all_nine_saved_register_words_overwritten=saved,
        native_saved_LR_overwritten_by_fixture_text=True,exit_commands_reached_before_fault=True,
        source_QA_end_operand_changes_did_not_resolve_overflow=True,
        earlier_successful_fixture_bytes=len(old_block),production_reviewed_blocks=[dict(block=g['block'],parent_bytes=g['current_bytes'],target_bytes=g['target_bytes']) for g in rebuilt['groups']],
        all_ten_production_blocks_inside_conservative_bound=True,production_max_target_block_bytes=max(g['target_bytes'] for g in rebuilt['groups']),
        QA_fixture_construction_defect_not_a_production_script_edit=True,no_engine_orfont_change_required=True,
        next_action='Split the100 copied commands at complete block boundaries; check each padded QA block against this limit before writing a ROM. Keep all96 bindings andfour menus, then freshly verify returns.',
        capacity_guard_andbounded_gameplay_still_required=True,new_credit=0,
        evidence={str(p):digest(p) for p in [terminal,observer,Path(snap['path']),fixture,ROOT/'reconstruction_v1/reconstruction.json',Path(__file__)]}))
    print('Observed10540-byte QA script overwrites all nine caller-saved words; safe QA limit9216. All ten production blocks<=3276 bytes.')

if __name__=='__main__':main()
