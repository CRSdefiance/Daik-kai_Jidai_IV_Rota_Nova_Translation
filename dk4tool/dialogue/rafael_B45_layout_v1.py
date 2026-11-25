"""Exact approved B45 prose; deterministic automatic wrapping and unchanged base QA."""
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.rafael_B45_profile_v1 import contract,expected_profile
from dk4tool.dialogue.rafael_B45_plan_v1 import plan as frozen_plan
def binding(raw,text,profile):
    prefix="Rafael-B45-source-bound-v1:"
    if not profile.name.startswith(prefix):raise ValueError("Exact per-record Rafael-B45 profile required")
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d["record_bindings"] or profile!=expected_profile(ident):
        raise ValueError("Rafael-B45 font/window/page/selector/guard/macro profile changed")
    r=d["record_bindings"][ident]
    if not isinstance(raw,bytes) or raw.hex()!=r["compiler_source_hex"] or text!=r["planning_record"]["english"] or any(v in text for v in ["{LB","{ALIGN","{PAD","\n","\r"]):
        raise ValueError("Exact Rafael-B45 complete source and reviewed logical paragraph required")
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r["planning_record"]))
    if p["encoded_hex"]!=r["compiled_hex"] or p["lines"]!=r["lines"]:
        raise ValueError("Frozen Rafael-B45 native paragraph changed")
    encoded=bytes.fromhex(p["encoded_hex"])
    if encoded[0]!=r["source_selector"] or b"\0" in encoded[1:]:
        raise ValueError("Complete original speaker preamble and NUL-free body required")
    return RelocatableDialogueEncoding(p["formatted_markup"],encoded,tuple(DialogueDiagnostic(**v) for v in p["diagnostics"]))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,"encode_relocatable_dialogue":encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile);issues=report["issues"]
    if issues!=r["base_QA_issues"] or any(i["severity"] in ["warning","error"] for i in issues):
        raise ValueError("Exact Rafael-B45 base QA diagnostics required without waivers")
    report.update(base_QA_issues=list(issues),all_original_base_QA_issues_preserved=True,
        native_rows_per_page=4,native_page_count=1,row_count_reason=r["row_count_reason"],
        reviewed_ordinary_boundaries=r["ordinary_wrap_reasons"],no_warning_removal_orwaivers=True,
        original_consumer=r["consumer"],source00_preamble_separate_from_body=r["source_selector"]==0)
    return report
