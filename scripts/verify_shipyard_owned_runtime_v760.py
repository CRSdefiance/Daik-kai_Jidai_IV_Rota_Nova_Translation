"""Execute the actual owned-placement component, with constant-bank write watch."""

from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch import shipyard_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, machine
from scripts.review_shipyard_editorial_v759 import CURRENT, NUMERIC_RAM
import scripts.probe_shipyard_runtime_v759 as prototype
import scripts.verify_shipyard_research_v759 as prior_verifier
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shipyard_storage_v760/native_owned')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    target, plan = owned.runtime_transform(source)
    assert target == Path('work/analysis/shipyard_storage_v760/research_ARM9.bin').read_bytes()
    old_matrix = read('work/analysis/shipyard_editorial_v759/typed_literal_runtime_RESEARCH/native_layout_matrix.json')
    assert old_matrix['count'] == 1124 and old_matrix['findings_count'] == 0
    writes, initialized_machines = [], []
    def load(unused_arm, unused_blobs):
        u = machine(target)
        u.mem_write(BASE, NUMERIC_RAM.read_bytes())
        # Restore only declared immutable main-section patches over the exact
        # captured V758 initialized state. New ITCM loaded by machine() remains.
        for patch in plan['patches']:
            if patch['section'] == 0:
                old = bytes.fromhex(patch['source_hex'])
                assert bytes(u.mem_read(patch['address'], len(old))) == old
                u.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))
        def watch(cpu, kind, at, size, value, unused):
            if any(at < hi and at + size > lo for lo, hi in owned.BANKS):
                writes.append([at, size, value])
                raise AssertionError(f'Native code wrote immutable source bank at{at:#x}')
        u.hook_add(UC_HOOK_MEM_WRITE, watch)
        initialized_machines.append(True)
        return u
    # Reuse frozen verification logic, injecting the real component and its
    # symbol locations only within this disposable verifier process.
    prototype.loaded = load
    prototype.LITERAL = owned.LITERAL
    prior_verifier.loaded = load
    prior_verifier.QUANTITY = owned.QUANTITY
    prior_verifier.DEST = ROOT
    dispatch = prototype.dispatch_cases(source, {})
    buffers = prior_verifier.quantity_buffer_contract(source, {})
    fragments = prior_verifier.source_copy_arguments(source, {})
    inherited = prior_verifier.inherited(source, {})
    print('Owned code dispatch, complete RAM-buffer, actual numeric-call fragments and inherited outputs pass.', flush=True)
    doc = read('translations/shipyard_editorial_manuscript_v2.json')
    paragraphs = {r['message_id']: b' ' + r['english'].removesuffix('{PAD}').encode('ascii') for r in doc['records']}
    checks, u = [], load(source, {})
    for index, old in enumerate(old_matrix['cases']):
        if index % 64 == 0:
            u = load(source, {})
        n = old['id']
        row = prototype.layout(u, paragraphs[n], n, tuple(bytes.fromhex(v) for v in old['values_hex']))
        assert row == old, (n, row, old)
        checks.append(row)
    fonts = prior_verifier.font_planes(target, checks)
    prior_fonts = read('work/analysis/shipyard_editorial_v759/typed_literal_runtime_RESEARCH/verification.json')['full_font_planes']
    assert len(fonts) == len(prior_fonts) == 68
    assert [r['sha256'] for r in fonts] == [r['sha256'] for r in prior_fonts]
    assert writes == []
    report = {'source_ARM9_sha256': sha(source), 'owned_runtime_ARM9_sha256': sha(target),
        'runtime_plan': plan, 'dispatch': dispatch, 'all77_complete_RAM_buffer_comparisons': buffers,
        'all24_original_numeric_call_and_copy_fragments': fragments, 'all180_complete_inherited_outputs': inherited,
        'all1124_complete_native_layouts_equal_verified_prototype': checks,
        'all68_complete_font_planes_equal_independent_rasters_and_prior_reviewed_previews': fonts,
        'all_initialized_RAM_source_patch_spans_match_original_file_before_install': True,
        'constant_bank_writes': writes, 'write_watched_loaded_machines': len(initialized_machines),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'scope': 'Original native execution with owned component code and initialized V758 RAM. No playable ROM, complete source-table repack, DS startup/loading or actual Yard scene verification yet.'}
    save(ROOT / 'verification.json', report)
    print(f'Owned placement: {len(checks)} native layouts, {len(fonts)} independent full font planes; zero const-bank writes. No ROM built.', flush=True)


if __name__ == '__main__':
    main()
