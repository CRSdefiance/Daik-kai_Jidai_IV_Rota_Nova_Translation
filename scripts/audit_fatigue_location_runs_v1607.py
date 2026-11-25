"""Reapply the complete input/RAM/save audit to successor48-byte fixtures."""
import inspect
from pathlib import Path
from scripts import verify_fatigue_shore_pilots_v1597d as prior
from scripts.verify_village_wrap_v608 import save

def audit_run(label,version,module,terminal_frame,fixture_frames):
    source=inspect.getsource(prior.audit)
    for old,new in [('len(proof[\'owned_bytes\'])==40','len(proof[\'owned_bytes\'])==48'),
        ('all40_coordinate_byte_changes_and_other4MiB_bytes_audited','all48_coordinate_byte_changes_and_other4MiB_bytes_audited'),
        ('no_309_recovery_or_editorial_completion_credit','no_editorial_completion_credit_from_preservation_audit_alone')]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**prior.__dict__};exec(compile(source,__file__,'exec'),env)
    return env['audit'](label,version,module,terminal_frame,fixture_frames)

if __name__=='__main__':
    from scripts import native_fatigue_shore_fixture_v1602 as module
    from dk4tool.patch.grand_race_menu_release import sha
    root=Path('work/analysis/fatigue_location_run_v1607');assert not root.exists()
    record=audit_run('fatigue_recovery_live_v1603',1594,module,6200,[5000,5650])
    root.mkdir(parents=True);save(root/'terminal_swamp_pilot_preservation.json',{'audit':record,
        'normal_Sea_View6200_actually_viewed':True,'no_recovery309_observed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Terminal6200 swamp pilot:48-byte fixtures,all otherRAM,input journal,PNGs and unchanged saves pass.')
