"""Preserve the failed preparer and qualify only three invalid numeric-leading receipt identifiers."""
import io,re,tokenize
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/prepare_Hodram_B54_B60_completion_audit_v8871.py')
NEW=Path('scripts/prepare_Hodram_B54_B60_completion_audit_v8871b.py')
ROOT=Path('work/analysis/Hodram_B54_B60_completion_audit_syntax_v8871b')
def high_numbers(text):
    values=[]
    for t in tokenize.generate_tokens(io.StringIO(text).readline):
        if t.type==tokenize.NUMBER:
            try:value=int(t.string,0)
            except ValueError:continue
            if value>=0x20000:values.append(value)
    return Counter(values)
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();source=OLD.read_text(encoding='utf-8')
    changes={'63actual19offline_all_main_focused':'observed63_offline19_all_main_focused',"'82_speeches_seven_blocks":"'all82_speeches_seven_blocks","'63_observed_utterances19_offline":"'observed63_utterances19_offline",'Hodram_B54_B60_completion_audit_tools_v8871':'Hodram_B54_B60_completion_audit_tools_v8871b'}
    assert all(source.count(k)==1 for k in changes)
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],source)
    compile(target,str(NEW),'exec');assert high_numbers(source)==high_numbers(target)
    NEW.write_text(target,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'preserved_syntax_failure_andqualified_preparer.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),original_failure='SyntaxError:invalid decimal literal in receipt keyword starting63; two generated receipt identifiers also started with numbers',only_three_metadata_identifier_names_andnew_receipt_root_changed=True,tokenized_native_high_integer_constants_andmultiplicity_preserved=True,generated_auditor_still_uses_full_original_AST_source_lock=True,no_completion_stage_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
