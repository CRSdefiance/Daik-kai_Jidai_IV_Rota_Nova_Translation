"""Record native integration and startup without claiming ceremony completion."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_ceremony_common_v809 import ROOT
from scripts.ceremony_runtime_v808 import ROOT as RUNTIME_ROOT
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
ROM=Path('out/all_routes_combined_v809_candidate.nds')
DOC=Path('docs/ceremony_integration_v809_checkpoint.md')
SUMMARY=('V809 registers51 ceremony paragraphs after the full V803 stack. All3617 other COMMON strings,opaque payloads,470 batches,114 accepted layers and earlier routes/graphics are exact. V808 fits the new runtime in existing384-byte banks and128-byte modal wrapper:35704 selector/ABI,140 whole8MiB status,2326 literal-equivalence,3668 modal-ID and231 wrong-parent controls pass.201 stored-template layouts/complete fonts and7336 complete warm/cold copies pass;clean-input patch reconstructs exactly and seven ordinary cold-boot/New Game frames match. A6000-frame isolated calendar-fixture town-menu exploration does not activate a ceremony and gets no scene/effect/transition credit. Original historic-site access mapping and actual ceremony samples remain next. V803 stays the last gameplay-verified reference;continue from the registered V809 stack.550 complete/605 source-prose/55 pending unchanged;full editorial and separate graphics audits remain active.')


def main():
    proof=read(ROOT/'registered_verification.json');startup=read(ROOT/'newgame_regression.json')
    assert proof['candidate_sha256']==startup['candidate_sha256']==sha(ROM.read_bytes())
    assert proof['candidate_sha256']=='4b85eae04e1f1654022433c2a9a2aafd8b719daf10cc5f2120a32f9781728ae2'
    assert startup['all_pixels_exact'] and len(startup['whole_screen_frame_pairs'])==7
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/ceremony_v809_probe_interactive/capture_report.json')
    report=read(cap)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames']==6000 and report['ROM_sha256']==proof['candidate_sha256']
    fixtures=report['synthetic_condition_fixtures'];assert len(fixtures)==1
    assert fixtures[0]['day']==24 and fixtures[0]['all_other4MiB_bytes_including_code_speaker_dialogue_selection_menu_outcome_and_inventory_exact']
    protected=Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
    assert sha(protected.read_bytes())=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    harness=Path('scripts/headless_desmume_v193.py')
    assert sha(harness.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    proof.update(ordinary_cold_boot_regression=str(ROOT/'newgame_regression.json'),
        all_seven_ordinary_cold_boot_frames_exact=True,
        calibration_only_town_menu_navigation=str(cap),
        calibration_run_complete_not_revised_ceremony_gameplay=True,
        no_ceremony_scene_effect_or_transition_approval=True,
        original_donor_and_frozen_harness_hashes_preserved=True)
    save(ROOT/'registered_verification.json',proof);save(ROM.with_suffix('.verification.json'),proof)
    ledger=read(LEDGER);assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['records_editorially_completed']==550 and ledger['records_with_source_and_prose_pass']==605
    assert ledger['current_integrated_candidate']['sha256']=='7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad'
    before=ROOT/'editorial_ledger_before_v809_checkpoint.json'
    if not before.exists():shutil.copyfile(LEDGER,before)
    ledger['pending_registered_ceremony_candidate']=dict(path=str(ROM),sha256=proof['candidate_sha256'],
        profile='all-routes-unified-v809',manifest=str(ROM.with_suffix('.manifest.json')),
        verification=str(ROM.with_suffix('.verification.json')),patch=proof['patch'],patch_sha256=proof['patch_sha256'],
        ARM9_sha256=proof['ARM9_sha256'],MESFILE_sha256=proof['COMMON_sha256'],
        manuscript='translations/ceremony_editorial_manuscript_v3.json',
        complete_native_relocation_map=str(ROOT/'complete_current_message_map_v809.json'),
        status='registered-native-patch-and-startup-verified;actual-ceremony-scenes-pending',documentation=str(DOC),
        new_editorial_completion_credit=0,full_goal_complete=False)
    ledger['next_integrated_profile_for_goal_continuation']='all-routes-unified-v809'
    ledger['next_ceremony_source_packet'].update(production_manuscript='translations/ceremony_editorial_manuscript_v3.json',
        runtime_verification=str(RUNTIME_ROOT/'native_runtime_verification.json'),
        production_layouts=str(ROOT/'production_layout.json'),registered_candidate=str(ROM),
        registered_verification=str(ROOT/'registered_verification.json'),
        status='registered-native-copies-patch-and-startup-verified;actual-ceremony-scenes-pending',
        completion_credit=0,next='Map original historic-site access eligibility,then actual complete ceremony scenes/effects/normal returns. Shared64 retains its original presentation.')
    ledger['active_source_prose_drafts']['production_manuscripts']=['translations/ceremony_editorial_manuscript_v3.json']
    ledger['active_source_prose_drafts']['status']='750-752-context-unmapped;ceremony52-integrated-native-verified-actual-scenes-pending'
    ledger['latest_checkpoint']=SUMMARY
    for version,doc in (('V808','docs/ceremony_runtime_v808_checkpoint.md'),('V809',str(DOC))):
        id=version+'-ceremony-runtime-or-integration'
        if not any(r['id']==id for r in ledger['research_checkpoints']):
            ledger['research_checkpoints'].append(dict(id=id,documentation=doc,new_source_prose_reviewed=0,
                new_editorially_completed=0,new_ROM=version=='V809',full_goal_complete=False))
    save(LEDGER,ledger)
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        p=Path('docs')/name;s=p.read_text(encoding='utf-8');heading='## V809: ceremony integration; actual scenes pending'
        if heading not in s:p.write_text(s+'\n\n'+heading+'\n\n'+SUMMARY+' See [V808 runtime](ceremony_runtime_v808_checkpoint.md) and [V809 integration](ceremony_integration_v809_checkpoint.md).\n',encoding='utf-8')
    archive=Path('E:/Rota Nova translations/Editorial review/V809 Ceremony integration');archive.mkdir(parents=True,exist_ok=True)
    files=[DOC,Path('docs/ceremony_runtime_v808_checkpoint.md'),LEDGER,
        Path('translations/ceremony_editorial_manuscript_v3.json'),Path('translations/ceremony_editorial_release_v1.json'),
        ROM.with_suffix('.manifest.json'),ROM.with_suffix('.verification.json'),
        *(Path('scripts')/n for n in ('ceremony_runtime_v808.py','verify_ceremony_runtime_v808.py','verify_ceremony_consumers_v808.py',
            'prepare_ceremony_common_v809.py','verify_ceremony_copies_v809.py','verify_ceremony_production_v809.py',
            'register_ceremony_release_v809.py','verify_ceremony_release_v809.py','native_ceremony_fixture_v809.py',
            'run_ceremony_capture_v809.py','record_ceremony_integration_v809.py')),
        Path('dk4tool/patch/ceremony_editorial.py')]
    artifacts=[]
    for sub,paths in (('final',files),('runtime',list(RUNTIME_ROOT.glob('*.json'))),('integration',list(ROOT.glob('*.json')))):
        dest=archive/sub;dest.mkdir(exist_ok=True)
        for p in paths:
            q=dest/p.name;shutil.copyfile(p,q);assert sha(p.read_bytes())==sha(q.read_bytes())
            artifacts.append(dict(source=str(p),archived=str(q),sha256=sha(q.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,registered_ROM=str(ROM.resolve()),
        ROM_sha256=proof['candidate_sha256'],exact_patch=str(Path(proof['patch']).resolve()),
        actual_ceremony_or_guide_screenshot_approval=False))
    print(f'V809 recorded and{len(artifacts)} metadata/source artifacts archived on E.550 complete;605 source/prose;55 pending. Actual ceremony scenes remain;no emulator process live.',flush=True)


if __name__=='__main__':main()
