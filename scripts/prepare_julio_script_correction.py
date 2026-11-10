"""Store the tested normal-font paragraph so the old catalogue key no longer matches."""
import argparse
import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.sparse_scene_rebuild import rebuild_sparse_block
from scripts.audit_story_glyph_consistency import independent_pixels, load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_name_catalog_glyphs_v278 import raster


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists()
    batch = load('work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json')
    parent = Path(batch['research_ROM'])
    image = NdsImage.open(parent)
    assert sha(parent.read_bytes()) == batch['research_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    path = '/data/SC0.DK4'
    original = image.read_file(path)
    blocks = IlnkContainer.parse(original).blocks
    sources = IlnkContainer.parse(clean.read_file(path)).blocks
    draft = load('translations/julio_deck_glyph_review_v1.json')
    change = dict(file_path=path, block=43, source_hex=draft['source_reference']['source_hex'],
                  current_hex=draft['current_storage_reference']['source_hex'],
                  compiled_hex=draft['proposed_hex'])
    inventory, _, _ = scoped_inventory()
    target, proof = rebuild_sparse_block(arm, sources[43], blocks[43], path, 43,
                                         {draft['id']: change}, inventory)
    texts = {r['id']: r for r in proof['text_records']}
    stored = bytes.fromhex(texts[draft['id']]['stored_hex'])
    expanded = stored[1:].replace(b'FI', b'Rafael')
    pixels, events, font = raster(arm, expanded)
    assert pixels == independent_pixels(arm, font, events)
    assert all(e['kind'] == 'ascii' for e in events)
    args.out.mkdir(parents=True)
    pic = Image.new('RGB', (216, 64))
    colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
    pic.putdata([colors[v] for v in pixels])
    pic.save(args.out / 'stored_native.png')
    blocks[43] = target
    archive = IlnkContainer(blocks).to_bytes()
    image.replace_file(path, archive)
    full = args.out / 'Hodram_and_Julio_RESEARCH_ONLY.nds'
    full.write_bytes(bytes(image.rom.save()))
    original_blocks = IlnkContainer.parse(original).blocks
    assert [i for i, (a, b) in enumerate(zip(original_blocks, blocks, strict=True)) if a != b] == [43]
    inverse = list(blocks)
    inverse[43] = original_blocks[43]
    assert IlnkContainer(inverse).to_bytes() == original
    assert image.read_file('/__arm9__.bin') == arm
    (args.out / 'SC0_B43_RESEARCH_ONLY.bin').write_bytes(target)
    (args.out / 'SC0_RESEARCH_ONLY.DK4').write_bytes(archive)

    # Source-owned initialization from the real Rafael opening; preserve every
    # complete tutorial command, including its Deck and final FE instruction.
    opening = blocks[44]
    commands, speeches = inventory(arm, opening)
    first = speeches[0]['offset']
    prelude = opening[8:first]
    assert prelude == sources[44][8:first] and first == 40
    initializers = [c for c in commands if c['offset'] < first]
    assert len(initializers) == 10 and len(prelude) == 32
    end = proof['new_logical_end']
    logical = bytearray(opening[:8] + prelude + target[8:end])
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    parsed, shown = inventory(arm, fixture)
    assert len(parsed) == len(proof['all_target_commands']) + 10 and len(shown) == 12
    for command in proof['all_target_commands']:
        moved = next(c for c in parsed if c['offset'] == command['offset'] + 32)
        assert moved['whole_command_hex'] == command['whole_command_hex']
    fixture_blocks = list(blocks)
    fixture_blocks[44] = fixture
    image.replace_file(path, IlnkContainer(fixture_blocks).to_bytes())
    fixture_rom = args.out / 'Julio_tutorial_initialized_RESEARCH_ONLY.nds'
    fixture_rom.write_bytes(bytes(image.rom.save()))
    inputs = [r for r in load('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
              if r['buttons'] != ['RIGHT']]
    inputs += [dict(start=f, duration=5, buttons=['A']) for f in range(4000, 9500, 240)]
    input_path = args.out / 'ordinary_Rafael_inputs.json'
    save(input_path, inputs)
    save(args.out / 'reconstruction.json', dict(parent=str(parent), parent_sha256=sha(parent.read_bytes()),
        file_path=path, block=43, changed_ID=draft['id'], changed_records=1,
        source_archive_sha256=sha(original), target_archive=str(args.out / 'SC0_RESEARCH_ONLY.DK4'),
        target_archive_sha256=sha(archive), current_block_sha256=sha(original_blocks[43]),
        clean_block_sha256=sha(sources[43]), target_block=str(args.out / 'SC0_B43_RESEARCH_ONLY.bin'),
        target_block_sha256=sha(target), block_proof=proof,
        change=change, full_research_ROM=str(full), full_research_ROM_sha256=sha(full.read_bytes()),
        fixture_ROM=str(fixture_rom), fixture_ROM_sha256=sha(fixture_rom.read_bytes()),
        source_opening_initializers=initializers, source_opening_prelude_hex=prelude.hex(),
        inputs=str(input_path), inputs_sha256=sha(input_path.read_bytes()),
        all11_unselected_speech_bytes_exact_not_new_editorial_credit=True,
        ARM9_fonts_andruntime_unchanged=True, four_row_stored_native_check_pass=True,
        original10_initializers_plus_complete16_command_tutorial_not_natural_activation=True,
        no_RAM_flags_roster_RNG_orresult_override=True, actual_andregistered_integration_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('One reviewed glyph correction stored;11 other speech records and the entire ARM9 unchanged. Tutorial fixture prepared.')


if __name__ == '__main__':
    main()
