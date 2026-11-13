"""Preserve both failed attempts; fix original-source keys and continuation guard reservation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B215_tool_successors_v6748b')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[('scripts/plan_lil_B215_layout_v6747.py','scripts/plan_lil_B215_layout_v6747b.py',{'layout_v6747':'layout_v6747b','if length+reserve>36:':'if length+reserve+int(line>0)>36:'}),('scripts/prepare_lil_B215_source_fixture_v6748.py','scripts/prepare_lil_B215_source_fixture_v6748b.py',{'fixture_tools_v6748':'fixture_tools_v6748b',"'Complete B215 clean-source18-speech prophecy fixture with all27 commands,four relative controls,one unforced predicate,original4821/4720 staging,one A000 effect,oneFI andcomplete normal end.'":"'Complete B213 clean-source18-speech prophecy fixture with all27 commands,four relative controls,one unforced predicate,original4821/4720 staging,one A000 effect,oneFI andcomplete normal end.'"})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    proofs=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_successors.json',dict(derivations=proofs,prior_executed_producers_and_failures_preserved=True,no_prose_or_ROM_changes=True,full_goal_complete=False))
