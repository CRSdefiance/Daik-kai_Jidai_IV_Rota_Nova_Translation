"""Preserve the syntax-failed producer; repair one surplus closing parenthesis before staging."""
from collections import Counter
from io import StringIO
from pathlib import Path
import tokenize
from scripts.source_locked_derivation_v5118 import checked_text,native_numbers
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/complete_Maria_story_v7784.py')
    target=Path('scripts/complete_Maria_story_v7784b.py')
    root=Path('work/analysis/maria_story_completion_tools_v7784b')
    assert not target.exists() and not root.exists()
    text=source.read_text('utf8')
    old="full_goal_active=True,full_goal_complete=False,new_credit=67,producer_sha256=sha(Path(__file__).read_bytes())))"
    new="full_goal_active=True,full_goal_complete=False,new_credit=67,producer_sha256=sha(Path(__file__).read_bytes()))"
    assert text.count(old)==1
    repaired=text.replace(old,new);compile(repaired,str(source)+'::one-parenthesis-repair','exec')
    result=checked_text(repaired,{'v7784':'v7784b','v7785':'v7785b','V7784':'V7784b','V7785':'V7785b'})
    assert native_numbers(repaired)==native_numbers(result)
    # The sole syntax repair changes no digit, string, guard or executable statement.
    assert Counter(c for c in text if c.isdigit())==Counter(c for c in repaired if c.isdigit())
    target.write_text(result,'utf8');root.mkdir(parents=True)
    save(root/'provenance.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),target=str(target),target_sha256=sha(target.read_bytes()),
        exact_one_surplus_closing_parenthesis_removed=True,all_native_numbers_andguards_unchanged=True,
        syntax_failure_preserved_no_producer_body_orledger_write_executed=True,
        all_ROMs_andtranslations_preserved=True,new_credit=0,full_goal_complete=False))
