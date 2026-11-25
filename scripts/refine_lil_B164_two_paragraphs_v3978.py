"""Resolve two remaining wraps with complete natural clauses; keep both failed plans."""
from copy import deepcopy
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B164_refinement_v3978')
INPUT=Path('translations/lil_B164_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B164_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));texts={150:"Match the ship to your funds and market share. Otherwise, you can't buy a full cargo but still need more sailors.",183:"Eventually, you'll switch to large ships. You may keep old medium ships for future regional fleets rather than sell them."};changed=[]
    for r in doc['records']:
        if r['source_record_index'] in texts:r['english']='{SPEAKER:0D}'+texts[r['source_record_index']];r['localization_note']+=' Complete concise clauses preserve every source fact; full cargo means goods sufficient to fill the ship, and switching to large ships preserves eventual replacement. No numeric or conditional fact is waived.';changed.append(r['id'])
    assert len(changed)==2;doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),two_paragraph_refinement_producer=__file__,two_paragraph_refinement_producer_sha256=sha(Path(__file__).read_bytes()));save(OUTPUT,doc);tools=[]
    tools.append(derive('scripts/plan_lil_B164_layout_v3977.py','scripts/plan_lil_B164_layout_v3979.py',{'lil_B164_layout_v3977':'lil_B164_layout_v3979','lil_B164_editorial_manuscript_v3':'lil_B164_editorial_manuscript_v5','lil_B164_editorial_manuscript_v4':'lil_B164_editorial_manuscript_v6'}))
    tools.append(derive('scripts/verify_lil_B164_fonts_v3974.py','scripts/verify_lil_B164_fonts_v3980.py',{'lil_B164_fonts_v3974':'lil_B164_fonts_v3980','lil_B164_layout_v1':'lil_B164_layout_v2','lil_B164_editorial_manuscript_v2':'lil_B164_editorial_manuscript_v6'}));ROOT.mkdir(parents=True);save(ROOT/'two_complete_clause_refinements.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),changed_ids=changed,tools=tools,same_source_meanings_and_decisions=True,no_authored_layout_or_waiver=True,no_ROM_registry_ledger_credit_change=True,full_goal_complete=False));print('Two full-clause refinements recorded;all previous wording/plans preserved.')
