"""Prepare approval after all four complete B172 native sheets were viewed."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_approval_tools_v4378')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/approve_lil_B171_native_v4328.py').read_text(encoding='utf-8')
    old_review=next(line for line in old.splitlines() if "'review': 'Viewed complete native sheet:" in line)
    new_review="                       'review': 'Viewed complete native sheet: all leading/internal/trailing glyphs present, zero row origins and complete four-row planes. Julian florid hyperbole and anxious price concern,Mihwa qualified date reply,his overeager promise reading,Lil dry aside then curiosity and independent search,and the final offer/request reversal read coherently. Silla Gold Crown and Seoul use exact current bindings;ordinary complete-word wraps retain every word. No item-title split or added relationship. Offline native rendering only.'})"
    a=old.index('    macro_negatives = []');b=old.index('    names_path = ',a)
    new_macro='''    macro_negatives = []
    absence_negatives = []
    for name in ['FI','FA','FO']:
        selected = doc['records'][0]
        try:
            validate_source_macros(bytes.fromhex(selected['source_hex']), selected['english']+' {MACRO:'+name+'}')
        except ValueError as error:
            absence_negatives.append(dict(case='invented-source-'+name,rejected=True,error=str(error)))
        else:
            raise AssertionError(name)
    assert not macro_negatives and len(absence_negatives)==3
'''
    tool=derive('scripts/approve_lil_B171_native_v4328.py','scripts/approve_lil_B172_native_v4378.py',{
        old_review:new_review,old[a:b]:new_macro,
        'all37':'all27','all five complete native sheets':'all four complete native sheets',
        'lil_B171_layout_v1':'lil_B172_layout_v1','lil_B171_profile':'lil_B172_profile',
        'lil_B171_native_approval_v4328':'lil_B172_native_approval_v4378',
        'lil_B171_editorial_manuscript_v3':'lil_B172_editorial_manuscript_v2',
        'lil_B171_editorial_manuscript_v4':'lil_B172_editorial_manuscript_v3','lil_B171_fonts_v4327':'lil_B172_fonts_v4377',
        "len(font['cases']) == 37":"len(font['cases']) == 27","font['current_original_macro_alignment_calls'] == 296":"font['current_original_macro_alignment_calls'] == 216",
        'blocks[171]':'blocks[172]','len(sheets) == 5':'len(sheets) == 4','block=171':'block=172',
        "assert macros == {b'FI': 1}":"assert not macros",
        "{'revise':24, 'retain-wording':13}":"{'revise':19, 'retain-wording':8}",
        "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 16":"sum(bool(row.get('qa_waivers')) for row in doc['records']) == 13",
        "assert len(names) == 6 and all(row['original_scratch_rings'] and row['original_getter_writes'] for row in names)":"assert len(names) == 6\n    assert all(row['original_scratch_rings'] and row['original_getter_writes'] for row in names if row['actor_ID'] in [2,26])\n    assert len([row for row in names if row['actor_ID']==201])==2 and all(row['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not row['original_scratch_rings'] and not row['original_getter_writes'] for row in names if row['actor_ID']==201)",
        'current_original_macro_alignment_calls=296,new_current_original_macro_alignment_calls=296':'current_original_macro_alignment_calls=216,new_current_original_macro_alignment_calls=216',
        'progressive_planes=37':'progressive_planes=27',
        'source_macro_preservation_negatives=macro_negatives,':'source_macro_preservation_negatives=macro_negatives,source_macro_absence_negatives=absence_negatives,',
        'source_FI1_and_three_selectors_preserved':'source_macro_absence_and_three_selectors_preserved',
        'source_four_presentations_one_resource_C200_and_both_ends_preserved':'source_five_presentations_three_resources_C200_then_A000_and_single_end_preserved',
        'no_source_A000_or2000_pause_or_earned_event_claim':'source_later_A000_retained_without_packed_semantics_or_earned_event_claim',
        'revised=24,retained=13':'revised=19,retained=8',
        'current_macro_alignment_cases=296':'current_macro_alignment_cases=216',
        'source_macro_negatives=1':'source_macro_negatives=0,source_macro_absence_negatives=3',
        'narrow_row_count_notes=16':'narrow_row_count_notes=13','actual_selected_B171_IDs':'actual_selected_B172_IDs',
        'B171:37 five-gate reviews approved,24 revisions/13 retentions;37 native planes/296 cases;15+1+14 rejection controls.':'B172:27 five-gate reviews approved,19 revisions/8 retentions;27 native planes/216 original alignment cases;15 source-consumer,3 macro-absence and14 formatter rejection controls.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,all4_native_sheets_viewed=True,source_macro_count=0,
        expected_processor_alignment_cases=216,expected_progressive_planes=27,
        original_name_consumers_four_owned_scratch_and_two_Mihwa_readonly=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
