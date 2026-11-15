"""Require exact cumulative reconstruction, honest evidence scope and current representative checks."""
from pathlib import Path
from dk4tool.patch import lil_B210_editorial_v1 as story,Al_Ferid_name_release_v1 as name
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis');RELEASE=ROOT/'B210_Ferid_release_v6542/registered_release_verification.json';START=ROOT/'B210_Ferid_startup_v6544/cold_boot_Lil_startup_town_verification.json';VIEW=START.parent/'current_six_frame_visual_review.json';REG=ROOT/'B210_Ferid_registration_v6540/registration_receipt.json';PIN=ROOT/'B210_Ferid_retention_v6542/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(story.CONFIG);doc=read(conf['manuscript']);story.observations(doc,read(conf['reference_map']),conf)
    assert release['all602_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_component_graphic_route_font_and_code_exact_to_V6488'] and release['only_five_owned_name_data_bytes_changed']
    assert start['all_current_requested_and_final_framebuffers_equal_V6488'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes()) and reg['negative_counts']==[117,69] and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'B210_Ferid_regressions_v6541/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    assert release['ARM9_sha256']==name.TARGET;registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==602 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for module in [story,name]:
        for p,h in read(module.CONFIG)['dependencies'].items():assert sha(Path(p).read_bytes())==h
    return release
