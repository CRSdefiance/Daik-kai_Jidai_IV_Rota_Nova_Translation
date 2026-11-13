"""Source-locked whole-paragraph compiler for B211 and its twelve complete progressive/FE single-page paragraphs."""
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B211_profile_v2 import contract,expected_profile
from scripts.plan_lil_B211_layout_v6559c import plan as frozen_plan
def binding(source_raw,target_markup,profile):
    prefix='lil-B211-source-bound-v2:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B211 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B211 font,viewport,page,selector,guard or substitution profile changed')
    r=d['record_bindings'][ident]
    if source_raw.hex()!=r['compiler_source_hex']:raise ValueError('B211 exact source/kind/virtual-selector contract required')
    if target_markup!=r['planning_record']['english'] or any(v in target_markup for v in ['{LB','{ALIGN','{PAD','\n','\r']):raise ValueError('B211 reviewed logical paragraph and complete selector required')
    return ident,r
def encode_relocatable_dialogue(source_raw,target_markup,profile):
    ident,r=binding(source_raw,target_markup,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B211 source/prose/native layout changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**d) for d in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    ident,r=binding(source_raw,target_markup,profile);report=_audit(source_raw,target_markup,profile);removed=[]
    for issue in list(report['issues']):
        if issue['code']=='weak-line-ending' and issue['message'] in r['approved_base_weak_messages']:
            report['issues'].remove(issue);removed.append(issue)
    if len(removed)!=len(r['approved_base_weak_messages']):raise ValueError('Exact reviewed B211 ordinary boundary no longer present')
    report['reviewed_ordinary_boundaries']=r['ordinary_wrap_reasons'];report['native_rows_per_page']=4;report['native_page_count']=r['native_page_count'];report['row_count_reason']=r['row_count_reason']
    return report
