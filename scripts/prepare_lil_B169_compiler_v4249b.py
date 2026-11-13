"""Correct the unexecuted derived adapter's tuple-key substitution; preserve v1."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_compiler_tools_v4249b')
OLD = Path('dk4tool/patch/lil_B169_editorial_v1.py')
NEW = Path('dk4tool/patch/lil_B169_editorial_v2.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    text = OLD.read_text(encoding='utf-8')
    bad = "doc['scoped_profile_module', 'source_effect_operand_notation_amendment']"
    assert text.count(bad)==1
    assert len([n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Tuple)])==1
    text = text.replace(bad,"doc['scoped_profile_module']")
    assert not [n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Tuple)]
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation_and_AST_check.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        explanation='Preview review caught a broad list-suffix replacement also altering one dictionary key into a tuple. Only that unexecuted access is corrected; the added ninth proof dependency remains required. Preserve the generated v1 and its producer as history.',
        no_tuple_subscript_keys_in_successor=True,no_ROM_registry_ledger_orcredit_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B169 compiler v2 prepared;one unintended tuple-key access corrected before execution;v1 and producer preserved.')
