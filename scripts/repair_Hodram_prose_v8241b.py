"""Preserve the pre-output syntax failure and repair its single surplus closing parenthesis."""
import ast,io,tokenize
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/review_Hodram_B137_B45_B46_prose_v8241.py')
    target=Path('scripts/review_Hodram_B137_B45_B46_prose_v8241b.py')
    root=Path('work/analysis/Hodram_prose_repair_v8241b')
    assert not target.exists() and not root.exists()
    text=source.read_text('utf8');old='            source_prose_orcompletion_credit_added=False))'
    assert text.count(old)==1
    planned=text.replace(old,old[:-1]).replace('Hodram_B137_B45_B46_prose_v8241','Hodram_B137_B45_B46_prose_v8241b')
    ast.parse(planned)
    def numbers(value):return [t.string for t in tokenize.generate_tokens(io.StringIO(value).readline) if t.type==tokenize.NUMBER]
    assert numbers(text)==numbers(planned)
    target.write_text(planned,encoding='utf8',newline='\n');root.mkdir(parents=True)
    save(root/'exact_syntax_only_repair.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),target=str(target),target_sha256=sha(target.read_bytes()),
        change='One surplus closing parenthesis removed;output root gets successor suffix. All prose and numeric tokens exact.',source_failed_before_any_output=True,full_goal_complete=False))
