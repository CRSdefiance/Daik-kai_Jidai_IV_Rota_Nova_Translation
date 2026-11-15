"""Validate all replacements against original text before creating the source-locked relocation tool."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B211_relocation_tools_v6564c')
if __name__=='__main__':
    assert not ROOT.exists();failed=Path('scripts/prepare_lil_B211_relocation_v6564.py');tree=ast.parse(failed.read_text());changes=next(ast.literal_eval(n.args[2]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='derive');assert changes.pop('relocation_v6513')=='relocation_v6564';assert changes.pop('block[640:]==bytes(2)')=='block[640:]==bytes(0)';assert changes.pop('blocks[210]')=='blocks[211]';changes.update({'block[686:]==bytes(2)':'block[640:]==bytes(0)','bank[210]':'bank[211]','relocation_research_v6513':'relocation_research_v6564c'})
    source=Path('scripts/research_lil_B210_relocation_v6513.py');text=source.read_text();absent=[k for k in changes if k not in text];assert not absent,absent;proof=derive(str(source),'scripts/research_lil_B211_relocation_v6564c.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_relocation_tool.json',dict(proof=proof,preserved_failed_preparers={str(p):sha(p.read_bytes()) for p in [failed,Path('scripts/prepare_lil_B211_relocation_v6564b.py')]},both_preparations_rejected_before_successor_or_ROM_write=True,all_native_constants_and_640_byte_source_inverse_preserved=True,full_goal_complete=False))
