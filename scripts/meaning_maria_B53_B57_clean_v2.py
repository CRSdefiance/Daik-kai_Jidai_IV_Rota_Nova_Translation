"""Retain v1 failure; recognize the ending's single optional Japanese full stop."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/meaning_maria_B53_B57_clean_v1.py').read_text(encoding='utf-8'),{
    "def normalized(row):return ''.join(row['source_Japanese'].split())":
        "def normalized(row):return ''.join(row['source_Japanese'].split()).replace('。','')",
    'same_selector_andJapanese_except_whitespace=True':
        'same_selector_andJapanese_except_whitespace_orfull_stop=True,source_Japanese=row[\'source_Japanese\'],matched_source_Japanese=prior[\'source_Japanese\']',
})
if __name__=='__main__':exec(compile(source,__file__+'::unchanged-meaning-notes-two-ending-punctuation-variants','exec'),globals())
