"""Seal all directly viewed pages and rebuild the seven exact source blocks."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import ROOT, CURRENT, PROSE, STAGED
PLAIN = ROOT / 'ordinary_formatting_manuscript_v5.json'
FINAL_PLAN = ROOT / 'plans_v7/automatic_plans.json'
from scripts.rebuild_rafael_B166_B167_reviewed_v1 import source as rebuild, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/seal_rafael_B166_B167_offline_display_v1.py')
source = checked_text(BASE.read_text(encoding='utf-8'), {
    'from scripts.plan_rafael_B166_B167_ordinary_v1 import CURRENT, ROOT': '',
    "PROSE=Path('translations/rafael_B166_B167_contextual_review_v5.json')\nPLAIN=ROOT/'ordinary_formatting_manuscript_v4.json'\nSTAGED=ROOT/'source_staged_FE_inputs_v2.json'\nFINAL_PLAN=ROOT/'ordinary_plans_v10/automatic_plans.json'": '',
    "'ordinary_native_v1','ordinary_wrap_delta_native_v1','ordinary_wrap_delta_native_v2'":
        "'ordinary_native_v1','visual_delta_native_v1','final_rows_delta_native_v1'",
    "STAGED_NATIVE=ROOT/'staged_FE_native_v7/staged_display.json'": "STAGED_NATIVE=ROOT/'staged_FE_native_v2/staged_display.json'",
    '==[(164,165),(24,25),(2,3)]': '==[(187,187),(15,15),(1,1)]',
    "==len(ordinary_plan['records'])==164": "==len(ordinary_plan['records'])==187",
    "==22 and not staged_display['failed']": "==3 and not staged_display['failed']",
    "names['distinct_strings']==24": "names['distinct_strings']==13",
    'assert len(sheets)==24 and': "assert len(sheets)==sum(len(p['review_sheets']) for p in (*plain_displays,staged_display,names)) and",
    'len(source)==186': 'len(source)==190',
    "        assert r['editorial_logical_English']==original['english']":
        "        if r['editorial_logical_English']!=original['english']:\n"
        "            assert r['decision']=='revision' and r['visual_revision_previous_English']==original['english']",
    'len(plans)==186': 'len(plans)==190',
    "block=166,kind='system-FE'": "block=row['block'],kind='system-FE'",
    "block=166,source_selector=254": "block=row['block'],source_selector=254",
    "'physical_speech_objects':186,'ordinary_speech_objects':186": "'physical_speech_objects':190,'ordinary_speech_objects':190",
    "'source_staged_FE_panels':22": "'source_staged_FE_panels':3",
    "'pages':187": "'pages':190",
    "'fresh_compiled_alignments':744": "'fresh_compiled_alignments':760",
    "'body_pages':187": "'body_pages':190",
    "'scoped_name_count':24,'source_staged_FE_pages':22": "'scoped_name_count':13,'source_staged_FE_pages':3",
    "'source_only_actor8_contextual_header_risk_pending':True,": "'original_locations_and_actual_nameplates_unvisited':True,",
    'Sealed 186 exact bodies, 187 pages and 24 default nameplates.': 'Sealed 190 exact bodies and pages and 13 nameplates.',
    "if __name__=='__main__':\n    main()": '',
})
seal_env = {**globals(), '__file__': __file__}
exec(compile(source, __file__+'::same-visual-binding-contract', 'exec'), seal_env)
OUT = seal_env['OUT']
reconstruction_source = checked_text(rebuild, {
    "len(doc['records'])==186": "len(doc['records'])==190",
    "==len(native['records'])==186": "==len(native['records'])==190",
    '==(186,0,0)': '==(190,0,0)',
    'len(changed)==2': 'len(changed)==7',
    'speech_count=186': 'speech_count=190',
    'ordinary_speeches=186': 'ordinary_speeches=190',
    'menu_labels=0,changed_blocks=2': 'menu_labels=0,changed_blocks=7',
    "visual['body_pages']==187": "visual['body_pages']==190",
    'Rafael B166–B167 complete 186-speech': 'Rafael B170–B176 complete 190-speech',
})

if __name__ == '__main__':
    if sys.argv[1:] == ['--seal']:
        seal_env['main']()
    else:
        exec(compile(reconstruction_source, __file__+'::same-exact-seven-block-reconstruction', 'exec'), globals())
