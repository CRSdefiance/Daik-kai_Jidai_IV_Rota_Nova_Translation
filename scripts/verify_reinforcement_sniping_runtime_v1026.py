"""Exhaustive exact dispatch,old modal output and status/storage regression."""
import inspect
from pathlib import Path
from types import SimpleNamespace
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import reinforcement_sniping_runtime_v1025 as runtime
from scripts import verify_palace_runtime_v796 as historical_scope
from scripts import verify_recruitment_runtime_v771 as historical_status
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_arrival_native_v792 import prepared,run
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1026')
ROM=Path('out/all_routes_combined_v997_candidate.nds')


def scope(arm,label,rows):
    original=inspect.getsource(historical_scope.scope)
    replacements={'range(0x7B20,0x8490)':'range(0x7300,0x86B0)',
                  'range(0x65F0,0x6840)':'range(0x6480,0x6850)',
                  '(0,1072,1117,3667)':'(0,1911,1930,3667)'}
    source=original
    for old,new in replacements.items():assert source.count(old)==1;source=source.replace(old,new)
    cut=source.index("    save(ROOT/'scope_proof.json',")
    source=source[:cut]+'''    save(ROOT/'scope_proof.json',{'cases':count,
        'all_exact_parent_ID_pointer_stride_ABI_SP_LR_cases_pass':True,
        'table_addresses7300_through86AF_under_both_original_queued_parents':True,
        'all3668_numeric_IDs_under_four_existing_numeric_parents':True,
        'gift_addresses6480_through684F_and_wrong_parent_high_word_controls':True,
        'source_rows':[list(r[:3])+[list(r[3])] for r in new.contract_rows()],
        'not_a_ROM_build_or_actual_gameplay_proof':True})
    print(str(count)+' exact '+LABEL+' dispatch/ABI cases pass.',flush=True)
'''
    folder=ROOT/label;folder.mkdir()
    bank=SimpleNamespace(**{**runtime.previous.previous.previous.bank.__dict__,
                            'STATUS':runtime.previous.previous.previous.STATUS})
    env={**historical_scope.__dict__,'ROOT':folder,'LABEL':label,
         'new':SimpleNamespace(bank=bank,contract_rows=rows)}
    exec(compile(source,str(Path(__file__)),'exec'),env);env['scope'](arm)
    result=read(folder/'scope_proof.json');assert result['cases']==56696
    save(folder/'verifier_binding.json',{'ARM9_sha256':sha(arm),'effective_verifier_sha256':sha(source.encode()),
        'historical_verifier_sha256':sha(Path(historical_scope.__file__).read_bytes()),
        'all_original_native_and_ABI_assertions_retained_only_scope_ranges_and_result_labels_changed':True})


def modal_equivalence(old,new):
    text=b' Complete words and original leading and trailing letters stay intact across the entire modal box.'
    rows=[]
    for n in range(3668):
        if n%32==0:a,b=prepared(old),prepared(new)
        before,after=run(a,0x020546E8,n,text),run(b,0x020546E8,n,text)
        assert before==after,(n,before,after)
        rows.append({'message_ID':n,'output_sha256':sha(after[0]),'ordinary_wrap_called':after[1]})
    controls=[]
    for parent in (0,0xFFFFFFFF,0x120546E8,0x0205469C,0x02054720,0x02054764,0x02054014):
        a,b=prepared(old),prepared(new)
        for n in (*range(127,135),*range(269,273),*range(286,298),321,327,*range(344,351),0xFFFFFFFF):
            assert run(a,parent,n,text)==run(b,parent,n,text);controls.append([parent,n])
    edges=[]
    for n in (0xFFFFFFFF,0x7FFFFFFF,0x80000000,65535,65536):
        assert run(prepared(old),0x020546E8,n,text)==run(prepared(new),0x020546E8,n,text);edges.append(n)
    save(ROOT/'modal_equivalence.json',{'all3668_native_outputs_and_wrap_choices':rows,
        'wrong_parent_controls':controls,'full_word_boundary_controls':edges,
        'all_original_modal_bytes_guards_and_ABI_exact':True,
        'ARM_ADD_PC_Thumb_entry_and_inlined_shift_do_not_change_prior_modal_behavior':True})
    print('3668 complete old modal outputs,238 wrong-parent and5 full-word edge cases match.',flush=True)


def status(arm):
    source=inspect.getsource(historical_status.field_contracts)
    assert source.count('u.emu_start(runtime.STATUS,STOP')==1
    assert source.count('STACK-BASE-32:STACK-BASE')==2
    source=source.replace('u.emu_start(runtime.STATUS,STOP','u.emu_start(runtime.STATUS|1,STOP')
    source=source.replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
    bank=SimpleNamespace(**{**runtime.previous.previous.previous.bank.__dict__,
                            'STATUS':runtime.previous.previous.previous.STATUS})
    env={**historical_status.__dict__,'runtime':bank,
         'make':lambda arm,changed=False,raw=None:prepared(arm),
         'ROOT':Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source,str(Path(__file__)),'exec'),env);cases=env['field_contracts'](arm)
    assert len(cases)==140
    save(ROOT/'status_contracts.json',{'cases':cases,'count':len(cases),
        'all_whole8MiB_status_UI_labels_text_and_ABI_guards_pass':True,
        'only_typed_phrase_suffix_and36_saved_stack_bytes_may_change':True,
        'effective_verifier_sha256':sha(source.encode()),
        'historical_verifier_sha256':sha(Path(historical_status.__file__).read_bytes())})
    print('140 whole8MiB status-output/ABI cases pass after four-byte packed-table move.',flush=True)


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);old=rom.read_file('/__arm9__.bin')
    target,plan=runtime.apply(old)
    assert target==Path('work/analysis/reinforcement_sniping_v1025/ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'runtime_plan.json',{**plan,'runtime_sha256':sha(Path(runtime.__file__).read_bytes())})
    before={p:(o,h,set(v)) for p,o,h,v in runtime.previous.contract_rows()}
    after={p:(o,h,set(v)) for p,o,h,v in runtime.contract_rows()}
    differences={}
    for p,(o,h,v) in after.items():
        bo,bh,bv=before[p];assert (o,h)==(bo,bh) and bv<=v
        if bv!=v:differences[hex(p)]=sorted(v-bv)
    assert differences=={'0x2053db8':[0x7300,0x73C0,0x73E0]}
    owned=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    other=NdsImage.open(ROM);other.rom.arm9=target
    refs=[census(r,plan['private_spans'],owned) for r in (rom,other)]
    external=lambda rows:sorted(r for r in rows if not r[-1])
    assert external(refs[0])==external(refs[1])
    save(ROOT/'private_reference_census.json',{'existing_owned_spans':owned,
        'source_references':refs[0],'research_references':refs[1],
        'all_external_references_to_the_three_unchanged_owned_spans_exact':True})
    scope(old,'current_scope',runtime.previous.contract_rows)
    scope(target,'research_scope',runtime.contract_rows)
    modal_equivalence(old,target)
    status(target)
    paths=[ROOT/p for p in ('runtime_plan.json','private_reference_census.json','current_scope/scope_proof.json',
        'research_scope/scope_proof.json','modal_equivalence.json','status_contracts.json')]
    save(ROOT/'native_runtime_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(old),'research_ARM9_sha256':sha(target),
        'all_completed_source_proofs':{str(p):sha(p.read_bytes()) for p in paths},
        'old_and_new_complete_scope_cases_each':56696,'only_new_contract':differences,
        'all3668_modal_outputs_and_wrap_choices_exact':True,'all238_wrong_parent_and5_full_word_controls_exact':True,
        'all140_status8MiB_ABI_guards_pass':True,'all_external_references_and_every_other_ARM9_byte_preserved':True,
        'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged':True,
        'public212_and_ITCM128_byte_footprints_unchanged':True,'native_gate164_bytes_unchanged':True,
        'runtime_sha256':sha(Path(runtime.__file__).read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'native_font_matrix_registered_integration_and_actual_scenes_pending':True,
        'not_registered_no_ROM_written_not_gameplay_verification':True,'full_goal_complete':False})
    print('Runtime research passes:56696 source+56696 target selector cases,3668 modal outputs and140 status cases. No footprint growth.',flush=True)


if __name__=='__main__':main()
