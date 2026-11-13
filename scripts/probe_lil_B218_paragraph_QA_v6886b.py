"""Expose unmodified base QA diagnostics for each already measured native paragraph."""
from dataclasses import replace
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B218_base_QA_v6886');DOC=Path('translations/lil_B218_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B218_layout_v6881b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes.json');FONT=Path('work/analysis/lil_B218_native_pages_v6882/all13_paragraphs13_complete_native_pages104_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,font=map(read,[DOC,PLAN,FONT]);assert plan['manuscript_sha256']==font['manuscript_sha256']==sha(DOC.read_bytes()) and font['layout_plan_sha256']==sha(PLAN.read_bytes());proofs=[]
    for p in plan['records']:
        row=next(r for r in doc['records'] if r['id']==p['id']);native=next(r for r in font['records'] if r['id']==p['id']);assert native['compiled_hex']==p['encoded_hex'];profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B218-source-native-QA-research:'+row['id'],max_lines=p['max_total_rows'],leading_speaker_bytes=frozenset([2,21]))
        def encoded(raw,text,prof):
            assert raw.hex()==row['source_hex'] and text==row['english'] and prof==profile
            return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**d) for d in p['diagnostics']))
        audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encoded},argdefs=qa.audit_relocatable_dialogue_record.__defaults__);report=audit(bytes.fromhex(row['source_hex']),row['english'],profile);proofs.append(dict(id=row['id'],lines=p['lines'],base_QA=report));print(row['id'],report['issues'])
    ROOT.mkdir(parents=True);save(ROOT/'all13_base_QA_diagnostics_before_any_scoped_classification.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),records=proofs,unmodified_base_QA_no_issues_removed_or_waived=True,formatting_policy_approval_negative_controls_names_actual_reference_and_release_pending=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,FONT,Path(__file__)]},full_goal_complete=False))
