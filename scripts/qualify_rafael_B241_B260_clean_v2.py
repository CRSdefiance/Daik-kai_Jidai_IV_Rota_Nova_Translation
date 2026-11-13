"""Advance the next clean intake through both complete letter exchanges."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.qualify_rafael_B241_B260_clean_v1 import OUT as BEFORE, PATHS, ROOT
from scripts.write_rafael_B221_B240_contextual_v1 import digest

OUT = ROOT/'clean_source_census_v2.json'
DRAFT = ROOT/'B245_B248_clean_drafts_v1.json'

if __name__ == '__main__':
    assert not OUT.exists()
    census, packet, styles, draft = map(load, (BEFORE, PATHS[0], PATHS[2], DRAFT))
    assert census['new_eligible_objects'] == 292 and census['prior_reviewed_records'] == 18
    assert census['source_only_no_current_English_extracted'] and draft['no_current_English_extracted_for_this_intake_before_drafts']
    assert draft['records_count'] == 44 and draft['complete_blocks'] == [245,247,248]
    expected = {row['id'] for group in packet['groups'] if group['block'] in draft['complete_blocks']
                for row in group['records']} | {row['id'] for row in styles['records']}
    assert {row['id'] for row in draft['records']} == expected and draft['physical_style_alternatives'] == 14
    assert draft['all_five_gates_pending']
    assert all(digest(Path(path)) == checksum for path, checksum in draft['evidence'].items())
    save(OUT, {**census, 'independently_drafted_records':94, 'complete_draft_blocks':[241,242,243,244,245,247,248],
        'remaining_clean_drafts':198, 'source_only_no_current_English_extracted':True,
        'evidence':{**census['evidence'],**{str(path):digest(path) for path in (BEFORE,DRAFT,Path(__file__))}}})
    print('94 clean-only drafts across seven blocks, with B246 preserved as earlier reviewed context.')

