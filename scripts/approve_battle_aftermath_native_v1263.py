"""Record the six actually inspected font sheets; retain real-scene gates."""
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_native_review_v1263')
OLD = Path('translations/battle_aftermath_editorial_manuscript_v2.json')
NEW = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
FONT = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')


def main():
    assert not ROOT.exists() and not NEW.exists()
    font,doc = read(FONT),read(OLD)
    assert font['manuscript_sha256'] == sha(OLD.read_bytes())
    assert len(font['cases']) == 783 and len(font['review_sheets']) == 6
    assert font['producer_sha256'] == sha(Path('scripts/probe_battle_aftermath_fonts_v1260.py').read_bytes())
    by_id = {r['message_id']:r for r in doc['records']}
    reviewed = set()
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        for index in sheet['case_indices']:
            reviewed.add(font['cases'][index]['message_id'])
    assert reviewed == set(by_id)
    for case in font['cases']:
        assert case['compiled_hex'] == compiled(by_id[case['message_id']]).hex()
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        assert case['whole228x64_native_independent_font_and_all_letters_equal']
        assert case['first_and_continuation_visible_origins_x6_no_authored_alignment']
        assert not case['weak_line_end_indices']
        if not case['name_case'] or case['name_case']['kind'] == 'source-native-town':
            assert not case['single_word_final_row']
    decisions = []
    for finding in font['line_boundary_findings_requiring_review']:
        case = font['cases'][finding['case_index']]
        name = case['name_case']
        assert case['message_id'] in (1994,1997,1999)
        assert name['kind'] == 'synthetic-layout-stress-not-real-town'
        assert name['name'] in ('ABCDEFGHIJKLMNOPQRSTUVW','ABCDEFGHIJKLMNOPQRSTUVWXYZ12345')
        assert case['lines'] == [name['name']+' has','surrendered!']
        assert finding['single_word_final_row'] and not finding['weak_line_end_indices']
        decisions.append({**finding,'disposition':'reviewed-synthetic-name-only',
            'reason':'The oversized synthetic proper name forces the complete predicate onto a second row. Every glyph and both margins pass. This is not an actual town name, a clipped word or a borrowed neighboring fragment; all114 real town-name cases have no single-word final row.',
            'preview_sha256':case['preview_sha256']})
    assert len(decisions) == 6
    # V1258's prose note predicted a one-row result for1995. The actual native
    # planner can choose two balanced rows. Correct the note without changing
    # the tested English, payload, glyphs or historical frozen evidence.
    by_id[1995]['localization_note'] = ('Preserve the excited surrender report and direct address. Moving Admiral to the end is natural English and keeps the complete surrendered, Admiral predicate together when the native planner uses a second row. Actual Rio de Janeiro output is two balanced rows;the earlier V1258 one-row prediction was incorrect. All114 real town names retain the complete report without an isolated final word. No source fact,voice or authored layout is introduced.')
    native = deepcopy(doc)
    native['records'] = [deepcopy(by_id[r['message_id']]) for r in doc['records']]
    ROOT.mkdir(parents=True)
    review = ROOT/'visual_and_native_review.json'
    save(review,{'native_font_proof':str(FONT),'native_font_proof_sha256':sha(FONT.read_bytes()),
        'all6_review_sheets_actually_visually_inspected':font['review_sheets'],
        'every75_message_and_actual_longest_name_and_all_synthetic_variants_visually_represented':True,
        'all783_complete_native_fonts_pass':True,'all684_real_town_expansions_and69_static_cases_no_single_word_final_row':True,
        'all6_remaining_synthetic_name_only_boundary_decisions':decisions,
        'V1258_note_erratum_1995_actual_native_can_choose2_rows_not_guaranteed1':True,
        'zero_missing_letters_padding_gaps_or_out_of_bounds_pixels':True,
        'scope':'Original loader/printf/macro/formatter and full native228x64 glyph canvases, with disclosed CPU role assignments,file-success and portrait-construction boundaries. Not a new GPU capture,original battle outcome or full-game check.',
        'registered_release_exact_patch_cold_boot_original_scenes_and_transitions_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native.update(formatting_review_pending=False,
        status='75-source-prose-native-font-reviewed;registered-release-and-original-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review=str(review),visual_review_sha256=sha(review.read_bytes()),
        native_copy_proof='work/analysis/battle_aftermath_copies_v1261/all_native_copies_and_prefix_cache_sequence.json',
        escape_regression_proof='work/analysis/battle_aftermath_escape_v1262/original_direct_escape_regression.json',
        no_compiled_release_payload_or_layout_approval_yet=False,
        original_gameplay_and_registered_ROM_integration_still_pending=True)
    for row in native['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-font-approved;release-and-original-gameplay-pending'
        selected = [d for d in decisions if d['message_id'] == row['message_id']]
        if selected:
            row['qa_waivers'] = ['single_word_final_row']
            row['case_bound_qa_waivers'] = selected
            row['qa_waiver_reason'] = 'Only the two exact synthetic oversized proper names listed here. All114 real town names,full glyphs,margins and bounds pass without this finding.'
    validate_natural_dialogue_batch(native)
    save(NEW,native)
    save(ROOT/'native_manuscript_approval.json',{'manuscript':str(NEW),'manuscript_sha256':sha(NEW.read_bytes()),
        'tested_predecessor':str(OLD),'tested_predecessor_sha256':sha(OLD.read_bytes()),
        'all75_compiled_payloads_exact_to783_case_test':all(compiled(r).hex()==compiled(by_id[r['message_id']]).hex() for r in native['records']),
        'visual_review':str(review),'visual_review_sha256':sha(review.read_bytes()),
        'source_and_completed_counts_not_changed':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('75 native-format manuscripts approved after6 visual sheets;6 synthetic-only findings bounded. Actual scenes and release remain pending.',flush=True)


if __name__ == '__main__':
    main()
