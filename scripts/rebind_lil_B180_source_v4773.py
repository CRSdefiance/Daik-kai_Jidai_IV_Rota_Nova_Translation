"""Rebind the complete B180 source packet to the verified current cumulative ROM."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_source_v4773')
PRIOR=Path('work/analysis/lil_B180_source_v4758/all11_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists()
    audit=read('work/analysis/shop657_checkpoint_v4771/post_apply_audit.json')
    assert audit['all_original_root_and_nested_ledger_history_preserved']
    ledger=read('translations/editorial_review_current_v1.json');current=ledger['current_integrated_candidate']
    packet=read(PRIOR);old,image=NdsImage.open(packet['current_ROM']),NdsImage.open(current['path'])
    assert sha(Path(current['path']).read_bytes())==current['sha256']=='c3a9a133f7d149995a5d0feae824da32bc6741603f023ba7cda1cefb79ff4503'
    for p in ['/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert old.read_file(p)==image.read_file(p)
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=image.read_file('/__arm9__.bin')
    for span in packet['source_exact_spans']:
        a,b=span['start'],span['end'];assert sha(arm[a:b])==span['sha256'] and arm[a:b]==original[a:b]
    terminal=read('work/analysis/shop657_startup_v4769/newgame_terminal.json');report=read(terminal['report'])
    assert terminal['terminal'] and report['ROM_sha256']==current['sha256'] and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    snapshot=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000)
    assert snapshot['read_only_export'] and sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    rebound=deepcopy(packet)
    rebound.update(previous_current_source_packet=str(PRIOR),previous_current_source_packet_sha256=sha(PRIOR.read_bytes()),
        previous_current_ROM=packet['current_ROM'],previous_current_ROM_sha256=packet['current_ROM_sha256'],
        current_ROM=current['path'],current_ROM_sha256=current['sha256'],current_ARM9_sha256=sha(arm),
        current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        current_actual_context_capture_report=terminal['report'],current_actual_context_report_sha256=sha(Path(terminal['report']).read_bytes()),
        current_actual_context_snapshot=snapshot,context_is_current_Lil_opening_not_B180_activation=True,
        all11_source_current_speech_hex_preambles_and28_commands_exact_to_prior_packet=True,
        same_all_four_story_files_and_EV2_proved=True,prior_native_pixel_approvals_not_inherited_for_new_font=True,
        current_native_context_roles_voices_dispatch_and_names_need_fresh_binding=True,
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,
        source_packet_rebind_evidence={str(PRIOR):sha(PRIOR.read_bytes()),'translations/editorial_review_current_v1.json':sha(Path('translations/editorial_review_current_v1.json').read_bytes())},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    assert rebound['records']==packet['records'] and rebound['blocks']==packet['blocks']
    ROOT.mkdir(parents=True);save(ROOT/'all11_clean_current_complete_context.json',rebound)
    print('All11 B180 source/current records rebound to V4766;all four stories/EV2 exact. Fresh opening context available;no B180 gameplay or credit.')
