"""Frozen B214 whole paragraphs and automatic voice-body formatting."""
import struct
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B214_profile_v1 import contract,expected_profile
from scripts.plan_lil_B214_layout_v6705b import plan as frozen_plan
def binding(raw,text,profile):
    prefix='lil-B214-source-bound-v1:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B214 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B214 font/window/page/selector/guard/macro profile changed')
    r=d['record_bindings'][ident]
    if raw.hex()!=r['compiler_source_hex'] or text!=r['planning_record']['english'] or any(v in text for v in ['{LB','{ALIGN','{PAD','\n','\r']):raise ValueError('Exact B214 complete source and reviewed logical paragraph required')
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B214 native paragraph changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile)
    if any(i['severity'] in ['error','warning'] for i in report['issues']):raise ValueError('Unwaived B214 base QA issue')
    report.update(native_rows_per_page=4,native_page_count=r['native_page_count'],row_count_reason=r['row_count_reason'],reviewed_ordinary_boundaries=r['ordinary_wrap_reasons'],no_base_QA_issue_removed=True)
    return report