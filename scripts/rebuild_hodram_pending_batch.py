"""Materialize the reviewed 224 records in a research image, with exact inverses."""
import argparse
from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild import rebuild_block
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    manuscript = Path('translations/hodram_B61_B70_editorial_manuscript_v2.json')
    plans = Path('work/analysis/Hodram_B61_B70_glyphs_20261101/automatic_plans.json')
    packet_path = Path('work/analysis/Hodram_B61_B70_current_v8885/current_effective.json')
    doc, layout, packet = map(load, (manuscript, plans, packet_path))
    assert layout['manuscript_sha256'] == sha(manuscript.read_bytes())
    assert len(doc['records']) == len(layout['records']) == 224 and not layout['failures']
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    archive = image.read_file(doc['file_path'])
    assert sha(arm) == doc['current_ARM9_sha256']
    assert sha(archive) == doc['current_archive_sha256'] == packet['current_archive_sha256']
    container = IlnkContainer.parse(archive)
    assert len(container.blocks) == 325
    inventory, _, _ = scoped_inventory()
    compiled = {r['id']: r for r in layout['records']}
    blocks = list(container.blocks)
    args.out.mkdir(parents=True)
    groups = []
    for group in packet['groups']:
        block = group['block']
        current, clean = blocks[block], bytes.fromhex(group['clean_block_hex'])
        assert current.hex() == group['current_block_hex'] and sha(current) == group['current_block_sha256']
        assert sha(clean) == group['clean_block_sha256']
        assert inventory(arm, current)[0] == group['all_current_commands']
        assert inventory(arm, clean)[0] == group['all_source_commands']
        records = [r for r in doc['records'] if r['block'] == block]
        target, proof = rebuild_block(arm, clean, current, records, compiled, inventory)
        blocks[block] = target
        path = args.out / f'SC1_B{block}_RESEARCH_ONLY.bin'
        path.write_bytes(target)
        groups.append(dict(block=block, file_path=doc['file_path'], current_sha256=sha(current),
                           clean_sha256=sha(clean), target_sha256=sha(target), target_block=str(path),
                           current_bytes=len(current), target_bytes=len(target), **proof))
    expected = list(range(61, 71))
    assert [g['block'] for g in groups] == expected
    result = IlnkContainer(blocks).to_bytes()
    parsed = IlnkContainer.parse(result)
    assert [i for i, (a, b) in enumerate(zip(container.blocks, parsed.blocks, strict=True)) if a != b] == expected
    inverse = list(parsed.blocks)
    for number in expected:
        inverse[number] = container.blocks[number]
    assert IlnkContainer(inverse).to_bytes() == archive
    planned = deepcopy(image)
    planned.replace_file(doc['file_path'], result)
    assert [p for _, p, data in image.iter_files() if planned.read_file(p) != data] == [doc['file_path']]
    assert all(planned.read_file(p) == data for p, data in image.iter_components())
    restored = deepcopy(planned)
    restored.replace_file(doc['file_path'], archive)
    assert bytes(restored.rom.save()) == bytes(image.rom.save())
    archive_path = args.out / 'SC1_B61_B70_RESEARCH_ONLY.DK4'
    archive_path.write_bytes(result)
    research = args.out / 'Hodram_B61_B70_RESEARCH_ONLY.nds'
    research.write_bytes(bytes(planned.rom.save()))
    reopened = NdsImage.open(research)
    assert reopened.read_file(doc['file_path']) == result
    assert reopened.read_file('/__arm9__.bin') == arm
    save(args.out / 'reconstruction.json', dict(parent=doc['current_ROM'], parent_sha256=doc['current_ROM_sha256'],
        manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        plan=str(plans), plan_sha256=sha(plans.read_bytes()),
        packet=str(packet_path), packet_sha256=sha(packet_path.read_bytes()),
        source_archive_sha256=sha(archive), target_archive=str(archive_path), target_archive_sha256=sha(result),
        research_ROM=str(research), research_ROM_sha256=sha(research.read_bytes()), groups=groups,
        command_count=sum(len(g['command_map']) for g in groups), speech_count=224,
        relative_sites=sum(len(g['relative_fixups']) for g in groups),
        other315_blocks_andall_other_files_components_exact=True,
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,
        registered_right_bound_runtime_preserved=True, source_sourceprose_andcompletion_credit_added=0,
        stored_native_pages_gameplay_andregistered_release_pending=True,
        producers={str(p): sha(p.read_bytes()) for p in [Path(__file__), Path('dk4tool/script/reviewed_scene_rebuild.py')]}))
    print('224 speeches /', sum(len(g['command_map']) for g in groups), 'commands /',
          sum(len(g['relative_fixups']) for g in groups), 'relative sites reconstructed; 315 other blocks unchanged.')
    print('Research image only; full inverses and current right-bound runtime preserved.')


if __name__ == '__main__':
    main()
