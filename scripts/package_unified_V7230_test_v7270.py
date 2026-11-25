"""Package the latest fully registered ROM for the user's promotion andtesting."""
import json,os
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B225_completion_gates_v7236 import gates
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/unified_V7230_test_package_v7270');DEST=Path('out/Translation_DS_Unified_V7230_Test');STEM='Translation_DS_Unified_V7230_Test'
if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists();release=gates();verified=read('work/analysis/editorial_handoff_verification_v7237/verified_handoff.json');ledger=Path('translations/editorial_review_current_v1.json');assert sha(ledger.read_bytes())==verified['ledger_sha256'] and release['candidate_sha256']==verified['candidate_sha256']
    source=Path(release['candidate']);patch=Path(release['patch']);manifest=Path(release['manifest']);assert release['profile']=='all-routes-unified-v7230' and release['whole_ROM_reconstruction_byte_exact'] and sha(source.read_bytes())==release['candidate_sha256'] and sha(patch.read_bytes())==release['patch_sha256']
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);rom=DEST/(STEM+'.nds');delta=DEST/(STEM+'.xdelta');mf=DEST/(STEM+'.manifest.json')
    for before,after in [(source,rom),(patch,delta),(manifest,mf)]:copy2(before,after);assert before.read_bytes()==after.read_bytes()
    summary=dict(profile=release['profile'],ROM=str(rom.resolve()),ROM_sha256=sha(rom.read_bytes()),patch=str(delta.resolve()),patch_sha256=sha(delta.read_bytes()),original_registered_ROM=str(source),original_registered_manifest=str(manifest),manifest=str(mf.resolve()),manifest_sha256=sha(mf.read_bytes()),clean_input_sha256=release['clean_input_sha256'],exact_clean_input_reconstruction_verified=True,registered_batches=618,accepted_layers=114,registered_release_checks=18,regressions_passed=110,latest_integrated_scene='Lil SC2 B225',B226_twenty_reviewed_speeches_sealed_but_not_in_this_test_ROM=True,actual_validation_scope='Targeted automated emulator tests: current NewGame4001 and inherited town17401 cold boots,31 whole-frame comparisons andfive actor/captain controls;source/English B225 initialized scene capture separately verified. Not an exhaustive route orhardware test.',editorial_completed=6680,source_prose_reviewed=6683,full_editorial_names_andretrospective_wrapping_goal_active=True,main_promotion_unchanged='all-routes-unified-v4701',preserve_every_prior_ROM_translation_proof_andfailure=True)
    save(DEST/'validation_summary.json',summary)
    notes=f'''# Translation DS — unified test build V7230

Use `{rom.name}` directly in your emulator or supported DS setup. This is the latest fully integrated, registered cumulative ROM, ready for your testing and promotion decision.

It combines all 618 registered batches and 114 accepted layers, including the completed dialogue, name-label and wrapping work through Lil's B225 scene. All 18 release checks and 110 regression tests pass. The accompanying patch reconstructs this exact ROM from the required clean input.

## Files

- `{rom.name}` — complete unified test ROM.
- `{delta.name}` — optional clean-input xdelta patch.
- `{mf.name}` — original registered build manifest.
- `validation_summary.json` — package hashes and validation scope.

ROM SHA256: `{summary['ROM_sha256']}`

Patch SHA256: `{summary['patch_sha256']}`

Required clean-input SHA256 for the patch: `{summary['clean_input_sha256']}`

## Coverage and remaining work

Current-build validation includes targeted automated New Game and town cold boots, 31 whole-frame comparisons and five actor/captain controls. The latest integrated dialogue batch also has complete native display and initialized source/English scene checks. These are targeted tests, not complete route playthroughs or hardware verification.

The full editorial review remains active across every storyline, earlier dialogue, shops/towns, random scenes, Help, names/roles/aliases and earlier line breaks. B226's 20 speeches have been reviewed and captured, but their registered integration is still pending, so this version contains their preceding translation. Separate graphics work and the later older-record technical re-audit remain open.

This package does not change the promoted main build (V4701), overwrite an earlier ROM or alter your saves. Keep your usual save backups when testing a new build.
'''
    (DEST/'README.md').write_text(notes,encoding='utf-8');(DEST/'SHA256SUMS.txt').write_text('\n'.join(sha(p.read_bytes())+'  '+p.name for p in [rom,delta,mf,DEST/'validation_summary.json',DEST/'README.md'])+'\n',encoding='utf-8')
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);assert not any(Path(v['path']).resolve()==rom.resolve() for v in values);added=dict(path=str(rom.resolve()),reason='User-requested unified V7230 test/promote package;byte-identical to verified registered cumulative ROM. Preserve every ROM. SHA256 '+summary['ROM_sha256']);encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'package_receipt.json',dict(package=str(DEST.resolve()),files={str(p.resolve()):sha(p.read_bytes()) for p in DEST.iterdir() if p.is_file()},registered_ROM=str(source),registered_ROM_sha256=release['candidate_sha256'],all_package_binary_files_byte_identical_to_verified_release=True,all_prior_pins_ROMs_andtranslations_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),main_promotion_unchanged='all-routes-unified-v4701',no_editorial_credit_added=True,ledger_sha256=sha(ledger.read_bytes()),B226_registered_integration_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(package=str(DEST.resolve()),ROM_sha256=summary['ROM_sha256'],patch_sha256=summary['patch_sha256'],ready_for_user_testing_andpromotion=True))
