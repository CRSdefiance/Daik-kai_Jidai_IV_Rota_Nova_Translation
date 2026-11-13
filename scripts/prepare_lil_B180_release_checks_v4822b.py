"""Prepare exact patch verification and current-font startup comparisons."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_release_tools_v4822')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/verify_lil_B179_release_v4750.py').read_text(encoding='utf-8')
    a=old.index("    builder=Path('scripts/build_integrated_release.py')");b=old.index("    clean=Path('work/clean.nds')",a)
    hook='''    builder=Path('scripts/build_integrated_release.py').read_bytes()
    start=builder.index(b"    lil_proof = profile_config.get('lil_B180_editorial')")
    finish=builder.index(b'    # Lexically valid',start);added=builder[start:finish]
    assert builder.count(added)==1 and b'from dk4tool.patch.lil_B180_editorial_v4 import' in added
    assert builder.replace(added,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
'''
    tools=[derive('scripts/verify_lil_B179_release_v4750.py','scripts/verify_lil_B180_release_v4822.py',{
        old[a:b]:hook,'B179':'B180','lil_B179_editorial_v1':'lil_B180_editorial_v4',
        'release_v4750':'release_v4822','combined_v4749':'combined_v4821','combined_v4701':'combined_v4766',
        'registration_v4748':'registration_v4820d','build_v4749':'build_v4821',
        "manifest['profile']=='all-routes-unified-v4749'":"manifest['profile']=='all-routes-unified-v4821'",
        "registry['profiles']['all-routes-unified-v4701']":"registry['profiles']['all-routes-unified-v4766']",
        "len(manifest['batches'])==555":"len(manifest['batches'])==562",'all555':'all562','manifest_batches=555':'manifest_batches=562',
        'exact_to_V4701':'exact_to_V4766','out/lil_B179_reference_v4734_RESEARCH_ONLY.nds':'out/lil_B180_reference_v4801_RESEARCH_ONLY.nds',
        'lil_B179_editorial':'lil_B180_editorial'})]
    tools.append(derive('scripts/run_lil_B179_startup_v4751.py','scripts/run_lil_B180_startup_v4823.py',{
        'B179':'B180','runs_v4751':'runs_v4823','v4751_':'v4823_','version=4749':'version=4821'}))
    tools.append(derive('scripts/run_lil_B179_startup_v4751.py','scripts/run_lil_B180_parent_town_v4823.py',{
        'B179':'B180','runs_v4751':'parent_runs_v4823','v4751_':'parent_v4823_','version=4749':'version=4766',
        "choices=['newgame','town']":"choices=['town']"}))
    tools.append(derive('scripts/verify_lil_B179_startup_v4752.py','scripts/verify_lil_B180_startup_v4824.py',{
        'B179':'B180','startup_v4752':'startup_v4824','runs_v4751':'runs_v4823',
        'combined_v4749':'combined_v4821','combined_v4701':'combined_v4766',
        "oldtp=Path('work/analysis/lil_B178_runs_v4703')/(case+'_terminal.json')":
        "oldtp=(Path('work/analysis/shop657_startup_v4769') if case=='newgame' else Path('work/analysis/lil_B180_parent_runs_v4823'))/(case+'_terminal.json')",
        'V4701':'V4766','Current4749':'Current4821'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_checks.json',dict(tools=tools,
        newgame_control_reuses_exact_current_font_V4766_capture=True,
        new_parent_town_control_needed_for_fresh_current_font_Refit_comparison=True,
        parent_control_is_full_registered_V4766_not_a_research_fixture=True,full_goal_complete=False))
    print('Prepared full cumulative patch checks and exact-current-font startup controls.')
