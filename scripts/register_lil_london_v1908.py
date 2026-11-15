"""Register London after the complete preserved V1875 stack."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import lil_london_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_london_references_v1907 import DOC as NEW, MAP, ACTUAL
from scripts.verify_village_wrap_v608 import read, save

CONFIG = 'translations/lil_london_editorial_release_v1.json'
ROOT = Path('work/analysis/lil_London_release_v1908')
PROFILE = 'all-routes-unified-v1909'
PARENT = Path('out/all_routes_combined_v1875_candidate.nds')
RESEARCH = Path('work/analysis/lil_London_research_v1901/lil_London_V1875_derived_RESEARCH_ONLY.nds')

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(CONFIG).exists()
    assert sha(PARENT.read_bytes()) == '872f4047dd3c9ee335dc7e6dbff5e96af668c67b07e145f29422db71c0871d97'
    assert sha(RESEARCH.read_bytes()) == 'fdc6757a13af0a04c4f2355ade3c66163a6382a0a7081efa03a457b1198dd1d1'
    base_path = Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base_path.read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image, base, clean = map(NdsImage.open, (PARENT, base_path, 'work/clean.nds'))
    doc, mapping = map(read, (NEW, MAP))
    files = {NEW, MAP, ACTUAL, 'dk4tool/patch/lil_london_editorial.py', __file__,
        'work/analysis/lil_London_approval_v1907/final_source_reference_approval.json',
        'dk4tool/dialogue/profiles.py', 'dk4tool/dialogue/layout.py', 'dk4tool/dialogue/encoder.py',
        'dk4tool/dialogue/codec.py', 'dk4tool/dialogue/review.py'}
    files.update(mapping['evidence'])
    config = dict(format='dk4-lil-london-editorial-release-v1', manuscript=NEW, reference_map=MAP,
        source_SC2_sha256=sha(image.read_file(owned.PATH)),
        target_SC2_sha256=sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        canonical_SC2_sha256=sha(base.read_file(owned.PATH)), clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()), clean_SC2_sha256=sha(clean.read_file(owned.PATH)),
        required_runtime_arm9_sha256=sha(image.read_file('/__arm9__.bin')),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(files)})
    rp = Path('translations/release_stack.json')
    builder = Path('scripts/build_integrated_release.py')
    raw, before = rp.read_bytes(), builder.read_bytes()
    registry = read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v1492'
    assert b"profile_config.get('lil_london_editorial')" not in before
    stage = b'''    lil_london_editorial = profile_config.get('lil_london_editorial')
    if lil_london_editorial:
        from dk4tool.patch.lil_london_editorial import apply_release as apply_lil_london_editorial

        london_report = apply_lil_london_editorial(candidate, baseline, lil_london_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in london_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_london_editorial'] = {
            'release_config': lil_london_editorial,
            'release_config_sha256': sha256(Path(lil_london_editorial).read_bytes()),
            'proof': london_report}
        london_batch = Path(london_report['manuscript'])
        if london_batch in release_batches:
            raise ValueError('London must run after the complete frozen cumulative stages')
        release_batches.append(london_batch)

'''
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    at = before.index(anchor)
    after = before[:at]+stage+before[at:]
    compile(after, str(builder), 'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(CONFIG, config)
    plan = owned.apply_release(image, base)
    assert plan['block_growth_bytes'] == 864 and len(plan['changed_records']) == 111
    assert image.read_file(owned.PATH) == NdsImage.open(RESEARCH).read_file(owned.PATH)
    save(ROOT/'native_source_release_plan.json', plan)
    negatives = []

    def reject(label, im, cfgpath=CONFIG):
        previous = im.read_file(owned.PATH)
        try:
            owned.apply_release(im, base, cfgpath)
        except ValueError as error:
            assert im.read_file(owned.PATH) == previous
            negatives.append(dict(case=label, error=str(error), no_partial_SC2_mutation=True))
        else:
            raise AssertionError('Invalid London release accepted: '+label)

    reject('repeat_application', image)
    for label, path in [('wrong_runtime', '/__arm9__.bin'), ('wrong_source', owned.PATH)]:
        im = NdsImage.open(PARENT)
        data = bytearray(im.read_file(path))
        data[0x100] ^= 1
        im.replace_file(path, bytes(data))
        reject(label, im)
    for label in ['incomplete_map', 'wrong_command_destination', 'wrong_relative_span',
                  'wrong_span_target', 'missing_map_record', 'unreviewed_formatting',
                  'changed_prose', 'changed_speaker', 'authored_padding', 'wrong_consumer']:
        bad = deepcopy(config)
        is_map = label in ['incomplete_map', 'wrong_command_destination', 'wrong_relative_span',
                           'wrong_span_target', 'missing_map_record', 'wrong_consumer']
        value = deepcopy(mapping if is_map else doc)
        if label == 'incomplete_map': value['external_references_complete'] = False
        elif label == 'wrong_command_destination': value['commands'][3]['new_offset'] += 2
        elif label == 'wrong_relative_span': value['relative_skip_fixups'][0]['target_span'] += 2
        elif label == 'wrong_span_target': value['relative_skip_fixups'][0]['matched_skip_target'] += 2
        elif label == 'missing_map_record': value['records'].pop()
        elif label == 'wrong_consumer':
            next(r for r in value['records'] if r['consumer']=='original_FE_modal_5473C_mode1')['consumer']='original_progressive_54020'
        elif label == 'unreviewed_formatting': value['records'][0]['review']['formatting'] = False
        elif label == 'changed_prose': value['records'][0]['english'] += ' Extra words.'
        elif label == 'changed_speaker': value['records'][0]['english'] = value['records'][0]['english'].replace('SPEAKER:02','SPEAKER:11')
        else: value['records'][0]['english'] += '{PAD}'
        path = ROOT/(label+'.json')
        save(path, value)
        bad['reference_map' if is_map else 'manuscript'] = str(path)
        bad['dependencies'][str(path)] = sha(path.read_bytes())
        cfgpath = ROOT/(label+'_config.json')
        save(cfgpath, bad)
        reject(label, NdsImage.open(PARENT), cfgpath)
    assert len(negatives) == 13
    profile = deepcopy(registry['profiles']['all-routes-unified-v1875'])
    profile.update(lil_london_editorial=CONFIG, status='experimental',
        description='Complete V1875 stack plus111 contextually reviewed London speeches.',
        note='SC2B26 +864bytes;262commands92typed spans;105actual speeches210holds,sixconditional offline;registered identity/patch/startup pending. V1492 remains promoted.')
    registry['profiles'][PROFILE] = profile
    assert rp.read_bytes() == raw and builder.read_bytes() == before
    pending = rp.with_name('release_stack_v1908_pending.json')
    assert not pending.exists()
    save(pending, registry)
    builder.write_bytes(after)
    os.replace(pending, rp)
    restored = deepcopy(read(rp))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1) == before
    save(ROOT/'registration_provenance.json', dict(profile=PROFILE, source_profile='all-routes-unified-v1875',
        source_parent=str(PARENT), source_parent_sha256=sha(PARENT.read_bytes()),
        all_previous_profiles_accepted_layers_and_promotion_preserved=True,
        registry_before_sha256=sha(raw), registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before), builder_after_sha256=sha(after),
        release_config_sha256=sha(Path(CONFIG).read_bytes()), negative_cases=negatives,
        new_registered_candidate_not_yet_built=True, full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(profile=PROFILE, negative_release_cases=len(negatives), source_compiler_equals_research=True))


