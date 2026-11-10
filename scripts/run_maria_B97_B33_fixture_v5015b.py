"""Cold-boot two explicit B33-entry content fixtures; no event97 eligibility claim."""
import argparse
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['clean_Japanese','reviewed_English'],required=True);args=parser.parse_args()
    fixturepath=Path('work/analysis/maria_B97_fixture_v5014/B97_reversible_relocation_and_B33_content_fixture.json');fixture=read(fixturepath)
    selected=next(r for r in fixture['fixtures'] if r['case']==args.case)
    ROM=Path(selected['research_ROM']);assert sha(ROM.read_bytes())==selected['research_ROM_sha256']
    prior=Path('scripts/run_maria_opening_context_v2035.py');text=prior.read_text(encoding='utf-8')
    root='work/analysis/maria_B97_B33_fixture_run_v5015b_'+args.case
    cap='E:/Rota Nova translations/Generated/work/emulation_v193/maria_B97_B33_fixture_v5015b_'+args.case
    substitutions=[
        ("ROOT=Path('work/analysis/maria_opening_context_v2035')",'ROOT=Path('+repr(root)+')'),
        ("CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030')",'CAP=Path('+repr(cap)+')'),
        ("ROM=Path('out/all_routes_combined_v2030_candidate.nds')",'ROM=Path('+repr(str(ROM))+')'),
        ("assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']",'assert digest=='+repr(selected['research_ROM_sha256'])),
        ("Ordinary Maria NewGame/opening and practical town visits;existing isolated system unlock,not earned. No story/location/RNG/funds/outcome fixture.",
         'B97 '+args.case+' content substituted in B33 NewGame slot on full V4987. Existing isolated system unlock is not earned. No source event97 eligibility or earned progression claim; initialized Maria3 actor/UI context comes from ordinary NewGame.'),
        ("journal.write_text('',encoding='utf-8')","journal.write_text('{\"stop\":true}\\n',encoding='utf-8')"),
        ('no_savestate_or_story_location_RNG_funds_outcome_fixture=True','no_savestate_or_location_RNG_funds_outcome_RAM_fixture=True,B97_content_in_B33_entry_ROM_fixture=True,source_event97_not_selected=True'),
        ("runner_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False", "runner_sha256=sha(Path(__file__).read_bytes()),fixture_scope_manifest="+repr(str(fixturepath))+",fixture_scope_manifest_sha256="+repr(sha(fixturepath.read_bytes()))+",runner_template_sha256="+repr(sha(prior.read_bytes()))+",full_goal_complete=False")]
    for old,new in substitutions:assert old in text,old;text=text.replace(old,new)
    assert "'--capture-every','999999'" in text and "'--dump-capture-ram'," in text
    text=text.replace("'--capture-every','999999'","'--capture-every','60'").replace("'--dump-capture-ram',",'')
    exec(compile(text,str(prior)+'::explicit-B97-B33-fixture','exec'),{'__name__':'__main__','__file__':__file__})
