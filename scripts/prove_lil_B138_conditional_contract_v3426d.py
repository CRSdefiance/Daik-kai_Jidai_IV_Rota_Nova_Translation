"""Source-bound raw predicate results; preserve a legitimate result2 at B138+039C."""
import inspect
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_crew_items_controls_v3114 import predicate as original_predicate
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_conditional_contract_v3426d')
DIAGNOSTIC=Path('work/analysis/lil_B138_conditional_diagnostic_v3426c/all11_original_assertion_results.json')
SCOPED_RESULTS={'00818900':0,'0080ffff00010ea2':0,'0080ffff00000ea0':1,'0080ffff14fe0030':1,'0080ffff200301a1':2,'0080ffff15fe0030':0,'0080ffff0efe0030':1,'0080ffff16fe0030':0,'0080ffff17fe0030':0,'0080ffff000009a0':1}

def source_owned_predicate():
    text=inspect.getsource(original_predicate)
    before="assert values[0]==2 and values[1] in [0,1] and extent==command['native_extent']"
    after="assert values[0]==2 and values[1]==SCOPED_RESULTS[command['whole_command_hex']] and extent==command['native_extent']"
    assert text.count(before)==1;text=text.replace(before,after)
    env={**original_predicate.__globals__,'SCOPED_RESULTS':SCOPED_RESULTS};exec(compile(text,str(Path(__file__))+'::source-exact-predicate','exec'),env)
    return env['predicate'],text

if __name__=='__main__':
    assert not ROOT.exists();observed=read(DIAGNOSTIC);assert len(observed['cases'])==11
    failed=[r for r in observed['cases'] if not r['original_assertions_pass']];assert len(failed)==1 and failed[0]['offset']==924 and failed[0]['observed']['values']==[2,2,0,0,0,0]
    assert all(SCOPED_RESULTS[r['observed']['command']['whole_command_hex']]==r['observed']['values'][1] for r in observed['cases'])
    source=read('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');current=NdsImage.open(source['current_ROM']).read_file('/__arm9__.bin');historical=NdsImage.open(source['historical_snapshot_ROM']).read_file('/__arm9__.bin')
    start,end=0x29874,0x299C8;assert clean[start:end]==current[start:end]==historical[start:end]
    assert current[0x29960:0x29964]==bytes.fromhex('040086e5') and current[0x29980:0x299A0]==bytes.fromhex('aee7ffeb000050e30110a0130200a0e30010a003000086e510d08de2041086e5')
    # 8000 stores the expression evaluator's raw r0. Only 8100 normalizes its query result.
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);ROOT.mkdir(parents=True);dis=ROOT/'source_exact_8000_raw_and8100_boolean_handlers.txt'
    dis.write_text('\n'.join(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in decoder.disasm(current[start:end],0x02000000+start))+'\n',encoding='utf-8')
    fn,text=source_owned_predicate();p=ROOT/'scoped_predicate.py';p.write_text(text,encoding='utf-8')
    save(ROOT/'native_result_contract.json',dict(source_context='work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json',diagnostic=str(DIAGNOSTIC),diagnostic_sha256=sha(DIAGNOSTIC.read_bytes()),unchanged_handler_span=[start,end],unchanged_handler_sha256=sha(current[start:end]),disassembly=str(dis),disassembly_sha256=sha(dis.read_bytes()),source_owned_helper=str(p),source_owned_helper_sha256=sha(p.read_bytes()),scoped_expected_unforced_results=SCOPED_RESULTS,all11_results_bound_to_exact_source_operands_and_historical_context=True,source_8000_preserves_raw_evaluator_r0_in_result_slot=True,source_8100_normalizes_event_completion_query_to_boolean=True,B138_offset924_result2_is_valid_not_a_boolean=True,relative_0400_last_result2_native_path_already_checked=True,no_fixture_code_patch_source_change_or_check_waiver=True,first_query_diagnostic_did_not_reproduce_failure_and_is_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    a=Path('scripts/prove_lil_B138_controls_v3426.py');b=Path('scripts/prove_lil_B138_controls_v3426e.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    t=t.replace("ROOT=Path('work/analysis/lil_B138_controls_v3426')","ROOT=Path('work/analysis/lil_B138_controls_v3426e')")
    t=t.replace("    cases=[]","    from scripts.prove_lil_B138_conditional_contract_v3426d import source_owned_predicate\n    scoped_predicate,scoped_text=source_owned_predicate()\n    adapters['predicate']=scoped_text\n    cases=[]",1)
    assert 'ctx.execute(prior.predicate,' in t;t=t.replace('ctx.execute(prior.predicate,','ctx.execute(scoped_predicate,')
    t=t.replace("source_macro_counts=macros,","source_macro_counts=macros,source_exact_conditional_result_contract='work/analysis/lil_B138_conditional_contract_v3426d/native_result_contract.json',source_exact_conditional_result_contract_sha256=sha(Path('work/analysis/lil_B138_conditional_contract_v3426d/native_result_contract.json').read_bytes()),")
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    save(ROOT/'successor_provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),all_previous_failures_and_producers_preserved=True,full_goal_complete=False))
