"""Keep four completed startup derivations; remove one absent prose-replacement key before completion generation."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_startup_completion_repair_v8379b');assert not root.exists();source=Path('scripts/prepare_Hodram_fixture_startup_completion_v8379.py');tree=ast.parse(source.read_text('utf8'));calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='derive'];assert len(calls)==5;results=[]
    for i,call in enumerate(calls):
        previous,successor,changes=map(ast.literal_eval,call.args);before,after=Path(previous),Path(successor)
        if i==4:
            assert 'newbuilder behavior hasseparate8negative evidence' not in before.read_text('utf8');changes.pop('newbuilder behavior hasseparate8negative evidence');assert not after.exists();results.append(derive(previous,successor,changes))
        else:
            assert after.read_text('utf8')==checked_text(before.read_text('utf8'),changes);results.append(dict(previous=previous,previous_sha256=sha(before.read_bytes()),successor=successor,successor_sha256=sha(after.read_bytes()),completed_exact_derivation_reused_without_overwrite=True))
    root.mkdir(parents=True);save(root/'startup_completion_derivations.json',dict(derivations=results,earlier_preparer_preserved=True,four_existing_exact_startup_tools_reused=True,only_one_absent_replacement_removed=True,no_native_rule_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
