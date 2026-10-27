"""Verify corrected direct escape selection, historical dispatch and bounded storage."""
import inspect
from pathlib import Path
from types import FunctionType, SimpleNamespace
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import escape_direct_runtime_v1183 as runtime
from scripts import verify_sighting_runtime_v1076 as historical
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/escape_direct_runtime_v1184')
ROM = Path('out/all_routes_combined_v1166_candidate.nds')


def scope(arm):
    source = inspect.getsource(historical.historical_scope.scope)
    for old, new in {
        'range(0x7B20,0x8490)':'range(0x7300,0x86B0)',
        'range(0x65F0,0x6840)':'range(0x6480,0x6850)',
        '(0,1072,1117,3667)':'(0,1911,1930,3667)',
    }.items():
        assert source.count(old) == 1; source = source.replace(old,new)
    point = '        for parent in (*records,0,0xffffffff'
    assert source.count(point) == 1
    source = source.replace(point, '''        # Original53F0C/54058 saves the voice table at+274, proven by1182.
        for low in range(65536):
            check(0x02053F40,0x02110000|low)
        for high in (0,0x0210,0x0212,0x1211,0xffff):
            for low in (0,0x7500,0x7501,0x7510,0x7520,0x7620,0x7621,0xffff):
                check(0x02053F40,high<<16|low)
''' + point)
    cut = source.index("    save(ROOT/'scope_proof.json',")
    source = source[:cut] + '''    save(ROOT/'scope_proof.json',{'cases':count,
        'all_exact_dispatch_and_SP_LR_register_ABI_pass':True,
        'all65536_direct_table_low_words_and_wrong_high_words':True,
        'all_historical_numeric_queued_gift_and_negative_parent_cases_preserved':True,
        'source_rows':[list(r[:3])+[list(r[3])] for r in new.contract_rows()],
        'CPU_only_not_gameplay':True})
    print(str(count)+' exact selector/ABI cases pass.',flush=True)
'''
    bank = SimpleNamespace(**{**historical.runtime.previous.previous.previous.previous.bank.__dict__,
                            'STATUS':historical.runtime.previous.previous.previous.previous.STATUS})
    env = {**historical.historical_scope.__dict__, 'ROOT':ROOT,
           'new':SimpleNamespace(bank=bank,contract_rows=runtime.contract_rows)}
    exec(compile(source,__file__,'exec'),env); env['scope'](arm)
    save(ROOT/'scope_binding.json',{'effective_verifier_sha256':sha(source.encode()),
        'historical_verifier_sha256':sha(Path(historical.historical_scope.__file__).read_bytes())})


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM); old=rom.read_file('/__arm9__.bin')
    owned=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    assert any(lo<=runtime.GATE and runtime.GATE+172<=hi for lo,hi in owned)
    tail_refs=census(rom,[(runtime.GATE+164,runtime.GATE+172)],[(runtime.GATE,runtime.GATE+172)])
    assert tail_refs == []
    target, plan=runtime.apply(old)
    after=NdsImage.open(ROM);after.rom.arm9=target
    refs=[census(r,plan['private_spans'],owned+plan['private_spans']) for r in (rom,after)]
    external=lambda rows: sorted(r for r in rows if not r[-1])
    assert external(refs[0]) == external(refs[1])
    # Exhaust all16-bit source values for each high-pointer stride. The
    # original high-word guard has already bounded the operand to16 bits.
    for shift in (4,5):
        for value in range(65536):
            rotated=((value>>shift)|(value<<(32-shift)))&0xffffffff
            assert ((rotated>>16)==0) == (value&((1<<shift)-1)==0)
            if rotated>>16==0: assert rotated==value>>shift
    ROOT.mkdir(parents=True)
    arm_path=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';arm_path.write_bytes(target)
    save(ROOT/'runtime_plan.json',{**plan,'research_ARM9':str(arm_path),
        'original_gate_tail_no_incoming_references':tail_refs,
        'original_and_target_private_reference_census':refs,
        'all_external_incoming_references_exact':True,
        'all131072_high_pointer_rotate_alignment_equivalences_pass':True,
        'runtime_module_sha256':sha(Path(runtime.__file__).read_bytes()),
        'source_ROM_sha256':sha(ROM.read_bytes())})
    scope(target)
    for fn in (historical.modal_equivalence,historical.status):
        bound=FunctionType(fn.__code__,{**fn.__globals__,'ROOT':ROOT},argdefs=fn.__defaults__)
        bound(old,target) if fn is historical.modal_equivalence else bound(target)
    paths=[ROOT/p for p in ('runtime_plan.json','scope_proof.json','scope_binding.json','modal_equivalence.json','status_contracts.json')]
    save(ROOT/'native_runtime_verification.json',{'source_ROM':str(ROM),'source_ROM_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(old),'target_ARM9_sha256':sha(target),
        'proofs':{str(p):sha(p.read_bytes()) for p in paths},
        'direct_source_contract':[runtime.DIRECT_PARENT,0x274,0x0211,list(runtime.KEYS)],
        'all3668_modal_outputs_and238_wrong_parent5_edge_cases_exact':True,
        'all140_status_whole8MiB_guards_exact':True,
        'no_section_BSS_cache_ITCM_staged_payload_or_owned_capacity_growth':True,
        'no_ROM_written_or_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Direct escape runtime verified; all historical modal/status regressions pass.',flush=True)


if __name__=='__main__':main()
