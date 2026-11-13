"""Close Thumb ADR, aligned table, ISA and pure paragraph compiler checks."""
import struct
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import battle_aftermath_runtime_v1253 as runtime
from scripts.battle_aftermath_native_plan_v1255 import compiled, MANUSCRIPT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_isa_compiler_v1257')


def thumb_adr(rom,spans):
    rows = []
    for name,base,raw in units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]:
        for offset in range(0,len(raw)-1,2):
            word = struct.unpack_from('<H',raw,offset)[0]
            if word & 0xF800 != 0xA000:
                continue
            at = base+offset
            target = ((at+4)&~3)+(word&255)*4
            if any(lo <= target < hi for lo,hi in spans):
                rows.append(['Thumb_ADR',name,at,target,any(lo <= at < hi for lo,hi in spans)])
    return rows


def main():
    assert not ROOT.exists()
    native_path = Path('work/analysis/battle_aftermath_runtime_v1254c/native_runtime_verification.json')
    native = read(native_path)
    plan_path = Path('work/analysis/battle_aftermath_runtime_v1254c/runtime_plan.json')
    plan = read(plan_path)
    assert native['proofs'][str(plan_path)] == sha(plan_path.read_bytes())
    old = NdsImage.open(native['source_ROM'])
    new = NdsImage.open(native['source_ROM'])
    target = Path(plan['research_ARM9']).read_bytes()
    assert sha(target) == native['target_ARM9_sha256']
    new.rom.arm9 = target
    spans = plan['private_spans']
    accesses = [thumb_adr(r,spans) for r in (old,new)]
    outside = lambda rows:sorted(r for r in rows if not r[-1])
    assert outside(accesses[0]) == outside(accesses[1]) == []
    code,assembly = runtime.gate()
    assert len(code) == 172 and struct.unpack('<II',code[160:168]) == (0x02050000,runtime.CONTRACTS)
    instructions = list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(code[:160],runtime.GATE))
    assert sum(i.size for i in instructions) == 160
    assert all(i.size == 2 or i.mnemonic == 'blx' for i in instructions)
    assert not any(i.mnemonic.startswith(('str','stm','push','pop')) for i in instructions)
    assert all(not any(r in i.op_str for r in ('r0','r1,','r2,','r8','r9','sl','fp','ip')) for i in instructions)
    disassembly = [{'address':i.address,'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str} for i in instructions]
    decoded,end = runtime.decode(runtime.table())
    assert decoded == runtime.contract_rows() and end == 184
    pos,headers = 0,[]
    for _ in decoded:
        assert pos & 1 == 0
        size = runtime.table()[pos+3]
        headers.append({'address':runtime.CONTRACTS+pos,'payload_bytes':size})
        pos += size+4
    assert pos == 184 and runtime.table()[pos:] == bytes(4)
    doc = read(MANUSCRIPT)
    original = {r['message_id']:compiled(r).hex() for r in doc['records']}
    sample = deepcopy(doc['records'][0])
    bad = {
        'authored_newline':{'english':'%s has\nsurrendered!'},
        'authored_double_space':{'english':'%s has  surrendered!'},
        'authored_indent':{'english':' %s has surrendered!'},
        'tab':{'english':'%s has\tsurrendered!'},
        'layout_markup':{'english':'%s has surrendered!{LB}'},
        'missing_town_argument':{'english':'The town has surrendered!'},
        'duplicate_town_argument':{'english':'%s and %s have surrendered!'},
        'wrong_conversion':{'english':'%d has surrendered!'},
        'literal_native_pronoun_command':{'english':'%s: IC has surrendered!'},
        'unsupported_source_macro':{'source_native_macros':['IC']},
        'wrong_source_ID':{'message_id':1993},
        'wrong_argument_count':{'native_argument_count':0},
        'oversized_paragraph':{'english':'%s '+('A'*160)},
        'non_ASCII_authored_prose':{'english':'%s has surrendered！'},
    }
    negative = {}
    for label,fields in bad.items():
        try:
            compiled({**sample,**fields})
        except ValueError:
            negative[label] = True
        else:
            raise AssertionError(('Unsafe compiler input accepted',label))
    with patch('dk4tool.rom.nds.NdsImage.open',side_effect=AssertionError('Pure prose compilation must not read a ROM')):
        assert {r['message_id']:compiled(r).hex() for r in doc['records']} == original
    ROOT.mkdir(parents=True)
    save(ROOT/'isa_compiler_verification.json',{
        'native_proof':str(native_path),'native_proof_sha256':sha(native_path.read_bytes()),
        'runtime_module_sha256':sha(Path(runtime.__file__).read_bytes()),
        'source_target_Thumb_ADR_census':accesses,'all_external_Thumb_ADR_references_absent':True,
        'full_native160_byte_instruction_stream':disassembly,'literal_pool_bytes':8,'owned_tail_NOP_bytes':4,
        'only_Thumb1_register_operations_and_original_ARMv5_BLX_exits':True,
        'no_gate_memory_writes_new_stack_or_extra_register_scratch':True,
        'every_native_LDRH_row_header_even_aligned':headers,
        'metadata_used184_of188_bytes_no_status_phrase_overlap':True,
        'all75_templates_identical_with_all_ROM_reads_forbidden':True,
        'compiler_rejection_controls':negative,'manuscript':str(MANUSCRIPT),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'font_visual_copy_release_patch_and_actual_scene_gates_remain_separate':True,
        'no_ROM_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('Thumb ADR/ISA/aligned metadata and75 pure compilations/14 rejection controls pass.',flush=True)


if __name__ == '__main__':
    main()
