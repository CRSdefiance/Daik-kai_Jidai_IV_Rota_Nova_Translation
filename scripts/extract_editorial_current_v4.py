"""Bind speech alongside separately inventoried three-choice andpersonality objects."""
from scripts import extract_editorial_current_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "elif source['word'] in (0x100, 0x200, 0x300, 0x400, 0x2100):\n                assert a[:2] == b[:2]":
    """elif source['word'] in (0x100, 0x200, 0x300, 0x400, 0x2100, 0x2200, 0x4100):
                assert a[:2] == b[:2]
                if source['word']==0x4100:assert a[18:20]==b[18:20]""",
})
exec(compile(source,__file__+'::separate-variable-text-object-membership','exec'),globals())
