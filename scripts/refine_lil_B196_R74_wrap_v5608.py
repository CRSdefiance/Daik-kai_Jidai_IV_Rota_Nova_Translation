"""Permit only three source/prose-bound ordinary wraps;retain every word and guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_wrap_tools_v5608')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B196_editorial_manuscript_v1.json')
    row=next(r for r in doc['records'] if r['source_record_index']==74)
    planned=read('work/analysis/lil_B196_layout_v5607b/all24_paragraph_layout_QA.json')
    lines=next(r for r in planned['records'] if r['id']==row['id'])['qa']['visible_lines']
    assert lines==['(...Admiral, if they halved the','price on the first try, they must','have been overcharging us. You can','haggle at least twice more.)']
    reason=('This complete129-character,23-word aside preserves the Admiral address,one-try halving inference and at-least-two-more advice. '
        'The three automatic complete-word boundaries after the,must and can use the verified available width;the next complete word cannot fit on each row under unchanged native lint. '
        'They are ordinary soft wraps in one paragraph,not dramatic pauses. Keep every word rather than shortening good prose or narrowing the whole passage to avoid a heuristic. '
        'This exact source/prose/row approval does not waive split words,glyphs,bounds,guard bytes,phase,controls,macros,pagination or any other record.')
    tail='''

def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_audit_before_reviewed_R74(source_raw,target_markup,profile)
    if source_raw.hex()==SOURCE_LITERAL and target_markup==TARGET_LITERAL:
        assert report['visible_lines']==LINES_LITERAL
        endings={1:'the',2:'must',3:'can'}
        approved=[i for i in report['issues'] if i['code']=='weak-line-ending' and any(
            i['message']==f"line {line} ends with weak wrap word {word!r}" for line,word in endings.items())]
        assert len(approved)==3
        report['issues']=[i for i in report['issues'] if i not in approved]
        report['reviewed_ordinary_boundaries']=[dict(line=line,after_word=word,exact_source_hex=SOURCE_LITERAL,
            exact_target=TARGET_LITERAL,reason=REASON_LITERAL) for line,word in endings.items()]
    return report
'''
    for key,value in {'SOURCE_LITERAL':row['source_hex'],'TARGET_LITERAL':row['english'],'LINES_LITERAL':lines,'REASON_LITERAL':reason}.items():tail=tail.replace(key,repr(value))
    rows=[derive('dk4tool/dialogue/lil_B196_layout_v2.py','dk4tool/dialogue/lil_B196_layout_v3.py',{
        'def audit_relocatable_dialogue_record(':'def _audit_before_reviewed_R74(',
        '    return report\n':'    return report\n'+tail})]
    rows.append(derive('scripts/plan_lil_B196_layout_v5607b.py','scripts/plan_lil_B196_layout_v5608.py',{
        'lil_B196_layout_v2':'lil_B196_layout_v3','layout_v5607b':'layout_v5608',
        "        r['compiled_hex']=encoded.encoded.hex();reports.append(":
        "        if qa.get('reviewed_ordinary_boundaries'):r['reviewed_ordinary_boundaries']=qa['reviewed_ordinary_boundaries']\n        r['compiled_hex']=encoded.encoded.hex();reports.append("}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_R74_ordinary_wrap_review.json',dict(tools=rows,
        record_ID=row['id'],exact_source_hex=row['source_hex'],exact_target=row['english'],visible_lines=lines,reason=reason,
        all24_words_encoded_bytes_and_native_guards_to_be_compared_separately=True,
        no_global_weak_word_waiver_authored_break_prose_shortening_metric_width_guard_or_phase_change=True,
        stopped_v1_v2_profiles_codecs_and_planners_preserved=True,new_editorial_credit=0,full_goal_complete=False))
