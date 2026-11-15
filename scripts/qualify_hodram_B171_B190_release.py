"""Test the new two-choice/terminal-event adaptation; reuse unchanged stage qualifications."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_scene_batch_v8 import plan_release
from dk4tool.patch.registered_owned_static_text_v1 import plan_release as static_plan
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_release_qualification_20261104')
PREP = Path('work/analysis/Hodram_B171_B190_release_20261104/registered_preparation.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    prepared = load(PREP)
    config_path = Path(prepared['config'])
    conf = load(config_path)
    image = NdsImage.open(prepared['canonical_parent'])
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before, base_before = bytes(image.rom.save()), bytes(baseline.rom.save())
    target, proof = plan_release(image, baseline, config_path)
    assert sha(bytes(target.save())) == prepared['pre_runtime_ROM_sha256'] and len(proof['changed_records']) == 435
    ROOT.mkdir()
    rejected = []
    cases = ['failed-fifth-gate', 'encoded-layout-tampering', 'terminal-nonspace-event', 'wrong-choice-index', 'stale-scene-parent', 'missing-highlight-index']
    for kind in cases:
        config = deepcopy(conf)
        if kind == 'stale-scene-parent':
            config['parent_ROM_sha256'] = '0' * 64
        else:
            field = {'encoded-layout-tampering': 'plan', 'terminal-nonspace-event': 'stored_native', 'missing-highlight-index': 'focused_pixels'}.get(kind, 'manuscript')
            doc = load(config[field])
            if kind == 'failed-fifth-gate':
                doc['records'][0]['review']['formatting'] = False
            elif kind == 'wrong-choice-index':
                next(r for r in doc['records'] if r['kind'] == 'typed-choice-label')['source_index'] = 1
            elif kind == 'encoded-layout-tampering':
                row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B171_R0075')
                row['encoded_hex'] = row['encoded_hex'][:-2] + '41'
            elif kind == 'terminal-nonspace-event':
                row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B179_R0047')
                row['complete_stored_native_display']['planned_native_row_comparison']['qualified_events'][0]['code'] = 65
            else:
                doc['menu_samples'][1]['selected_option'] = 0
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
    assert len(rejected) == 6
    spec = load('translations/release_stack.json')['profiles'][prepared['profile']]['late_editorial_extensions'][-1]
    shared, _ = plan_extensions(image, baseline, [spec])
    assert bytes(shared.save()) == bytes(target.save())
    source = NdsImage.open(prepared['post_grouped_ROM'])
    original = bytes(source.rom.save())
    arm, static_proof = static_plan(source, prepared['static_config'])
    final = deepcopy(source)
    final.replace_file('/__arm9__.bin', arm)
    assert sha(bytes(final.rom.save())) == prepared['target_ROM_sha256'] and bytes(source.rom.save()) == original
    prior_path = Path('work/analysis/Hodram_B151_B170_release_qualification_20261102/qualification.json')
    prior = load(prior_path)
    assert len(prior['semantic_rejections']) == 8
    save(ROOT / 'qualification.json', dict(scene_config=str(config_path), positive_scene_plan=proof,
        direct_andshared_scene_targets_equal=True, positive_static_plan=static_proof, semantic_rejections=rejected,
        all_inputs_andunowned_bytes_preserved=True, inherited_guards_not_retested_without_changes=True,
        unchanged_static_stage_negative_cases_reused=dict(path=str(prior_path), sha256=sha(prior_path.read_bytes()), cases=prior['semantic_rejections'][5:]),
        all_six_prior_runtime_name_static_drivers_unchanged=True, registered_build_patch_andown_startup_pending=True,
        new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS435-record direct/shared production plans; six new invalid cases rejected; unchanged final static stage passes with reused negative qualification.')
