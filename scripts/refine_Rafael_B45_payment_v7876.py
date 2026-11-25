"""Payment-first explanation in the complete exchange; preserve the v1 manuscript."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('translations/rafael_B45_editorial_manuscript_v1.json')
OUTPUT=Path('translations/rafael_B45_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/Rafael_B45_payment_refinement_v7876')
if __name__=='__main__':
    assert not OUTPUT.exists() and not ROOT.exists();before=read(SOURCE);after=deepcopy(before)
    row=next(r for r in after['records'] if r['source_record_index']==29)
    assert row['english']=="Go to the Palace or Governor's Office and pay the local ruler a contract fee. That gives you the right to trade in that town."
    row['english']="You pay the local ruler a contract fee at the Palace or Governor's Office. That gives you the right to trade there."
    row['localization_note']=row['editorial_finding']="Explain the contract directly in response to Rafael's question: payment to the local ruler at either office grants the right to trade there. Reorder the full explanation around payment, then its result. Both destinations, the ruler, contract fee and local trading permission remain explicit; the instruction to pay at the named office implies visiting it. No fee amount, bribery, universal right or sales contract is invented. This is complete natural prose without authored layout or an inherited allocation limit."
    after['prior_manuscript']=dict(path=str(SOURCE),sha256=sha(SOURCE.read_bytes()))
    after['payment_first_refinement_preserves_all_source_facts_andeleven_other_record_objects']=True
    save(OUTPUT,after)
    ROOT.mkdir(parents=True);save(ROOT/'payment_first_complete_exchange_refinement.json',dict(
        before=str(SOURCE),before_sha256=sha(SOURCE.read_bytes()),after=str(OUTPUT),after_sha256=sha(OUTPUT.read_bytes()),
        changed_record=row['id'],source_meaning=row['source_meaning'],English=row['english'],note=row['localization_note'],
        eleven_other_records_exact=True,all12_formatting_gates_still_false=True,new_credit=0,full_goal_complete=False))
    assert sum(a!=b for a,b in zip(before['records'],after['records'],strict=True))==1
    print('R29 payment-first explanation;all source facts retained;eleven other record objects exact.')
