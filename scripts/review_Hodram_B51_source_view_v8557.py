"""Record the directly viewed clean B51 source pages and qualified names."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_source_view_v8557')
DISPLAY = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
CONTROL = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    proof, control = map(read, [DISPLAY, CONTROL])
    assert proof['current_B51_English_dialogue_bodies_unconsulted'] and control['current_B51_English_dialogue_bodies_still_unconsulted']
    assert proof['source_controls_sha256'] == sha(CONTROL.read_bytes())
    sheet = proof['review_sheet']
    assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    rows = []
    for row in proof['records']:
        pages = row['complete_native_source_display']['pages']
        assert len(pages) == 1
        for page in pages:
            assert sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256']
        rows.append(dict(id=row['id'], source_reference=row['source_reference'], source_selector=row['source_selector'],
            complete_source_preamble_hex=row['complete_source_preamble_hex'], pages=1,
            directly_viewed_complete_first_internal_final_characters=True,
            source_authored_lines_preserved_as_evidence_not_English_wrap_instructions=True))
    assert len(rows) == 5 and [r['source_selector'] for r in rows] == [113, 1, 113, 18, 16]
    branches = control['source_relative_cases']
    assert len(branches) == 8 and sum(len(b['cases']) for b in branches) == 40
    scoped_names = proof['scoped_clean_current_four_names_andreused_native_consumers']
    assert [n['actor_ID'] for n in scoped_names] == [1, 16, 18, 113]
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_view.json', dict(source_native_proof=str(DISPLAY), source_native_proof_sha256=sha(DISPLAY.read_bytes()),
        source_controls=str(CONTROL), source_controls_sha256=sha(CONTROL.read_bytes()), directly_viewed_sheet=sheet, records=rows,
        all5_complete_source_pages_andfour_qualified_reused_nameplanes_directly_viewed=True,
        original_source_speakers=['Port Worker', 'Hodram Bergstrom', 'Port Worker', 'Charles Rochefort', 'Gerhard Adernkatz'],
        whole_exchange_reading='A gruff port worker warns Hodram to leave the South Mediterranean. Hodram asks what the warning means. The worker explains that someone alarming is there and urges a different sea area for self-preservation. Charles has a conditional questioning echo; Gerhard has a separate parenthesized, startled possibility. The person remains unnamed. The source does not confirm recognition or a specific enemy identity.',
        source_relative_cases=branches,
        branch_interpretation_limit='These are original command extents for explicit structural previous-result arguments, not actual routed conversation traces. The 8100 instruction queries event30; the 8000 predicate is separate. Native result forwarding and full executed paths still require focused verification. Do not flatten the nested Charles speech into every path or assert outer event eligibility, chronology, location or naturally reached activation.',
        source_nested_Charles_speech_header=262, source_nested_0100_scope=258,
        source_private_Gerhard_speech_header=294,
        native_source_names_andvoices_bound_without_inventing_relationship_rank_gender_orbiography=True,
        unused_Europe_name_metadata_not_a_spoken_nationality_orpart_of_current_Port_Worker_header=True,
        source_B51_has_no_FE_item_picture_typed_choice_or_FI_FA_FO=True,
        not_actual_gameplay_orall207_name_review=True, current_B51_English_bodies_still_unconsulted=True,
        source_name_editorial_current_prose_formatting_actual_andregistered_release_pending=True,
        new_credit=0, new_emulator_runs=0, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Directly viewed five complete Japanese native pages and four qualified reused names; original branch extents retained with explicit path limits. Current B51 English still unread; zero credit.')
