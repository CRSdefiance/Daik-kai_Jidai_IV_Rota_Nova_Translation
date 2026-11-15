"""Preserve failed probes and prepare scoped complete-prose pagination successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_scoped_successors_v6983')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[
        ('scripts/prove_lil_B221_choices_v6977.py','scripts/prove_lil_B221_choices_v6977b.py',{
            "                    planes.append(dict(**proof,index=index,style=style,whole_native_plane_sha256=sha(pixels)))":
            "                    assert proof['style']==style\n                    planes.append(dict(**proof,index=index,whole_native_plane_sha256=sha(pixels)))"}),
        ('scripts/plan_lil_B221_layout_v6976.py','scripts/plan_lil_B221_layout_v6976b.py',{
            'layout_v6976':'layout_v6976b',
            "words=body.split();assert ' '.join(words)==body":
            "words=body.split();assert ' '.join(words)==body;maximum=8 if row['id'] in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060'] else 4",
            'if line==4:return None':'if line==maximum:return None',
            "            if not final and words[stop-1]=='I':continue":
            "            if not final and words[stop-1]=='I':continue\n            if line==3 and not final and row['id'] in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060'] and words[stop-1]!=('slaughter...' if row['id'].endswith('0046') else 'terms.'):continue",
            'max_lines=4,leading_speaker_bytes':'max_lines=maximum,leading_speaker_bytes',
            'max_total_rows=4,native_rows_per_page=4,expected_native_pages=1':
            'max_total_rows=maximum,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4',
            'no_inherited_letter_style_or_multipage_exception=True':
            "no_inherited_letter_style_or_multipage_exception=True,scoped_two_page_records=['DK4_MES_B221_R0046','DK4_MES_B221_R0060'],page_boundary_reasons={'DK4_MES_B221_R0046':'The reported wealth question and plunder/slaughter examples remain together on the first page. The second page keeps the complete anything-went report and its hearsay tag together, rather than stranding so I hear alone. No word is cut or added.','DK4_MES_B221_R0060':'The first page completes all three examples of humane conduct, including peace terms. The second page contains the entire following praise without splitting dirty tricks across a page. No word, viewport or native row limit changes.'}"}),
        ('scripts/verify_lil_B221_native_pages_v6980.py','scripts/verify_lil_B221_native_pages_v6980b.py',{
            'layout_v6976/':'layout_v6976b/','native_pages_v6980':'native_pages_v6980b',
            "assert len(rendered['pages'])==record['expected_native_pages']==1":
            "assert len(rendered['pages'])==record['expected_native_pages']==(2 if record['id'] in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060'] else 1)",
            "assert page['first_visible_origin']==[0,0]":
            "assert page['first_visible_origin']==([0,0] if page['page']==1 else [6,0])",
            'len(cases)==len(pictures)==14 and alignments==112':
            'len(cases)==14 and len(pictures)==16 and alignments==112',
            'all14_paragraphs14_complete_native_pages112_alignments':'all14_paragraphs16_complete_native_pages112_alignments',
            'complete_native_pages=14':'complete_native_pages=16',
            'all14_single_pages=True':'twelve_single_two_two_page_paragraphs=True',
            '14 complete single native pages/112 alignments':
            '14 paragraphs/16 complete native pages/112 alignments',
            'native_name_planes_actual_headers_controls_reference_and_release_pending=True':
            'native_name_planes_actual_headers_controls_reference_and_release_pending=True,actual_two_page_button_progression_required_for_R46_R60=True'}),
    ]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    ROOT.mkdir(parents=True)
    save(ROOT/'preserved_initial_failure_and_exact_native_successors.json',dict(derivations=rows,
        preserved_failed_single_page_plan='work/analysis/lil_B221_layout_v6976/fourteen_whole_paragraph_plans_no_macros_no_prose_changes.json',
        preserved_initial_choice_probe='scripts/prove_lil_B221_choices_v6977.py',
        choice_failure_duplicate_style_keyword_was_reporting_only_not_native_pixel_or_bounds_failure=True,
        complete_prose_and_original_four_rows_per_216x64_native_page_unchanged=True,
        no_manual_paragraph_break_padding_or_alignment_in_editable_prose=True,
        scoped_pagination_not_global_profile_or_source_instruction_change=True,
        full_goal_complete=False))
    print('Three source-locked successors prepared; original failures/producers preserved.')
