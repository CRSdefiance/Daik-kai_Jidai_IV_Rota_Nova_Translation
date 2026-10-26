"""Keep regional fleets together by natural clause order; preserve all failed producers/plans."""
from copy import deepcopy
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B164_refinement_v3981')
INPUT=Path('translations/lil_B164_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B164_editorial_manuscript_v7.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));r=next(r for r in doc['records'] if r['source_record_index']==183);r['english']="{SPEAKER:0D}Eventually, you'll switch to large ships. For future regional fleets, you may keep old medium ships rather than sell them.";r['localization_note']+=' Natural clause reordering keeps the established regional fleets term together while preserving eventual switching and optional retention for future fleets instead of sale.';doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),fleet_sentence_refinement_producer=__file__,fleet_sentence_refinement_producer_sha256=sha(Path(__file__).read_bytes()));save(OUTPUT,doc);tools=[]
    tools.append(derive('scripts/plan_lil_B164_layout_v3979.py','scripts/plan_lil_B164_layout_v3982.py',{'lil_B164_layout_v3979':'lil_B164_layout_v3982','lil_B164_editorial_manuscript_v5':'lil_B164_editorial_manuscript_v7','lil_B164_editorial_manuscript_v6':'lil_B164_editorial_manuscript_v8'}))
    tools.append(derive('scripts/verify_lil_B164_fonts_v3980.py','scripts/verify_lil_B164_fonts_v3983.py',{'lil_B164_fonts_v3980':'lil_B164_fonts_v3983','lil_B164_editorial_manuscript_v6':'lil_B164_editorial_manuscript_v8'}));ROOT.mkdir(parents=True);save(ROOT/'one_natural_clause_order_refinement.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),changed_id=r['id'],tools=tools,same_source_meanings_and_decisions=True,all_failed_plans_and_producers_preserved=True,no_authored_layout_or_waiver=True,no_ROM_registry_ledger_credit_change=True,full_goal_complete=False));print('Regional-fleet clause reordered naturally;all facts and drafts preserved.')
