"""Correct the pre-execution dictionary syntax; retain the original failed producer."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/reconcile_lil_B169_terms_v4219.py')
    text = source.read_text(encoding='utf-8')
    replacements = {
        'variants.append({**item,current_complete_reference=ref,current_hex=raw.hex(),':
            'variants.append(dict(item,current_complete_reference=ref,current_hex=raw.hex(),',
        "clean_full_form_japanese_present='覇者の証' in jp[1:].decode('cp932')})":
            "clean_full_form_japanese_present='覇者の証' in jp[1:].decode('cp932')))",
    }
    for old, new in replacements.items():
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    exec(compile(text, str(source) + '::syntax-corrected', 'exec'), dict(__name__='__main__',__file__=__file__))
