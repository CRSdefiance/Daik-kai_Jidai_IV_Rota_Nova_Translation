"""Compare complete token multisets, including source dictionaries with explicit zero counts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/finalize_maria303_prose_v1.py').read_text(encoding='utf-8'),{
    'scoped20_names_editorial_review_v1.json':'scoped20_names_editorial_review_v2.json',
    "assert dict(Counter(re.findall(r'F[A-Z]',text)))==r['source_macros'],r['id']":
    "assert Counter(re.findall(r'F[A-Z]',text))==Counter(r['source_macros']),r['id']",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-prose-gates-exact-token-multisets','exec'),globals())
