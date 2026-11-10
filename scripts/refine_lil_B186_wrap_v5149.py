"""Review the visually premature R13 wrap using its exact source and full prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B186_wrap_finding_v5149')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B186_editorial_manuscript_v2.json')
    row=next(r for r in doc['records'] if r['source_record_index']==13)
    prior=read('work/analysis/lil_B186_layout_v5147/all12_paragraph_layout_QA.json')
    old=next(r for r in prior['records'] if r['id']==row['id'])
    assert old['qa']['visible_lines']==['Yes! The customers',"won't be satisfied",'with a flavor this light.','It has to be sweeet! Sweet!']
    target=row['english'];raw=row['source_hex'];labels=tuple(target.split('}',1)[1].split())
    helper='REVIEWED_SOURCE_HEX='+repr(raw)+'\nREVIEWED_TARGET='+repr(target)+'\nREVIEWED_LABELS='+repr(labels)+'''\n
def _reviewed_ordinary_boundary_at(labels,index):
    # An ordinary complete-word soft wrap within this exact long sentence
    # allows its judgment in two rows and the repeated sweet emphasis in one.
    return (tuple(labels)==REVIEWED_LABELS and index+1<len(labels)
        and labels[index:index+2]==['be','satisfied'])

'''
    review='''    if source_raw.hex()==REVIEWED_SOURCE_HEX and target_markup==REVIEWED_TARGET:
        approved=[r for r in report['issues'] if r['code']=='weak-line-ending' and r['message']=="line 1 ends with weak wrap word 'be'"]
        if approved:
            assert len(approved)==1 and report['visible_lines'][0].split()[-1]=='be'
            report['issues']=[r for r in report['issues'] if r not in approved]
            report['reviewed_ordinary_boundaries']=[dict(line=1,after_word='be',
                exact_source_hex=REVIEWED_SOURCE_HEX,exact_target=REVIEWED_TARGET,
                reason='In this exact complete paragraph,an ordinary complete-word soft wrap within the long judgment avoids a premature fourth row and leaves the repeated sweet emphasis intact. No global weak-ending,glyph,bounds,page or control exemption.')]
'''
    tools=[derive('dk4tool/dialogue/lil_B186_layout_v2.py','dk4tool/dialogue/lil_B186_layout_v3.py',{
        'source=inspect.getsource(layout._balanced_wrap)':helper+'source=inspect.getsource(layout._balanced_wrap)',
        'end_word in weak and not _noun_will_at(labels,end)':'end_word in weak and not _reviewed_ordinary_boundary_at(labels,end) and not _noun_will_at(labels,end)',
        "'_complete_locative_at':_complete_locative_at}":"'_complete_locative_at':_complete_locative_at,'_reviewed_ordinary_boundary_at':_reviewed_ordinary_boundary_at}",
        '    return _encode(source_raw,target_markup,profile)':"    if target_markup==REVIEWED_TARGET and source_raw.hex()!=REVIEWED_SOURCE_HEX:\n        raise ValueError('Reviewed ordinary boundary requires exact clean B186 R13 source')\n    return _encode(source_raw,target_markup,profile)",
        '    return report':review+'    return report',
    })]
    tools.append(derive('scripts/plan_lil_B186_layout_v5147.py','scripts/plan_lil_B186_layout_v5150.py',{
        'lil_B186_layout_v2':'lil_B186_layout_v3','layout_v5147':'layout_v5150','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    tools.append(derive('scripts/verify_lil_B186_fonts_v5148.py','scripts/verify_lil_B186_fonts_v5151.py',{
        'lil_B186_layout_v2':'lil_B186_layout_v3','fonts_v5148':'fonts_v5151','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'exact_R13_visual_finding_and_boundary_review.json',dict(
        manuscript='translations/lil_B186_editorial_manuscript_v2.json',manuscript_sha256=sha(Path('translations/lil_B186_editorial_manuscript_v2.json').read_bytes()),
        record_ID=row['id'],source_hex=raw,logical_prose=target,previous_visible_lines=old['qa']['visible_lines'],
        initial_native_checks_passed_but_visual_editorial_wrap_rejected=True,
        finding='The strong weak-be penalty spread one judgment over three short rows,then used a fourth for sweet emphasis. Its full unchanged judgment can occupy two safe rows with an ordinary soft wrap after be.',
        exact_source_and_prose_required_for_boundary_review=True,no_prose_shortening_or_authored_break=True,
        no_global_weak_word_phrase_metric_font_guard_or_pagination_change=True,tools=tools,
        native_successor_and_visual_review_pending=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Prepared exact R13 ordinary-boundary successor; all words,controls and display limits preserved.')
