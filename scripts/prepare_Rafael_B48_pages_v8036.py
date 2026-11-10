"""Prepare complete native B48 glyph/page proofs with exact two unapproved QA warnings retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B48_page_tools_v8036')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_pages_v7933.py','scripts/prove_Rafael_B48_pages_v8036.py',{
        'Rafael_B46_pages_v7933':'Rafael_B48_pages_v8036',
        'Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json':
            'Rafael_B48_layout_v8035c/91_automatic_plans_full_native_width_source_preambles4_FE.json',
        'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json':
            'Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json',
        'rafael_B46_editorial_manuscript_v1.json':'rafael_B48_editorial_manuscript_v2.json',
        'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
        "assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])":
            """warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert not any(i['severity']=='error' for r in plan['records'] for i in r['base_QA']['issues'])
    assert warnings==[
        dict(id='DK4_MES_B48_R0086',issue=dict(code='weak-line-ending',message="line 1 ends with weak wrap word 'the'",severity='warning')),
        dict(id='DK4_MES_B48_R0406',issue=dict(code='weak-line-ending',message="line 2 ends with weak wrap word 'of'",severity='warning')),
    ]""",
        """assert ' '.join(expected.decode('ascii').split())==row['english'].replace('FI','Rafael').replace('FA','Castor').replace('FO','Castor Co.')""":
            """assert ' '.join(expected.decode('cp932').split())==row['english'].replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')""",
        'len(rows)==24 and not ctx.machines and sum(len(r[\'pages\']) for r in rows)==24':
            'len(rows)==91 and not ctx.machines and sum(len(r[\'pages\']) for r in rows)==92',
        'Rafael_B46_native_pages_sheet':'Rafael_B48_native_pages_sheet',
        '24_complete_native_pages96_compiled_alignments12_FE.json':'91_complete_native_paragraphs92_pages364_compiled_alignments4_FE.json',
        'fresh_compiled_alignment_cases=96,progressive_alignment_cases=48,FE_null_actor_alignment_cases=48':
            'fresh_compiled_alignment_cases=364,progressive_alignment_cases=348,FE_null_actor_alignment_cases=16',
        'complete_progressive_pages=12,complete_FE_logical_andphysical_pages=12':
            'complete_progressive_paragraphs=87,complete_progressive_pages=88,complete_FE_logical_andphysical_pages=4',
        'all26_formatting_gates_false=True':
            'all91_formatting_gates_false=True,unapproved_exact_ordinary_boundary_warnings=warnings,all_original_QA_issues_preserved=True',
        '24 complete native pages/96 fresh compiled alignments pass. Four sheets need viewing;choice fonts,actual scenes,relocation andregistered release pending.':
            '91complete native paragraphs/92pages/364fresh compiled alignments pass. Sixteen sheets need viewing;names,actual scenes,relocation andrelease pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B48 native92-page proof;preserve both exact warnings anddistinct four FE consumers.')
