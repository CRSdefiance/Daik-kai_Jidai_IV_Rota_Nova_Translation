"""Repack complete selections for the18 reviewed service entries, no ROM."""

import importlib
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import port_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
import dk4tool.script.common_message_table as parser_module
from scripts.review_port_services_v761 import CURRENT, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/port_services_v762')


def main():
    native = read(ROOT / 'owned_native_verification.json')
    assert native['all40_complete_layout_font_planes_identical_to_reviewed_research']
    assert native['all1124_prior_Yard_outputs_and36680_dispatch_cases_pass']
    assert not native['writes_into_all_four_immutable_banks']
    rom = NdsImage.open(CURRENT); common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    runtime, proof = owned.runtime_transform(arm)
    authored = {r['message_id']: owned.compile_text(r) for r in read(MANUSCRIPT)['records']}
    c, a, fields, mapping = owned.plan(common, runtime, authored)
    before = parser_module.common_message_entries(common, arm, clean=False)
    digest = sha(a[parser_module.DIRECTORY_OFFSET:parser_module.TABLE_OFFSET])
    parser = Path(parser_module.__file__)
    text = parser.read_text(encoding='utf-8')
    assert digest not in text
    snapshot = ROOT / 'common_message_table_before_v762.py'
    assert not snapshot.exists(); snapshot.write_text(text, encoding='utf-8')
    addition = ('    # V762: exact1549 selections164-1712;18 reviewed Port/service replies.\n'
        f'    "{digest}",\n')
    marker = 'RELOCATED_DIRECTORY_HASHES = frozenset({\n'
    assert text.count(marker) == 1
    parser.write_text(text.replace(marker, marker + addition, 1), encoding='utf-8')
    importlib.reload(parser_module)
    after = parser_module.common_message_entries(c, a, clean=False)
    assert all(b.text == authored.get(x.message_id, x.text) for x, b in zip(before, after, strict=True))
    old, new = [IlnkContainer.parse(x).blocks for x in (common, c)]
    assert all(x == y for k, (x, y) in enumerate(zip(old, new, strict=True)) if k not in range(2, 19))
    restored = bytearray(a)
    for at, length in fields: restored[at:at + length] = runtime[at:at + length]
    assert bytes(restored) == runtime and len(a) == len(arm)
    (ROOT / 'research_COMMON.bin').write_bytes(c); (ROOT / 'research_combined_ARM9.bin').write_bytes(a)
    save(ROOT / 'common_repack_plan.json', {'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': digest,
        'metadata_fields': fields, 'complete1549_selection_map': mapping,
        'all3650_unselected_complete_strings_exact': True, 'all24_other_blocks_and_packed19_onward_exact': True,
        'only_verified_NUL_ASCII_space_gaps_discarded': True, 'all_metadata_restores_exact_runtime_component': True,
        'monotonic_one_exact_digest_parser_addition_only': True, 'parser_before_sha256': sha(snapshot.read_bytes()),
        'parser_after_sha256': sha(parser.read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'no_ROM_emitted': True, 'all_copies_registered_integration_and_gameplay_pending': True})
    print(f'18 paragraphs in existing17 native blocks;3650 other strings and24 blocks exact;directory {digest}.', flush=True)


if __name__ == '__main__': main()
