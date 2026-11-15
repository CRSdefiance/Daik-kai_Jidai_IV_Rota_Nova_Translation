"""Keep B50's now-measured distinct source FA/FI expansions in the pending clean-only handoff."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_completion_tools_v8127d')
PROOF='work/analysis/Rafael_B50_macros_names_v8133/three_clean_FA_FI_paragraphs12_fresh_alignments_six_exact_reused_name_getters.json'
PENDING='Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127'
if __name__=='__main__':
    assert not ROOT.exists() and Path(PROOF).exists()
    source=Path('scripts/complete_Rafael_B49_v8127c.py').read_text('utf8');tree=ast.parse(source)
    following=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NEXT' for t in n.targets))
    lead=next(ast.literal_eval(n.args[1]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='put' and len(n.args)==2 and isinstance(n.args[0],ast.List) and len(n.args[0].elts)==1 and isinstance(n.args[0].elts[0],ast.Constant) and ast.literal_eval(n.args[0])==[PENDING])
    updated=dict(lead,native_source_macro_andname_binding=PROOF,fresh_exact_source_FA_FI_alignment_cases=12,exact_reused_name_getters=6,measured_default_FA='Castor',measured_default_FI='Rafael')
    newer=following.replace('full effects/itemidentity,nativeFA2/FI1expansion/title/context/callers andcurrentEnglish comparison remainpending.',
        'FA2/FI1expansion nowpasses12fresh nativealignmentcases onthe exactthreeJapanese paragraphs:FAdefaults toCastor(surname),FItoRafael(given),not interchangeable. Six exactnamegetters0/2/9are reused underunchangedcode/fields/actorcontext at '+PROOF+'. Full effects/itemidentity/title/context/callers andcurrentEnglish comparison remainpending.')
    assert newer!=following
    result=derive('scripts/complete_Rafael_B49_v8127c.py','scripts/complete_Rafael_B49_v8127d.py',{
        repr(lead):repr(updated),'NEXT='+repr(following):'NEXT='+repr(newer),
        "Path(__file__)]}":"Path("+repr(PROOF)+"),Path(__file__)]}",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared completion successor with B50FA=Castor/FI=Rafael exact native source bindings;B50 English body remains unread/no credit.')
