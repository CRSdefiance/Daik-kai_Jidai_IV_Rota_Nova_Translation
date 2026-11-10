"""Correct the receipt's inherited block label without rewriting its ROM or history."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_reference_v8570b')
OLD = Path('work/analysis/Hodram_B51_reference_v8570/research_image_receipt.json')
MAP = Path('work/analysis/Hodram_B51_relocation_v8565/reconstruction.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    original, mapping = map(read, [OLD, MAP])
    assert original['only_changed_blocks'] == [50]
    parent, revised = [NdsImage.open(original[key]) for key in ['parent', 'research_ROM']]
    assert all(sha(Path(original[k]).read_bytes()) == original[k + '_sha256'] for k in ['parent', 'research_ROM'])
    assert [p for _, p, data in parent.iter_files() if revised.read_file(p) != data] == ['/data/SC1.DK4']
    assert all(revised.read_file(p) == data for p, data in parent.iter_components())
    a, b = [IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks for image in [parent, revised]]
    changed = [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y]
    assert changed == [51] and sha(b[51]) == mapping['groups'][0]['target_block_sha256']
    revised.replace_file('/data/SC1.DK4', parent.read_file('/data/SC1.DK4'))
    assert bytes(revised.rom.save()) == Path(original['parent']).read_bytes()
    result = deepcopy(original)
    result.update(only_changed_blocks=changed, historical_receipt=str(OLD), historical_receipt_sha256=sha(OLD.read_bytes()),
        corrected_metadata_only=dict(field='only_changed_blocks', previous=[50], current=[51],
            reason='The source-locked producer retained a B50 numeric receipt label. Its executed archive-diff assertion and actual ROM correctly select51. Fresh whole-file, block and complete parent-ROM inverse checks confirm the actual scope.'),
        no_ROM_pin_ledger_registry_orprior_artifact_rewritten=True)
    ROOT.mkdir(parents=True)
    save(ROOT / 'research_image_receipt.json', result)
    save(ROOT / 'qualification.json', dict(previous=str(OLD), previous_sha256=sha(OLD.read_bytes()), corrected=str(ROOT / 'research_image_receipt.json'),
        corrected_sha256=sha((ROOT / 'research_image_receipt.json').read_bytes()), actual_changed_blocks=changed,
        whole_parent_ROM_inverse_byte_exact=True, original_producer_receipt_ROM_andpins_preserved=True,
        new_credit=0, new_ROMs=0, new_emulator_runs=0, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Qualified B51 receipt: actual changed block51; inherited label50 corrected in successor only. ROM, original receipt/producer and all pins unchanged; whole-parent inverse exact.')
