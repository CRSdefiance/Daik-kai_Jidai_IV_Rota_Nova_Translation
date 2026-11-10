"""Refine three premature wraps seen in full planes;retain two reviewed ordinary boundaries and every word."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_viewed_wraps_v6296');TARGET=Path('dk4tool/dialogue/lil_B206_layout_v3.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists();doc=read('translations/lil_B206_editorial_manuscript_v3.json');prior=read('work/analysis/lil_B206_wrap_review_v6293/two_exact_source_paragraph_word_boundary_reviews.json');rules=[]
    new={24:('that','unusual',"Cristina's skeptical appearance comment is one continuous English sentence. An ordinary complete-word boundary between that and unusual permits two substantial rows instead of ending the first row prematurely after look. Her subjective doubt and every word remain intact. The qualifying that is followed immediately by unusual within the same paragraph,without punctuation,page or added input hold. This exact source/prose boundary is reviewed;no global weak-ending exception or font,width,guard or phrase rewrite is introduced."),53:('pick','up',"The seller explains friendship as a route to information and claims women at the tavern know plenty. An ordinary complete-word pick/up boundary lets the full paragraph occupy three substantial rows instead of four rows with prematurely short introductory fragments. The phrasal verb remains contiguous prose across a soft wrap;no dramatic pause,punctuation or page is added. All words,claims and the final tavern-information point remain exact. This exact boundary alone is reviewed;all complete-glyph,control,bounds,pagination and source checks remain."),90:('your','ceramic',"The existing Good eye flattery and full ceramic-earring handover are already natural. An ordinary complete-word wrap after your keeps ceramic earrings together and produces two substantial rows rather than prematurely ending the first after Here. The possessive connects directly to the intact object name in the same uninterrupted paragraph. Retain every word and the source material;do not shorten or pad a good line. This exact source/prose boundary does not exempt other pronouns,phrases or native display checks.")}
    for idx in [24,46,53,90,117]:
        row=next(r for r in doc['records'] if r['kind']=='progressive' and r['source_record_index']==idx)
        if idx in new:after,before,reason=new[idx]
        else:
            old=next(r for r in prior['rules'] if r['id']==row['id']);after,before,reason=old['after_word'],old['before_word'],old['reason']
        rules.append(dict(id=row['id'],source_hex=row['source_hex'],target=row['english'],labels=tuple(row['english'].split('}',1)[1].split()),after_word=after,before_word=before,reason=reason))
    helper='''REVIEWED_WRAP_RULES=RULES_LITERAL
def _reviewed_ordinary_at(labels,index):
    return any(tuple(labels)==r['labels'] and list(labels[index:index+2])==[r['after_word'],r['before_word']] for r in REVIEWED_WRAP_RULES)

'''.replace('RULES_LITERAL',repr(rules))
    source=Path('dk4tool/dialogue/lil_B206_layout_v1.py');text=checked_text(source.read_text('utf-8'),{
      'def _word(value):':helper+'def _word(value):',
      "return index+1<len(labels) and (_word(labels[index]),_word(labels[index+1])) in PROTECTED_BOUNDARIES":"return index+1<len(labels) and not _reviewed_ordinary_at(labels,index) and (_word(labels[index]),_word(labels[index+1])) in PROTECTED_BOUNDARIES",
      'end_word in weak and not _noun_will_at(labels,end)':'end_word in weak and not _reviewed_ordinary_at(labels,end) and not _noun_will_at(labels,end)',
      "'_noun_will_at':_noun_will_at,":"'_reviewed_ordinary_at':_reviewed_ordinary_at,'_noun_will_at':_noun_will_at,",
    })
    suffix='''
_encode_before_wrap_review=encode_relocatable_dialogue
def encode_relocatable_dialogue(source_raw,target_markup,profile):
    for rule in REVIEWED_WRAP_RULES:
        if target_markup==rule['target'] and source_raw.hex()!=rule['source_hex']:
            raise ValueError('Reviewed B206 boundary requires its exact clean source')
    return _encode_before_wrap_review(source_raw,target_markup,profile)
_audit=_clone(qa.audit_relocatable_dialogue_record,{'encode_relocatable_dialogue':encode_relocatable_dialogue})
_audit_before_wrap_review=audit_relocatable_dialogue_record
def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_audit_before_wrap_review(source_raw,target_markup,profile)
    for rule in REVIEWED_WRAP_RULES:
        if source_raw.hex()!=rule['source_hex'] or target_markup!=rule['target']:continue
        lines=report['visible_lines'];locations=[i for i in range(len(lines)-1) if lines[i].split()[-1:]==[rule['after_word']] and lines[i+1].split()[:1]==[rule['before_word']]]
        assert len(locations)==1
        line=locations[0]+1;allowed=[('weak-line-ending',f"line {line} ends with weak wrap word {rule['after_word']!r}"),('split-protected-phrase',f"line {line} splits the phrase {rule['after_word']} {rule['before_word']}")]
        accepted=[i for i in report['issues'] if (i['code'],i['message']) in allowed]
        assert len(accepted)==(2 if rule['id'].endswith('R0046') else 1)
        report['issues']=[i for i in report['issues'] if i not in accepted]
        report['reviewed_ordinary_boundaries']=[dict(line=line,after_word=rule['after_word'],before_word=rule['before_word'],exact_source_hex=rule['source_hex'],exact_target=rule['target'],reason=rule['reason'])]
    return report
ORDINARY_WRAP_REVIEWS=REVIEWED_WRAP_RULES
'''
    text+=suffix;compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    tool=derive('scripts/plan_lil_B206_layout_v6292.py','scripts/plan_lil_B206_layout_v6297.py',{'lil_B206_layout_v1':'lil_B206_layout_v3','lil_B206_layout_v6292':'lil_B206_layout_v6297',"OUTPUT=Path('translations/lil_B206_editorial_manuscript_v4.json')":"OUTPUT=Path('translations/lil_B206_editorial_manuscript_v5.json')"})
    ROOT.mkdir(parents=True);save(ROOT/'five_exact_source_word_boundaries_three_visual_layout_improvements.json',dict(rules=rules,formatter=str(TARGET),formatter_sha256=sha(TARGET.read_bytes()),source_formatter=str(source),source_formatter_sha256=sha(source.read_bytes()),planner_successor=tool,three_visual_wrap_improvement_indices=[24,53,90],two_previous_ordinary_boundary_reviews_retained=[46,117],all28_English_words_source_current_references_decisions_and_controls_unchanged=True,no_global_lint_profile_font_width_guard_or_pair_phase_change=True,new_native_planes_for_changed_compiled_inputs_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Three viewed premature wraps refined;two exact prior word-boundary reviews retained. No prose or native metric changes;new layout/native reconciliation pending.')
