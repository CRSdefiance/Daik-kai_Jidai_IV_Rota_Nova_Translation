"""Check the complete native FE command preamble separately from its body selector."""
from scripts.finalize_maria303_prose_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'scoped20_names_editorial_review_v2.json':'scoped20_names_editorial_review_v3.json',
    "assert r['source_complete_preamble_hex'].startswith('fe')":
    "assert r['source_complete_preamble_hex']=='0040ffff00fe' and r['source_hex'].startswith('fe')",
})
if __name__=='__main__':exec(compile(source,__file__+'::exact-complete-FE-preamble-andbody-selector','exec'),globals())
