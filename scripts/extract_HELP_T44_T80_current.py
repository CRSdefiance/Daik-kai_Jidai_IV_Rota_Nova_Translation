"""Bind37 current Help bodies only after the clean whole-article drafts aresealed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/extract_HELP_T21_T43_current.py').read_text(encoding='utf-8'),{
    'Shared_HELP_T21_T43_clean_20261104':'Shared_HELP_T44_T80_clean_20261104',
    'clean_meanings_andfull_drafts_v2.json':'clean_meanings_andfull_drafts_v1.json',
    "len(draft['records'])==23 and draft['prior_producer_English_exposure_disclosed_topic_IDs']==[21,23]":
        "len(draft['records'])==37 and draft['fresh_drafts_precede_current_full_body_packet'] and draft['no_blanket_claim_of_no_prior_English_exposure']",
    'Rafael_B61_B80_release_verified_20261104':'Early_HELP23_release_verified_20261104',
    'len(blocks)==211':'len(blocks)==212',
    "sha(archive)=='015ee6aaab9544555a2bcd90f74dbd10450ca20e441954cf5b99f8196e275cc0'":"sha(archive)==release['target_HELP_sha256']",
    '[117,118,119,121,142,150,151,152,157,187,194,201]':'[110,113,120,123,127,139,150,184]',
    'current_topic_count=211':'current_topic_count=212',
    'no_wholly_unconsulted_old_English_claim_for21_and23=True':'prior_UI_term_exposure_disclosed_no_blanket_unconsulted_claim=True',
    "    for row in rows:print('\\nTOPIC',row['topic_id'],row['current_English_with_link_IDs'])":
        "    for row in rows:\n        if row['topic_id']<=62:print('\\nTOPIC',row['topic_id'],row['current_English_with_link_IDs'])",
})
exec(compile(source,__file__+'::same-exact-reference-extraction-after-sealed-clean-drafts-37-topics','exec'),globals())
