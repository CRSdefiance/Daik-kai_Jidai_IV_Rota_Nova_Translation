"""Reuse original role dispatch on a registered candidate's own startup context."""
import argparse
import inspect
from pathlib import Path
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.reconcile_lil_B111_B119_voices_v3218 import dynamic
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('packet','release','startup','out'):parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();packet=load(args.packet)
    selectors=sorted({r['source_selector'] for g in packet['groups'] for r in g['records'] if 207<=r['source_selector']<224})
    assert selectors and 207 in selectors
    rows=[r for g in packet['groups'] for r in g['records'] if r['source_selector'] in selectors]
    assert all(r['source_complete_preamble_hex']=='0040ffff00'+f"{r['source_selector']:02x}" for r in rows)
    adapter=checked_text(inspect.getsource(dynamic),{
        "['resolved_actor_ID']==captain==2":"['resolved_actor_ID']==captain==1",
        'historical_London_context_not_selected_new_scene_participation=True':
            'own_registered_startup_context_not_actual_new_scene_role_assignment=True',
    })
    env=dict(dynamic.__globals__);exec(compile(adapter,__file__+'::unchanged-native-role-dispatch','exec'),env)
    ctx=RegisteredRuntime(args.release,args.startup);result=ctx.execute(env['dynamic'],selectors)
    save(args.out,dict(source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),runtime=ctx.receipt(),
        source_records=[dict(id=r['id'],source_reference=r['source_reference'],source_complete_preamble_hex=r['source_complete_preamble_hex']) for r in rows],
        native_roles=result,source_owned_adapter=adapter,current_startup_not_new_conditional_scene_participation=True,
        no_role_roster_event_RNG_orname_assignment=True,no_historical_RAM_overlay=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [Path('scripts/reconcile_lil_B111_B119_voices_v3218.py'),Path(__file__)]}))
    print('Bound original dynamic roles in own registered startup:',result['rows'])

if __name__=='__main__':main()
