"""Test new release adaptations; reuse unchanged engine/menu/name qualifications."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_scene_batch_v7 import plan_release
from dk4tool.patch.registered_owned_static_text_v1 import plan_release as static_plan
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B151_B170_release_qualification_20261102')
PREP = Path('work/analysis/Hodram_B151_B170_release_20261102/registered_preparation.json')


def main():
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    prepared = load(PREP)
    config_path = Path(prepared['config'])
    conf = load(config_path)
    image = NdsImage.open(prepared['canonical_parent'])
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before, base_before = bytes(image.rom.save()), bytes(baseline.rom.save())
    target, proof = plan_release(image, baseline, config_path)
    assert sha(bytes(target.save())) == prepared['pre_runtime_ROM_sha256'] and len(proof['changed_records']) == 642
    print('Positive complete scene plan passes.', flush=True)
    rejected = []
    for kind in ['failed-fifth-gate', 'cinematic-layout-tampering', 'clean-cinematic-body-tampering', 'wrong-choice-index', 'stale-scene-parent']:
        config = deepcopy(conf)
        if kind == 'stale-scene-parent':
            config['parent_ROM_sha256'] = '0' * 64
        else:
            field = 'plan' if kind == 'cinematic-layout-tampering' else 'manuscript'
            doc = load(config[field])
            if kind == 'failed-fifth-gate':
                doc['records'][0]['review']['formatting'] = False
            elif kind == 'wrong-choice-index':
                next(r for r in doc['records'] if r['kind'] == 'typed-choice-label')['source_index'] = 1
            elif kind == 'clean-cinematic-body-tampering':
                next(r for r in doc['records'] if r['id'] == 'DK4_MES_B156_R0165')['source_Japanese'] += '？'
            else:
                next(r for r in doc['records'] if r.get('individually_documented_automatic_source_staging'))['lines'][0] = 'Unreviewed text'
            path = ROOT / (kind + '.json')
            save(path, doc)
            config[field] = str(path)
            config['dependencies'][str(path)] = sha(path.read_bytes())
        path = ROOT / (kind + '_config.json')
        save(path, config)
        try:
            plan_release(image, baseline, path)
        except (ValueError, AssertionError, KeyError) as error:
            rejected.append(dict(case=kind, error=str(error)))
        else:
            raise AssertionError('Accepted invalid case: ' + kind)
        assert bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == base_before
    spec = load('translations/release_stack.json')['profiles'][prepared['profile']]['late_editorial_extensions'][-1]
    shared, _ = plan_extensions(image, baseline, [spec])
    assert bytes(shared.save()) == bytes(target.save())
    print('Direct/shared scene plans agree;five invalid scene cases rejected.', flush=True)
    source = NdsImage.open(prepared['post_grouped_ROM'])
    original = bytes(source.rom.save())
    static_conf = load(prepared['static_config'])
    arm, static_proof = static_plan(source, prepared['static_config'])
    final = deepcopy(source)
    final.replace_file('/__arm9__.bin', arm)
    assert sha(bytes(final.rom.save())) == prepared['target_ROM_sha256']
    for kind in ['stale-static-parent', 'wrong-static-target', 'failed-scoped-name-gate']:
        config = deepcopy(static_conf)
        if kind == 'stale-static-parent':
            config['parent_ROM_sha256'] = '0' * 64
        elif kind == 'wrong-static-target':
            config['target_ROM_sha256'] = '0' * 64
        else:
            doc = load(config['manuscript'])
            doc['records'][0]['review']['formatting'] = False
            path = ROOT / (kind + '.json')
            save(path, doc)
            config['manuscript'] = str(path)
            config['dependencies'][str(path)] = sha(path.read_bytes())
        path = ROOT / (kind + '_config.json')
        save(path, config)
        try:
            static_plan(source, path)
        except (ValueError, AssertionError, KeyError) as error:
            rejected.append(dict(case=kind, error=str(error)))
        else:
            raise AssertionError('Accepted invalid case: ' + kind)
        assert bytes(source.rom.save()) == original
    assert len(rejected) == 8 and bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == base_before
    save(ROOT / 'qualification.json', dict(scene_config=str(config_path), positive_scene_plan=proof,
        direct_andshared_scene_targets_equal=True, positive_static_plan=static_proof, semantic_rejections=rejected,
        all_inputs_andunowned_bytes_preserved=True, inherited_guards_not_retested_without_changes=True,
        static_data_ten_negative_cases_reused='work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json',
        all_prior_runtime_name_drivers_unchanged=True, registered_build_patch_andown_startup_pending=True,
        new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS642-record direct/shared scene production;separate15-byte owned static stage;eight new semantic rejections.', flush=True)


if __name__ == '__main__':
    main()
