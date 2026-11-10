"""Preserve fourteen real independent-guard gaps; source-lock the corrected atomic compiler."""
from copy import deepcopy
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B45_production_guard_tools_v7907')
CONFIG=Path('translations/rafael_B45_editorial_release_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    report=read('work/analysis/Rafael_B45_atomic_challenges_v7906/challenge_report.json')
    assert report['planned_cases']==131 and report['guard_rejections']==117 and len(report['gaps'])==14 and not report['ready_for_registration']
    assert report['all_physical_inputs_ROM_registry_ledger_policy_andpins_unchanged']
    result=derive('dk4tool/patch/rafael_B45_editorial_v1.py','dk4tool/patch/rafael_B45_editorial_v2.py',{
        "CONFIG='translations/rafael_B45_editorial_release_v1.json'":"CONFIG='translations/rafael_B45_editorial_release_v2.json'",
        "    expected_names={r['actor_ID']:r['name'] for r in names['records']}":"""    wanted_ids={r['id'] for r in rows}
    require(len(sourcefont['source_records'])==12 and {r['id'] for r in sourcefont['source_records']}==wanted_ids and len({r['id'] for r in sourcefont['source_records']})==12,'complete unique independent source font records')
    require(len(native['records'])==12 and {r['id'] for r in native['records']}==wanted_ids and len({r['id'] for r in native['records']})==12,'complete unique native font records')
    expected_names={r['actor_ID']:r['name'] for r in names['records']}""",
        "            require(before['source']['instruction_offset']==after['source']['instruction_offset']==at and before['source']['first_word']==word==pair['word'],'actual command source offset/opcode')":"""            require(before['source']['instruction_offset']==after['source']['instruction_offset']==at and before['source']['first_word']==word==pair['word'],'actual command source offset/opcode')
            for observed in [before,after]:
                resident=observed['source']
                require(resident['classification']=='original_SC_cache' and resident['route']==0 and resident['block']==44,'actual original cache route/block identity')
                require(resident['actual_sha256']==resident['registered_sha256']==fixture['fixture_block_sha256'] and resident['payload_bytes']==fixture['fixture_stored_bytes'],'exact actual resident fixture identity')
                require(resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256'],'actual complete resident payload andentry offset')""",
        "    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'complete natural-dialogue-v2 approval')":"""    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'complete natural-dialogue-v2 approval')
    require(doc['file_path']==PATHS[0] and doc['route']==0 and doc['route_identity']=='Rafael' and doc['block']==45,'complete source document route/file/block identity')
    require(doc['current_ROM']==conf['parent_ROM']==packet['current_ROM'] and doc['current_ROM_sha256']==conf['parent_ROM_sha256']==packet['current_ROM_sha256'],'complete source document parent identity')
    require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'complete source document runtime identity')
    require(doc['complete_clean_glosses_precede_current_comparison'] is True,'clean glosses before current comparison')
    header_group=mapping['groups'][0];header_packet=packet['groups'][0]
    current_header=IlnkContainer.parse(image.read_file(PATHS[0])).blocks[45][:8].hex()
    require(header_group['source_header_hex']==header_packet['current_header_hex']==current_header,'complete predecessor header metadata')
    require(header_group['approved_manuscript_sha256']==doc['native_approved_manuscript_sha256']==sha(Path(doc['native_approved_manuscript']).read_bytes()),'approved manuscript map lineage')""",
    })
    oldpath=Path('translations/rafael_B45_editorial_release_v1.json');conf=deepcopy(read(oldpath))
    conf['dependencies'][str(oldpath)]=sha(oldpath.read_bytes())
    for path in [Path('dk4tool/patch/rafael_B45_editorial_v2.py'),Path(__file__),
        Path('work/analysis/Rafael_B45_atomic_challenges_v7906/challenge_report.json'),
        Path('work/analysis/Rafael_B45_atomic_challenges_v7906/non_rejection_gaps.json')]:
        conf['dependencies'][str(path)]=sha(path.read_bytes())
    conf['preserved_v1_guard_gap_report']='work/analysis/Rafael_B45_atomic_challenges_v7906/challenge_report.json'
    save(CONFIG,conf)
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivation=result,
        preserved_v1_positive_andall131_actual_changing_challenges=True,
        v1_independent_guard_rejections=117,v1_real_gaps=14,all_v1_commit_attempts_trapped_before_mutation=True,
        explicit_root_source_runtime_header_lineage_unique_font_andactual_trace_identity_guards_added=True,
        all_original_native_high_constants_reconstruction_controls_QA_andatomic_commit_order_preserved=True,
        no_prose_ROM_font_source_commands_orcontroller_change=True,
        config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),new_credit=0,full_goal_complete=False))
    print('Production v2 adds independent checks for all14 observed gaps. V1 positives/failures preserved;v2 positive andall131 negative cases must pass before registration.')
