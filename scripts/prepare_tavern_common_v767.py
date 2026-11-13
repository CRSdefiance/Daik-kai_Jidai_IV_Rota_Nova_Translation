"""Repack31 fully native-reviewed Tavern entries within the existing COMMON blocks."""

import importlib
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_conversations_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
import dk4tool.script.common_message_table as parser_module
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_release_v767')
RESEARCH = Path('work/analysis/tavern_coordinates_v766')
MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v3.json')
CURRENT = Path('out/all_routes_combined_v762_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'common_repack_plan.json').exists()
    native = read(RESEARCH / 'verification.json')
    assert native['complete_native_layouts'] == 38957 and native['all94_coordinate_pairs_intact']
    assert not native['native_bank_writes'] and len(native['complete_font_planes']) == 166
    assert read(RESEARCH / 'actual_leader_layout_matrix.json')['count'] == 14400
    assert read(RESEARCH / 'coordinate_buffer_contracts.json')['count'] == 104
    assert read(RESEARCH / 'visual_review.json')['all162_unmodified_font_planes_byte_identical_to_inspected_set']
    assert native['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    rom = NdsImage.open(CURRENT)
    assert sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    runtime, proof = owned.runtime_transform(arm)
    doc = read(MANUSCRIPT)
    before = parser_module.common_message_entries(common, arm, clean=False)
    for row in doc['records']:
        assert before[row['message_id']].text.hex() == row['current_text_hex']
        assert row['runtime_argument_contract'] == owned.ARGUMENTS.get(row['message_id'], [])
    authored = {r['message_id']: owned.compile_text(r) for r in doc['records']}
    c, a, fields, mapping = owned.plan(common, runtime, authored)
    digest = sha(a[parser_module.DIRECTORY_OFFSET:parser_module.TABLE_OFFSET])
    parser = Path(parser_module.__file__); text = parser.read_text(encoding='utf-8')
    assert digest not in text
    snapshot = ROOT / 'common_message_table_before_v767.py'
    assert not snapshot.exists(); snapshot.write_text(text, encoding='utf-8')
    marker = 'RELOCATED_DIRECTORY_HASHES = frozenset({\n'
    assert text.count(marker) == 1
    parser.write_text(text.replace(marker, marker + f'    # V767: exact1813 selections164-1976;two opaque copy spans preserved.\n    "{digest}",\n', 1), encoding='utf-8')
    importlib.reload(parser_module)
    after = parser_module.common_message_entries(c, a, clean=False)
    assert all(b.text == authored.get(x.message_id, x.text) for x, b in zip(before, after, strict=True))
    old, new = [IlnkContainer.parse(x).blocks for x in (common, c)]
    assert all(x == y for k, (x, y) in enumerate(zip(old, new, strict=True)) if k not in range(2, 21))
    opaque = []
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert old[x.block][x.block_offset:x.copy_end] == new[y.block][y.block_offset:y.copy_end]
        opaque.append({'id': n, 'complete_source_span_hex': old[x.block][x.block_offset:x.copy_end].hex(),
                       'source_text_hex': x.text.hex(), 'target_text_hex': y.text.hex()})
    restored = bytearray(a)
    for at, length in fields: restored[at:at + length] = runtime[at:at + length]
    assert bytes(restored) == runtime and len(a) == len(arm)
    (ROOT / 'research_COMMON.bin').write_bytes(c); (ROOT / 'research_combined_ARM9.bin').write_bytes(a)
    save(ROOT / 'common_repack_plan.json', {'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': digest,
        'metadata_fields': fields, 'complete1813_selection_map': mapping,
        'all3637_unselected_strings_exact': True, 'all22_other_blocks_exact': True,
        'all_opaque_bytes_and_native_spans_preserved': opaque,
        'only_verified_NUL_ASCII_space_gaps_discarded': True, 'metadata_restores_exact_runtime': True,
        'parser_before_sha256': sha(snapshot.read_bytes()), 'parser_after_sha256': sha(parser.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_emitted': True})
    print(f'31 Tavern paragraphs repacked;3637 other strings exact;directory {digest}.', flush=True)


if __name__ == '__main__': main()
