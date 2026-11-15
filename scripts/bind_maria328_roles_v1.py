"""Bind ordinary/style selectors to original current roles without assigning a future scene roster."""
import inspect
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.reconcile_lil_B111_B119_voices_v3218 import dynamic
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    out = ROOT/'dynamic_roles_current_v1.json'
    assert not out.exists()
    current_path, objects_path = ROOT/'current_v1/current_effective.json', ROOT/'current_objects_v1/current_objects.json'
    current, objects = map(load,[current_path,objects_path])
    assert current['runtime'] == objects['runtime']
    groups = {g['block']:g for g in current['groups']}
    records = []
    for group in current['groups']:
        for row in group['records']:
            if 207 <= row['source_selector'] < 224:
                assert row['source_complete_preamble_hex'] == '0040ffff00'+f"{row['source_selector']:02x}"
                records.append(dict(id=row['id'],kind='ordinary-speech',source_selector=row['source_selector'],
                    source_reference=row['source_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex']))
    for row in objects['style_records']:
        obj = next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
        raw = bytes.fromhex(obj['source_object_hex'])
        at = row['source_reference']['offset']-row['source_command_offset']
        body = bytes.fromhex(row['source_hex'])
        assert raw[:20].hex() == row['source_header_hex'] and raw[:2] == b'\0A'
        assert raw[18] == 0 and raw[19] == row['source_selector'] and raw[at:at+len(body)+1] == body+b'\0'
        block = bytes.fromhex(groups[row['block']]['clean_block_hex'])
        assert block[row['source_command_offset']:row['source_command_offset']+len(raw)] == raw
        records.append(dict(id=row['id'],kind='4100-style-alternative',source_selector=row['source_selector'],
            source_reference=row['source_reference'],source_header_hex=row['source_header_hex'],
            source_style_indices=row['source_style_indices'],virtual_prefix_not_in_stored_body=True))
    selectors = sorted({r['source_selector'] for r in records})
    assert len(records) == 38 and selectors == [207,208,214,215]
    adapter = checked_text(inspect.getsource(dynamic), {
        "['resolved_actor_ID']==captain==2": "['resolved_actor_ID']==captain==3",
        'historical_London_context_not_selected_new_scene_participation=True':
            'own_registered_startup_context_not_actual_new_scene_role_assignment=True',
    })
    env = dict(dynamic.__globals__)
    exec(compile(adapter,__file__+'::same-original-role-dispatch-current-Maria','exec'),env)
    runtime = current['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt() == runtime
    result = ctx.execute(env['dynamic'],selectors)
    save(out,dict(runtime=runtime,source_records=records,source_selectors=selectors,captain_control_selector=207,
        native_roles=result,source_owned_adapter=adapter,source_packet=str(current_path),source_packet_sha256=digest(current_path),
        source_styles=str(objects_path),source_styles_sha256=digest(objects_path),
        all14_ordinary_and24_physical_style_references_bound=True,
        virtual_prefix_from_each_original_4100_header_not_assumed_D0=True,
        current_startup_not_actual_new_conditional_scene_participation=True,
        no_role_roster_event_RNG_orname_assignment=True,no_static_actor207_208_214_215_lookup=True,
        FE_not_resolved_as_actor254_orfallback208=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current_path,objects_path,Path(__file__),Path('scripts/reconcile_lil_B111_B119_voices_v3218.py')]}))
    print(result['rows'])


if __name__ == '__main__':
    main()
