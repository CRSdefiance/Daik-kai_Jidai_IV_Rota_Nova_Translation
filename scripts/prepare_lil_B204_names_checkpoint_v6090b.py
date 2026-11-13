"""Preserve the unexecuted syntax failure;correct only the dict-construction delimiters."""
import io,tokenize
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/checkpoint_lil_B204_names_culture_v6090.py');target=source.with_name('checkpoint_lil_B204_names_culture_v6090b.py');root=Path('work/analysis/lil_B204_names_checkpoint_preparation_v6090b')
    assert not target.exists() and not root.exists();text=source.read_text('utf-8')
    a='result={**prior,previous_verified_handoff=';b='producer_sha256=sha(Path(__file__).read_bytes())}'
    assert text.count(a)==text.count(b)==1;fixed=text.replace(a,'result=dict(prior,previous_verified_handoff=').replace(b,'producer_sha256=sha(Path(__file__).read_bytes()))')
    compile(fixed,str(target),'exec')
    numbers=lambda s:[t.string for t in tokenize.generate_tokens(io.StringIO(s).readline) if t.type==tokenize.NUMBER]
    assert numbers(text)==numbers(fixed)
    target.write_text(fixed,'utf-8');root.mkdir(parents=True);save(root/'syntax_only_successor_receipt.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()),only_dict_constructor_delimiters_corrected=True,all_numeric_tokens_preserved=True,no_prior_checkpoint_or_shared_file_mutation_occurred=True,full_goal_complete=False))
    print('Syntax-only checkpoint successor prepared;all numeric tokens and failed producer preserved.')
