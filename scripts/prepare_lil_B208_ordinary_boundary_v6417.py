"""Review one complete-clause temporal-adjunct soft boundary,without a blanket waiver."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_ordinary_boundary_tools_v6417')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B208_editorial_manuscript_v2.json');row=next(r for r in doc['records'] if r['source_record_index']==59);target=row['english'];labels=tuple(target.split('}',1)[1].split())
    reason='The full reported clause They say she lost it ends after its complete verb/object,and during the fighting is its intact temporal adjunct. A normal soft wrap after it keeps lost it together and avoids stranding the preposition during. This exact four-row layout preserves the battle,region,participation and hearsay with all words unchanged. The break adds no punctuation,dramatic pause,page or input hold. Only the exact clean source/prose it/during boundary is approved;no general pronoun,weak-ending,phrase,font,viewport,guard,pair-phase or pagination exemption is introduced.'
    rule=dict(id=row['id'],source_hex=row['source_hex'],target=target,labels=labels,after_word='it',before_word='during',reason=reason)
    helper='REVIEWED_WRAP_RULES='+repr([rule])+'''

def _reviewed_ordinary_at(labels,index):
    return any(tuple(labels)==r['labels'] and index+1<len(labels) and labels[index]==r['after_word'] and labels[index+1]==r['before_word'] for r in REVIEWED_WRAP_RULES)

'''
    tail='''
_encode_before_wrap_review=encode_relocatable_dialogue
def encode_relocatable_dialogue(source_raw,target_markup,profile):
    for rule in REVIEWED_WRAP_RULES:
        if target_markup==rule['target'] and source_raw.hex()!=rule['source_hex']:
            raise ValueError('Reviewed B208 it/during boundary requires its exact complete clean source')
    return _encode_before_wrap_review(source_raw,target_markup,profile)
_audit=_clone(qa.audit_relocatable_dialogue_record,{'encode_relocatable_dialogue':encode_relocatable_dialogue})
_audit_before_wrap_review=audit_relocatable_dialogue_record
def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_audit_before_wrap_review(source_raw,target_markup,profile)
    for rule in REVIEWED_WRAP_RULES:
        if source_raw.hex()!=rule['source_hex'] or target_markup!=rule['target']:continue
        assert report['visible_lines']==['She took part in a great','naval battle in the Caribbean.','They say she lost it','during the fighting.']
        approved=[i for i in report['issues'] if (i['code'],i['message'])==('weak-line-ending',"line 3 ends with weak wrap word 'it'")]
        assert len(approved)==1
        report['issues']=[i for i in report['issues'] if i not in approved]
        report['reviewed_ordinary_boundaries']=[dict(line=3,after_word='it',before_word='during',exact_source_hex=rule['source_hex'],exact_target=rule['target'],reason=rule['reason'])]
    return report
ORDINARY_WRAP_REVIEWS=REVIEWED_WRAP_RULES
'''
    sourcepath=Path('dk4tool/dialogue/lil_B208_layout_v4.py');source=sourcepath.read_text('utf-8');end=source[source.rindex('    return report'):]
    rows=[derive(str(sourcepath),'dk4tool/dialogue/lil_B208_layout_v5.py',{
        'def _word(value):':helper+'def _word(value):',
        'end_word in weak and not _noun_will_at':'end_word in weak and not _reviewed_ordinary_at(labels,end) and not _noun_will_at',
        "namespace={**layout.__dict__,":"namespace={**layout.__dict__,'_reviewed_ordinary_at':_reviewed_ordinary_at,",
        end:end+tail,
    })]
    rows.append(derive('scripts/plan_lil_B208_layout_v6415.py','scripts/plan_lil_B208_layout_v6419.py',{'lil_B208_layout_v4':'lil_B208_layout_v5','layout_v6415':'layout_v6419','editorial_manuscript_v4.json':'editorial_manuscript_v5.json',"r['reviewed_ordinary_boundaries']=[]":"r['reviewed_ordinary_boundaries']=qa.get('reviewed_ordinary_boundaries',[])"}))
    negative='''    for rule in ORDINARY_WRAP_REVIEWS:
        raw=bytes.fromhex(rule['source_hex']);bad=raw[:1]+bytes([raw[1]^1])+raw[2:]
        reject('ordinary-boundary-wrong-source',lambda bad=bad,r=rule:encode_relocatable_dialogue(bad,r['target'],prog))
        changed=audit_relocatable_dialogue_record(raw,rule['target']+' Huh?',prog)
        assert not changed.get('reviewed_ordinary_boundaries');negatives.append(dict(case='ordinary-boundary-changed-English-no-exemption',rejected=True,error='Changed prose receives no exact-source boundary approval'))
    assert len(negatives)==30'''
    rows.append(derive('scripts/verify_lil_B208_fonts_v6416.py','scripts/verify_lil_B208_fonts_v6420.py',{
        'lil_B208_layout_v4':'lil_B208_layout_v5','fonts_v6416':'fonts_v6420','editorial_manuscript_v4.json':'editorial_manuscript_v5.json',
        'import encode_relocatable_dialogue,audit_relocatable_dialogue_record':'import encode_relocatable_dialogue,audit_relocatable_dialogue_record,ORDINARY_WRAP_REVIEWS',
        "expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines":"expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines,reviewed_ordinary_boundaries=qa.get('reviewed_ordinary_boundaries',[])",
        '    assert len(negatives)==28':negative,'and28 source-consumer/formatter negatives':'and30 source-consumer/formatter negatives',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'one_exact_source_it_during_boundary_and_tools.json',dict(rule=rule,tools=rows,no_B207_it_if_or_blanket_boundary_rule_inherited=True,no_changed_words_font_metrics_native_guard_or_pagination=True,phase_reservation_proof_unchanged=True,full_goal_complete=False));print('One exact B208 it/during full-clause soft boundary reviewed;native planes/negative controls prepared,all words unchanged.')
