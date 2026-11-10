"""Require registered reconstruction, scoped native/actual evidence, regressions and current startup."""
from pathlib import Path
from dk4tool.patch import lil_B209_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
RELEASE=ROOT/'lil_B209_release_v6489/registered_release_verification.json'
START=ROOT/'lil_B209_startup_v6492/cold_boot_Lil_startup_town_verification.json'
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=ROOT/'lil_B209_registration_v6487/registration_receipt.json'
PIN=ROOT/'lil_B209_retention_v6490/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(owned.CONFIG);doc=read(conf['manuscript']);mapping=read(conf['reference_map']);owned.observations(doc,mapping,conf)
    assert release['all600_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6439']
    assert start['all_current_requested_and_final_framebuffers_equal_V6439'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==128 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B209_regressions_v6488/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path(conf['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==600 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
