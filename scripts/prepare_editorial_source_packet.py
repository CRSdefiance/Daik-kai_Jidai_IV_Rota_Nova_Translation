"""Reusable clean-only whole-scene intake; no English draft or completion approval."""
import argparse
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--route', type=int, choices=range(4), required=True)
    ap.add_argument('--blocks', type=int, nargs='+', required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists() and len(set(args.blocks)) == len(args.blocks)
    clean_path = Path('work/clean.nds')
    digest = sha(clean_path.read_bytes())
    assert digest == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image = NdsImage.open(clean_path)
    path = f'/data/SC{args.route}.DK4'
    archive, arm = image.read_file(path), image.read_file('/__arm9__.bin')
    bank = IlnkContainer.parse(archive).blocks
    inventory, _, _ = scoped_inventory()
    groups = []
    for number in args.blocks:
        block = bank[number]
        commands, speeches = inventory(arm, block)
        records = []
        for command in speeches:
            at = command['offset'] + 5
            raw = block[at:block.index(0, at + 1)]
            index = block[:at].count(b'\0')
            try:
                japanese, error = raw[1:].decode('cp932'), None
            except UnicodeDecodeError as exc:
                japanese, error = None, str(exc)
            records.append(dict(id=f'DK4_MES_B{number:02d}_R{index:04d}', file_path=path,
                block=number, source_selector=raw[0], source_hex=raw.hex(),
                source_complete_preamble_hex=block[at - 5:at + 1].hex(),
                source_reference=dict(file_path=path, block=number, offset=at,
                                      header_offset=at - 5, record_index=index, length=len(raw)),
                source_Japanese=japanese, source_decode_error=error,
                source_0100_ancestors=command['ancestor_0100_offsets'],
                native_extent=command['native_extent'],
                source_macros={m.decode(): raw[1:].count(m) for m in (b'FI', b'FA', b'FO')},
                source_preamble_andname_consumer_approval_not_inferred=True,
                earlier_English_unconsulted=True, source_context_localization_formatting_gates_pending=True))
        groups.append(dict(block=number, file_path=path, clean_block_hex=block.hex(),
                           clean_block_sha256=sha(block), all_source_commands=commands, records=records))
    args.out.mkdir(parents=True)
    save(args.out / 'clean_source_packet.json', dict(source_ROM=str(clean_path), source_ROM_sha256=digest,
        source_archive_sha256=sha(archive), source_ARM9_sha256=sha(arm), route=args.route,
        file_path=path, groups=groups, records=sum(len(g['records']) for g in groups),
        clean_only_no_prior_English_ornew_editorial_credit=True,
        conditional_membership_is_structural_not_natural_activation=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Clean-only source intake:', sum(len(g['records']) for g in groups), 'speeches in', len(groups), 'whole blocks.')


if __name__ == '__main__':
    main()
