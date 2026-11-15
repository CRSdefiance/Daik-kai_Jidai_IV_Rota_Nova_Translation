"""Stored B51 parity, native controls, exact references and whole-image inverse.

Only research block/archive files are written. Existing exact native alignments
and planes are reused; the single changed parity tail is freshly exercised.
"""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B50_registered_route_context_v8546 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_stored_v8566')
RELOCATION = Path('work/analysis/Hodram_B51_relocation_v8565/reconstruction.json')
NATIVE = Path('work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json')
VIEW = Path('work/analysis/Hodram_B51_native_review_v8564/native_body_review.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v2.json')
INPUT = Path('work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json')
SOURCE = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
DISPLAY = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
CURRENT = Path('work/analysis/Hodram_B51_current_v8559/current_effective.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    relocation, native, view, doc, source, display, current = map(read, [RELOCATION, NATIVE, VIEW, DOC, SOURCE, DISPLAY, CURRENT])
    assert relocation['manuscript_sha256'] == view['manuscript_sha256'] == sha(DOC.read_bytes())
    assert native['manuscript_sha256'] == sha(Path(doc['predecessor_manuscript']).read_bytes())
    assert view['all_five_complete_bodies_visually_read'] and view['directly_viewed_sheet'] == native['review_sheet']
    group = relocation['groups'][0]
    target, archive = Path(group['target_block']).read_bytes(), Path(relocation['target_archive']).read_bytes()
    assert sha(target) == group['target_block_sha256'] and sha(archive) == relocation['target_archive_sha256']
    assert IlnkContainer.parse(archive).blocks[51] == target
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == current['current_ROM_sha256']
    arm, font = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    before_rom = bytes(image.rom.save())
    before_archive = image.read_file('/data/SC1.DK4')
    planned = deepcopy(image)
    planned.replace_file('/data/SC1.DK4', archive)
    assert [p for _, p, data in image.iter_files() if planned.read_file(p) != data] == ['/data/SC1.DK4']
    assert all(planned.read_file(p) == data for p, data in image.iter_components())
    inverse = deepcopy(planned)
    inverse.replace_file('/data/SC1.DK4', before_archive)
    assert bytes(inverse.rom.save()) == before_rom
    pixels, unused_factory, oracle = bind(image)
    pe = {**original_pages.__globals__, 'expected_pixels': pixels, 'codes': codes}
    exec(compile(native['source_owned_target_page_adapter'], __file__ + '::unchanged-complete-page-oracle', 'exec'), pe)
    prog = dict(progressive_expand.__globals__)
    exec(compile(native['source_owned_progressive_adapter'], __file__ + '::unchanged-progressive', 'exec'), prog)
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    rows, fresh, reused, dispatches, queries, opaque = [], [], [], [], [], []
    ns = {**inherited.__dict__, 'SOURCE': INPUT, 'route': 1, 'route_mask': 2, 'CATALOG_LOOKUP': {}}
    for key, text in display['source_owned_dispatch_adapters'].items():
        exec(compile(text, __file__ + '::' + key, 'exec'), ns)
    ns['CATALOG_LOOKUP'], catalogue = ns['bind_current_catalog'](image)
    exec(compile(display['source_owned_macro_body_adapter'], __file__ + '::exact-macro-body', 'exec'), ns)
    for row in doc['records']:
        ref = next(r for r in group['text_records'] if r['id'] == row['id'])
        old = next(r for r in native['records'] if r['id'] == row['id'])
        compiled, stored, at = bytes.fromhex(ref['compiled_hex']), bytes.fromhex(ref['target_hex']), ref['new_offset']
        assert compiled.hex() == row['compiled_hex'] == old['compiled_hex'] and stored == compiled + (b' ' if ref['parity_space_added'] else b'')
        assert target[at:at + len(stored) + 1] == stored + b'\0' and target[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        assert target[:at].count(b'\0') == ref['new_record_index'] and stored[0] == row['source_selector']
        body = stored[1:]
        assert b'\0' not in body and not any(m in body for m in [b'FI', b'FA', b'FO'])
        if stored == compiled:
            assert body.hex() == old['expanded_native_hex']
            for page in old['pages']:
                assert sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256']
            proof = deepcopy(old)
            reused.append(row['id'])
        else:
            aligned = ctx.execute(prog['expand'], body, row['source_selector'])
            ctx.machines.pop()
            assert len(aligned['cases']) == 4 and all(c['output_hex'] == body.hex() for c in aligned['cases'])
            rendered = pe['pages'](arm, font, body)
            assert len(rendered['pages']) == len(old['pages']) == 1 and rendered['complete_consumed_bytes'] == len(body)
            for page, previous in zip(rendered['pages'], old['pages'], strict=True):
                plane = bytes.fromhex(page.pop('native_plane_hex'))
                assert sha(plane) == previous['native_plane_sha256'] == sha(Path(previous['native_plane']).read_bytes())
                page.update(viewed_native_plane=previous['native_plane'], viewed_native_plane_sha256=sha(plane))
            proof = dict(native_alignment=aligned, **rendered)
            fresh.append(row['id'])
        dispatch = ctx.execute(ns['dispatch'], stored[0], body)
        ctx.machines.pop()
        assert dispatch['resolved_actor_ID'] == stored[0] and dispatch['source_voice_class'] == {1: 1, 16: 1, 18: 0, 113: 0}[stored[0]]
        boundary = next(b for b in dispatch['boundaries'] if b['kind'] == 'unexecuted-progressive-body')
        assert boundary['text_hex'] == body.hex() and dispatch['registered_catalog_match'] is None and not dispatch['FE_original_null_actor_calls']
        dispatches.append(dict(id=row['id'], **dispatch))
        rows.append(dict(id=row['id'], file_path=row['file_path'], block=51, source_selector=row['source_selector'], source_reference=row['source_reference'],
            current_reference=row['current_reference'], final_reference=dict(file_path='/data/SC1.DK4', block=51, offset=at, bytes=len(stored), header_offset=at - 5,
                record_index=ref['new_record_index'], target_block_sha256=sha(target)), source_hex=row['source_hex'], current_hex=row['current_hex'],
            stored_hex=stored.hex(), compiled_hex=compiled.hex(), compiler_owned_parity_space=ref['parity_space_added'],
            reused_exact_native_body=stored == compiled, complete_native_stored_proof=proof, complete_native_ink_exact_to_directly_viewed_page=True))
    for command, mapping, original in zip(group['all_target_commands'], group['command_map'], source['all_original_source_commands'], strict=True):
        word = command['word']
        assert word == mapping['word'] == original['word'] and command['offset'] == mapping['new_offset']
        if word in [0x8000, 0x8100]:
            case = ctx.execute(probe, target, command)
            ctx.machines.pop()
            previous = next(q for q in source['source_raw_query_cases'] if q['word'] == word)
            assert case['native_result'] == previous['native_result'] and case['source_command_hex'] == previous['source_command_hex']
            queries.append(case)
        elif word not in [0, 0x4000, 0x100, 0x200, 0x300, 0x400]:
            raw = bytes.fromhex(command['whole_command_hex'])
            assert command['whole_command_hex'] == original['whole_command_hex']
            # Independent original linear decoder, with opaque effect bridges disclosed.
            import struct
            isolated = b'CS\0\1' + struct.pack('<H', len(raw)) + bytes(2) + raw
            result = walk(arm, isolated)
            assert result['error'] is None and result['stopped_offset'] == result['logical_end'] == len(isolated) and len(result['rows']) == 1
            opaque.append(dict(source_offset=original['offset'], target_offset=command['offset'], word=word, original_linear_decode=result))
    end_env = dict(end_case.__globals__)
    exec(compile(source['source_owned_seeded_end_adapter'], __file__ + '::original-full-value-carry-end', 'exec'), end_env)
    terminal = group['all_target_commands'][-1]
    assert terminal['word'] == 0 and terminal['native_extent'] == 4 and terminal['offset'] + 4 == group['target_logical_end']
    ends = [end_env['end_case'](arm, target, terminal['offset'], previous, value)
        for previous in [0, 1, 2, 3, 0xFFFFFFFF] for value in [0, 1, 2, 3, 0xFFFFFFFF]]
    assert len(rows) == 5 and len(fresh) == 1 and len(reused) == 4 and len(dispatches) == 5 and len(queries) == 2 and len(opaque) == 4 and len(ends) == 25 and not ctx.machines
    assert all(e['native_result'][1] == e['initial_value_word'] for e in ends)
    assert sum(len(c['cases']) for c in group['relocated_skip_cases']) == 40
    save(ROOT / 'stored_native_controls_andrefs.json', dict(candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), relocation=str(RELOCATION), relocation_sha256=sha(RELOCATION.read_bytes()),
        records=rows, fresh_parity_tail_records=fresh, exact_native_reused_records=reused, fresh_native_alignment_cases=4, exact_reused_native_alignment_cases=16,
        all5_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass=True, compiler_tail_creates_no_blank_oradditional_page=True,
        stored_dispatches=dispatches, stored_queries=queries, four_opaque_structural_decodes=opaque, normal_seeded_ends=ends,
        reused_exact_relocated_native_skip_cases=group['relocated_skip_cases'], complete_native_four_byte_end_andseparate_tail_bound=True,
        all20_commands5_preambles8_relative_sites2_queries4_opaque_controls_andwhole_source_current_inverses_bound=True,
        all324_other_blocks_andall_other_files_components_exact=True, whole_current_inmemory_ROM_inverse_byte_exact=True,
        research_whole_ROM_sha256=sha(bytes(planned.rom.save())), whole_ROM_not_written_orregistered=True,
        target_oracle_binding=oracle, registered_catalogue_binding=catalogue, native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_owned_seeded_end_adapter=source['source_owned_seeded_end_adapter'], source_owned_query_probe=source['source_owned_query_probe'],
        actual_B51_branch_name_header_transition_effect_semantics_loaders_policy_atomic_andregistered_release_pending=True,
        offline_CPU_fragments_andlinear_effect_bridges_not_actual_gameplay_ornatural_activation=True, new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [RELOCATION, NATIVE, VIEW, DOC, INPUT, SOURCE, DISPLAY, CURRENT, Path(__file__)]}))
    print('B51 stored: one parity tail/four fresh alignments, four exact bodies/sixteen reused alignments; five dispatches, two queries, forty reused branch cases, twenty-five complete value-carry ends. Exact whole-ROM inverse; no ROM write or credit.')
