"""Use current Rafael getters and the proven native style11 name-plane renderer."""
from pathlib import Path
from types import FunctionType, SimpleNamespace
from PIL import Image, ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts import check_hodram_B171_B190_scoped_names as proven

ROOT = Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104')
BINDINGS = Path('work/analysis/Rafael_early_tutorial_B42_B43_names_20261104/names.json')
RELEASE = Path('work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json')
STARTUP = Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=0)
    prior = load(BINDINGS)
    assert prior['actors'] == [0, 4, 5, 6]
    assert prior['runtime']['ARM9_sha256'] == sha(ctx.arm) and prior['runtime']['COMMON_sha256'] == sha(ctx.common)
    env = {**original_names.__globals__, 'ACTORS': prior['actors']}
    exec(compile(prior['source_owned_current_adapter'], __file__ + '::same-readonly-name-getters-current-captain0', 'exec'), env)
    current = ctx.execute(env['names'])
    consumers = [{k: r[k] for k in ['actor_ID', 'consumer', 'text', 'text_hex']} for r in current['rows']]
    assert consumers == [{k: r[k] for k in ['actor_ID', 'consumer', 'text', 'text_hex']} for r in prior['current_names']['rows']]
    assert len(consumers) == 8
    sections = MainCodeFile(ctx.arm, BASE).sections
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    def machine(value):
        assert value == ctx.arm
        cpu = proven.paint_machine(value)
        def exact(u, pc, size, _):
            hits = [s for s in owners if s.ramAddress <= pc and pc + size <= s.ramAddress + len(s.data)]
            assert len(hits) == 1
            section = hits[0]
            assert bytes(u.mem_read(pc, size)) == bytes(section.data[pc - section.ramAddress:pc - section.ramAddress + size])
        cpu.hook_add(UC_HOOK_CODE, exact)
        return cpu
    styleproof = FunctionType(proven.style.style_source_proof.__code__,
        {**proven.style.style_source_proof.__globals__, 'ARM9': sha(ctx.arm)})(ctx.arm)
    oracle = dict(proven.expected_pixels.__globals__)
    exec(compile(proven.PROGRESSIVE_ORACLE_SOURCE, __file__ + '::same-independent-font-oracle', 'exec'), oracle)
    renderer = {**proven.raster.__globals__, 'machine': machine}
    exec(compile(proven.style.NATIVE_NAME_RASTER_SOURCE, __file__ + '::same-source-proven-style11', 'exec'), renderer)
    ROOT.mkdir()
    planes = []
    sheet = Image.new('RGB', (912, 128), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, text in enumerate(sorted({r['text'] for r in consumers})):
        raw = text.encode('ascii')
        pixels, events, font = renderer['raster'](ctx.arm, raw)
        assert font == ctx.image.read_file('/GRP/KANJI.FNT')
        assert pixels == oracle['expected_pixels'](ctx.arm, font, events)
        emitted, flushes = proven.original_name_events(events, raw)
        assert emitted == proven.codes(raw)
        assert all(e['kind'] == 'ascii' and e['style'] == 11 and e['y'] == 0 and 0 <= e['x'] and e['x'] + 6 <= 216 for e in events)
        assert max(e['x'] + 6 for e in events) == 6 * (len(raw) + len(raw) % 2) <= 216
        path = ROOT / f'name_{index}.bin'
        path.write_bytes(pixels)
        picture = Image.new('RGB', (216, 64))
        picture.putdata([(65, 53, 42) if v else (250, 245, 223) for v in pixels])
        png = path.with_suffix('.png')
        picture.save(png)
        x, y = index % 2 * 456, index // 2 * 64
        draw.text((x + 3, y + 2), text + ' native style11', fill='white')
        sheet.paste(picture.crop((0, 0, 216, 16)).resize((432, 32), Image.Resampling.NEAREST), (x, y + 22))
        planes.append(dict(text=text, native_plane=str(path), native_plane_sha256=sha(pixels), preview=str(png), preview_sha256=sha(png.read_bytes()),
            native_events=events, native_zero_ink_flushes=flushes, complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True))
    assert len(planes) == 4
    png = ROOT / 'four_tutorial_names.png'
    sheet.save(png)
    save(ROOT / 'native_name_planes.json', dict(runtime=ctx.receipt(), consumer_bindings=consumers, native_getters=current,
        clean_name_binding=str(BINDINGS), clean_name_binding_sha256=sha(BINDINGS.read_bytes()),
        clean_source_getters_reused=8, fresh_current_captain0_getters=8, fresh_name_planes=4, planes=planes, style_proof=styleproof,
        review_sheets=[dict(path=str(png), sha256=sha(png.read_bytes()), strings=4)],
        all_current_names_ASCII_andfull_characters_fit_original216px=True,
        style11_full_name_literal_test_not_actual_catalogue_UI_layout_orB42_B43_gameplay=True,
        no_name_data_change=True, direct_visual_review_pending=True, actual_gameplay=False, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [BINDINGS, RELEASE, STARTUP, Path(proven.__file__), Path(__file__)]}))
    print('Four names/eight fresh current Rafael getters/four native planes pass; direct view pending.')
