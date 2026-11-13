"""Keep the complete R64 question together using an exact source/prose boundary."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_wrap_finding_v5372')
if __name__=='__main__':
    assert not ROOT.exists();docpath=Path('translations/lil_B191_editorial_manuscript_v2.json');doc=read(docpath)
    row=next(r for r in doc['records'] if r['source_record_index']==64)
    old=next(r for r in read('work/analysis/lil_B191_layout_v5369/all13_paragraph_layout_QA.json')['records'] if r['id']==row['id'])
    assert old['qa']['visible_lines']==['What are you waiting',"for? It'll be too late","once it's sold out."]
    target,raw=row['english'],row['source_hex'];labels=tuple(target.split('}',1)[1].split())
    helper='REVIEWED_SOURCE_HEX='+repr(raw)+'\nREVIEWED_TARGET='+repr(target)+'\nREVIEWED_LABELS='+repr(labels)+'''\n
def _reviewed_ordinary_boundary_at(labels,index):
    # This exact complete interrogative ends with for?;it does not strand a
    # preposition awaiting a continuation. No other use of for is exempted.
    return (tuple(labels)==REVIEWED_LABELS and index+1<len(labels)
        and labels[index:index+2]==['for?',"It'll"])

'''
    review='''    if source_raw.hex()==REVIEWED_SOURCE_HEX and target_markup==REVIEWED_TARGET:
        approved=[r for r in report['issues'] if r['code']=='weak-line-ending' and r['message']=="line 1 ends with weak wrap word 'for?'"]
        if approved:
            assert len(approved)==1 and report['visible_lines']==['What are you waiting for?',"It'll be too late once it's sold out."]
            report['issues']=[r for r in report['issues'] if r not in approved]
            report['reviewed_ordinary_boundaries']=[dict(line=1,after_word='for?',exact_source_hex=REVIEWED_SOURCE_HEX,exact_target=REVIEWED_TARGET,
                reason='For? completes this exact full question. Its ordinary sentence-boundary soft wrap keeps both the question and following warning intact in two safe rows. All words,216px width,glyphs,guards,pair phase,bounds,controls and one-page checks remain. No global preposition waiver or authored break.')]
'''
    rows=[derive('dk4tool/dialogue/lil_B191_layout_v1.py','dk4tool/dialogue/lil_B191_layout_v2.py',{
        'source=inspect.getsource(layout._balanced_wrap)':helper+'source=inspect.getsource(layout._balanced_wrap)',
        'end_word in weak and not _noun_will_at(labels,end)':'end_word in weak and not _reviewed_ordinary_boundary_at(labels,end) and not _noun_will_at(labels,end)',
        "'_complete_locative_at':_complete_locative_at}":"'_complete_locative_at':_complete_locative_at,'_reviewed_ordinary_boundary_at':_reviewed_ordinary_boundary_at}",
        '    return _encode(source_raw,target_markup,profile)':"    if target_markup==REVIEWED_TARGET and source_raw.hex()!=REVIEWED_SOURCE_HEX:\n        raise ValueError('Reviewed question boundary requires exact clean B191 R64 source')\n    return _encode(source_raw,target_markup,profile)",
        '    return report':review+'    return report',
    })]
    rows.append(derive('scripts/plan_lil_B191_layout_v5369.py','scripts/plan_lil_B191_layout_v5373.py',{
        'lil_B191_layout_v1':'lil_B191_layout_v2','layout_v5369':'layout_v5373','editorial_manuscript_v1':'editorial_manuscript_v2','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    rows.append(derive('scripts/verify_lil_B191_fonts_v5370.py','scripts/verify_lil_B191_fonts_v5374.py',{
        'lil_B191_layout_v1':'lil_B191_layout_v2','fonts_v5370':'fonts_v5374','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'exact_R64_complete_question_wrap_finding.json',dict(manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),
        record_ID=row['id'],source_hex=raw,logical_prose=target,previous_visible_lines=old['qa']['visible_lines'],
        finding='The generic weak-for penalty split a complete question and forced three rows despite two safe sentence rows.',
        complete_question_boundary_after_for_question_mark=True,exact_source_and_prose_required=True,
        all_words_and_other_record_targets_must_remain_unchanged=True,no_manual_break_or_global_weak_word_font_width_guard_exemption=True,
        tools=rows,native_successor_and_visual_review_pending=True,new_credit=0,full_goal_complete=False))
