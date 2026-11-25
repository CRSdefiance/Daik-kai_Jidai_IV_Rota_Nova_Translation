"""Reuse 18 exact name planes and render only 13 newly scoped current strings."""
import math
from copy import deepcopy
from pathlib import Path
from types import FunctionType, SimpleNamespace
from PIL import Image, ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.probe_button_prompt_native import machine as paint_machine
from scripts import lil_B207_name_style_v6354d as style
from scripts.shady_man_font_oracles_v6263 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels, raster
from scripts.prove_lil_B208_name_planes_v6405 import codes, original_name_events

ROOT = Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104')
BINDINGS = Path('work/analysis/Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json')
NAMES = Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
PRIOR = Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102/native_name_planes.json')
RELEASE = Path('work/analysis/Hodram_B151_B170_release_verified_20261102/registered_release_verification.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    bound, names, prior = map(load, [BINDINGS, NAMES, PRIOR])
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'))
    assert bound['runtime'] == ctx.receipt() and prior['runtime'] == bound['previous_runtime']
    assert bound['all32_actor_inputs_models_COMMON_font_andname_consumer_dependencies_match']
    inverse = bound['complete_latest_static_data_inverse']
    assert inverse['complete_parent_inverse_exact'] and inverse['all_unowned_bytes_pointer_fields_sections_fonts_andallocations_unchanged']
    assert (inverse['parent_ARM9_sha256'], inverse['target_ARM9_sha256']) == (prior['runtime']['ARM9_sha256'], sha(ctx.arm))
    consumers = [dict(actor_ID=r['actor_ID'], consumer=c['consumer'], text=c['text'], text_hex=c['text_hex'], binding_record=i)
        for i, r in enumerate(bound['records']) for c in r['current_consumers']]
    assert len(consumers) == 64 and len(bound['records']) == 32
    for r in bound['records']:
        assert sha(Path(r['native_proof']).read_bytes()) == r['native_proof_sha256']
    texts = sorted({r['text'] for r in consumers})
    assert all(r['text'].encode('ascii').hex() == r['text_hex'] for r in consumers)
    previous = {r['text']: r for r in prior['planes']}
    sections = MainCodeFile(ctx.arm, BASE).sections
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    def machine(value):
        assert value == ctx.arm
        cpu = paint_machine(value)
        def exact(u, pc, size, _):
            hits = [s for s in owners if s.ramAddress <= pc and pc + size <= s.ramAddress + len(s.data)]
            assert len(hits) == 1
            section = hits[0]
            assert bytes(u.mem_read(pc, size)) == bytes(section.data[pc - section.ramAddress:pc - section.ramAddress + size])
        cpu.hook_add(UC_HOOK_CODE, exact)
        return cpu
    styleproof = FunctionType(style.style_source_proof.__code__, {**style.style_source_proof.__globals__, 'ARM9': sha(ctx.arm)})(ctx.arm)
    oracle = dict(expected_pixels.__globals__)
    exec(compile(PROGRESSIVE_ORACLE_SOURCE, __file__ + '::same-font-oracle', 'exec'), oracle)
    env = {**raster.__globals__, 'machine': machine}
    exec(compile(style.NATIVE_NAME_RASTER_SOURCE, __file__ + '::same-style11', 'exec'), env)
    ROOT.mkdir()
    planes, pictures = [], []
    fresh = reused = 0
    for index, text in enumerate(texts):
        raw = text.encode('ascii')
        if text in previous:
            plane = deepcopy(previous[text])
            pixels = Path(plane['native_plane']).read_bytes()
            assert sha(pixels) == plane['native_plane_sha256'] and sha(Path(plane['preview']).read_bytes()) == plane['preview_sha256']
            plane['exact_previous_plane_reused'] = dict(path=str(PRIOR), sha256=sha(PRIOR.read_bytes()), text=text,
                complete_native_code_font_style_andliteral_dependencies_match=True)
            reused += 1
        else:
            pixels, events, font = env['raster'](ctx.arm, raw)
            assert font == ctx.image.read_file('/GRP/KANJI.FNT')
            assert pixels == oracle['expected_pixels'](ctx.arm, font, events)
            emitted, flushes = original_name_events(events, raw)
            assert emitted == codes(raw)
            assert all(e['kind'] == 'ascii' and e['style'] == 11 and e['y'] == 0 and 0 <= e['x'] and e['x'] + 6 <= 216 for e in events)
            assert max(e['x'] + 6 for e in events) == 6 * (len(raw) + len(raw) % 2) <= 216
            path = ROOT / f'name_{index:02d}.bin'
            path.write_bytes(pixels)
            picture = Image.new('RGB', (216, 64))
            picture.putdata([(65, 53, 42) if v else (250, 245, 223) for v in pixels])
            png = path.with_suffix('.png')
            picture.save(png)
            plane = dict(text=text, native_plane=str(path), native_plane_sha256=sha(pixels), preview=str(png), preview_sha256=sha(png.read_bytes()),
                native_events=events, native_zero_ink_flushes=flushes, complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True,
                style11_proven_progressive_name_consumer=True, full_name_literal_font_test_not_actual_catalogue_UI_layout_approval=True)
            fresh += 1
        picture = Image.open(plane['preview']).convert('RGB')
        pictures.append((text, picture))
        planes.append(plane)
    assert (len(planes), fresh, reused) == (31, 13, 18)
    sheets = []
    for at in range(0, len(pictures), 16):
        part = pictures[at:at + 16]
        sheet = Image.new('RGB', (912, math.ceil(len(part) / 2) * 64), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (text, picture) in enumerate(part):
            x, y = i % 2 * 456, i // 2 * 64
            draw.text((x + 3, y + 2), text + ' native style11', fill='white')
            sheet.paste(picture.crop((0, 0, 216, 16)).resize((432, 32), Image.Resampling.NEAREST), (x, y + 22))
        path = ROOT / f'names_{at // 16 + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), strings=len(part)))
    save(ROOT / 'native_name_planes.json', dict(runtime=ctx.receipt(), bindings=str(BINDINGS), bindings_sha256=sha(BINDINGS.read_bytes()),
        individual_localization_decisions=str(NAMES), individual_localization_decisions_sha256=sha(NAMES.read_bytes()),
        actors=32, consumer_bindings=consumers, current_getters_reused_not_replayed=64, fresh_planes=13, exact_reused_planes=18,
        distinct_current_strings=31, planes=planes, review_sheets=sheets, style_proof=styleproof,
        all_current_names_ASCII_andfull_characters_fit_original216px=True,
        native_style11_full_name_literals_not_catalogue_UI_observation=True,
        no_name_data_change=True, direct_visual_review_pending=True, representative_headers_andEnglish_gameplay_pending=True,
        new_credit=0, new_ROM=False, evidence={str(p): sha(p.read_bytes()) for p in [BINDINGS, NAMES, PRIOR, Path(__file__)]}))
    print('PASS 32 actors / 64 bound consumers / 31 native strings: 13 fresh planes, 18 exact reused. Direct visual review pending.')
