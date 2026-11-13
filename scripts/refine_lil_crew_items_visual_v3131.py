"""Three faithful paragraph refinements from complete native-sheet visual review."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Crew_Items_visual_refine_v3131')
OLD=Path('translations/lil_crew_items_editorial_manuscript_v4.json')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_Crew_Items_fonts_v3128/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Crew_Items_FE_v3129/current_FE_macro_font_and_typed_paper_proof.json')
MENU=Path('work/analysis/lil_Crew_Items_choices_v3130/all1_typed_menu_native_proof.json')
CHANGES={
'DK4_MES_B88_R0075':("I brought it up, anyway. You're a funny man, Yukihisa.",'Preserve Angelo first-person ownership of the topic andthe funny-word setup forYukihisa reaction. Natural concise phrasing keeps brought it up together rather than splitting the idiom acrossrows;no character intent orstoryfact changes.'),
'DK4_MES_B92_R0044':("I appreciate your faith in Christina, Admiral. But she's still my granddaughter. Think of an old man's feelings.",'Preserve gratitude,admiral trust,explicit granddaughter andappeal tounderstand anoldman. The natural direct appeal replaces a stranded Please atrowend without weakening his concern oradding a relationship.'),
'DK4_MES_B94_R0013':("Let's find the Jaguar God's Vest!",'Keep the shared search proposal andexact itemname. Find here states the proposed goal,not a guaranteed discovery;the next source lines explicitly remain rumors. This natural wording avoids splitting the short look-for proposal around the protected itemname.')}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));font,fe,menu=map(read,[FONT,FE,MENU])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==191
    sheets=font['review_sheets']+fe['review_sheets']+[dict(path=m['review_sheet'],sha256=m['review_sheet_sha256']) for m in menu['menus']]
    assert len(sheets)==26 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    # All24ordinary/oneFE/onemenu sheets were viewed before this producer.
    changes=[]
    for row in doc['records']:
        if row['id'] not in CHANGES:continue
        prose,note=CHANGES[row['id']];previous=row['english']
        if row.get('qa_waivers')==['line-break-count']:
            suffix=' '+row['qa_waiver_reason'];assert row['localization_note'].endswith(suffix)
            row['localization_note']=row['localization_note'][:-len(suffix)];row.pop('qa_waivers');row.pop('qa_waiver_reason')
        row['english']=previous.split('}',1)[0]+'}'+prose;row['localization_note']+=' '+note
        assert row['editorial_decision']=='revise' and not row['review']['formatting']
        changes.append(dict(id=row['id'],source_Japanese=row['source_Japanese'],source_meaning=row['source_meaning'],previous=previous,english=row['english'],reason=note))
    assert len(changes)==3
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),visual_refinements_require_complete_delta_native_revalidation=True)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'three_native_visual_flow_findings.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,all26_initial_native_sheets_viewed=sheets,prior_fonts=str(FONT),prior_fonts_sha256=sha(FONT.read_bytes()),FE=str(FE),FE_sha256=sha(FE.read_bytes()),menu=str(MENU),menu_sha256=sha(MENU.read_bytes()),no_global_or_formatter_change=True,all_failed_drafts_plans_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),native_delta_fonts_reference_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Three faithful visual-flow refinements;all26initial native sheets viewed. Changed planes require native reexecution;unchanged planes require exact reuse hashes.')
