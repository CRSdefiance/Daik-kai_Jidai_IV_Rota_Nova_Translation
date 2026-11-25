"""Repair the syntax-only failure with numeric-token equality, preserving both earlier attempts."""
import ast,io,tokenize
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/map_Hodram_B47_B48_current_v8317.py');target=Path('scripts/map_Hodram_B47_B48_current_v8317c.py');root=Path('work/analysis/Hodram_current_tools_v8317c')
    assert not target.exists() and not root.exists();text=source.read_text('utf8')
    old='source_prose_orcompletion_credit_added=False,prose_formatting_actual_effects_andregistered_release_pending=True))';assert text.count(old)==1
    planned=text.replace(old,old[:-1]).replace('Hodram_B47_B48_current_v8317','Hodram_B47_B48_current_v8317c');ast.parse(planned)
    def numbers(value):return [t.string for t in tokenize.generate_tokens(io.StringIO(value).readline) if t.type==tokenize.NUMBER]
    assert numbers(text)==numbers(planned);target.write_text(planned,encoding='utf8',newline='\n');root.mkdir(parents=True)
    save(root/'syntax_only_repair_numeric_tokens_exact.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),target=str(target),target_sha256=sha(target.read_bytes()),
        one_surplus_parenthesis_removed_only_output_root_suffix_changed=True,all_numeric_tokens_exact=True,earlier_AST_derivation_failed_before_outputs_because_source_does_not_parse=True,all_attempts_preserved=True,new_credit=0,full_goal_complete=False))
