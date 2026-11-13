"""Bind source group roles to fleet identities, independent of world-slot ordering."""
from pathlib import Path


def main():
    path=Path('scripts/verify_sighting_compass_v1094b.py')
    assert not path.exists()
    body=Path('scripts/verify_sighting_compass_v1094.py').read_text(encoding='utf-8')
    body=body.replace("ROOT=Path('work/analysis/sighting_compass_v1094')", "ROOT=Path('work/analysis/sighting_compass_v1094b')")
    before="    groups=list(cpu.mem_read(root+0x2080,16));assert groups[0:2]==[1,0] and groups[4:6]==[8,2] and groups[8:10]==[57,1]\n"
    assert body.count(before)==1
    after="""    groups=list(cpu.mem_read(root+0x2080,16))
    by_id={groups[k]:groups[k+1] for k in range(0,16,4) if groups[k]!=64}
    assert by_id=={1:0,57:1,8:2}
    assert groups[0:2]==[1,0]
    for fleet,company in ((1,2),(57,2),(8,8)):
        assert get(0x35320,root+4+fleet*132)==company
    # Original77DA4 sets the enemy's selected group+1 to2; original
    # support discovery changes Manuel's existing world slot to1.
    # The source indexes by selected group record, not by fleet order.
    control_cpu,control=get_machine(arm,raw[5310])
    control_root=control(0xCB1A8)
    control_groups=list(control_cpu.mem_read(control_root+0x2080,16))
    before_roles={control_groups[k]:control_groups[k+1] for k in range(0,16,4) if control_groups[k]!=64}
    assert before_roles=={1:0,57:5,8:2}
    assert [groups[k] for k in range(0,16,4)]==[control_groups[k] for k in range(0,16,4)]
"""
    body=body.replace(before,after)
    body=body.replace("'normal_sighting_A_dismissal_to_original_covering_fire_then_normal_A_to_battle':True,",
        "'normal_sighting_A_dismissal_to_original_covering_fire_then_normal_A_to_sea':True,\n        'original_pending_battle_setup_and_identity_bound_roles_verified':True,\n        'visually_observed_sea_return_not_complete_battle_playthrough':True,\n        'prior_verifier_rejected_fixed_slot_order_preserved':'scripts/verify_sighting_compass_v1094.py',")
    path.write_text(body,encoding='utf-8')
    print('Created identity-bound verifier; failed fixed-order predecessor preserved.')


if __name__=='__main__':main()
