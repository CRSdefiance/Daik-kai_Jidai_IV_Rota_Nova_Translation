"""Bind ordinary and4100 virtual selectors using the own registered startup roles."""
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
    for arg in ['packet','styles','release','startup','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();packet,styles=map(load,[args.packet,args.styles])
    assert styles['source_packet_sha256']==sha(args.packet.read_bytes())
    ordinary=[r for g in packet['groups'] for r in g['records'] if 207<=r['source_selector']<224]
    assert all(r['source_complete_preamble_hex']=='0040ffff00'+f'{r["source_selector"]:02x}' for r in ordinary)
    records=[]
    for row in ordinary:records.append(dict(id=row['id'],kind='ordinary-speech',source_selector=row['source_selector'],source_reference=row['source_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex']))
    for row in styles['records']:
        raw=bytes.fromhex(row['source_choice_object_hex']);at=row['source_reference']['offset']-row['source_command_offset']
        assert raw[:20].hex()==row['source_header_hex'] and raw[:2]==b'\0\x41' and raw[18]==0 and raw[19]==row['source_selector']
        assert raw[at:at+len(bytes.fromhex(row['source_hex']))+1]==bytes.fromhex(row['source_hex'])+b'\0'
        records.append(dict(id=row['id'],kind='4100-style-alternative',source_selector=row['source_selector'],source_reference=row['source_reference'],source_header_hex=row['source_header_hex'],source_style_indices=row['source_style_indices'],virtual_prefix_not_in_stored_body=True))
    selectors=sorted({r['source_selector'] for r in records});assert selectors and 207 in selectors
    adapter=checked_text(inspect.getsource(dynamic),{
        "['resolved_actor_ID']==captain==2":"['resolved_actor_ID']==captain==1",
        'historical_London_context_not_selected_new_scene_participation=True':'own_registered_startup_context_not_actual_new_scene_role_assignment=True',
    })
    env=dict(dynamic.__globals__);exec(compile(adapter,__file__+'::unchanged-original-role-dispatch','exec'),env)
    ctx=RegisteredRuntime(args.release,args.startup);result=ctx.execute(env['dynamic'],selectors)
    save(args.out,dict(source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),source_styles=str(args.styles),source_styles_sha256=sha(args.styles.read_bytes()),runtime=ctx.receipt(),source_records=records,native_roles=result,source_owned_adapter=adapter,
        current_startup_not_actual_new_conditional_scene_participation=True,no_role_roster_event_RNG_orname_assignment=True,no_historical_RAM_overlay=True,
        new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [Path('scripts/reconcile_lil_B111_B119_voices_v3218.py'),Path(__file__)]}))
    print(dict(selectors=selectors,source_records=len(records),roles=result['rows'],future_conditional_participation_not_claimed=True))

if __name__=='__main__':main()
