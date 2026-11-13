"""Open navigator selection for a real room with an available officer."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_room_gender_v694 import ROOT, Observer
from scripts.run_village_visits_v664 import CAP
from scripts.trace_deck_gender_v692 import DONOR_HASHES, DONORS
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v692_candidate.nds')


def prepare():
    ROOT.mkdir()
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in ('work/clean.nds', ROM)]
    targets = []
    for pc, name in ((0x0209C244, 'cast_done'), (0x0209C260, 'room_done'),
        (0x020157D8, 'gender_entry'), (0x02015848, 'raw_gender'), (0x02015854, 'identity'),
        (0x020158DC, 'gender_ready'), (0x0209C27C, 'after_gender_or_bypass')):
        offset = pc - 0x02000000
        assert arms[0][offset:offset + 4] == arms[1][offset:offset + 4]
        word = struct.unpack_from('<I', arms[0], offset)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'CPSR_cpu_prefix_offset': 80, 'original_class': '18CDeckPersonnelView',
        'cast_result_register': 7, 'associated_parent_field': 0x3DC,
        'actual_room_lookup': 0x0201BAB4, 'room_definition_field_argument': 0x6C,
        'a_null_lookup_is_an_original_bypass_not_an_observer_error': True})
    scratch = ROOT / 'prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', read(ROOT / 'source_contract.json'))
    old = checks.ROOT
    checks.ROOT = scratch
    try:
        checks.main()
    finally:
        checks.ROOT = old
    assert len(read(scratch / 'native_prefix_controls.json')['native_host_cases']) == 35
    inputs = [r for r in read('work/analysis/deck_gender_v692/unassigned_inputs.json') if r['start'] <= 7201]
    inputs += [{'start': 7601, 'duration': 8, 'buttons': ['B']},
        {'start': 8001, 'duration': 8, 'touch': [20, 65]},
        {'start': 8401, 'duration': 8, 'buttons': ['A']}]
    inputs += [{'start': f, 'duration': 8, 'buttons': [key]} for f, key in (
        (8801, 'RIGHT'), (9201, 'X'), (9601, 'DOWN'), (10001, 'A'),
        (10401, 'UP'), (10801, 'A'), (11201, 'RIGHT'), (11601, 'RIGHT'),
        (12001, 'LEFT'), (12401, 'LEFT'), (12801, 'B'))]
    save(ROOT / 'inputs.json', inputs)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('work/clean.nds'),
             Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donors': {n: {'path': str(p), 'sha256': DONOR_HASHES[n]} for n, p in DONORS.items()},
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_room_gender_v694.py').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V693 original clock/DMA full same-frame proof recorded',
        'full_goal_complete': False})
    print('V694 actual parent/room branches,35 native controls and ordinary room-selection schedule pinned.', flush=True)


def run(case, donor, baseline):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['producer_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['observer_sha256'] == sha(Path('scripts/observe_room_gender_v694.py').read_bytes())
    assert pre['inputs_sha256'] == sha((ROOT / 'inputs.json').read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert sha(DONORS[donor].read_bytes()) == DONOR_HASHES[donor]
    folder = CAP / ('room_gender_v694_' + case)
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'donor': donor, 'baseline': baseline,
        'producer_sha256': pre['producer_sha256'], 'observer_sha256': pre['observer_sha256'],
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'normal_menu_duty_changes_no_live_RAM_code_or_location_fixture': True,
        'historical_Maria_selection_unlock_not_earned': donor == 'maria'})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if not baseline and str(path).lower().endswith('desmume_libretro.dll'):
            tracer = Observer(core, folder)
            tracer.install()
            installed.append(tracer)
            original = core.retro_run
            original.restype = None

            def advance():
                tracer.header[0] += 1
                original()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    frames = (1, 60, 180, 1600, *range(2000, 13201, 400))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '13200', '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen',
        '--battery-save', str(DONORS[donor]), '--capture-every', '999999',
        '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for tracer in installed:
            tracer.close()
    for tracer in installed:
        tracer.save()
    print('V694 room-selection capture terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case')
    parser.add_argument('--donor', choices=DONORS)
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        run(args.case, args.donor, args.baseline)
