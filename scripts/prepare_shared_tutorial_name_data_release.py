"""Qualify and register one cumulative tutorial/name data successor, without promotion."""
import os
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.registered_reviewed_text_data_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_tutorial_name_data_release_v2_20261104')
PROFILE = 'all-routes-rafael-tutorial-name-data-20261104'
OLD = 'all-routes-rafael-b36-b41-static-text-20261104'
PARENT = Path('out/all_routes_combined_rafael_b36_b41_static_text_20261104_candidate.nds')
CONFIG = Path('translations/shared_tutorial_pedro_hayreddin_data_release_v1.json')
PANEL_ROOT = Path('work/analysis/Shared_Deck_current_native_v5_20261104')
NAME_ROOT = Path('work/analysis/Rafael_B36_B41_name_fields_native_20261104')


def main():
    assert not ROOT.exists() and not CONFIG.exists()
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == 'fea98878fcc2c58a6e0c9fed87e038a1446051abec4209ee6011ac4734a088d3'
    registry = load(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    image = NdsImage.open(PARENT)
    parent_bytes = PARENT.read_bytes()
    assert sha(parent_bytes) == 'ee04bf6f954ecbdb15b01fb68b5754c5c38366a767ce8a40aec8bd04f2ed985e'
    ROOT.mkdir()
    (ROOT / 'release_stack.before.json').write_bytes(before)
    paths = dict(panels='translations/shared_deck_four_panels_contextual_final_v1.json',
        names='translations/pedro_hayreddin_catalogue_fields_final_v1.json',
        panel_native=str(PANEL_ROOT / 'native_andstorage_verification.json'),
        panel_connected='work/analysis/Shared_Deck_connected_current_20261104/connected_verification.json',
        panel_actual='work/analysis/Shared_Deck_actual_UI_20261104/representative_UI_verification.json',
        panel_visual='work/analysis/Shared_Deck_four_panel_checked_20261104/visual_andresearch_approval.json',
        name_native=str(NAME_ROOT / 'native_name_fields_verification.json'),
        name_visual='work/analysis/Pedro_Hayreddin_catalogue_fields_checked_20261104/reuse_andeditorial_approval.json',
        name_proposal='work/analysis/Rafael_B36_B41_name_field_proposals_20261104/owned_fields_proposal.json')
    arm = image.read_file('/__arm9__.bin')
    target_arm = bytearray(arm)
    for r in load(paths['panels'])['records']:
        p = r['planned_integrated_reference']; new = bytes.fromhex(p['padded_hex'])
        assert len(new) == p['capacity']
        target_arm[p['offset']:p['offset'] + p['capacity']] = new
    for r in load(paths['name_proposal'])['fields']:
        at = r['physical_offset']; new = bytes.fromhex(r['target_hex'])
        assert arm[at:at + r['owned_bytes']].hex() == r['source_hex'] and len(new) == r['owned_bytes']
        target_arm[at:at + len(new)] = new
    reference = deepcopy(image)
    reference.replace_file('/__arm9__.bin', bytes(target_arm))
    payload = bytes(reference.rom.save())
    reference_path = ROOT / 'six_owned_spans_REFERENCE_ONLY.nds'
    reference_path.write_bytes(payload)
    dependencies = {str(Path(p)): sha(Path(p).read_bytes()) for p in paths.values()}
    # Freeze directly used proof dependencies. Historical proof chains are referenced,
    # while exact current ARM9/COMMON checks establish which technical proofs apply.
    def freeze_evidence(doc):
        for key in ['evidence', 'formatting_evidence', 'dependencies']:
            for p, digest in doc.get(key, {}).items():
                assert sha(Path(p).read_bytes()) == digest
                normalized = str(Path(p))
                if normalized in dependencies:
                    continue
                dependencies[normalized] = digest
    for p in paths.values():
        freeze_evidence(load(p))
    for p in [*Path('scripts').glob('build_integrated_release_with_*.py'),
              Path('scripts/build_integrated_release.py'), Path('scripts/shared_deck_formatting_v1.py'),
              Path('scripts/source_locked_derivation_v5118.py'), Path('dk4tool/patch/owned_name_fields_v2.py'),
              Path('dk4tool/patch/registered_reviewed_text_data_v1.py'), Path(__file__)]:
        dependencies[str(p)] = sha(p.read_bytes())
    config = dict(format='dk4-registered-reviewed-text-data-v1', **paths, clean_ROM='work/clean.nds',
        clean_ROM_sha256='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        parent_ROM_sha256=sha(parent_bytes), target_ROM_sha256=sha(payload), target_ARM9_sha256=sha(bytes(target_arm)),
        dependencies=dependencies)
    save(CONFIG, config)
    planned, proof = plan_release(image, CONFIG)
    assert planned == bytes(target_arm) and len(proof['changed_records']) == 6
    assert bytes(image.rom.save()) == parent_bytes
    rejected = []
    for case in ['stale-parent', 'wrong-target', 'missing-panel', 'failed-formatting-gate', 'altered-panel-glyph',
                 'failed-name-gate', 'changed-name-owner', 'unreviewed-dependency']:
        conf = deepcopy(config)
        if case == 'stale-parent': conf['parent_ROM_sha256'] = '0' * 64
        elif case == 'wrong-target': conf['target_ARM9_sha256'] = '0' * 64
        elif case == 'unreviewed-dependency': conf['dependencies'][str(Path(paths['panels']))] = '0' * 64
        else:
            key = 'name_proposal' if case == 'changed-name-owner' else 'names' if case == 'failed-name-gate' else 'panels'
            doc = load(paths[key])
            if case == 'missing-panel': doc['records'].pop()
            elif case in ['failed-formatting-gate', 'failed-name-gate']: doc['records'][0]['review']['formatting'] = False
            elif case == 'altered-panel-glyph': doc['records'][0]['english'] = 'Missing approved source meaning.{PAD}'
            elif case == 'changed-name-owner': doc['fields'][0]['owners'][0]['actor'] = 32
            path = ROOT / (case + '.json'); save(path, doc)
            conf[key] = str(path); conf['dependencies'][str(path)] = sha(path.read_bytes())
        path = ROOT / (case + '_config.json'); save(path, conf)
        try:
            plan_release(image, path)
        except (ValueError, AssertionError, KeyError) as error:
            rejected.append(dict(case=case, error_type=type(error).__name__, error=str(error)))
        else:
            raise AssertionError('Invalid plan accepted: ' + case)
        assert bytes(image.rom.save()) == parent_bytes
    profile = deepcopy(registry['profiles'][OLD])
    profile['owned_reviewed_text_data'] = str(CONFIG)
    profile['note'] = ('Experimental cumulative Rafael-priority successor:four shared tutorial reviews (one revision,three retentions),'
        'four formatting fixes andtwo catalogue-name component corrections. All six earlier stages remain exact;no main promotion.')
    registry['profiles'][PROFILE] = profile
    prior = load(ROOT / 'release_stack.before.json')
    assert all(registry[k] == v for k, v in prior.items() if k != 'profiles')
    assert all(registry['profiles'][k] == v for k, v in prior['profiles'].items())
    assert {k:v for k,v in profile.items() if k not in ['owned_reviewed_text_data','note']} == {
        k:v for k,v in prior['profiles'][OLD].items() if k != 'note'}
    assert registry_path.read_bytes() == before
    pending = registry_path.with_name('release_stack.reviewed_text_data.pending.json')
    save(pending, registry); os.replace(pending, registry_path)
    pins_path = Path('translations/rom_retention_pins.json'); pins_before = pins_path.read_bytes()
    (ROOT / 'pins.before.json').write_bytes(pins_before); pins = load(pins_path)
    pins.append(dict(path=str(reference_path.resolve()), reason='Exact six-span registered data reference;preserve all ROMs. SHA256 ' + sha(payload)))
    pending = pins_path.with_name('rom_retention_pins.reviewed_text_data.pending.json')
    save(pending, pins); assert pins_path.read_bytes() == pins_before; os.replace(pending, pins_path)
    save(ROOT / 'registered_preparation.json', dict(profile=PROFILE, config=str(CONFIG), config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM=str(PARENT), parent_ROM_sha256=sha(parent_bytes), reference_ROM=str(reference_path),
        target_ROM_sha256=sha(payload), target_ARM9_sha256=sha(bytes(target_arm)), registry_sha256=sha(registry_path.read_bytes()),
        positive_plan=proof, semantic_rejections=rejected, accepted_layers=114, expected_manifest_entries=667,
        all_six_prior_stage_configs_andall_previous_profiles_exact=True, registered_build_patch_andown_startup_pending=True,
        new_credit=0, no_promotion=True, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered', PROFILE, sha(payload), 'six typed spans/eight rejected defects;prior six stages exact.', flush=True)


if __name__ == '__main__':
    main()
