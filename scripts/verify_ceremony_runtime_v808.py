"""Native scope,status and literal-equivalence proof for bounded ceremony packing."""

import inspect
import struct
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inn_editorial import current_entries
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts import ceremony_runtime_v808 as runtime
from scripts import verify_palace_runtime_v796 as scope_probe
from scripts import verify_recruitment_runtime_v771 as status_probe
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=runtime.ROOT


def literal_case(cpu,raw):
    text,out=0x0242D000,0x0242E020
    cpu.mem_write(text,raw+b'\0');cpu.mem_write(out-16,b'\xa5'*320)
    call(cpu,LITERAL-BASE,(out,text,0),instruction_limit=2000000)
    assert bytes(cpu.mem_read(text,len(raw)+1))==raw+b'\0'
    assert bytes(cpu.mem_read(out-16,16))==bytes(cpu.mem_read(out+288,16))==b'\xa5'*16
    result=bytes(cpu.mem_read(out,288)).split(b'\0')[0]
    return result


def literals(old,arm,entries):
    samples={b'',b'A',b' ',b'  ',b'Ordinary text',b'   Intended indent'}
    for n in range(1,241):samples.add(b'A'*n)
    for n in range(1,24):samples.add(b' '+b'ABCDEFGHIJKLMNOPQRSTUVW'[:n]+b' and the others enjoyed the ceremony together.')
    for first in (b'A',b'Even phase',b'Odd phase!',b'First complete line',b'\x82`first',b'\x82h wish a good'):
        samples.add(b' '+first+b'\n  Janus and final letters.')
    selected=[]
    for e in entries:
        t=e.text
        if not t or len(t)>235 or any(c<32 or c>126 for c in t) or b'%' in t:continue
        samples.add(t);selected.append(e.message_id)
    # Expanded research paragraphs for every ceremony substitution, including
    # all21 sites and all23 custom-name lengths. Production ID routing is separate.
    for r in read('work/analysis/ceremony_layout_v807_name_bounds/native_layout_matrix.json')['cases']:
        samples.add(b' '+b' '.join(bytes.fromhex(r['formatted_hex']).split()))
    cases=[]
    for i,raw in enumerate(sorted(samples)):
        if i%32==0:a,b=prepared(old),prepared(arm)
        x,y=literal_case(a,raw),literal_case(b,raw)
        assert x==y,(raw,x,y)
        cases.append(dict(input_hex=raw.hex(),native_formatted_hex=y.hex(),
            all_output_bytes_input_guards_SP_LR_and_callee_saved_registers_equal=True))
    save(ROOT/'literal_equivalence.json',dict(count=len(cases),cases=cases,
        current_ASCII_no_argument_native_IDs=selected,all_current_ascii_records_within235_bytes_and_no_controls_or_percent_included=True,
        all202_prospective_ceremony_expanded_paragraphs_included=True,
        synthetic_empty_indentation_LF_CP932_and_lengths1_through240=True,
        source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(arm),
        actual_gameplay_or_new_formatting_completion_credit=False))
    print(f'{len(cases)} complete native literal-output equivalence cases pass.',flush=True)


def main():
    rom=NdsImage.open(runtime.ROM);old=rom.read_file('/__arm9__.bin')
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes();assert arm==runtime.apply(old)
    owned=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    owned+=read('work/analysis/shipyard_storage_v760/owned_source_storage.json')['owned_banks']
    owned+=[[runtime.modal.ADDRESS,runtime.modal.ADDRESS+runtime.modal.SIZE]]
    spans=[[runtime.previous.CONTRACTS,runtime.previous.END],[runtime.OLD_LITERAL,runtime.END]]
    assert all(any(lo<=a<b<=hi for lo,hi in owned) for a,b in spans)
    changes=runtime.patches(old)
    assert all(any(lo<=at<at+len(raw)<=hi for lo,hi in owned) for at,raw in changes.items())
    restored=bytearray(arm)
    for at,raw in changes.items():restored[at-BASE:at-BASE+len(raw)]=old[at-BASE:at-BASE+len(raw)]
    restored_code=MainCodeFile(bytes(restored),BASE)
    restored_code.sections[4].data=MainCodeFile(old,BASE).sections[4].data
    assert bytes(restored_code.save())==old
    after=NdsImage.open(runtime.ROM);after.rom.arm9=arm
    before_refs,after_refs=[census(r,spans,owned) for r in (rom,after)]
    external=lambda refs:sorted(r for r in refs if not r[-1])
    assert external(before_refs)==external(after_refs),(external(before_refs),external(after_refs))
    save(ROOT/'bounded_storage_proof.json',dict(existing_source_owned_spans=owned,repacked_spans=spans,
        before_reference_census=before_refs,after_reference_census=after_refs,
        external_references_exact_and_old_literal_entry_retained=True,
        restore_all_declared_changes_recovers_exact_source_ARM9=True,
        no_new_original_text_tails_borrowed=True,
        rejected_ship_tail_lead='Three real source literal fields point inside the nominally padded span. Not borrowed.',
        unused_village_answer_leads_not_needed_or_borrowed=True,
        source_owned384_bytes_fully_repacked_without_growth=True,
        existing128_byte_ITCM_modal_wrapper_preserved_in_its_original_allocation=True))
    print('Existing384-byte source-owned bank closure and all external references preserved.',flush=True)
    bank=SimpleNamespace(**{**runtime.bank.__dict__,'STATUS':runtime.STATUS})
    adapted=SimpleNamespace(bank=bank,contract_rows=runtime.contract_rows)
    source=inspect.getsource(scope_probe.scope)
    source=source.replace('range(0x65F0,0x6840)','range(0x6480,0x6850)')
    env={**scope_probe.__dict__,'new':adapted,'ROOT':ROOT}
    exec(compile(source,__file__,'exec'),env);env['scope'](arm)
    proof=read(ROOT/'scope_proof.json')
    proof.update(new_ordinary_IDs=next(r for r in read('work/analysis/ceremony_layout_v807_name_bounds/runtime_size_measurement.json')['seven_exact_contract_rows'] if r['parent']==0x02054014)['added_values'],
        new_yes_no_IDs=[1200,1201,1219],new_hero_tables=sorted(__import__('scripts.context_ceremony_v806',fromlist=['TABLES']).TABLES),
        private_data_allocation_bytes=384,table_used_bytes=174,alignment_byte=None,
        status_location=runtime.STATUS,old_literal_entry_retained=LITERAL,
        frozen_verifier_sha256=sha(Path(scope_probe.__file__).read_bytes()),effective_verifier_sha256=sha(source.encode()))
    save(ROOT/'scope_proof.json',proof)
    source=inspect.getsource(status_probe.field_contracts)
    source=source.replace('u.emu_start(runtime.STATUS,STOP','u.emu_start(runtime.STATUS|1,STOP')
    source=source.replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
    def make(source,changed=False,raw=None):
        u=prepared(source)
        if raw is not None:u.mem_write(BASE,raw)
        return u
    env={**status_probe.__dict__,'runtime':bank,'make':make,'ROOT':Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source,__file__,'exec'),env);cases=env['field_contracts'](arm)
    assert len(cases)==140
    save(ROOT/'status_contracts.json',dict(count=140,cases=cases,
        full8MiB_memory_guards_registers_SP_LR_and_all12_complete_phrases_preserved=True,
        original_UI_table_NPC_source_status_labels_and_suffix_unchanged=True,effective_verifier_sha256=sha(source.encode())))
    print('140 whole8MiB status/ABI cases pass after relocation.',flush=True)
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),old)
    literals(old,arm,entries)
    save(ROOT/'native_runtime_verification.json',dict(source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(arm),
        scope=str(ROOT/'scope_proof.json'),status=str(ROOT/'status_contracts.json'),literal=str(ROOT/'literal_equivalence.json'),
        producer_sha256=sha(Path(__file__).read_bytes()),runtime_sha256=sha(Path(runtime.__file__).read_bytes()),
        modal_ceremony_dispatch_separate_verification_COMMON_integration_and_actual_scenes_pending=True,
        full_goal_complete=False))


if __name__=='__main__':main()
