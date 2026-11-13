"""Retain native limits; use complete page clauses when one-page trials cannot fit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    parent=Path('translations/rafael_B141_B160_visual_preferences_v4.json')
    failed=Path('work/analysis/Rafael557_automatic_plans_v4_20261105/automatic_plans.json')
    out=Path('translations/rafael_B141_B160_visual_preferences_v5.json')
    assert not out.exists();prefs=deepcopy(load(parent));plan=load(failed)
    assert {r['id'] for r in plan['failures']}=={'DK4_MES_B143_R0115','DK4_MES_B143_R0129','DK4_MES_B143_R0189','DK4_MES_B150_R0013'}
    targets={
        'DK4_MES_B143_R0115':('Some, however, engage in inhumane practices.','Keep the complete second sentence on the new page instead of stranding its prepositional ending; the one-page trial does not fit the unchanged native limits.'),
        'DK4_MES_B143_R0129':('and take Espinosa into custody.','Keep the complete coordinated custody action on page two instead of stranding into custody; the native one-page trial is impossible.'),
        'DK4_MES_B143_R0189':('That is where you come in.','Move the complete concluding sentence onto page two instead of stranding you come in; preserve the original native page limits.'),
        'DK4_MES_B150_R0013':("to predict the year's events.",'Keep the entire purpose phrase on page two rather than stranding the year\'s events; do not widen or shorten the source-faithful prose.'),
    }
    for ident,(clause,reason) in targets.items():
        row=prefs['records'][ident];assert row.pop('one_page')
        row.update(page_clause=clause,reason=reason)
    prefs['records']['DK4_MES_B143_R0372'].update(line_phrases=['the Guild'],ordinary_boundaries=[['go','to']],
        reason='Fit the complete war-declaration instruction on one native page. Keep the Guild name together and permit an ordinary go/to continuation; retain full width, phase and base QA checks.')
    prefs['records']['DK4_MES_B143_R0380']['line_phrases']=['at war with','their reputation falls']
    prefs['records']['DK4_MES_B143_R0403']['line_phrases']=['proper fleet']
    prefs['records']['DK4_MES_B152_R0144'].update(page_clause="but I can't support you in anything else.",line_phrases=['defeat him'],
        reason='Keep the whole adversative limit on page two rather than its final object, without artificially spreading the short political preface over four rows.')
    prefs.update(previous_preferences=str(parent),previous_preferences_sha256=sha(parent.read_bytes()),
        rejected_one_page_trials=str(failed),rejected_one_page_trials_sha256=sha(failed.read_bytes()),
        no_native_width_font_controls_orprose_changes=True)
    save(out,prefs);print('Retained native limits afterfour failedone-page trials;wholeclauses andphrase continuity nowtargeted.No prose shortened.')
