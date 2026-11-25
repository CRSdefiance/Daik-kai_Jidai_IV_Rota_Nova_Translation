"""Keep exact individual source/current/decision guards for335 original objects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/maria328_contextual_writer_v1.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria328_clean_v1 import ROOT, key':'from scripts.meaning_maria335_B137_B151_v1 import ROOT, key',
    'all328_independent_drafts_v1.json':'all335_independent_drafts_v3.json',
    "len(drafts['records']) == 328":"len(drafts['records']) == 335",
    "original['independent_English_draft']":"original['english']",
})
exec(compile(source,__file__+'::same-individual-source-current-decision-macro-andzero-credit-contract','exec'),globals())
