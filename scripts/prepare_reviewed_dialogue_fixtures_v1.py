"""Copy selected complete native commands into disclosed initialized QA sequences."""
import argparse
import os
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ORDINARY = Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['reconstruction', 'stored', 'selection', 'out']:
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rebuilt, stored, selection = map(load, [args.reconstruction, args.stored, args.selection])
    assert stored['reconstruction_sha256'] == sha(args.reconstruction.read_bytes())
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    doc, native, menuproofs = map(load, [rebuilt['manuscript'], rebuilt['native'], rebuilt['menu']])
    parent = Path(rebuilt['research_ROM'])
    assert sha(parent.read_bytes()) == rebuilt['research_ROM_sha256']
    image = NdsImage.open(parent)
    arm = image.read_file('/__arm9__.bin')
    path = doc['file_path']
    assert path == '/data/SC0.DK4'
    archive = image.read_file(path)
    bank = IlnkContainer.parse(archive).blocks
    inventory, _, _ = scoped_inventory()
    opening, texts = inventory(arm, bank[44])
    first = texts[0]['offset']
    assert first == 40 and len([c for c in opening if c['offset'] < first]) == 10
    speeches = [r for r in doc['records'] if r['kind'] in ['progressive', 'system-FE']]
    byid = {r['id']: r for r in speeches}
    bynative = {r['id']: r for r in native['records']}
    expanded = {r['id']: r['expanded_hex'] for r in stored['records']}
    groups = {g['block']: g for g in rebuilt['groups']}
    commands = {t['id']: (g, next(c for c in g['all_target_commands'] if c['offset'] == t['new_offset']-5), t)
        for g in rebuilt['groups'] for t in g['text_records']}
    end = rebuilt['groups'][-1]['all_target_commands'][-1]
    assert end['word'] == 0
    args.out.mkdir(parents=True)
    created = []
    for spec in selection['fixtures']:
        logical = bytearray(bank[44][:first])
        selected = set(spec.get('speech_ids', []))
        selected |= {r['id'] for r in speeches if r['block'] in spec.get('speech_blocks', [])}
        for actor in spec.get('first_actor_IDs', []):
            selected.add(next(r['id'] for r in speeches if r['source_selector'] == actor))
        assert selected <= set(byid)
        sequence = spec.get('sequence') or [dict(speech=r['id']) for r in speeches if r['id'] in selected]
        bindings, copied, menus = [], [], []
        pages = 0
        for action in sequence:
            if 'speech' in action:
                ident = action['speech']
                row = byid[ident]
                group, command, text = commands[ident]
                raw, encoded = bytes.fromhex(command['whole_command_hex']), bytes.fromhex(text['stored_hex'])
                assert raw[:6].hex() == row['source_complete_preamble_hex'] and raw[5:6+len(encoded)] == encoded+b'\0'
                at = len(logical)
                logical += raw
                bindings.append(dict(id=ident, block=row['block'], selector=row['source_selector'], fixture_offset=at,
                    stored_command_offset=command['offset'], stored_hex=text['stored_hex'],
                    expected_expanded_body_hex=expanded[ident], logical_English=row['english']))
                copied.append(dict(block=row['block'], original_offset=command['offset'], fixture_offset=at,
                    whole_command_hex=command['whole_command_hex'], word=command['word']))
                pages += 1 if row['source_selector'] == 254 else len(bynative[ident]['complete_native_English_display']['pages'])
            else:
                request = action['menu']
                proof = next(m for m in menuproofs['menus'] if m['block'] == request['block'] and m['source_command_offset'] == request['source_command_offset'])
                command = next(c for c in groups[request['block']]['all_target_commands'] if c['whole_command_hex'] == proof['target_object_hex'])
                assert command['word'] in [0x2100, 0x2200]
                at = len(logical)
                logical += bytes.fromhex(command['whole_command_hex'])
                menus.append(dict(block=request['block'], fixture_offset=at, stored_command_offset=command['offset'],
                    source_command_offset=request['source_command_offset'], word=command['word'], command_hex=command['whole_command_hex']))
                copied.append(dict(block=request['block'], original_offset=command['offset'], fixture_offset=at,
                    whole_command_hex=command['whole_command_hex'], word=command['word']))
        logical += bytes.fromhex(end['whole_command_hex'])
        struct.pack_into('<H', logical, 4, len(logical)-8)
        block = bytes(logical)+bytes(-len(logical) % 4)
        actual, actual_texts = inventory(arm, block)
        assert len(actual_texts) == len(bindings) and actual[-1]['word'] == 0 and actual[-1]['offset']+4 == len(logical)
        assert all(next(c for c in actual if c['offset'] == r['fixture_offset'])['whole_command_hex'] == r['whole_command_hex'] for r in copied)
        changed = list(bank)
        changed[44] = block
        fixture = NdsImage.open(parent)
        fixture.replace_file(path, IlnkContainer(changed).to_bytes())
        assert [p for _, p, v in image.iter_files() if fixture.read_file(p) != v] == [path]
        assert all(fixture.read_file(p) == v for p, v in image.iter_components())
        name = spec['name']
        assert name.isidentifier()
        rom = args.out/(name+'_RESEARCH_ONLY.nds')
        fixture.save(rom)
        inverse = NdsImage.open(rom)
        inverse.replace_file(path, archive)
        assert bytes(inverse.rom.save()) == parent.read_bytes()
        frames = spec.get('frames', 4001+(pages+len(menus)+4)*240)
        inputs = args.out/(name+'_inputs.json')
        controls = load(ORDINARY)+[dict(start=f, duration=5, buttons=['A']) for f in range(4000, frames-500, 240)]
        controls += spec.get('extra_inputs', [])
        controls.sort(key=lambda r: r['start'])
        save(inputs, controls)
        proof = args.out/(name+'_fixture.json')
        save(proof, dict(research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()), parent=str(parent), parent_sha256=sha(parent.read_bytes()),
            text_language='reviewed-English', purpose=spec['purpose'], frames=frames, inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
            capture_extra=spec.get('capture_extra', []), expected_FE_bodies_hex=[r['expected_expanded_body_hex'] for r in bindings if r['selector'] == 254],
            selected_records=bindings, expected_pages=pages, selected_source_blocks=sorted({r['block'] for r in copied}), copied_commands=copied,
            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,
            ordinary_actor_IDs=sorted({r['selector'] for r in bindings if r['selector'] != 254}),
            complete_original_scene_including_transitions_andbranches_retained=False,
            focused_fixture_not_a_complete_story_exchange=True, all_selected_command_bytes_andcomplete_speaker_controls_exact=True,
            original_location_earned_chronology_natural_activation_fullroute_andhardware_unvisited=True,
            no_savestate_battery_RAM_roster_money_RNG_eventflag_orcondition_result_override=True,
            branch_andstat_effects_not_simulated=True, all_unowned_files_components_andserialized_parent_inverse_exact=True,
            not_registered_candidate_or_natural_activation=True, new_credit=0, guide_photos=False,
            evidence={str(p): sha(p.read_bytes()) for p in [args.reconstruction, args.stored, args.selection, ORDINARY, Path(__file__)]}))
        created.append(dict(fixture=str(proof), fixture_sha256=sha(proof.read_bytes()), path=str(rom), sha256=sha(rom.read_bytes()),
            utterances=len(bindings), pages=pages, menus=len(menus), frames=frames))
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    for item in created:
        rom = Path(item['path'])
        assert not any(Path(v['path']).resolve() == rom.resolve() for v in values)
        values.append(dict(path=str(rom.resolve()), reason='Preserve disclosed native-command dialogue fixture. SHA256 '+item['sha256']))
    (args.out/'pins.before.json').write_bytes(before)
    pending = pins.with_name('rom_retention_pins.'+args.out.name+'.pending.json')
    assert not pending.exists()
    save(pending, values)
    assert pins.read_bytes() == before
    os.replace(pending, pins)
    save(args.out/'fixtures.json', dict(fixtures=created, actual_observation_pending=True, new_credit=0, guide_photos=False))
    print(created, flush=True)


if __name__ == '__main__':
    main()
