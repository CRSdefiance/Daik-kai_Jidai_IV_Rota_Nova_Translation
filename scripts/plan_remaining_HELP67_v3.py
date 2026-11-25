"""Refine only the observed sparse phrase tails; preserve every word and existing page allocation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

previous=Path('scripts/plan_remaining_HELP67_v1.py')
source=checked_text(previous.read_text(encoding='utf-8'),{
    'from dk4tool.dialogue.reviewed_help_pages_v13 import plan_articles':'from dk4tool.dialogue.reviewed_help_pages_v16 import plan_articles',
    "ROOT=Path('work/analysis/Remaining_HELP67_formatting_20261105')":"ROOT=Path('work/analysis/Remaining_HELP67_formatting_20261105/refined_v3')",
    'whole_article_comparisons_v1.json':'whole_article_comparisons_v2.json',
    "    ROOT.mkdir();manuscript=ROOT/'formatting_input_v1.json'":"    ROOT.mkdir(parents=True);manuscript=ROOT/'formatting_input_v1.json'",
    "Path('dk4tool/dialogue/reviewed_help_pages_v13.py')":"Path('dk4tool/dialogue/reviewed_help_pages_v16.py')",
})
if __name__=='__main__':exec(compile(source,str(previous)+'::same-source-locked-planner-refined-phrase-tails','exec'),globals())
