"""Bind the measured40-frame page interval to additional read-only capture frames."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B61_B80_actual_fixtures_20261104')
ORIGINAL=ROOT/'Charlotte_complete_scene_fixture.json'
TERMINAL=Path('work/analysis/Rafael_B69_complete_scene_run_20261104/terminal.json')
TARGET=ROOT/'Charlotte_brief_page_dense_capture_fixture.json'

if __name__=='__main__':
    assert not TARGET.exists()
    fixture,terminal=map(load,[ORIGINAL,TERMINAL])
    observer_path=Path(terminal['observer']);report_path=Path(terminal['report'])
    assert sha(observer_path.read_bytes())==terminal['observer_sha256']
    assert sha(report_path.read_bytes())==terminal['report_sha256']
    observer,report=map(load,[observer_path,report_path])
    paints=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>=3000]
    body=next(r['expected_expanded_body_hex'] for r in fixture['selected_records'] if r['id']=='DK4_MES_B69_R0100')
    at=next(i for i,r in enumerate(paints) if r['text_hex']==body)
    start,end=paints[at]['frame'],paints[at+1]['frame']
    assert (start,end)==(9495,9535)
    assert not any(start<=r['frame']<end for r in report['frames_captured'])
    value=deepcopy(fixture)
    value.update(capture_extra=[9498,9504,9510,9518,9528],
        capture_gap_finding=dict(id='DK4_MES_B69_R0100',start=start,end=end,
            cause='The native scene transition leaves a40-frame display interval between the120-frame screenshot samples.',
            existing_run_ordered_all66_calls_passed_but65_complete_pages_captured=True,
            no_text_font_control_ROM_input_or_timing_change=True),
        predecessor_fixture=str(ORIGINAL),predecessor_fixture_sha256=sha(ORIGINAL.read_bytes()),
        predecessor_terminal=str(TERMINAL),predecessor_terminal_sha256=sha(TERMINAL.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(TARGET,value)
    print('Measured sampling gap9495..9535; five exact captures added. ROM,full scene andcontroller schedule unchanged.')
