"""Execute original dynamic-role dispatch in an explicitly selected own registered captain context."""
import argparse
import inspect
from pathlib import Path
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.reconcile_lil_B111_B119_voices_v3218 import dynamic
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['packet','release','startup','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--captain',type=int,choices=range(4),required=True)
    args=parser.parse_args()
    assert not args.out.exists()
    packet=load(args.packet)
    rows=[r for g in packet['groups'] for r in g['records'] if 207<=r['source_selector']<224]
    selectors=sorted({r['source_selector'] for r in rows})
    assert selectors and all(r['source_complete_preamble_hex']=='0040ffff00'+f"{r['source_selector']:02x}" for r in rows)
    adapter=checked_text(inspect.getsource(dynamic),{
        "['resolved_actor_ID']==captain==2":f"['resolved_actor_ID']==captain=={args.captain}",
        'historical_London_context_not_selected_new_scene_participation=True':
            'own_registered_startup_context_not_actual_new_scene_role_assignment=True'})
    env=dict(dynamic.__globals__)
    exec(compile(adapter,__file__+'::same-native-role-dispatch-explicit-captain', 'exec'),env)
    ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)
    result=ctx.execute(env['dynamic'],sorted(set([207,*selectors])))
    save(args.out,dict(source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),runtime=ctx.receipt(),
        source_records=[dict(id=r['id'],source_reference=r['source_reference'],source_complete_preamble_hex=r['source_complete_preamble_hex']) for r in rows],
        source_selectors=selectors,native_roles=result,source_owned_adapter=adapter,
        role0_control_not_new_scene_participation=True,current_startup_not_new_conditional_scene_participation=True,
        no_role_roster_event_RNG_orname_assignment=True,no_historical_RAM_overlay=True,no_static_actor207_table_lookup=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.packet,Path('scripts/reconcile_lil_B111_B119_voices_v3218.py'),Path(__file__)]}))
    print(dict(source_records=len(rows),source_selectors=selectors,native_roles=result['rows'],new_credit=0))


if __name__=='__main__':
    main()
