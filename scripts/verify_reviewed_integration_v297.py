"""Fixed allocations and full native expansion/glyphs for the reviewed packet.

Captured player data is reused in a controlled CPU fixture with current code and
pool restored. This is not a new gameplay run or a claim about deep route scenes.
"""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.message_actor_integrity import verify_original_actors
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK
from scripts.prepare_reviewed_names_v297 import DIGEST, ROM, ROOT
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_name_catalog_glyphs_v278 import WIDTH, expected_pixels, raster
from scripts.verify_ordinary_name_fidelity_research import initialized


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fixed_files(prep):
    image = NdsImage.open(ROM)
    assert sha(ROM.read_bytes()) == DIGEST
    source = {path: image.read_file(path) for path in prep['current_source_file_sha256']}
    assert {p: sha(raw) for p, raw in source.items()} == prep['current_source_file_sha256']
    containers = {p: IlnkContainer.parse(raw) for p, raw in source.items()}
    modified = {p: [bytearray(b) for b in c.blocks] for p, c in containers.items()}
    spans, changes = {p: [] for p in source}, []
    for row in prep['records']:
        if row['storage'] != 'fixed':
            continue
        path, ident = row['file_path'], row['id']
        block, index = int(ident.split('_B')[1].split('_')[0]), int(ident.split('_R')[1])
        original = containers[path].blocks[block]
        parts = original.split(b'\0')
        at = sum(len(s) + 1 for s in parts[:index])
        key, target = bytes.fromhex(row['current_key_hex']), bytes.fromhex(row['fixed_target_hex'])
        assert parts[index] == key and len(key) == len(target) and b'\0' not in target
        assert row['native_actor'] is None or key[0] == target[0] == row['native_actor']
        assert all(block != b or at + len(target) <= lo or hi <= at for b, lo, hi in spans[path])
        modified[path][block][at:at + len(target)] = target
        spans[path].append((block, at, at + len(target)))
        changes.append({'file_path': path, 'id': ident, 'block': block, 'native_offset': at,
                        'span_bytes': len(target), 'actor': row['native_actor']})
    targets = {}
    for path, container in containers.items():
        container.blocks = [bytes(b) for b in modified[path]]
        targets[path] = container.to_bytes()
        assert len(targets[path]) == len(source[path])
        for number, (before, after) in enumerate(zip(IlnkContainer.parse(source[path]).blocks, container.blocks, strict=True)):
            assert len(before) == len(after)
            assert all(a == b or any(n == number and lo <= at < hi for n, lo, hi in spans[path])
                       for at, (a, b) in enumerate(zip(before, after, strict=True)))
        (ROOT / (Path(path).name + '.research_only')).write_bytes(targets[path])
    # V275 supplies the pre-alignment NUL ordinals; V296 and this transform keep
    # native object byte positions stable, including both consumed alignment NULs.
    old = NdsImage.open('out/all_routes_combined_v275_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    actors = verify_original_actors({p: old.read_file(p) for p in source}, targets,
                                   {p: clean.read_file(p) for p in source})
    proof = {'records': changes, 'fixed_records': len(changes), 'original_native_actors_checked': actors,
             'all_archive_block_object_and_following_command_addresses_preserved': True,
             'source_file_sha256': {p: sha(raw) for p, raw in source.items()},
             'target_file_sha256': {p: sha(raw) for p, raw in targets.items()}}
    assert len(changes) == 197
    (ROOT / 'fixed_transform_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')


def main(*, root=ROOT, verify_fixed=True):
    prep, plan = read(root / 'preparation.json'), read(root / 'catalog_plan.json')
    if verify_fixed:
        fixed_files(prep)
    arm = (root / 'catalog_arm9_research_only.bin').read_bytes()
    assert sha(arm) == plan['target_arm9_sha256']
    code = MainCodeFile(arm, BASE)
    pool = bytes(code.sections[3].data[:-48])
    contexts, copies, cases, failures, pictures = [], [], [], [], []
    for route, name in enumerate(('rafael', 'hodram', 'lil', 'maria')):
        path = f'/data/SC{route}.DK4'
        fixture = Path('work/analysis/name_editorial_v280/' + (
            'maria_selection_research_only.nds' if name == 'maria' else 'named_catalog_research_only.nds'))
        capture = read(f'work/emulation_v193/name_editorial_v280_{name}/capture_report.json')
        assert capture['ROM_sha256'] == sha(fixture.read_bytes())
        assert capture['cold_boot'] and not capture['savestate_loaded'] and not capture['callback_errors']
        snapshot = capture['read_only_RAM_snapshot']
        ram = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(ram) == 4194304 and sha(ram) == snapshot['sha256']
        cpu = initialized(arm)
        cpu.mem_write(BASE, ram)
        # Captured dynamic player state stays intact; current static instructions,
        # name fields and complete catalog replace the older fixture's code/pool.
        cpu.mem_write(code.sections[0].ramAddress, bytes(code.sections[0].data))
        cpu.mem_write(POOL, pool)
        assert int.from_bytes(cpu.mem_read(ROUTE, 4), 'little') == route
        defaults = {k: expand(cpu, k.encode('ascii')) for k in ('FI', 'FA', 'FO', 'FU')}
        expected_names = (('Rafael', 'Castor'), ('Hodram', 'Bergstrom'), ('Lil', 'Argot'), ('Maria', 'Li'))[route]
        assert defaults['FI'].decode('cp932') == expected_names[0]
        assert defaults['FA'].decode('cp932') == expected_names[1]
        contexts.append({'route': path, 'captured_RAM': snapshot,
                         'controlled_current_code_and_pool_overlay': True,
                         'defaults': {k: v.decode('cp932') for k, v in defaults.items()},
                         'Maria_selection_is_test_only_not_legitimate_unlock': name == 'maria'})
        for row in plan['records']:
            if not row['route_mask'] & (1 << route):
                continue
            key, expected = bytes.fromhex(row['key_hex']), bytes.fromhex(row['target_hex'])
            for macro, value in defaults.items():
                expected = expected.replace(macro.encode('ascii'), value)
            for align in range(4):
                for field in CALLS:
                    source, destination, stop = 0x02430020 + align, 0x02431020, BASE + field + 4
                    cpu.mem_write(0x02430000, b'\xA5' * 640)
                    cpu.mem_write(source, key + b'\0')
                    guard = bytes(cpu.mem_read(0x02430000, 640))
                    cpu.mem_write(destination - 32, b'\xA5' * 576)
                    for reg, value in ((UC_ARM_REG_R0, destination), (UC_ARM_REG_R1, source),
                                       (UC_ARM_REG_R2, 0), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, stop)):
                        cpu.reg_write(reg, value)
                    cpu.emu_start(plan['entry'], stop, count=600000)
                    assert cpu.reg_read(UC_ARM_REG_PC) == stop and cpu.reg_read(UC_ARM_REG_SP) == STACK
                    assert bytes(cpu.mem_read(0x02430000, 640)) == guard
                    assert bytes(cpu.mem_read(destination - 32, 576)) == b'\xA5' * 32 + expected + b'\0' + b'\xA5' * (543 - len(expected))
                    copies.append([path, row['key_hex'], align, field])
        for row in prep['records']:
            if row['file_path'] != path:
                continue
            target = bytes.fromhex(row['fixed_target_hex'] if row['storage'] == 'fixed' else row['target_hex'])
            if row['native_actor'] is not None:
                assert target[0] == row['native_actor']
                target = target[1:]
            expected = target
            for macro, value in defaults.items():
                expected = expected.replace(macro.encode('ascii'), value)
            try:
                output = expand(cpu, target)
                assert output == expected
                height = 96 if row['profile']['max_lines'] == 5 else 64
                pixels, events, font = raster(arm, output, canvas_height=height)
                assert pixels == expected_pixels(arm, font, events, canvas_height=height)
                semantic = [('ascii', ord(c)) if len(c.encode('cp932')) == 1 else
                            ('cp932', int.from_bytes(c.encode('cp932'), 'big'))
                            for c in output.decode('cp932') if c not in ' \n']
                assert [(e['kind'], e['code']) for e in events if e['code'] != 32] == semantic
                lines = sorted({e['y'] for e in events if e['code'] != 32})
                assert lines == list(range(0, len(lines) * 16, 16)) and len(lines) <= row['profile']['max_lines']
                image = Image.new('RGB', (WIDTH, height))
                image.putdata([(239, 232, 201) if p == 0 else (0, 8, 0) if p == 1 else (98, 97, 98) for p in pixels])
                pictures.append((path + ' ' + row['id'], image.resize((WIDTH * 2, height * 2), Image.Resampling.NEAREST)))
                cases.append({'file_path': path, 'id': row['id'], 'storage': row['storage'],
                              'expanded_body_hex': output.hex(), 'glyphs': len(semantic), 'visible_rows': lines,
                              'complete_native_ink_shadow_cells_bounds_first_final_letters_verified': True,
                              'input_output_canvas_header_and_ABI_guards_pass': True})
            except (AssertionError, ValueError) as error:
                failures.append({'file_path': path, 'id': row['id'], 'error': str(error)})
        assert bytes(cpu.mem_read(POOL, len(pool))) == pool
        print(f'{name}: {sum(c["file_path"] == path for c in cases)} full bodies verified', flush=True)
    sheets = []
    for start in range(0, len(pictures), 8):
        sheet = Image.new('RGB', (WIDTH * 4, 4 * 218), '#333333')
        draw = ImageDraw.Draw(sheet)
        for number, (label, image) in enumerate(pictures[start:start + 8]):
            x, y = number % 2 * WIDTH * 2, number // 2 * 218
            draw.text((x + 3, y + 4), label, fill='white')
            sheet.paste(image, (x, y + 24))
        output = root / f'native_full_review_{start // 8:02d}.png'
        sheet.save(output)
        sheets.append(str(output))
    proof = {'format': 'dk4-reviewed-full-route-native-integration-v297', 'ARM9_sha256': sha(arm),
             'preparation_sha256': sha((root / 'preparation.json').read_bytes()),
             'contexts': contexts, 'native_full_catalog_copies': copies, 'cases': cases, 'failures': failures,
             'sheets': sheets, 'all444_complete_body_glyphs_pass': len(cases) == 444 and not failures,
             'no_getter_or_macro_bridges': True, 'visual_sheet_review_pending': True,
             'scope': 'Controlled current native code with captured route player data, not an actual new gameplay run.',
             'full_registered_release_and_gameplay_tests_pending': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (root / 'full_native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} complete bodies; {len(copies)} native catalog copies; {len(failures)} failures.', flush=True)
    for failure in failures[:10]:
        print(failure, flush=True)
    assert not failures and len(cases) == 444


if __name__ == '__main__':
    main()
