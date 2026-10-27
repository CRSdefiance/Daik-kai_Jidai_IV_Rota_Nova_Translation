"""Bind LF-separated Help headings inside complete NUL-terminated pages; retain both failures."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/reconcile_lil_B169_terms_v4219.py')
    text = source.read_text(encoding='utf-8')
    replacements = {
        'variants.append({**item,current_complete_reference=ref,current_hex=raw.hex(),':
            'variants.append(dict(item,current_complete_reference=ref,current_hex=raw.hex(),',
        "clean_full_form_japanese_present='覇者の証' in jp[1:].decode('cp932')})":
            "clean_full_form_japanese_present='覇者の証' in jp[1:].decode('cp932')))",
        "source_title = raw.split(b'\\0',1)[0].decode('cp932')":
            "source_title = raw.split(b'\\n',1)[0].decode('cp932')",
        "target_title = target.split(b'\\0',1)[0].decode('cp932')":
            "target_title = target.split(b'\\n',1)[0].decode('cp932').rstrip(' ')",
        "source_title == '覇者の証'": "source_title == '覇者の証（ゲームの目的）'",
        "clean_complete_title_hex=raw[:raw.index(0)+1].hex(),current_complete_title_hex=target[:target.index(0)+1].hex(),":
            "clean_title_before_LF_hex=raw.split(b'\\n',1)[0].hex(),current_title_before_LF_hex=target.split(b'\\n',1)[0].hex(),complete_page_first_NUL_offsets=[raw.index(0),target.index(0)],",
        'new_actual_gameplay_or_UI_body_calls=0,':
            "new_actual_gameplay_or_UI_body_calls=0,HELP_headings_are_before_first_LF_not_separate_C_strings=True,preserved_failed_producers={str(p):sha(p.read_bytes()) for p in FAILED},",
    }
    for old, new in replacements.items():
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    exec(compile(text, str(source) + '::Help-heading-boundary-corrected', 'exec'),
         dict(__name__='__main__',__file__=__file__,FAILED=[source,Path('scripts/reconcile_lil_B169_terms_v4219b.py')]))
