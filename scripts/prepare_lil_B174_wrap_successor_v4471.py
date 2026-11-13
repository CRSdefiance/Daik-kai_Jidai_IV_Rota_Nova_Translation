"""Preserve all initial native evidence; strengthen one scoped auxiliary boundary."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_wrap_successor_tools_v4471')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B174_layout_v1.py','dk4tool/dialogue/lil_B174_layout_v2.py',{
        "BASE_WEAK=frozenset(":"STRONG_ENDINGS = STRONG_ENDINGS | frozenset({\"she's\"})\n\nBASE_WEAK=frozenset(",
    }),derive('scripts/plan_lil_B174_layout_v4469.py','scripts/plan_lil_B174_layout_v4472.py',{
        'lil_B174_layout_v1':'lil_B174_layout_v2','lil_B174_layout_v4469':'lil_B174_layout_v4472',
        'lil_B174_editorial_manuscript_v2':'lil_B174_editorial_manuscript_v3',
        'lil_B174_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v4',
    }),derive('scripts/verify_lil_B174_fonts_v4470.py','scripts/verify_lil_B174_fonts_v4473.py',{
        'lil_B174_layout_v1':'lil_B174_layout_v2','lil_B174_fonts_v4470':'lil_B174_fonts_v4473',
        'lil_B174_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v4',
        "cases=[];qa_reports=[];pictures=[];macro_calls=0":
            """cases=[];qa_reports=[];pictures=[];macro_calls=0;new_macro_calls=0;reused=[]
    prior_path=Path('work/analysis/lil_B174_fonts_v4470/current_macro_QA_and_progressive_font_proof.json')
    prior=read(prior_path);old_doc=read(prior['manuscript'])
    assert sha(Path(prior['manuscript']).read_bytes())==prior['manuscript_sha256']
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    old_by={r['id']:r for r in prior['cases']};old_prose={r['id']:r['english'] for r in old_doc['records']}
    assert all(old_prose[r['id']]==r['english'] for r in doc['records'])""",
        "logical=row['english'].split('}',1)[1]":
            """old=old_by[row['id']]
        if old['encoded_hex']==result.encoded.hex():
            assert old['expanded_hex']==result.encoded[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.').hex()
            assert sha(Path(old['preview']).read_bytes())==old['preview_sha256']
            assert old['complete_native_independent216x64_plane_equal'] and old['all_first_final_internal_glyphs_in_order_and_unique_cells'] and old['all_visible_origins_zero_and16px_rows_within4rows']
            case={**old,'exact_reused_native_proof':str(prior_path),'exact_reused_native_proof_sha256':sha(prior_path.read_bytes()),'new_alignment_calls':0,'reused_alignment_calls':8}
            cases.append(case);reused.append(row['id']);macro_calls+=8
            with Image.open(old['preview']) as picture: pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],picture.copy()))
            continue
        logical=row['english'].split('}',1)[1]""",
        "macro_calls+=4;ctx.machines.pop()":"macro_calls+=4;new_macro_calls+=4;ctx.machines.pop()",
        "assert len(cases)==33 and len(qa_reports)==33 and macro_calls==264 and not ctx.machines":
            "assert len(cases)==33 and len(qa_reports)==33 and macro_calls==264 and new_macro_calls==8 and len(reused)==32 and not ctx.machines",
        'current_original_macro_alignment_calls=264,all_executed_macro_instructions_current_ROM_exact=True':
            'current_original_macro_alignment_calls=264,new_current_original_macro_alignment_calls=new_macro_calls,reused_original_macro_alignment_calls=256,exact_reused_IDs=reused,reused_native_proof=str(prior_path),reused_native_proof_sha256=sha(prior_path.read_bytes()),all_executed_macro_instructions_current_ROM_exact=True',
        '33 complete progressive planes,264 original processor/alignment cases,33 QA plans and17 source-consumer negatives pass;five sheets need visual review.':
            '33 complete progressive planes,8 fresh/256 exact-reused original alignment cases,33 QA plans and17 source-consumer negatives pass;changed sheet needs fresh visual review.',
    })]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,all5_initial_native_sheets_viewed=True,
        visual_finding=dict(id='DK4_MES_B174_R0124',old_row='to be jealous! She\'s',
            action='Treat contraction as a weak auxiliary row ending in B174-only successor; preserve every word.'),
        prose_change=False,no_shared_metric_geometry_guard_or_profile_change=True,
        prior264_cases_preserved=True,new_native_expected=8,exact_reuse_expected=256,
        full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Prepared stronger B174-only auxiliary rule, fresh layout and one-plane native successor with exact reuse.')
