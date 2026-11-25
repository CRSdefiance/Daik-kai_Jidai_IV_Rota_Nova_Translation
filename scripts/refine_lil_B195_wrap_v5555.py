"""Permit one ordinary plenty/of wrap for exact source and prose;preserve all words and limits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B195_wrap_finding_v5555')
if __name__=='__main__':
    assert not ROOT.exists();docpath=Path('translations/lil_B195_editorial_manuscript_v2.json');doc=read(docpath)
    row=next(r for r in doc['records'] if r['source_record_index']==17)
    priorpath=Path('work/analysis/lil_B195_layout_v5552/all20_paragraph_layout_QA.json')
    old=next(r for r in read(priorpath)['records'] if r['id']==row['id'])
    assert old['qa']['visible_lines']==["Our specialty! It's made",'with plenty of cheese,','and it tastes great!']
    target,raw=row['english'],row['source_hex'];labels=tuple(target.split('}',1)[1].split())
    helper='REVIEWED_SOURCE_HEX='+repr(raw)+'\nREVIEWED_TARGET='+repr(target)+'\nREVIEWED_LABELS='+repr(labels)+'''\n
def _reviewed_pair_at(labels,index):
    # An ordinary complete-word soft wrap after plenty fills two safe rows.
    # This exact paragraph alone may split this collocation;all other uses stay protected.
    return (tuple(labels)==REVIEWED_LABELS and index+1<len(labels)
        and labels[index:index+2]==['plenty','of'])

'''
    reason=('For this exact paragraph,an ordinary complete-word soft wrap after plenty uses two substantial rows instead of three prematurely short rows. '
            'Plenty/of cheese remains readable as continuous prose. The Barkeep’s specialty,cheese abundance and taste claim retain every word and punctuation. '
            '216px width,6px glyphs,guarded pair phase,four-row ceiling,all first/internal/final glyphs,source controls and one-page checks remain unchanged. '
            'This is one reviewed ordinary collocation boundary,not a global phrase/weak-word waiver or authored break.')
    review='''    if source_raw.hex()==REVIEWED_SOURCE_HEX and target_markup==REVIEWED_TARGET:
        approved=[r for r in report['issues'] if r['code']=='split-protected-phrase'
            and r['message']=='line 1 splits the phrase plenty of']
        assert len(approved)==1 and report['visible_lines']==["Our specialty! It's made with plenty",'of cheese, and it tastes great!']
        report['issues']=[r for r in report['issues'] if r not in approved]
        report['reviewed_ordinary_boundaries']=[dict(line=1,after_word='plenty',before_word='of',
            exact_source_hex=REVIEWED_SOURCE_HEX,exact_target=REVIEWED_TARGET,reason=REVIEWED_REASON)]
'''
    helper+='REVIEWED_REASON='+repr(reason)+'\n\n'
    rows=[derive('dk4tool/dialogue/lil_B195_layout_v1.py','dk4tool/dialogue/lil_B195_layout_v2.py',{
        'def _word(value):':helper+'def _word(value):',
        "return index+1<len(labels) and (_word(labels[index]),_word(labels[index+1])) in PROTECTED_BOUNDARIES":
        "return index+1<len(labels) and not _reviewed_pair_at(labels,index) and (_word(labels[index]),_word(labels[index+1])) in PROTECTED_BOUNDARIES",
        '    return _encode(source_raw,target_markup,profile)':
        "    if tuple(target_markup.split('}',1)[1].split())==REVIEWED_LABELS and (target_markup!=REVIEWED_TARGET or source_raw.hex()!=REVIEWED_SOURCE_HEX):\n        raise ValueError('Reviewed B195 R17 ordinary boundary requires exact clean source and prose')\n    return _encode(source_raw,target_markup,profile)",
        '    return report':review+'    return report',
    })]
    rows.append(derive('scripts/plan_lil_B195_layout_v5552.py','scripts/plan_lil_B195_layout_v5555.py',{
        'lil_B195_layout_v1':'lil_B195_layout_v2','layout_v5552':'layout_v5555','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    rows.append(derive('scripts/verify_lil_B195_fonts_v5553.py','scripts/verify_lil_B195_fonts_v5556.py',{
        'lil_B195_layout_v1':'lil_B195_layout_v2','fonts_v5553':'fonts_v5556','editorial_manuscript_v2':'editorial_manuscript_v3',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'exact_R17_ordinary_two_row_wrap_finding.json',dict(
        manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),source_layout_proof=str(priorpath),source_layout_proof_sha256=sha(priorpath.read_bytes()),
        record_ID=row['id'],source_hex=raw,logical_prose=target,previous_visible_lines=old['qa']['visible_lines'],
        finding='Inherited protection of plenty/of made three short rows despite two full-width complete-word rows being safe.',
        expected_successor_visible_lines=["Our specialty! It's made with plenty",'of cheese, and it tastes great!'],reason=reason,
        all_words_and19_other_targets_must_remain_exact=True,source_and_prose_exact_guard_required=True,
        no_global_phrase_weak_word_font_width_guard_or_page_exemption=True,tools=rows,
        successor_native_checks_visual_comparison_and_approval_pending=True,new_editorial_credit=0,full_goal_complete=False))
