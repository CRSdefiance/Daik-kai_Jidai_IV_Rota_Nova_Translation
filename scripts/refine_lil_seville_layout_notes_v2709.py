"""Document eight source/target line-count differences;retain all prose."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_layout_notes_v2709')
OLD=Path('translations/lil_seville_encounter_editorial_manuscript_v1.json')
OUT=Path('translations/lil_seville_encounter_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();doc=deepcopy(read(OLD));base=get_dialogue_profile('lil-opening-editorial-native-v1');profile=replace(base,leading_speaker_bytes=frozenset({2,4,16,20,31,254}));waivers=[]
    for row in doc['records']:
        result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert all(d.code=='line-break-count' and d.severity=='warning' for d in result.diagnostics)
        if result.diagnostics:
            reason='The Japanese ordinary line breaks are layout,not a dramatic pause. The complete faithful English is authored as one paragraph;the calibrated formatter owns its new wrapping. The differing line count alone is accepted. This waiver does not permit overflow,orphaned predicates,missing boundary glyphs,bad controls,blank pages or authored alignment;native complete glyph/consumer/pagination checks remain required.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason,localization_note=row['localization_note']+' '+reason)
            waivers.append(dict(id=row['id'],diagnostics=[dict(code=d.code,message=d.message) for d in result.diagnostics],reason=reason))
    assert len(waivers)==8
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),body_only_layout_waivers_documented=True,no_English_or_source_control_change=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(OLD)['records']]
    ROOT.mkdir(parents=True);save(OUT,doc);save(ROOT/'line_count_waivers.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),waivers=waivers,English_and_controls_unchanged=True,formatting_and_registered_release_still_pending=True,source_prose_credit_added=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('8line-count-only warnings documented individually;all18paragraphs unchanged. No overflow/orphan/control waiver orcompletion credit.')
