"""Seal the unchanged full scope using both capacity-safe complete-block QA runs."""
from pathlib import Path
from scripts import finalize_hodram_B301_B310_research_v1 as previous
from scripts.finalize_hodram_B301_B310_research_v1 import ROOT,INPUT,VIEW,REBUILT,STORED,LOOKUP,LOADERS,NATIVE,PLAN,MANUSCRIPT,NAMES,NAME_PLANES,OUT,FINAL,FINAL_NAMES,READY
from scripts.source_locked_derivation_v5118 import checked_text

LIVE=ROOT/'bounded_combined_v1/focused_actual_pixels.json'
MENU=ROOT/'bounded_combined_v1/menu_actual_pixels.json'
FIXTURE=ROOT/'bounded_combined_v1/fixture_set.json'
EXIT=ROOT/'fixture_exit_resolution_bounded_v1.json'
source=checked_text(previous.source,{
    "ROOT/'actual_menus_terminal_v4/model_qualification_reuse.json'":"ROOT/'bounded_combined_v1/model_qualification_reuse.json'",
    '(29201,96,97)':'(34162,96,97)',
    "ROOT/'actual_body_sheets_terminal_v4/receipt.json'":"ROOT/'actual_body_sheets_bounded_v1/receipt.json'",
    'total_frames=29201,initialized_fixture_runs=1':'total_frames=34162,initialized_fixture_runs=2',
    "    assert exit_proof['all_copied_commands_andbindings_exact']":
        "    assert exit_proof['qualified_runs']==2 and exit_proof['qualified_frames']==34162\n    assert exit_proof['native_stack_buffer_overflow_proven_andguarded']\n    assert exit_proof['all_copied_commands_andbindings_exact']",
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-individual-gates-full-scope-two-bounded-runs','exec'),env)

if __name__=='__main__':
    from scripts.audit_story_glyph_consistency import load,save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    model=ROOT/'bounded_combined_v1/model_qualification_reuse.json';assert not model.exists()
    prior=Path('work/Hodram_B231_B250_clean_20261107/actual_menus_band_v1/model_qualification.json')
    qualified=load(prior)
    assert digest(prior)=='1af1a246e88a9ba61a5e0dccc11987d5daaf2878cf0c7baf7d0d26edf33517c8'
    assert qualified['all6_pixel_andcursor_mutations_rejected'] and qualified['no_ROM_orcapture_mutation']
    for p,h in qualified['evidence'].items():assert digest(p)==h
    assert load(MENU)['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert load(EXIT)['following_native_dialogue_observed']
    save(model,dict(all6_pixel_andcursor_mutations_rejected=True,exact_checker_andnegative_cases_reused=True,
        prior=str(prior),prior_sha256=digest(prior),cases=qualified['cases'],no_ROM_orcapture_mutation=True,
        all_current_geometry_andcaption_pixels_freshly_checked=True,no_new_negative_case_execution=True,new_credit=0))
    env['main']()
