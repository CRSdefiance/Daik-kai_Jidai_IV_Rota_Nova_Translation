"""Finish the source-first refinement, retaining the one panting variant already correct."""
from pathlib import Path
from scripts import refine_hodram_B301_B310_clean_drafts_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
    'assert not MEANINGS.exists() and not OUT.exists()':'assert MEANINGS.exists() and not OUT.exists()',
    'save(MEANINGS,meanings)':'assert load(MEANINGS)==meanings',
    "before=row['english'];assert before!=text":"before=row['english']\n        if before==text:return",
    'assert len(findings)==11':'assert len(findings)==10',
    'source_first_refined_records=11':'source_first_refined_records=10',
    "ROOT/'source_first_refinement_v2.json'":"ROOT/'source_first_refinement_v3.json'",
    'prose_refinements=11,':
        "prose_refinements=10,already_correct_panting_variant_retained='SC1_B309_STYLE_2364_268',\n        retention_reason='The existing youthful two-breath pant and safety question already equal the reviewed refinement.',\n        previous_attempt_stopped_before_saving_drafts_at_identical_prose_assertion=True,",
    'Refined11 logical drafts':'Refined10 logical drafts; retained one already-correct panting variant',
})
env={**vars(previous),'__file__':__file__,'__name__':'source_first_refinement_recovery'}
exec(compile(source,__file__+'::same-refinement-preserve-sealed-meaning-and-valid-identical-prose','exec'),env)
if __name__=='__main__':env['main']()
