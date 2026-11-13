"""Verify the exact ordinary-wrap review cannot transfer or alter any prose byte."""
import itertools
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B196_profile_v2 import profile_for
from dk4tool.dialogue import lil_B196_layout_v3 as codec
from dk4tool.dialogue.layout import lint_dialogue
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_R74_wrap_v5611')
DOC=Path('translations/lil_B196_editorial_manuscript_v2.json')
STOPPED=Path('work/analysis/lil_B196_layout_v5607b/all24_paragraph_layout_QA.json')
FONT=Path('work/analysis/lil_B196_fonts_v5609b/all24_progressive_FE_native_planes_and192_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,stopped,font=map(read,[DOC,STOPPED,FONT])
    image=NdsImage.open(doc['current_ROM']);p=profile_for(image.read_file('/__arm9__.bin'),IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[196])
    row=next(r for r in doc['records'] if r['source_record_index']==74);raw=bytes.fromhex(row['source_hex'])
    body=row['english'].split('}',1)[1];words=body.split();assert len(body)==129 and len(words)==23
    report=codec.audit_relocatable_dialogue_record(raw,row['english'],p);lines=report['visible_lines']
    assert [(r['line'],r['after_word']) for r in report['reviewed_ordinary_boundaries']]==[(1,'the'),(2,'must'),(3,'can')]
    partitions=[]
    for a,b,c in itertools.combinations(range(1,len(words)),3):
        spans=[(0,a),(a,b),(b,c),(c,len(words))];candidate=[' '.join(words[i:j]) for i,j in spans]
        if any(len(s)>36 for s in candidate):continue
        issues=lint_dialogue(raw,'{SPEAKER:13}'+'{LB}'.join(candidate),p)
        if any(i.severity=='error' for i in issues):continue
        weak=[codec._word(s.split()[-1]) for s in candidate[:-1] if codec._word(s.split()[-1]) in codec.STRONG_ENDINGS and not codec._terminal_label(s.split()[-1])]
        pairs=[(codec._word(words[k-1]),codec._word(words[k])) for k in [a,b,c] if (codec._word(words[k-1]),codec._word(words[k])) in codec.PROTECTED_BOUNDARIES]
        partitions.append(dict(rows=candidate,weak_words=weak,split_protected_pairs=pairs,heuristic_count=len(weak)+len(pairs),native_lint_has_no_errors=True))
    assert len(partitions)==4 and min(c['heuristic_count'] for c in partitions)==3
    cuts=[];cursor=0
    for line in lines[:-1]:cursor+=len(line.split());cuts.append(cursor)
    next_word=[]
    for index in range(3):
        moved=cuts.copy();moved[index]+=1;stops=[0,*moved,len(words)]
        candidate=[' '.join(words[a:b]) for a,b in zip(stops,stops[1:])]
        assert ' '.join(candidate)==body
        errors=[dict(code=i.code,message=i.message) for i in lint_dialogue(raw,'{SPEAKER:13}'+'{LB}'.join(candidate),p) if i.severity=='error']
        assert errors;next_word.append(dict(line=index+1,attempted_rows=candidate,native_errors=errors))
    changes=[('changed-source-body',raw[:-1]+bytes([raw[-1]^1]),row['english']),
        ('changed-source-and-target-actor',b'\x14'+raw[1:],row['english'].replace('{SPEAKER:13}','{SPEAKER:14}')),
        ('changed-attempt-count',raw,row['english'].replace('first try','second try')),
        ('changed-at-least-quantity',raw,row['english'].replace('at least','exactly')),
        ('changed-source-title',raw,row['english'].replace('Admiral','Captain')),
        ('added-prose',raw,row['english']+' Really.')]
    negatives=[]
    for label,source,target in changes:
        try:result=codec.audit_relocatable_dialogue_record(source,target,p)
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,review_not_transferred=True,error=str(e)))
        else:assert not result.get('reviewed_ordinary_boundaries');negatives.append(dict(case=label,review_not_transferred=True))
    old={r['id']:r for r in stopped['records']};native={r['id']:r for r in font['cases']}
    for r in doc['records']:
        assert r['compiled_hex']==old[r['id']]['encoded_hex']==native[r['id']]['encoded_hex']
        assert native[r['id']]['all_first_final_internal_glyphs_in_order_and_unique_cells'] and native[r['id']]['one_native_page_consumes_complete_target']
    reason=report['reviewed_ordinary_boundaries'][0]['reason']
    ROOT.mkdir(parents=True);save(ROOT/'exact_R74_three_ordinary_boundaries_four_native_partitions_and_six_nontransfer_cases.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),record_ID=row['id'],exact_source_hex=row['source_hex'],exact_target=row['english'],
        paragraph_ASCII_characters=129,paragraph_words=23,retained_visible_rows=lines,retained_compiled_hex=row['compiled_hex'],
        native_valid_complete_word_four_row_partitions=partitions,next_complete_word_cannot_fit_each_reviewed_row=next_word,
        all_native_valid_four_row_partitions_have_at_least_three_weak_or_split_phrase_heuristics=True,
        exact_source_prose_boundaries=report['reviewed_ordinary_boundaries'],six_source_or_prose_changes_do_not_inherit_review=negatives,
        all24_words_source_controls_compiled_bytes_and_native_planes_unchanged=True,
        no_authored_break_global_weak_waiver_shortening_metric_width_guard_phase_or_pagination_change=True,
        individual_layout_retention_reason=reason,not_actual_B196_gameplay=True,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,STOPPED,FONT,Path('dk4tool/dialogue/lil_B196_layout_v2.py'),
            Path('dk4tool/dialogue/lil_B196_layout_v3.py'),Path('dk4tool/dialogue/lil_B196_profile_v2.py'),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('R74:all129 characters/23 words retained;three exact ordinary wraps;four valid native partitions;next word cannot fit each row;six review-transfer negatives;all24 encoded/native planes unchanged.')
