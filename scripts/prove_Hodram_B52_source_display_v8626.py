"""Clean-first B52 dispatch, complete Japanese pages and scoped native names.

Reuses byte-identical original adapters and qualified name tests; does not open
the current B52 dialogue. Every fresh CPU call uses the current captain1 snapshot.
"""
import copy
import inspect
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B51_registered_route_context_v8612 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_source_display_v8626')
GLOSS = Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')
CONTROL = Path('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')
INPUT = Path('work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json')
START = Path('work/analysis/Hodram_B51_registered_binding_v8612/own_Hodram_startup_andstrict_captain1_context.json')
VIEW = Path('work/analysis/Hodram_B51_registered_startup_view_v8613/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
NAMES = Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
OLD_NAMES = Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
SURNAME = Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
DISPATCH = Path('work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json')
STORED = Path('work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    gloss, control, inp, start, view, names, oldnames, surname, dispatch, stored = map(
        read, [GLOSS, CONTROL, INPUT, START, VIEW, NAMES, OLD_NAMES, SURNAME, DISPATCH, STORED])
    assert gloss['all3_clean_utterances_andtwo_choices_glossed_before_current_English'] and gloss['current_English_dialogue_bodies_andchoice_labels_still_unconsulted']
    assert control['current_B52_English_dialogue_bodies_still_unconsulted']
    image = NdsImage.open(inp['current_ROM'])
    arm, font = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    clean = NdsImage.open('work/clean.nds')
    assert sha(Path(inp['current_ROM']).read_bytes()) == inp['current_ROM_sha256'] == start['candidate_sha256'] == view['candidate_sha256']
    assert view['viewed'] and view['whole_actors_equal'] and view['reuse_requires_identical_complete_ARM9_COMMON_font_andwhole_actual_actors']
    oldimage = NdsImage.open(names['candidate'])
    assert all(oldimage.read_file(p) == image.read_file(p) for p in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT'])
    assert sha(arm) == names['ARM9_sha256'] == stored['ARM9_sha256'] and start['actual_original_captain_ID'] == 1
    actor_ids = [113]
    identities = copy.deepcopy([r for r in oldnames['complete_clean_andcurrent_name_fields'] if r['actor_ID'] in actor_ids])
    assert [r['actor_ID'] for r in identities] == actor_ids
    name_rows = []
    for identity in identities:
        for version, im in [('clean_fields', clean), ('current_fields', image)]:
            code = im.read_file('/__arm9__.bin')
            for field in identity[version]:
                at = field['table_field']
                assert code[at:at + 4].hex() == field['table_field_hex']
                if 'offset' in field:
                    offset, raw = field['offset'], bytes.fromhex(field['hex'])
                    assert code[offset:offset + len(raw) + 1] == raw + b'\0'
        actor = identity['actor_ID']
        getters = [r for r in names['native_twelve_progressive_andfull_getters']['rows'] if r['actor_ID'] == actor]
        plane = next(r for r in names['name_planes'] if r['actor_ID'] == actor)
        assert len(getters) == 2 and plane['complete_first_internal_final_characters_andbounds']
        assert sha(Path(plane['native_plane']).read_bytes()) == plane['native_plane_sha256']
        assert sha(Path(plane['preview']).read_bytes()) == plane['preview_sha256']
        identity.pop('original_getters')  # Historical pre-correction calls stay in OLD_NAMES, never relabelled as current.
        name_rows.append(dict(actor_ID=actor, exact_clean_current_fields=identity,
            reused_current_original_two_getters=getters, reused_current_original_style11_plane=plane))
    progressive = checked_text(inspect.getsource(progressive_expand), {
        'assert identity==prefix and captain==2': 'assert identity==prefix and captain==1'})
    pe = dict(progressive_expand.__globals__)
    exec(compile(progressive, __file__ + '::source-captain1-progressive', 'exec'), pe)
    pixels, unused_factory, oracle = bind(image)
    ns = {**inherited.__dict__, 'SOURCE': INPUT, 'route': 1, 'route_mask': 2, 'CATALOG_LOOKUP': {}}
    adapters = dict(dispatch['source_owned_dispatch_adapters'])
    adapters['bind_current_catalog'] = checked_text(adapters['bind_current_catalog'], {
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':
        '12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'})
    for key, text in adapters.items():
        exec(compile(text, __file__ + '::' + key, 'exec'), ns)
    ns['CATALOG_LOOKUP'], catalogue = ns['bind_current_catalog'](image)
    exec(compile(dispatch['source_owned_measured_macro_body_adapter'], __file__ + '::current-captain1-substitutions', 'exec'), ns)
    pages_env = {**original_pages.__globals__, 'expected_pixels': pixels, 'codes': codes}
    page_adapter = stored['source_owned_target_page_adapter']
    exec(compile(page_adapter, __file__ + '::unchanged-target-complete-pages', 'exec'), pages_env)
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    rows, pictures = [], []
    for group in gloss['groups']:
        for row in group['records']:
            raw = bytes.fromhex(row['source_hex'])
            prefix, body = raw[0], raw[1:]
            assert prefix in actor_ids and body not in ns['CATALOG_LOOKUP']
            assert row['source_complete_preamble_hex'] == '0040ffff00' + bytes([prefix]).hex()
            result = ctx.execute(ns['dispatch'], prefix, body)
            ctx.machines.pop()
            assert result['resolved_actor_ID'] == prefix and result['source_voice_class'] == {1: 1, 16: 1, 18: 0, 113: 0}[prefix]
            boundary = next(b for b in result['boundaries'] if b['kind'] == 'unexecuted-progressive-body')
            assert boundary['text_hex'] == body.hex() and result['registered_catalog_match'] is None
            assert not result['FE_original_null_actor_calls']
            aligned = ctx.execute(pe['expand'], body, prefix)
            ctx.machines.pop()
            assert len(aligned['cases']) == 4 and all(c['output_hex'] == body.hex() for c in aligned['cases'])
            rendered = pages_env['pages'](arm, font, body)
            for page in rendered['pages']:
                plane = bytes.fromhex(page.pop('native_plane_hex'))
                file = ROOT / (row['id'] + f'_page{page["page"]}.bin')
                file.write_bytes(plane)
                page.update(native_plane=str(file), native_plane_sha256=sha(plane))
                picture = Image.new('RGB', (216, 64))
                colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
                picture.putdata([colors[v] for v in plane])
                pictures.append((row['id'] + f' source p{page["page"]}', picture))
            assert rendered['complete_consumed_bytes'] == len(body)
            rows.append(dict(id=row['id'], file_path=row['file_path'], block=row['block'], source_reference=row['source_reference'],
                source_selector=prefix, complete_source_preamble_hex=row['source_complete_preamble_hex'], source_hex=raw.hex(),
                source_0100_ancestors=row['source_0100_ancestors'], original_dispatch=result,
                original_four_alignments=aligned, complete_native_source_display=rendered))
    assert len(rows) == 3 and sum(len(r['original_four_alignments']['cases']) for r in rows) == 12 and not ctx.machines
    page_count = len(pictures)
    for name in name_rows:
        plane = name['reused_current_original_style11_plane']
        pictures.append((f'actor{name["actor_ID"]}: {plane["text"]} (reused)', Image.open(plane['preview']).convert('RGB')))
    sheet = Image.new('RGB', (912, ((len(pictures) + 1) // 2) * 160), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, (label, picture) in enumerate(pictures):
        x, y = index % 2 * 456, index // 2 * 160
        draw.text((x + 3, y + 3), label + ' offline native', fill='white')
        sheet.paste(picture.resize((picture.width * 2, picture.height * 2), Image.Resampling.NEAREST), (x, y + 24))
    sheetfile = ROOT / 'three_complete_clean_source_pages_andone_reused_name.png'
    sheet.save(sheetfile)
    save(ROOT / 'source_display.json', dict(candidate=inp['current_ROM'], candidate_sha256=inp['current_ROM_sha256'],
        ARM9_sha256=sha(arm), font_sha256=sha(font), source_gloss=str(GLOSS), source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_controls=str(CONTROL), source_controls_sha256=sha(CONTROL.read_bytes()), records=rows,
        scoped_clean_current_one_name_andreused_native_consumers=name_rows,
        actual_same_captain1_whole_actors_code_COMMON_andfont_bind_prior_getters_andnameplanes=True,
        source_macro_counts=dict(FI=0, FA=0, FO=0), source_FE_count=0, default_FI6_FA9_FO15=names['measured_default_macro_lengths'],
        default_macro_lengths_are_reused_synthetic_tests_not_new_source_macros_orcustom_names=True,
        no_FE_dispatch_orpanel_calibration_claim=True, target_oracle_binding=oracle, registered_catalogue_binding=catalogue,
        source_owned_dispatch_adapters=adapters, source_owned_macro_body_adapter=dispatch['source_owned_measured_macro_body_adapter'],
        source_owned_progressive_adapter=progressive, source_owned_target_page_adapter=page_adapter,
        complete_native_source_page_count=page_count, review_sheet=dict(path=str(sheetfile), sha256=sha(sheetfile.read_bytes())),
        direct_view_pending=True, current_B52_English_dialogue_bodies_unconsulted=True,
        source_name_editorial_menu_branch_context_current_editorial_actual_andregistered_integration_pending=True,
        offline_native_CPU_tests_not_new_gameplay_all207_names_custom_player_names_ornatural_activation=True,
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [GLOSS, CONTROL, INPUT, START, VIEW, NAMES, OLD_NAMES, SURNAME, DISPATCH, STORED,
            Path('scripts/Hodram_FE_font_oracles_v8315.py'), Path(__file__)]}))
    print(f'B52 source: three dispatches, twelve guarded alignments, {page_count} complete native pages and one bound reused name. Current English unread; direct source view pending.')
