"""Record two exact ordinary word boundaries without changing prose,compiled rows or global lint."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_wrap_review_v6293');TARGET=Path('dk4tool/dialogue/lil_B206_layout_v2.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists();doc=read('translations/lil_B206_editorial_manuscript_v3.json');qa=read('work/analysis/lil_B206_layout_v6292/all24_spoken_paragraph_layout_QA.json');assert [r['id'] for r in qa['failures']]==['DK4_MES_B206_R0046','DK4_MES_B206_R0117'];rules=[]
    for idx in [46,117]:
        row=next(r for r in doc['records'] if r['kind']=='progressive' and r['source_record_index']==idx);report=next(r for r in qa['records'] if r['id']==row['id']);failure=next(r for r in qa['failures'] if r['id']==row['id'])
        if idx==46:
            reason='This complete seller pitch contrasts wearing the earrings with giving them to a woman at the tavern,winning her friendship and obtaining information. The ordinary complete-word wrap after her continues directly with over. in the same uninterrupted paragraph;there is no new punctuation,page,input hold or implied pause. Retain every source-qualified word and the full final friendship sentence rather than shorten natural prose or narrow all rows to avoid a heuristic. The four substantial automatic rows use the original guarded width;the independently reviewed glyph proof must preserve both her and over,all other words,controls,bounds and one-page return. This exact phrase boundary is acceptable continuous English prose,not a global permission to strand pronouns or change phrasal-verb wording.'
            line=3;after='her';before='over.'
        else:
            reason='The source seller complains that the customers still fail to understand after his explanation,then refuses the sale and dismisses them. The automatic complete-word boundary after still continues directly with don\'t get it? in the same paragraph. The adverb and negated question remain intact in meaning and delivery;no punctuation,page or extra input hold turns this into a dramatic pause. Three substantial rows retain his whole complaint and refusal without shortening or padding the English. This exact source/prose/row approval does not relax any complete-glyph,bounds,pagination,guard,pair-phase,control or other-record check.'
            line=1;after='still';before="don't"
        issues=[i for i in failure['issues'] if i['code'] in ['weak-line-ending','split-protected-phrase']];assert len(issues)==(2 if idx==46 else 1)
        rules.append(dict(id=row['id'],source_hex=row['source_hex'],target=row['english'],visible_lines=report['qa']['visible_lines'],approved_issue_signatures=[(i['code'],i['message']) for i in issues],line=line,after_word=after,before_word=before,reason=reason))
    suffix='''
# Two source/current/English/row-specific ordinary soft-wrap reviews.
ORDINARY_WRAP_REVIEWS=RULES_LITERAL
_encode_before_ordinary_review=encode_relocatable_dialogue
def encode_relocatable_dialogue(source_raw,target_markup,profile):
    for rule in ORDINARY_WRAP_REVIEWS:
        if target_markup==rule['target'] and source_raw.hex()!=rule['source_hex']:
            raise ValueError('Reviewed B206 ordinary boundary requires its exact complete source')
    return _encode_before_ordinary_review(source_raw,target_markup,profile)
_audit=_clone(qa.audit_relocatable_dialogue_record,{'encode_relocatable_dialogue':encode_relocatable_dialogue})
_audit_before_ordinary_review=audit_relocatable_dialogue_record
def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_audit_before_ordinary_review(source_raw,target_markup,profile)
    for rule in ORDINARY_WRAP_REVIEWS:
        if source_raw.hex()!=rule['source_hex'] or target_markup!=rule['target']:continue
        assert report['visible_lines']==rule['visible_lines']
        approved=[i for i in report['issues'] if (i['code'],i['message']) in rule['approved_issue_signatures']]
        assert len(approved)==len(rule['approved_issue_signatures'])
        report['issues']=[i for i in report['issues'] if i not in approved]
        report['reviewed_ordinary_boundaries']=[dict(line=rule['line'],after_word=rule['after_word'],before_word=rule['before_word'],exact_source_hex=rule['source_hex'],exact_target=rule['target'],reason=rule['reason'])]
    return report
'''.replace('RULES_LITERAL',repr(rules))
    source=Path('dk4tool/dialogue/lil_B206_layout_v1.py');text=source.read_text('utf-8')+suffix;compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    tool=derive('scripts/plan_lil_B206_layout_v6292.py','scripts/plan_lil_B206_layout_v6294.py',{'lil_B206_layout_v1':'lil_B206_layout_v2','lil_B206_layout_v6292':'lil_B206_layout_v6294'})
    ROOT.mkdir(parents=True);save(ROOT/'two_exact_source_paragraph_word_boundary_reviews.json',dict(rules=rules,previous_formatter=str(source),previous_formatter_sha256=sha(source.read_bytes()),formatter=str(TARGET),formatter_sha256=sha(TARGET.read_bytes()),original_formatter_is_exact_unchanged_prefix=True,planner_successor=tool,all24_English_words_and_compiled_rows_native_metrics_controls_guard_and_pair_phase_unchanged=True,no_global_phrase_or_weak_word_waiver=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Two exact-source ordinary word boundaries reviewed. All English words/compiled rows and global checks unchanged;new current native proofs still required.')
