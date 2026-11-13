"""Repair only absent original-text derivation keys; retain the rejected preparer unchanged."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B211_relocation_tools_v6564b')
if __name__=='__main__':
    assert not ROOT.exists();failed=Path('scripts/prepare_lil_B211_relocation_v6564.py');tree=ast.parse(failed.read_text());changes=next(ast.literal_eval(n.args[2]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='derive');assert changes.pop('relocation_v6513')=='relocation_v6564';assert changes.pop('block[640:]==bytes(2)')=='block[640:]==bytes(0)';changes['block[686:]==bytes(2)']='block[640:]==bytes(0)';changes['relocation_research_v6513']='relocation_research_v6564b'
    source=Path('scripts/research_lil_B210_relocation_v6513.py');assert all(k in source.read_text() for k in changes);proof=derive(str(source),'scripts/research_lil_B211_relocation_v6564b.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_relocation_tool.json',dict(proof=proof,failed_preparer=str(failed),failed_preparer_sha256=sha(failed.read_bytes()),first_preparation_rejected_absent_key_before_successor_write=True,all_native_constants_and_640_byte_source_inverse_preserved=True,full_goal_complete=False))
