"""Preserve the syntax-failed preparer and add its single missing concatenation operator."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
SOURCE=Path('scripts/prepare_Gerhard_checkpoint_v8212.py')
TARGET=Path('scripts/prepare_Gerhard_checkpoint_v8212b.py')
ROOT=Path('work/analysis/Gerhard_checkpoint_syntax_repair_v8212b')
if __name__=='__main__':
    assert not TARGET.exists() and not ROOT.exists();raw=SOURCE.read_bytes();source=raw.decode('utf8')
    key="    previous.NEXT[previous.NEXT.index('Keepfullobjective'):]"
    assert source.count(key)==1
    target=source.replace(key,"    +previous.NEXT[previous.NEXT.index('Keepfullobjective'):]")
    compile(target,str(TARGET),'exec');TARGET.write_text(target,encoding='utf8')
    assert SOURCE.read_bytes()==raw
    ROOT.mkdir(parents=True);save(ROOT/'single_operator_source_repair.json',dict(source=str(SOURCE),source_sha256=sha(raw),target=str(TARGET),target_sha256=sha(TARGET.read_bytes()),
        exact_single_missing_string_concatenation_operator_added=True,no_native_numbers_orlogic_changed=True,
        predecessor_failed_compile_no_checkpoint_orproject_document_writes=True,new_credit=0,full_goal_complete=False))
    print('Preserved syntax-failed preparer;successor adds only missing string concatenation operator.')
