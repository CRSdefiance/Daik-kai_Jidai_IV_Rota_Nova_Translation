"""Preserve B50's completed clean-source entry/control proof in the still-unapplied B49 completion."""
import ast
from pathlib import Path
from scripts.prepare_Rafael_B49_completion_v8127b import LEAD
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_completion_tools_v8127c')
CONTROL='work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json'
if __name__=='__main__':
    assert not ROOT.exists() and Path(CONTROL).exists()
    source=Path('scripts/complete_Rafael_B49_v8127b.py').read_text('utf8')
    following=next(ast.literal_eval(n.value) for n in ast.parse(source).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NEXT' for t in n.targets))
    updated=dict(LEAD,source_controls=CONTROL,original_EV0_entry37commands28speeches_zero_branches_predicates25_seeded_ends_pass=True)
    newer=following.replace('Verify exactFA2/FI1native getters,source4681/4720/4821 andall controls/item effects/callers/title/context before currentEnglish orprose.',
        'Native EV0entry,all37commands/28preambles,zero relative/predicate/query sites and25seeded normalvaluecarry ends nowpass at '+CONTROL+'. Opaque4821/4720/4681/A000bytes andextents arebound;full effects/itemidentity,nativeFA2/FI1expansion/title/context/callers andcurrentEnglish comparison remainpending.')
    assert newer!=following
    result=derive('scripts/complete_Rafael_B49_v8127b.py','scripts/complete_Rafael_B49_v8127c.py',{
        repr(LEAD):repr(updated),'NEXT='+repr(following):'NEXT='+repr(newer),
        "Path(__file__)]}":"Path("+repr(CONTROL)+"),Path(__file__)]}",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared completion successor preserving B50 source entry/control/end proof, without B50 editorial credit.')
