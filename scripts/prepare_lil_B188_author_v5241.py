"""Prepare all eleven individually reasoned contextual decisions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_author_tools_v5241')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/author_lil_B187_v5197.py');text=source.read_text(encoding='utf-8')
    a=text.index('    doc.update(records=rows');b=text.index('    ROOT.mkdir',a)
    semantic="""    doc.update(records=rows,revised=4,retained=7,
        source_Daimyo130_Guildmaster150_and_original_voice0_both_preserved=True,
        source_explicit_giyaman_glass_and_unfamiliar_name_echo_preserved=True,
        praise_conjecture_personal_discovery_collection_decision_order_and_formal_compliance_distinct=True,
        my_lord_supported_by_clean_Daimyo_role_and_marked_deference_not_inferred_kinship_or_new_title=True,
        source_all14_linear_commands_A000_C200_end_and_two_tailzeros_preserved=True,
        FE_prospective_Glass_Osaka_notice_distinct_from_character_existing_fashion_claim=True,full_goal_complete=False)
"""
    row=derive(source,'scripts/author_lil_B188_v5241.py',{
        text[a:b]:semantic,'B187':'B188','lil_B187_prose_v5196':'lil_B188_prose_v5240','author_v5197':'author_v5241',
        'comparison_v5195/all16':'comparison_v5239/all11',"len(gloss['records'])==16":"len(gloss['records'])==11",
        'voices_v5189':'voices_v5233','dispatches_v5190/all16':'dispatches_v5234/all11','controls_v5192':'controls_v5236',
        'entry_v5191':'entry_v5235','names_v5193':'names_v5237',"{'revise':7,'retain-wording':9}":"{'revise':4,'retain-wording':7}",
        'all16_clean_first_contextual_decisions':'all11_clean_first_contextual_decisions','all9_retentions':'all7_retentions','all16_records':'all11_records',
        'Record all16':'Record all11','B187:16 whole-exchange decisions,7 revisions/9 justified retentions.':'B188:11 whole-exchange decisions,4 revisions/7 justified retentions.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_contextual_author.json',dict(derivation=row,no_credit_or_ROM_change=True,full_goal_complete=False))
