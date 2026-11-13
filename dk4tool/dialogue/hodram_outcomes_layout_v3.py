"""Exact approved Hodram-outcomes prose; deterministic automatic wrapping and unchanged base QA."""
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.hodram_outcomes_profile_v3 import contract,expected_profile
from dk4tool.dialogue.hodram_outcomes_plan_v1 import plan as frozen_plan
def binding(raw,text,profile):
    prefix="Hodram-outcomes-source-bound-v1:"
    if not profile.name.startswith(prefix):raise ValueError("Exact per-record Hodram-outcomes profile required")
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d["record_bindings"] or profile!=expected_profile(ident):
        raise ValueError("Hodram-outcomes font/window/page/selector/guard/macro profile changed")
    r=d["record_bindings"][ident]
    if not isinstance(raw,bytes) or raw.hex()!=r["compiler_source_hex"] or text!=r["planning_record"]["english"] or any(v in text for v in ["{LB","{ALIGN","{PAD","\n","\r"]):
        raise ValueError("Exact Hodram-outcomes complete source and reviewed logical paragraph required")
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r["planning_record"]))
    if p["encoded_hex"]!=r["compiled_hex"] or p["lines"]!=r["lines"]:
        raise ValueError("Frozen Hodram-outcomes native paragraph changed")
    encoded=bytes.fromhex(p["encoded_hex"])
    if encoded[0]!=r["source_selector"] or b"\0" in encoded[1:]:
        raise ValueError("Complete original speaker preamble and NUL-free body required")
    return RelocatableDialogueEncoding(p["formatted_markup"],encoded,tuple(DialogueDiagnostic(**v) for v in p["diagnostics"]))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,"encode_relocatable_dialogue":encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile);issues=report["issues"]
    if issues!=r["base_QA_issues"] or any(i["severity"]=="error" for i in issues) or [i for i in issues if i["severity"]=="warning"]!=([r["qa_waiver_scope"]["exact_issue"]] if r["qa_waivers"] else []):
        raise ValueError("Exact Hodram-outcomes base QA diagnostics and exact source-bound warning exception required")
    report.update(base_QA_issues=list(issues),all_original_base_QA_issues_preserved=True,
        native_rows_per_page=4,native_page_count=r["native_page_count"],row_count_reason=r["row_count_reason"],
        reviewed_ordinary_boundaries=r["ordinary_wrap_reasons"],no_warning_removal=True,qa_waivers=r["qa_waivers"],qa_waiver_reason=r["qa_waiver_reason"],qa_waiver_scope=r["qa_waiver_scope"],
        original_consumer=r["consumer"],source00_preamble_separate_from_body=r["source_selector"]==0)
    return report
