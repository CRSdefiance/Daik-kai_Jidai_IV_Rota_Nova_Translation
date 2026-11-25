"""Expose B51 current English only after clean whole-exchange and native view."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B50_registered_route_context_v8546 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_current_v8559')
GLOSS = Path('work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json')
DISPLAY = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
VIEW = Path('work/analysis/Hodram_B51_source_view_v8557/source_view.json')
CONTROLS = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
INPUT = Path('work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json')
HANDOFF = Path('work/analysis/editorial_handoff_verification_v8554/verified_handoff.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    gloss, display, view, controls, inp, verified = map(read, [GLOSS, DISPLAY, VIEW, CONTROLS, INPUT, HANDOFF])
    ledger = Path('translations/editorial_review_current_v1.json')
    assert sha(ledger.read_bytes()) == verified['ledger_sha256'] and verified['completed'] == 7224
    assert gloss['all5_clean_utterances_glossed_before_current_English'] and display['current_B51_English_dialogue_bodies_unconsulted']
    assert controls['current_B51_English_dialogue_bodies_still_unconsulted'] and view['all5_complete_source_pages_andfour_qualified_reused_nameplanes_directly_viewed']
    assert display['source_gloss_sha256'] == controls['first_clean_gloss_sha256'] == sha(GLOSS.read_bytes())
    assert view['source_native_proof_sha256'] == sha(DISPLAY.read_bytes())
    assert sha(Path(display['review_sheet']['path']).read_bytes()) == display['review_sheet']['sha256']
    image = NdsImage.open(inp['current_ROM'])
    assert sha(Path(inp['current_ROM']).read_bytes()) == inp['current_ROM_sha256'] == verified['candidate_sha256'] == display['candidate_sha256']
    arm, archive = image.read_file('/__arm9__.bin'), image.read_file('/data/SC1.DK4')
    source = gloss['groups'][0]
    number = source['block']
    assert number == 51
    block = IlnkContainer.parse(archive).blocks[number]
    clean = bytes.fromhex(source['clean_block_hex'])
    inventory, walker, inventory_function = scoped_inventory()
    commands, speeches = inventory(arm, block)
    assert len(commands) == len(source['commands']) == 20 and len(speeches) == len(source['records']) == 5
    logical = 8 + int.from_bytes(block[4:6], 'little')
    assert commands[-1]['word'] == 0 and commands[-1]['offset'] + 4 == logical and block[logical:] == bytes(len(block) - logical)
    offset_map = {a['offset']: b['offset'] for a, b in zip(source['commands'], commands, strict=True)}
    offset_map[source['clean_logical_end']] = logical
    pairs, relative_maps = [], []
    for a, b in zip(source['commands'], commands, strict=True):
        assert a['word'] == b['word'] and [offset_map[x] for x in a['ancestor_0100_offsets']] == b['ancestor_0100_offsets']
        word, av, bv = a['word'], bytes.fromhex(a['whole_command_hex']), bytes.fromhex(b['whole_command_hex'])
        if word == 0x4000:
            assert av[:6] == bv[:6]
            kind = 'speech'
        elif word in [0x100, 0x200, 0x300, 0x400]:
            sa, ca = [struct.unpack_from('<H', raw, 2)[0] for raw in [av, bv]]
            st, ct = a['offset'] + 4 + sa, b['offset'] + 4 + ca
            assert ct == offset_map[st] and b['offset'] + 4 == offset_map[a['offset'] + 4]
            relative_maps.append(dict(source_offset=a['offset'], current_offset=b['offset'], word=word, source_span=sa,
                current_span=ca, source_next=a['offset'] + 4, current_next=b['offset'] + 4,
                source_skip_target=st, current_skip_target=ct, source_0100_ancestors=a['ancestor_0100_offsets']))
            kind = 'relative'
        else:
            assert av == bv
            kind = 'opaque-control-query-or-terminal'
        pairs.append(dict(word=word, kind=kind, source_offset=a['offset'], current_offset=b['offset'],
            source_extent=a['native_extent'], current_extent=b['native_extent'], source_hex=av.hex(), current_hex=bv.hex(), bytes_equal=av == bv))
    assert len(relative_maps) == 8
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    ns = {**inherited.__dict__, 'SOURCE': INPUT, 'route': 1, 'route_mask': 2, 'CATALOG_LOOKUP': {}}
    for name, text in display['source_owned_dispatch_adapters'].items():
        exec(compile(text, __file__ + '::exact-original-' + name, 'exec'), ns)
    ns['CATALOG_LOOKUP'], catalogue = ns['bind_current_catalog'](image)
    exec(compile(display['source_owned_macro_body_adapter'], __file__ + '::measured-captain1-defaults', 'exec'), ns)
    rows, dispatches, relative_cases, query_cases = [], [], [], []
    for original, command in zip(source['records'], speeches, strict=True):
        at = command['offset'] + 5
        raw = block[at:block.index(0, at + 1)]
        assert raw[0] == original['source_selector'] and block[at - 5:at + 1].hex() == original['source_complete_preamble_hex']
        result = ctx.execute(ns['dispatch'], raw[0], raw[1:])
        ctx.machines.pop()
        assert result['resolved_actor_ID'] == raw[0] and result['source_voice_class'] == {1: 1, 16: 1, 18: 0, 113: 0}[raw[0]]
        assert not result['FE_original_null_actor_calls']
        boundary = next(q for q in result['boundaries'] if q['kind'] == 'unexecuted-progressive-body')
        selected = ns['CATALOG_LOOKUP'].get(raw[1:])
        template = selected['target'] if selected else raw[1:]
        expanded = template.replace(b'FI', b'Hodram').replace(b'FA', b'Bergstrom').replace(b'FO', b'Bergstrom Fleet')
        assert boundary['text_hex'] == expanded.hex()
        row = deepcopy(original)
        row.update(kind='progressive', source_kind='progressive',
            current_reference=dict(file_path='/data/SC1.DK4', block=number, offset=at, bytes=len(raw), header_offset=at - 5, record_index=block[:at].count(b'\0')),
            current_hex=raw.hex(), current_record_index=block[:at].count(b'\0'), current_native_extent=command['native_extent'], current_0100_ancestors=command['ancestor_0100_offsets'],
            current_raw_storage_English=raw[1:].decode('cp932'), raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
            effective_predecessor_template_hex=template.hex(), effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),
            current_actual_default_expanded_hex=expanded.hex(), registered_catalogue_match=result['registered_catalog_match'],
            current_English_body_unread=False, current_English_dialogue_still_unconsulted=False, current_English_body_now_exposed=True,
            source_presentation_consumer_not_yet_approved=False, current_effective_dispatch_andcatalogue_pending=False,
            source_native_display_andoriginal_complete_preamble_bound_offline=True, source_prose_orcompletion_credit_added=False,
            current_contextual_prose_formatting_actual_andrelease_pending=True)
        rows.append(row)
        dispatches.append(dict(id=row['id'], version='current-English', **result))
    # Source calls already passed in the same exact current context at V8555/8556.
    # Only changed current command addresses are freshly exercised here.
    for command in commands:
        if command['word'] in [0x100, 0x200, 0x300, 0x400]:
            relative_cases.append(ctx.execute(native_skip, block, command))
            ctx.machines.pop()
        elif command['word'] in [0x8000, 0x8100]:
            query_cases.append(ctx.execute(probe, block, command))
            ctx.machines.pop()
    assert len(rows) == len(dispatches) == 5 and len(relative_cases) == 8 and len(query_cases) == 2 and not ctx.machines
    group = dict(block=51, file_path='/data/SC1.DK4', clean_block_hex=clean.hex(), clean_block_sha256=sha(clean),
        source_header_hex=clean[:8].hex(), current_block_hex=block.hex(), current_block_sha256=sha(block), current_header_hex=block[:8].hex(),
        current_stored_bytes=len(block), current_logical_end=logical, current_tail_bytes=len(block) - logical,
        all_source_commands=source['commands'], all_current_commands=commands, all_command_reference_pairs=pairs,
        relative_operand_maps=relative_maps, source_event_records=source['source_event_records'], records=rows)
    save(ROOT / 'current_effective.json', dict(current_ROM=inp['current_ROM'], current_ROM_sha256=inp['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm), current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')), current_archive_sha256=sha(archive),
        file_path='/data/SC1.DK4', records=rows, groups=[group], typed_choices=[],
        source_first_glosses_andcomplete_native_page_view_precede_current_English=True,
        source_gloss=str(GLOSS), source_gloss_sha256=sha(GLOSS.read_bytes()), source_native_display=str(DISPLAY), source_native_display_sha256=sha(DISPLAY.read_bytes()),
        source_native_view=str(VIEW), source_native_view_sha256=sha(VIEW.read_bytes()), source_controls=str(CONTROLS), source_controls_sha256=sha(CONTROLS.read_bytes()),
        current_native_five_dispatches=dispatches, current_native_relative_cases=relative_cases, current_native_query_cases=query_cases,
        source_calls_reused_from_exact_same_current_ROM_code_font_wholeactors_andcaptain1_context=True,
        reused_source_dispatches=display['records'], reused_source_relative_cases=controls['source_relative_cases'], reused_source_queries=controls['source_raw_query_cases'],
        registered_current_catalogue_binding=catalogue, all20_commands5_preambles8_relative_targets_queries_opaque_effects_andcomplete_end_bound=True,
        query_return_words_andstructural_extents_not_actual_conversation_paths=True, current_comparison_not_English_editorial_approval=True,
        current_native_input=str(INPUT), native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        inventory_walker=walker, inventory_function=inventory_function, no_ROM_write_orledger_credit=True, new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [GLOSS, DISPLAY, VIEW, CONTROLS, INPUT, HANDOFF, Path(__file__)]}))
    for row in rows:
        print(row['id'], repr(row['effective_predecessor_paragraph']), 'catalogue', row['registered_catalogue_match'])
    print('Five current dispatches, forty current relative cases and two queries; source tests explicitly reused. Exact source/current references mapped, zero editorial credit.')
