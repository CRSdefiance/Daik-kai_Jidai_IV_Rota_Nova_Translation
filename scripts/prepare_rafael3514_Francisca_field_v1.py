"""Qualify the exclusive name-field stage against the exact dialogue target."""
from pathlib import Path

from dk4tool.patch.registered_Francisca_name_field_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B241_B260_successor_spec_v1 import FIELD, READY, REBUILT, ROOT, digest


OUT = Path('work/Rafael3514_Francisca_field_preparation_v1_20261106')
CONFIG = Path('translations/Francisca_field_Rafael3514_release_v1.json')
CLEAN = Path('work/clean.nds')
NAME = 'rafael_frozen_rose_town_exchange'
MODULE = Path('dk4tool/patch/registered_Francisca_name_field_v1.py')


def main():
    assert not OUT.exists() and not CONFIG.exists()
    ready, rebuilt = map(load, (READY, REBUILT))
    assert ready['all_individual_five_gates_pass'] and ready['records'] == 292
    parent = Path(rebuilt['research_ROM'])
    assert digest(parent) == rebuilt['research_ROM_sha256']
    files = dict(manuscript=Path('translations/rafael_B241_B260_scoped_names_final_v1.json'),
        proposal=FIELD, native=FIELD.parent/'native/native_name_fields_verification.json',
        actual_pixels=ROOT/f'actual_pixels_{NAME}_v1/focused_actual_pixels.json',
        actual_visual=READY.with_name('complete_visual_approval.json'),
        fixture=ROOT/f'fixtures_v1/{NAME}_fixture.json')
    assert all(digest(path) == ready['evidence'][str(path)] for key, path in files.items()
               if key in ('manuscript', 'native', 'actual_pixels', 'actual_visual', 'fixture'))
    native = load(files['native'])
    arm = Path(native['proposed_ARM9'])
    assert digest(arm) == native['versions'][1]['ARM9_sha256']
    image = NdsImage.open(parent)
    parent_arm = image.read_file('/__arm9__.bin')
    assert parent_arm != arm.read_bytes() and digest(parent) == rebuilt['research_ROM_sha256']
    reference = NdsImage.open(parent)
    reference.replace_file('/__arm9__.bin', arm.read_bytes())
    expected = bytes(reference.rom.save())
    reference.replace_file('/__arm9__.bin', parent_arm)
    assert bytes(reference.rom.save()) == parent.read_bytes()
    from dk4tool.patch.grand_race_menu_release import sha
    config = dict(format='dk4-registered-Francisca-name-field-v1', **{key:str(path) for key, path in files.items()},
        parent_ROM=str(parent), parent_ROM_sha256=digest(parent), clean_ROM=str(CLEAN),
        clean_ROM_sha256=digest(CLEAN), target_ROM_sha256=sha(expected),
        tested_ARM9=str(arm), target_ARM9_sha256=digest(arm),
        dependencies={str(path):digest(path) for path in (
            *files.values(), arm, READY, REBUILT, MODULE, Path(__file__),
            Path('dk4tool/patch/owned_name_fields_v2.py'))})
    OUT.mkdir()
    draft = OUT/'candidate_config.json'
    save(draft, config)
    target, proof = plan_release(image, draft)
    assert target == arm.read_bytes() and proof['final_ROM_sha256'] == config['target_ROM_sha256']
    wrong = OUT/'wrong_predecessor_config.json'
    save(wrong, {**config, 'parent_ROM_sha256': '0' * 64})
    try:
        plan_release(image, wrong)
    except ValueError as exc:
        assert 'exact ordered eight-stage predecessor' in str(exc)
    else:
        raise AssertionError('Accepted a wrong predecessor')
    assert bytes(image.rom.save()) == parent.read_bytes()
    save(CONFIG, config)
    path = OUT/'dialogue_and_field_reference_RESEARCH_ONLY.nds'
    path.write_bytes(expected)
    assert digest(path) == config['target_ROM_sha256']
    save(OUT/'qualification.json', dict(config=str(CONFIG), config_sha256=digest(CONFIG),
        target_reference=str(path), target_reference_sha256=digest(path), owned_name_field_proof=proof,
        wrong_predecessor_rejected=True, all_preceding_layers_required=True,
        registration_and_own_startup_pending=True, new_credit=0))
    print('Qualified the exact actor 186 field, native getters and observed header. Whole-ROM inverse passes.')


if __name__ == '__main__':
    main()
