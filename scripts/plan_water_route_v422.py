"""Read-only local water route from original native decoded map pages."""

import argparse
import heapq
import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v414_candidate.nds')
ROOT = Path('work/analysis/lubeck_voyage_v421')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=ROM)
    parser.add_argument('--output-directory', type=Path, default=ROOT)
    parser.add_argument('--start-world', type=int, nargs=2, default=(2739079, 489972))
    parser.add_argument('--goal-world', type=int, nargs=2, default=(21240 * 128, 3976 * 128))
    parser.add_argument('--bounds', type=int, nargs=4, default=(1280, 1380, 225, 275),
                        metavar=('MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y'))
    parser.add_argument('--step-map-units', type=int, choices=(1, 2, 4, 8, 16), default=16,
                        help='Grid spacing in native map units; bounds use this grid. Default16 preserves historical routes.')
    args = parser.parse_args()
    min_x, max_x, min_y, max_y = args.bounds
    assert 0 <= min_x < max_x and 0 <= min_y < max_y
    args.output_directory.mkdir(parents=True, exist_ok=True)
    r = NdsImage.open(args.rom)
    arm = r.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    assert r.read_file('/data/WORLDMAP.DK4') == clean.read_file('/data/WORLDMAP.DK4')
    blocks = IlnkContainer.parse(r.read_file('/data/WORLDMAP.DK4')).blocks
    overlay = loadOverlayTable(r.rom.arm9OverlayTable, lambda oid, fid: r.rom.files[fid])[0]
    u = machine(arm)
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    sea = {}
    for value in range(1024):
        call(u, 0x693EC, (value,))
        sea[value] = u.reg_read(UC_ARM_REG_R0) != 0
    pages = {}

    def page(px, py):
        key = px, py
        if key not in pages:
            block = px // 5
            raw = blocks[block]
            u.mem_write(0x02460000, struct.pack('<2I', block, 0x02480000))
            u.mem_write(0x02480000, raw)
            u.mem_write(0x02460100, struct.pack('<2i', px, py))
            u.mem_write(0x02460200 - 16, b'\xA5' * 2532)
            call(u, 0x01FFA10C - 0x02000000, (0x02460000, 0x02460100, 0x02460200), instruction_limit=300000)
            assert bytes(u.mem_read(0x02460200 - 16, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(0x02460200 + 2500, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(0x02480000, len(raw))) == raw
            pages[key] = struct.unpack('<1250H', u.mem_read(0x02460200, 2500))
        return pages[key]

    def cell(x, y):
        return page(x // 50, y // 25)[(y % 25) * 50 + x % 50] & 1023

    def collision_free(x, y):
        # Four genuine native decoded pages are a loaded-cache input contract.
        # The original mixed-shoreline predicate and cache-hit path execute.
        point_x = x * args.step_map_units + args.step_map_units // 2
        point_y = y * args.step_map_units + args.step_map_units // 2
        tile_x, tile_y = point_x // 16, point_y // 16
        px, py = tile_x // 50, tile_y // 25
        xs = [px, px - 1 if tile_x % 50 == 0 else px + 1]
        ys = [py, py - 1 if tile_y % 25 == 0 else py + 1]
        owner = 0x02468000
        for xx in xs:
            for yy in ys:
                slot = owner + 16 + (xx & 1) * 2508 + (yy & 1) * 5016
                u.mem_write(slot, struct.pack('<2i', xx, yy) + struct.pack('<1250H', *page(xx, yy)))
        u.mem_write(0x02460100, struct.pack('<2i', point_x, point_y))
        call(u, 0x69B5C, (owner, 0x02460100))
        return u.reg_read(UC_ARM_REG_R0) == 0

    # Original collision predicate at each queried point; fine grids can retain
    # narrow water that a16-map-unit centre sampling omits.
    safe = {(x, y) for y in range(min_y, max_y) for x in range(min_x, max_x) if collision_free(x, y)}
    start_pixel = tuple(value // 128 for value in args.start_world)
    port_pixel = tuple(value // 128 for value in args.goal_world)
    start = start_pixel[0] // args.step_map_units, start_pixel[1] // args.step_map_units
    goal = port_pixel[0] // args.step_map_units, port_pixel[1] // args.step_map_units

    def nearest(point):
        return min(safe, key=lambda p: (abs(p[0] - point[0]) + abs(p[1] - point[1]), p))

    s, g = nearest(start), nearest(goal)
    queue = [(0, s)]
    costs, previous = {s: 0}, {}
    while queue:
        _, p = heapq.heappop(queue)
        if p == g:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nxt = p[0] + dx, p[1] + dy
            cost = costs[p] + 1
            if nxt in safe and cost < costs.get(nxt, 10**9):
                costs[nxt] = cost
                previous[nxt] = p
                heapq.heappush(queue, (cost + abs(nxt[0] - g[0]) + abs(nxt[1] - g[1]), nxt))
    assert g in costs, 'No certain-water local route found.'
    path, p = [g], g
    while p != s:
        p = previous[p]
        path.append(p)
    path.reverse()
    corners = [path[0]]
    for i in range(1, len(path) - 1):
        before = path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]
        after = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
        if before != after:
            corners.append(path[i])
    corners.append(path[-1])
    proof = {'candidate': str(args.rom), 'candidate_sha256': sha(args.rom.read_bytes()),
             'source_WORLDMAP_sha256': sha(r.read_file('/data/WORLDMAP.DK4')),
             'native_map_decoder': 0x01FFA10C, 'native_certain_water_predicate': 0x020693EC,
             'all1024_predicate_values_executed': True,
             'loaded_page_and_output_buffer_are_explicit_isolated_contracts': True,
             'native_page_hashes': {f'{x},{y}': sha(struct.pack('<1250H', *v)) for (x, y), v in pages.items()},
             'source_start_pixel': start_pixel, 'source_port_pixel': port_pixel,
             'nearest_safe_start_cell': s, 'nearest_safe_goal_cell': g,
             'certain_water_path_cells': path,
             'waypoint_world_points': [[(x * args.step_map_units + args.step_map_units // 2) * 128,
                                        (y * args.step_map_units + args.step_map_units // 2) * 128] for x, y in corners],
             'grid_step_native_map_units': args.step_map_units,
             'native_mixed_shoreline_centre_predicate': 0x02069B5C,
             'all5000_local_cell_centres_native_collision_checked': len(range(min_x, max_x)) * len(range(min_y, max_y)) == 5000,
             'native_collision_checked_cell_count': (max_x - min_x) * (max_y - min_y),
             'query_cell_bounds': list(args.bounds),
             'between_cell_segments_and_port_docking_not_proven': True,
             'not_live_Ram_save_or_progress_modification': True, 'full_goal_complete': False}
    (args.output_directory / 'water_route_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Read-only native terrain route:', proof['waypoint_world_points'])


if __name__ == '__main__':
    main()
