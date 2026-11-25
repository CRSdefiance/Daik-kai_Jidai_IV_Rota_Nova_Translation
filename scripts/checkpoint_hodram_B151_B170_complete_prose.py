"""Reuse the proven atomic checkpoint writer for the complete individual comparison pass."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha

NEW_SUMMARY = ('B151–B170:all642 whole-exchange comparisons recorded,269 proposed revisions/373 justified wording retentions. '
               '640 complete four-prose-gate passes;two Abkhaz/Abhaz localization records remain open. '
               'All642 logical paragraphs pass macro/CP932/scoped-name checks;three current Japanese lines corrected inprose. '
               'Scoped names,Elysion code consumer,B156 cinematic geometry andall new formatting/visual/stored/gameplay/release gates remain. '
               'No new credit,ROM orimages;8856 completed/current7fb6f6d7/main unchanged. '
               'Full scope/all earlier evidence preserved;no guide photos.')

base=Path('scripts/checkpoint_hodram_B151_B170_prose_progress.py')
source=checked_text(base.read_text(encoding='utf-8'),{
    "Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v1.json')":"Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v2.json')",
    "Path('docs/editorial_hodram_B151_B170_prose_20261102.md')":"Path('docs/editorial_hodram_B151_B170_full_prose_20261102.md')",
    "SUMMARY = (":"UNUSED_HISTORICAL_SUMMARY = (",
    "if __name__ == '__main__':":"SUMMARY = NEW_SUMMARY\n\nif __name__ == '__main__':",
    "'source_prose_progress_checkpoint_v2.json'":"'source_prose_progress_checkpoint_v3.json'",
    "== (42,22,20,40,2)":"== (642,269,373,640,2)",
    "'ledger_before_642_drafts_42_comparisons.json.gz'":"'ledger_before_642_complete_comparisons.json.gz'",
    "current_English_conversation_comparisons=42":"current_English_conversation_comparisons=642",
    "remaining_current_English_comparisons=600,proposed_revisions=22,wording_retentions=20":"remaining_current_English_comparisons=0,proposed_revisions=269,wording_retentions=373",
    "complete_four_gate_comparisons=40":"complete_four_gate_comparisons=640",
    "contextual_comparisons=42,remaining_current_comparisons=600,proposed_revisions=22,wording_retentions=20":"contextual_comparisons=642,remaining_current_comparisons=0,proposed_revisions=269,wording_retentions=373",
    "['DK4_MES_B153_R0009','DK4_MES_B153_R0016']":"['DK4_MES_B153_R0009','DK4_MES_B153_R0016','DK4_MES_B159_R0157']",
    "Path('translations/hodram_B151_B155_contextual_decisions_v1.json'),Path(__file__)]":
    "Path('translations/hodram_B151_B170_all_contextual_decisions_v1.json'),ROOT/'complete_prose_draft_consistency_v1.json',base,Path(__file__)]",
    "print('Checkpoint:642 drafts/current bindings;42 comparisons,22 revisions/20 retentions,40 four-gate passes/two name questions. All prior credit/releases unchanged.')":
    "print('Checkpoint:642 comparisons,269 revisions/373 retentions,640 four-prose-gate passes/two name questions. All prior credit/releases unchanged.')",
})

if __name__ == '__main__':
    manuscript=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v2.json')
    doc=load(manuscript)
    assert all(r['decision'] in ['revision','retention'] and not r['current_English_comparison_pending'] for r in doc['records'])
    assert all(r['logical_English']==r['prior_macro_normalized_comparison'] for r in doc['records'] if r['decision']=='retention')
    audit=load('work/analysis/Hodram_B151_B170_clean_20261102/complete_prose_draft_consistency_v1.json')
    assert audit['manuscript_sha256']==sha(manuscript.read_bytes()) and audit['macro_counts_CP932_logical_paragraphs_andscoped_name_checks_pass']
    combined=load('translations/hodram_B151_B170_all_contextual_decisions_v1.json')
    for path,digest in combined['evidence'].items():assert sha(Path(path).read_bytes())==digest,path

exec(compile(source,__file__+'::same-atomic-writer-complete-prose-counts','exec'),globals())
