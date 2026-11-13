"""Build and invert the source-qualified Assign Sailors text-only research ROM."""

from pathlib import Path

from dk4tool.patch.ship_command_label_v1 import transform
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


WORK = Path('work/SharedText_20261110_v1/ship_command_research_v1')
ARCHIVE = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
RELEASE = Path('work/lil261_B323_B335_release_v1/registered_release_verification.json')
ROM = WORK / 'ship_command_RESEARCH_ONLY.nds'
PROOF = WORK / 'research_ROM.json'


def main():
    assert not WORK.exists()
    release = load(RELEASE)
    native = ARCHIVE / 'ship_command_native_descriptor.json'
    original = load(native)
    historical = Path('work/analysis/battle_cooking_livestock_v911/additional_Japanese_menu_lead.json')
    lead = load(historical)
    assert digest(lead['capture']) == lead['capture_sha256']
    parent = Path(release['candidate'])
    assert digest(parent) == release['candidate_sha256'] == original['runtime']['candidate_sha256']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    image = NdsImage.open(parent)
    source = image.read_file('/__arm9__.bin')
    target, proof = transform(source)
    assert proof['pointer_field'] == original['pointer_field']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert clean[proof['original_pointer']-0x02000000:proof['original_pointer']-0x02000000+11].hex() == proof['source_terminated_hex']

    WORK.mkdir(parents=True)
    image.replace_file('/__arm9__.bin', target)
    ROM.write_bytes(bytes(image.rom.save()))
    reopened, unchanged = NdsImage.open(ROM), NdsImage.open(parent)
    assert reopened.read_file('/__arm9__.bin') == target
    assert list(reopened.iter_files()) == list(unchanged.iter_files())
    assert [p for p, data in unchanged.iter_components() if reopened.read_file(p) != data] == ['/__arm9__.bin']
    reopened.replace_file('/__arm9__.bin', source)
    assert bytes(reopened.rom.save()) == parent.read_bytes()
    save(PROOF, dict(**proof, parent=str(parent), parent_sha256=digest(parent),
        ROM=str(ROM), ROM_sha256=digest(ROM), candidate_research_only=True, full_parent_NDS_inverse_exact=True,
        all_files_exact_and_only_ARM9_component_changed=True, registered_integration_pending=True,
        clean_Japanese='船を捨てる', English='Abandon Ship', adjoining_command='Assign',
        finding='The menu acts on the selected ship. Abandon Ship states the complete action and fits the direct-command style beside Assign.',
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
        current_test_fixture_and_hardware_unverified=True, new_credit=0,
        evidence={str(p):digest(p) for p in [RELEASE, native, historical, Path(__file__)]}))
    print('Built the text-only Abandon Ship research ROM and verified its complete parent inverse.')


if __name__ == '__main__':
    main()
