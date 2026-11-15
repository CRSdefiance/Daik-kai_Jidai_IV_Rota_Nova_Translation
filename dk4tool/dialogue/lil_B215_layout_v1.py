"""Frozen B215 whole paragraphs with three individually scoped warning decisions."""
import struct
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B215_profile_v1 import contract,expected_profile
from scripts.plan_lil_B215_layout_v6747c import plan as frozen_plan
def binding(raw,text,profile):
    prefix='lil-B215-source-bound-v1:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B215 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B215 font/window/page/selector/guard/macro profile changed')
    r=d['record_bindings'][ident]
    if raw.hex()!=r['compiler_source_hex'] or text!=r['planning_record']['english'] or any(v in text for v in ['{LB','{ALIGN','{PAD','\n','\r']):raise ValueError('Exact B215 complete source and reviewed logical paragraph required')
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B215 native paragraph changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile)
    warnings=[i for i in report['issues'] if i['severity']=='warning']
    if any(i['severity']=='error' for i in report['issues']) or warnings!=r['approved_warning_issues'] or bool(warnings)!=bool(r['warning_waiver_reason']):raise ValueError('Unapproved B215 base QA issue')
    report.update(approved_warning_issues=r['approved_warning_issues'],warning_waiver_codes=r['warning_waiver_codes'],warning_waiver_reason=r['warning_waiver_reason'],all_base_diagnostics_retained=True)
    report.update(native_rows_per_page=4,native_page_count=r['native_page_count'],row_count_reason=r['row_count_reason'],reviewed_ordinary_boundaries=r['ordinary_wrap_reasons'],no_base_QA_issue_removed=True)
    return report