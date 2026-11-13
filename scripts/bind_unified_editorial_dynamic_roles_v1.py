"""Bind unified speech/style selectors through unchanged native dispatch on an explicit captain."""
import argparse
import inspect
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.reconcile_lil_B111_B119_voices_v3218 import dynamic
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['packet','runtime','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    packet, context = map(load,[args.packet,args.runtime])
    receipt = context['runtime']
    captain = receipt['captain']
    assert captain in range(4)
    rows = [r for g in packet['groups'] for r in g['records'] if 207<=r.get('source_selector',254)<224]
    assert rows
    for row in rows:
        if row['kind']=='ordinary-speech':
            assert row['source_complete_preamble_hex']=='0040ffff00'+f"{row['source_selector']:02x}"
        else:
            assert row['kind']=='physical-style-alternative'
            raw = bytes.fromhex(row['source_object_hex'])
            offset = row['source_reference']['offset']-row['source_command_offset']
            body = bytes.fromhex(row['source_hex'])
            assert raw[:20].hex()==row['source_header_hex'] and raw[:2]==b'\0\x41'
            assert raw[18]==0 and raw[19]==row['source_selector']
            assert raw[offset:offset+len(body)+1]==body+b'\0'
    selectors = sorted({r['source_selector'] for r in rows})
    adapter = checked_text(inspect.getsource(dynamic), {
        "['resolved_actor_ID']==captain==2":f"['resolved_actor_ID']==captain=={captain}",
        'historical_London_context_not_selected_new_scene_participation=True':
            'current_startup_context_not_actual_conditional_scene_participation=True'})
    env = dict(dynamic.__globals__)
    exec(compile(adapter,__file__+'::same-original-dispatch-explicit-captain','exec'),env)
    ctx = RegisteredRuntime(receipt['release_proof'],receipt['startup_proof'],captain=captain)
    assert ctx.receipt()==receipt
    result = ctx.execute(env['dynamic'],sorted({207,*selectors}))
    save(args.out,dict(runtime=ctx.receipt(),source_selectors=selectors,captain_control_selector=207,
        source_records=[dict(id=r['id'],kind=r['kind'],source_reference=r['source_reference'],
            source_selector=r['source_selector']) for r in rows],
        native_roles=result,source_owned_adapter=adapter,
        no_role_roster_event_RNG_orname_assignment=True,no_historical_RAM_overlay=True,
        current_startup_not_conditional_scene_role_orroster_coverage=True,
        evidence={str(p):digest(p) for p in [args.packet,args.runtime,Path(__file__)]},new_credit=0))
    print('Bound',len(rows),'source bodies/selectors',selectors,'on captain',captain,':',result['rows'])


if __name__=='__main__':
    main()
