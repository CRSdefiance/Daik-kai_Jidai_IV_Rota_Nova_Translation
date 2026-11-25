"""Prepare the nine-record author receipt; preserve the executed comparison."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B184_author_tools_v5048')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/author_lil_B183_v4934.py','scripts/author_lil_B184_v5048.py',{
        'all25':'all9','All25':'All9','B183':'B184','prose_v4933':'prose_v5047','author_v4934':'author_v5048',
        'comparison_v4932':'comparison_v5046','len(gloss[\'records\'])==25':"len(gloss['records'])==9",
        'voices_v4926':'voices_v5040','current207_catalog_eight_voices_and_five_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors',
        'dispatches_v4927':'dispatches_v5041','controls_v4929':'controls_v5043','entry_v4928':'entry_v5042',
        'names_v4930':'names_v5044','ten_original_progressive_and_catalogue_name_consumers':'four_original_progressive_and_catalogue_name_consumers',
        "('Impersonal impact sound' if index==53 else 'Impersonal fashion notice')":"'Impersonal fashion notice'",
        "{'revise':16,'retain-wording':9}":"{'revise':4,'retain-wording':5}",
        'revised=16,retained=9':'revised=4,retained=5',
        'five_source_roles_and_separate_Sailor_Retainer_catalogue_binding_preserved':'two_clean_couple_roles_without_marriage_age_or_kinship_inference',
        'private_shopkeeper_candor_and_collectors_competing_judgments_preserved':'household_request_and_willing_future_errand_with_personal_enjoyment_preserved',
        'FE_sound_and_prospective_Artwork_Basra_notice_distinct':'FE_prospective_Tea_Sofala_notice_distinct_from_household_supply',
        'source_all28_linear_commands_A000_C200_and_end_preserved':'source_all12_linear_commands_A000_C200_and_end_preserved',
        'all9_retentions_individually_justified':'all5_retentions_individually_justified',
        '25 whole-exchange decisions,16 revisions/9 justified retentions':'9 whole-exchange decisions,4 revisions/5 justified retentions'})
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_author_and_comparison_provenance.json',dict(author=tool,
        comparison_producer='scripts/compare_lil_B184_English_v5046.py',
        comparison_producer_sha256=sha(Path('scripts/compare_lil_B184_English_v5046.py').read_bytes()),
        comparison_producer_parent='scripts/compare_lil_B183_English_v4932.py',
        comparison_parent_sha256=sha(Path('scripts/compare_lil_B183_English_v4932.py').read_bytes()),
        earlier_inline_provenance_save_failed_missing_parent_but_comparison_completed=True,
        comparison_not_rerun_or_overwritten=True,new_review_credit=0,full_goal_complete=False))
