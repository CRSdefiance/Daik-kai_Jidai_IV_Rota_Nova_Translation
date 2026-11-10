"""Compose a qualified fixed-slot name proposal with a checked story research image."""
import argparse
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['reconstruction', 'native', 'out']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rebuilt, native = map(load, [args.reconstruction, args.native])
    proposal_path = Path(native['proposal'])
    assert native['proposal_sha256'] == sha(proposal_path.read_bytes())
    assert native['offline_visual_approved'] and not native['direct_view_pending']
    proposal = load(proposal_path)
    story_path = Path(rebuilt['research_ROM'])
    assert sha(story_path.read_bytes()) == rebuilt['research_ROM_sha256']
    story = NdsImage.open(story_path)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    target_arm, proof = plan_arm9_name_fields(story.read_file('/__arm9__.bin'), proposal, clean)
    assert proof == native['name_data_plan']
    assert target_arm == Path(native['proposed_ARM9']).read_bytes()
    final = deepcopy(story)
    final.replace_file('/__arm9__.bin', target_arm)
    assert all(final.read_file(p) == data for _, p, data in story.iter_files())
    assert [p for p, data in story.iter_components() if final.read_file(p) != data] == ['/__arm9__.bin']
    inverse = deepcopy(final)
    inverse.replace_file('/__arm9__.bin', story.read_file('/__arm9__.bin'))
    assert bytes(inverse.rom.save()) == story_path.read_bytes()
    args.out.mkdir(parents=True)
    path = args.out / 'reviewed_names_RESEARCH_ONLY.nds'
    path.write_bytes(bytes(final.rom.save()))
    reopened = NdsImage.open(path)
    assert reopened.read_file('/__arm9__.bin') == target_arm
    save(args.out / 'research_reference.json', dict(**{k: v for k, v in rebuilt.items() if k not in ['research_ROM', 'research_ROM_sha256']},
         research_ROM=str(path), research_ROM_sha256=sha(path.read_bytes()),
         story_reconstruction=str(args.reconstruction), story_reconstruction_sha256=sha(args.reconstruction.read_bytes()),
         story_only_research_ROM=str(story_path), story_only_research_ROM_sha256=sha(story_path.read_bytes()),
         name_native_proof=str(args.native), name_native_proof_sha256=sha(args.native.read_bytes()),
         owned_name_metadata_plan=proof, only_source_qualified_owned_name_fields_additionally_changed=True,
         whole_story_only_parent_inverse_exact=True, not_a_registered_release_orhandoff=True,
         name_composition_producer=str(Path(__file__)), name_composition_producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    pins.append(dict(path=str(path.resolve()), reason='Preserve complete B131–B150 story plus qualified three-owner/four-byte name research reference; no pruning.'))
    save(pins_path, pins)
    print(dict(research_ROM=str(path), sha256=sha(path.read_bytes()), owned_bytes=proof['owned_span_bytes'], complete_inverse=True))


if __name__ == '__main__':
    main()
