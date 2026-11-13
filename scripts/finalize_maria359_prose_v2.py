"""Keep both inherited fixed-UI guards; add scoped item/cannon bindings separately."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

wrapper=checked_text(Path('scripts/finalize_maria359_prose_v1.py').read_text(encoding='utf-8'),{
    "source=checked_text(source,{source[start:end]:'''":
    """retained_term_checks=source[start:end]
assert retained_term_checks.count('save(terms_path,')==1
retained_term_checks=\"    compatibility_path=ROOT/'retained_UI_label_compatibility_v1.json'\\n\"+retained_term_checks.replace('save(terms_path,','save(compatibility_path,')
source=checked_text(source,{source[start:end]:retained_term_checks+'''""",
    '[item_path,cannon_path,cp,Path(__file__)]':"[item_path,cannon_path,cp,compatibility_path,Path('scripts/finalize_maria359_prose_v1.py'),Path(__file__)]",
})
if __name__=='__main__':
    exec(compile(wrapper,__file__+'::same-complete-finalizer-retained-native-numeric-andUI-guards','exec'),globals())
