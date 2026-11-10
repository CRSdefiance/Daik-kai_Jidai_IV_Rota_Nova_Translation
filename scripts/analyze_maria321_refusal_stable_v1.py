"""Preserve all actual pixel checks and exclude one independently bound early transition."""
from pathlib import Path
from scripts import analyze_maria301_display_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

PROOF = Path('work/Maria_B196_B215_clean_20261110/name_header_transition_v1.json')


def stable_source(source):
    source = previous.maria_source(source)
    return checked_text(source, {
        "    for cap in report['frames_captured']:":
        """    transition=load(PROOF)
    assert digest(FIXTURE)==transition['fixture_sha256'] and digest(TERMINAL)==transition['terminal_sha256']
    assert digest(report_path)==transition['report_sha256'] and digest(observer_path)==transition['observer_sha256']
    assert transition['nonapproved_transition_frame']==10740 and transition['stable_frames']==[10800,10920]
    assert transition['all_later_stable_header_pixels_complete_andexact'] and transition['captured_header_transition_not_a_complete_name_approval']
    for cap in report['frames_captured']:
        if cap['frame']==10740:
            assert sha(Path(cap['path']).read_bytes())==cap['PNG_sha256']==transition['captures'][0]['capture']['PNG_sha256']
            continue""",
        "    assert {h['source_selector'] for h in headers} == set(fixture['source_selectors_with_header'])":
        """    assert len(samples)==len(headers)==2*len(expected)==60
    assert all(sum(s['id']==p['id'] and s['page']==p['page'] for s in samples)==2 for p in expected)
    assert {h['frame'] for h in headers if h['frame'] in [10800,10920]}=={10800,10920}
    assert {h['source_selector'] for h in headers} == set(fixture['source_selectors_with_header'])""",
        'complete_body_planes=len(samples), complete_header_planes=len(headers), body_pages=samples, headers=headers,':
        "complete_body_planes=len(samples), complete_header_planes=len(headers), body_pages=samples, headers=headers,\n        nonapproved_early_header_transition=str(PROOF),nonapproved_early_header_transition_sha256=digest(PROOF),regular_complete_body_andheader_holds_per_page=2,",
        'evidence = {str(p): sha(p.read_bytes()) for p in [':
        'evidence = {str(p): sha(p.read_bytes()) for p in [PROOF,',
    })


if __name__ == '__main__':
    exec(compile(previous.source, __file__+'::same-complete-ordered-pixel-checks-two-stable-holds-andexplicit-early-transition', 'exec'),
        {**vars(previous), **globals(), '__file__':__file__, '__name__':'__main__', 'maria_source':stable_source})
