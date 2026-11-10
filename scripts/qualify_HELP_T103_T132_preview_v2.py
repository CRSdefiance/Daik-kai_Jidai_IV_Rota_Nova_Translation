"""Correct the no-op negative fixture without changing the reviewed30 pages or original failed producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/qualify_HELP_T103_T132_preview.py').read_text(encoding='utf-8'),{
    ".replace('[[126|Deck]]','[[127|Deck]]')":".replace('[[126|','[[127|')",
    "        try:plan_articles(changed,*args,require_formatting=False)":
        "        assert changed!=doc,'Negative fixture must change the selected input'\n        try:plan_articles(changed,*args,require_formatting=False)",
})
exec(compile(source,__file__+'::same-source-native-visual-contract-with-an-effective-link-ID-negative-fixture','exec'),globals())
