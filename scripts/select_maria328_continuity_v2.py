"""Keep the successful one-page refinement anddocument unavoidable current-consumer word wrapping."""
from copy import deepcopy
from pathlib import Path
import textwrap
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    before = ROOT/'formatting_FE_v1/preferences_continuity_v1.json'
    out = ROOT/'formatting_FE_v1/preferences_continuity_v2.json'
    assert not out.exists()
    preferences = deepcopy(load(before))
    doc_path = ROOT/'formatting_FE_v1/physical_manuscript.json'
    rows = {r['id']:r for r in load(doc_path)['records']}
    findings = []
    for ident in ['DK4_MES_B73_R0020','DK4_MES_B88_R0204','DK4_MES_B89_R0030','DK4_MES_B94_R0073']:
        row = rows[ident]
        # This is a word-packing lower bound,not a native display proof. The
        # unchanged planner's pair phase reserves its pre-LF space at even
        # lengths,leaving at most35 visible ASCII characters on nonfinal rows.
        lower = textwrap.wrap(row['english'],width=35,break_long_words=False,break_on_hyphens=False)
        assert len(lower) == 5
        rule = preferences['records'][ident]
        assert rule.pop('one_page') is True
        rule['reason'] += ' Even unconstrained35-character word packing needs five rows;do not shorten prose orchange native phase rules to force four. Keep the required phrase intact;fresh native/visual page review remains required.'
        findings.append(dict(id=ident,unconstrained_word_packing_rows=lower,
            not_a_native_page_orfinal_visual_approval=True))
    preferences.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        word_packing_findings=findings,new_credit=0)
    save(out,preferences)
    print('Retained full-width phase rules;Julio one-page improvement kept;four genuine five-row paragraphs require visual pagination review.')


if __name__ == '__main__':
    main()
