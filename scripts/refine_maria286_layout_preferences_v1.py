"""Select same-prose layout trials and resolve the measured FE guard-width risk."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    out=ROOT/'formatting_v1/preferences_v3_candidates.json';report=ROOT/'layout_candidate_selection_v1.json'
    assert not out.exists() and not report.exists()
    doc_path=ROOT/'formatting_v1/formatting_input.json';doc=load(doc_path)
    rows={(r['block'],r.get('source_record_index')):r for r in doc['records']}
    prefs=deepcopy(load(ROOT/'formatting_v1/preferences_v2_trials.json'));rules=prefs['records']
    retentions=[]
    for key,reason in [
        ((38,29),'Retain the original complete-word trouble/you wrap: enforcing the phrase creates a sparse Should Europeans row without improving the whole paragraph.'),
        ((40,22),'Retain the original serves/as boundary: forcing the pair creates a sparse opening and degrades balance in the unchanged four-row paragraph.'),
        ((43,18),'Retain the original taken/the first step boundary: forcing the noun phrase strands We’ve and makes the predicate less natural.'),
        ((47,179),'Retain the original fight/for them boundary: enforcing all three words adds a sparse fourth row; the original reassurance reads naturally in context.'),
    ]:
        row=rows[key];rules.pop(row['id']);retentions.append(dict(id=row['id'],reason=reason))
    pages={
        (40,16):'the trade route is essentially a single line.',
        (48,194):"I'd like to hear about the situation there lately.",
        (48,216):'Admirals Valdes and Pasha keep skirmishing with each other.',
        (49,96):'Then, the moment he saw how tough the enemy was, he turned on me!',
        (49,136):"What's wrong with taking them back?",
    }
    for key,clause in pages.items():
        row=rows[key];rule=rules[row['id']];assert row['english'].count(clause)==1
        rule.pop('one_page');rule.update(page_clause=clause,
            reason='The identical prose does not fit four guarded rows. Keep this complete closing clause/question on a page, avoiding a stranded continuation.')
    row=rows[(48,21)];rules.pop(row['id'])
    retentions.append(dict(id=row['id'],reason='Retain the original two-page boundary: the full threat begins page two and its line break is coherent; a one-page plan cannot preserve all words and guards.'))
    additions={
        (48,57):(['pleased to meet you'],'Keep Maria’s short introduction formula intact.'),
        (48,83):(['idea you'],'Avoid the sparse I had no idea opening by keeping the transition into Rafael’s surprised compliment together.'),
        (48,227):(['strait of gibraltar'],'Keep the source-named strait together where it fits.'),
        (49,130):(["wasn't it"],'Keep the short rhetorical question tag together rather than isolating it? on the following row.'),
        (50,57):(['like you'],'Avoid breaking the short comparison after like in the mocking admiral farewell.'),
    }
    for key,(phrases,reason) in additions.items():
        row=rows[key]
        rules[row['id']]=dict(required_pairs=[list(p) for phrase in phrases for p in zip(phrase.split(),phrase.split()[1:])],
            one_page=True,reason=reason,bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    for key in [(50,36),(50,43),(50,53),(50,76)]:
        row=rows[key]
        rules[row['id']]=dict(FE_planning_cells=36,one_page=True,
            reason='Use the existing validated scoped FE36 guard budget on the unchanged physical228px consumer. Native R36 inserted a blank row at a guarded full line; R43 failed original complete-glyph/bounds checks. No viewport, font, executable or prose changes.',
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        if key==(50,43):rules[row['id']]['required_pairs']=[['far','east']]
    rules[rows[(47,140)]['id']]['required_pairs']=[['proof','of'],['of','conqueror']]
    assert len(rules)==32
    save(out,prefs)
    initial=ROOT/'initial_native_v1';files=sorted(initial.glob('DK4_MES_B50_*.png'))
    assert len(files)==7
    sheet=Image.new('RGB',(912,640),'#263238');draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(files):
        pic=Image.open(path).convert('RGB');x,y=i%2*456,i//2*160
        draw.text((x+3,y+3),path.stem+' initial pre-failure',fill='white')
        sheet.paste(pic.resize((pic.width*2,128),Image.Resampling.NEAREST),(x,y+24))
    sheet_path=ROOT/'B50_initial_completed7.png';sheet.save(sheet_path)
    save(report,dict(phase='candidates_only',preferences=str(out),preferences_sha256=digest(out),
        reviewed_initial_complete_blocks=list(range(37,50)),directly_viewed_initial_body_pages=276,
        initial_body_sheets=[dict(path=str(p),sha256=digest(p)) for p in sorted(initial.glob('B*_part*.png'))],
        all42_scoped_name_strings_andboth_menu_sheets_directly_viewed=True,
        layout_retentions=retentions,four_potential_pages_reclaimed_without_prose_changes=[rows[k]['id'] for k in [(47,53),(47,140),(49,85),(49,167)]],
        failed_one_page_trials_preserved=load(ROOT/'format_trials_v1/automatic_plans.json')['failures'],
        concrete_FE_risk='B50R36 blank native row; B50R43 original painter assertion. Keep original failure and do fresh B50 checks after scoped guard-budget planning.',
        native_FE_diagnostic=str(ROOT/'FE_row_diagnostic_v1.json'),native_FE_diagnostic_sha256=digest(ROOT/'FE_row_diagnostic_v1.json'),
        initial_B50_completed7_contact_sheet=dict(path=str(sheet_path),sha256=digest(sheet_path),direct_view_pending=True),
        final_new_pages_native_andvisual_approval_pending=True,all_fifth_gates_false=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,ROOT/'layout_trial_findings_v1.json',Path(__file__)]}))
    print('Saved32 layout candidates/five contextual layout retentions;FE risk bounded;no prose changes orfinal page approval.')

if __name__=='__main__':main()
