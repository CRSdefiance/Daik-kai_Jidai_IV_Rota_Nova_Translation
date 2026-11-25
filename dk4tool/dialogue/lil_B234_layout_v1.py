"""Frozen B234 whole paragraphs with source-bound complete-word boundaries and one exact R33 line1 article-wrap classification andeight informational row-count reasons."""
import struct
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B234_profile_v1 import contract,expected_profile
from scripts.plan_lil_B234_layout_v7586d import plan as frozen_plan
def binding(raw,text,profile):
    prefix='lil-B234-source-bound-v1:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B234 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B234 font/window/page/selector/guard/macro profile changed')
    r=d['record_bindings'][ident]
    if raw.hex()!=r['compiler_source_hex'] or text!=r['planning_record']['english'] or any(v in text for v in ['{LB','{ALIGN','{PAD','\n','\r']):raise ValueError('Exact B234 complete source and reviewed logical paragraph required')
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B234 native paragraph changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile)
    original=list(report['issues']);reviewed=r['exact_reviewed_base_warnings']
    if original!=r['base_QA_issues']:raise ValueError('Exact B234 base QA diagnostics changed')
    actual=[i for i in original if i['severity']=='warning']
    if actual!=reviewed or any(i['severity']=='error' for i in original):raise ValueError('Unwaived B234 base QA issue')
    if reviewed and (r['qa_waivers']!=['weak-line-ending'] or not r['qa_waiver_reason']):raise ValueError('Exact B234 record waiver reason required')
    report['issues']=[i for i in original if i not in reviewed]
    report.update(base_QA_issues=original,exact_reviewed_base_warnings=reviewed,
        qa_waivers=r['qa_waivers'],qa_waiver_reason=r['qa_waiver_reason'],
        native_rows_per_page=4,native_page_count=r['native_page_count'],
        row_count_reason=r['row_count_reason'],reviewed_ordinary_boundaries=r['ordinary_wrap_reasons'],
        all_original_base_QA_issues_preserved=True,no_global_weak_boundary_rule_changed=True)
    return report
