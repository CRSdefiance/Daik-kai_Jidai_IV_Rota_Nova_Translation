"""Reuse all exact-reference, individual-decision and no-credit guards for Maria330."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/maria328_contextual_writer_v1.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria328_clean_v1 import ROOT, key':'from scripts.meaning_maria330_clean_v1 import ROOT, key',
    'all328_independent_drafts_v1.json':'all330_independent_drafts_v1.json',
    "len(drafts['records']) == 328":"len(drafts['records']) == 330",
})
exec(compile(source,__file__+'::same-source-current-proposal-individual-gates-andzero-credit-guards330','exec'),globals())
