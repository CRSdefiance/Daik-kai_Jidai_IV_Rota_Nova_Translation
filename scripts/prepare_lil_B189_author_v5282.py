"""Prepare seventeen clean-first decisions with four independently bound source roles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_author_tools_v5282')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/author_lil_B188_v5241.py');text=source.read_text(encoding='utf-8')
    a=text.index('    doc.update(records=rows');b=text.index('    ROOT.mkdir',a)
    semantic="""    doc.update(records=rows,revised=10,retained=7,
        source_four_roles_and_eight_name_consumers_with_original_voice0_preserved=True,
        source_selectors_hex93_52_68_71_equal_decimal147_82_104_113=True,
        both_pairs_reviewed_as_one_scene_with_distinct_polite_and_casual_registers=True,
        source_recent_acquisition_value_judgments_invitation_market_claims_and_ironic_sale_boast_preserved=True,
        speakers_short_funds_not_customers_and_proposed_approach_not_second_sale=True,
        ceramics_source_collective_distinct_from_unchanged_UI_China42_and_no_Chinese_origin_invented=True,
        source_all20_linear_commands_A000_C200_end_and_two_tailzeros_preserved=True,
        FE_prospective_ceramics_Hamburg_notice_distinct_from_character_market_claims=True,full_goal_complete=False)
"""
    row=derive(source,'scripts/author_lil_B189_v5282.py',{
        text[a:b]:semantic,'B188':'B189','lil_B188_prose_v5240':'lil_B189_prose_v5281','author_v5241':'author_v5282',
        'comparison_v5239/all11':'comparison_v5280/all17',"len(gloss['records'])==11":"len(gloss['records'])==17",
        'voices_v5233/current207_catalog_eight_voices_and_two_source_selectors':'voices_v5274b/current207_catalog_eight_voices_and_four_source_selectors',
        'dispatches_v5234/all11':'dispatches_v5275b/all17','controls_v5236':'controls_v5277b','entry_v5235':'entry_v5276b',
        'names_v5237/four_original':'names_v5278b/eight_original',"{'revise':4,'retain-wording':7}":"{'revise':10,'retain-wording':7}",
        'all11_clean_first_contextual_decisions':'all17_clean_first_contextual_decisions','all11_records':'all17_records','Record all11':'Record all17',
        'B188:11 whole-exchange decisions,4 revisions/7 justified retentions.':'B189:17 whole-exchange decisions,10 revisions/7 justified retentions.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_contextual_author.json',dict(derivation=row,no_credit_or_ROM_change=True,full_goal_complete=False))
