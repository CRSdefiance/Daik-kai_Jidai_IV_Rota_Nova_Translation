"""Keep the refrain's determiner with its phrase without authored breaks or runtime changes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B198_refrain_layout_v5722')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('dk4tool/dialogue/lil_B198_layout_v1.py','dk4tool/dialogue/lil_B198_layout_v2.py',{
        'def _word(value):':"# Preserve the complete repeated call; do not strand its determiner.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('any','naughty')})\n\ndef _word(value):"})]
    rows.append(derive('scripts/plan_lil_B198_layout_v5720.py','scripts/plan_lil_B198_layout_v5722.py',{
        'lil_B198_layout_v1':'lil_B198_layout_v2','layout_v5720':'layout_v5722',
        "INPUT=Path('translations/lil_B198_editorial_manuscript_v1.json')":"INPUT=Path('translations/lil_B198_editorial_manuscript_v2.json')",
        "OUTPUT=Path('translations/lil_B198_editorial_manuscript_v2.json')":"OUTPUT=Path('translations/lil_B198_editorial_manuscript_v3.json')",
        'dk4tool/dialogue/lil_B198_layout_v1.py':'dk4tool/dialogue/lil_B198_layout_v2.py'}))
    rows.append(derive('scripts/verify_lil_B198_fonts_v5721b.py','scripts/verify_lil_B198_fonts_v5723.py',{
        'fonts_v5721b':'fonts_v5723','lil_B198_layout_v1':'lil_B198_layout_v2',
        'lil_B198_editorial_manuscript_v2.json':'lil_B198_editorial_manuscript_v3.json'}))
    prior=Path('work/analysis/lil_B198_fonts_v5721b/all17_progressive_FE_native_planes_and136_alignment_cases.json')
    assert len(read(prior)['cases'])==17
    ROOT.mkdir(parents=True)
    save(ROOT/'one_refrain_phrase_protection_and_unchanged_prose.json',dict(tools=rows,
        exact_source_indices=[10,14],refrain='Any naughty children here? Any naughty children here?',
        finding='The native preview split the second question after Any. Keep its determiner with naughty; each complete repeated question then occupies one readable row.',
        phrase_protection=['any','naughty'],no_authored_line_break_or_exact_row_override=True,
        all_words_native_metrics_width_guard_phase_bounds_pagination_and_runtime_unchanged=True,
        prior_native_proof=str(prior),prior_native_proof_sha256=sha(prior.read_bytes()),
        prior_layout_and_all_failed_producers_preserved=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared scoped any/naughty phrase protection;same prose and native metrics. Prior layout remains preserved.')
