"""Keep native reserves: three flowing rows require two exact ordinary boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B186_wrap_reserve_finding_v5152')
if __name__=='__main__':
    assert not ROOT.exists()
    initial=read('work/analysis/lil_B186_layout_v5147/all12_paragraph_layout_QA.json')
    attempted=read('work/analysis/lil_B186_layout_v5150/all12_paragraph_layout_QA.json')
    assert [r['encoded_hex'] for r in initial['records']]==[r['encoded_hex'] for r in attempted['records']]
    assert len('satisfied with a flavor this light.')==35
    assert 35*6+6+6>216
    reason='In this exact complete paragraph,two ordinary complete-word soft wraps use three flowing rows and leave the repeated sweet emphasis intact. All216px width,guard,pair-phase,glyph,page and control checks remain. No global weak-ending exemption.'
    rows=[derive('dk4tool/dialogue/lil_B186_layout_v3.py','dk4tool/dialogue/lil_B186_layout_v4.py',{
        "labels[index:index+2]==['be','satisfied']":"labels[index:index+2] in (['be','satisfied'],['this','light.'])",
        """        approved=[r for r in report['issues'] if r['code']=='weak-line-ending' and r['message']=="line 1 ends with weak wrap word 'be'"]""":
        """        approved=[r for r in report['issues'] if r['code']=='weak-line-ending' and r['message'] in ["line 1 ends with weak wrap word 'be'","line 2 ends with weak wrap word 'this'"]]""",
        "assert len(approved)==1 and report['visible_lines'][0].split()[-1]=='be'":"assert len(approved)==2 and [report['visible_lines'][i].split()[-1] for i in [0,1]]==['be','this']",
        "dict(line=1,after_word='be',":"dict(line=line,after_word=word,",
        "reason='In this exact complete paragraph,an ordinary complete-word soft wrap within the long judgment avoids a premature fourth row and leaves the repeated sweet emphasis intact. No global weak-ending,glyph,bounds,page or control exemption.')]":
        "reason="+repr(reason)+") for line,word in [(1,'be'),(2,'this')]]",
        'allows its judgment in two rows and the repeated sweet emphasis in one.':'allows three flowing rows with the repeated sweet emphasis intact.',
    })]
    rows.append(derive('scripts/plan_lil_B186_layout_v5150.py','scripts/plan_lil_B186_layout_v5153.py',{
        'lil_B186_layout_v3':'lil_B186_layout_v4','layout_v5150':'layout_v5153','editorial_manuscript_v3':'editorial_manuscript_v4',
    }))
    rows.append(derive('scripts/verify_lil_B186_fonts_v5151.py','scripts/verify_lil_B186_fonts_v5154.py',{
        'lil_B186_layout_v3':'lil_B186_layout_v4','fonts_v5151':'fonts_v5154','editorial_manuscript_v3':'editorial_manuscript_v4',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'corrected_native_reserve_and_two_ordinary_boundaries.json',dict(
        prior_one_boundary_attempt_did_not_change_any_compiled_target=True,
        prior_finding_two_rows_for_judgment_corrected='The proposed second row has35 characters:210px plus6px guard and6px phase reserve is222px,over216px. A safe three-row paragraph crosses the sentence at light.;do not relax reserves or shorten the prose.',
        exact_source_R13_and_full_prose_only=True,ordinary_boundary_after_words=['be','this'],reason=reason,tools=rows,
        all_other_native_checks_required=True,all_stopped_and_executed_producers_preserved=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared exact R13 two-boundary successor;the failed one-boundary proposal and all native reserves remain preserved.')
