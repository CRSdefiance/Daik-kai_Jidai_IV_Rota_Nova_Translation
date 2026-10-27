"""Preserve the full polite request and extensive-knowledge compliment in natural clauses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_request_v4181b')
INPUT=Path('translations/lil_B168_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B168_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT))
    r=next(r for r in doc['records'] if r['source_record_index']==146);r['prior_reviewed_English_before_request_refinement']=r['english']
    assert r['english']=="{SPEAKER:09}You're Mikhail, right? We'd like you to put all that knowledge to use for {MACRO:FO}."
    r['english']="{SPEAKER:09}You're Mikhail, right? We'd like you to use your extensive knowledge for {MACRO:FO}."
    r['localization_note']+=' Refine the complete request to use your extensive knowledge: this explicitly preserves 豊富な知識, the polite we-would-like-you intent, Mikhail name question and FO beneficiary. No clause, compliment, name, macro, fact or recruitment intent is removed. The source has no fixed allocation constraint requiring shortening.'
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),formatting_review_pending=True);save(OUTPUT,doc)
    tools=[derive('dk4tool/dialogue/lil_B168_layout_v1.py','dk4tool/dialogue/lil_B168_layout_v2.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('extensive','knowledge')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B168_layout_v4181.py','scripts/plan_lil_B168_layout_v4181b.py',{
        'lil_B168_layout_v1':'lil_B168_layout_v2','lil_B168_layout_v4181':'lil_B168_layout_v4181b',
        'lil_B168_editorial_manuscript_v1':'lil_B168_editorial_manuscript_v3','lil_B168_editorial_manuscript_v2':'lil_B168_editorial_manuscript_v4'}))
    tools.append(derive('scripts/verify_lil_B168_fonts_v4182.py','scripts/verify_lil_B168_fonts_v4182b.py',{
        'lil_B168_layout_v1':'lil_B168_layout_v2','lil_B168_fonts_v4182':'lil_B168_fonts_v4182b','lil_B168_editorial_manuscript_v2':'lil_B168_editorial_manuscript_v4'}))
    ROOT.mkdir(parents=True);save(ROOT/'full_source_name_knowledge_request_company_preserved.json',dict(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),changed_ID=r['id'],source_complete_polite_name_question_extensive_knowledge_request_and_FO_preserved=True,tools=tools,failed_plan_and_all_previous_words_retained=True,no_manual_layout_guard_metric_waiver_ROM_registry_orcredit_change=True))
