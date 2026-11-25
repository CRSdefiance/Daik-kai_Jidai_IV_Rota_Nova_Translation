"""Bind 32 exact repeats; author three repunctuated variants explicitly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/meaning_maria_B53_B57_clean_v1.py').read_text(encoding='utf-8'),{
    'def normalized(row):':
        """# These three source variants repunctuate sentences; each was reread in full.
MEANINGS[54].update({87:MEANINGS[53][82],128:MEANINGS[53][123],139:MEANINGS[53][134]})

def normalized(row):""",
    'len(reuse)==35':'len(reuse)==32',
    '35 same-source ending meanings reused':'32 exact same-source ending meanings reused;three repunctuated variants reread',
})
if __name__=='__main__':exec(compile(source,__file__+'::three-explicit-reread-punctuation-variants-rest-exact-source','exec'),globals())
