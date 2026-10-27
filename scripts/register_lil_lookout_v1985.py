"""Register one Lookout correction after the preserved complete V1971 stack."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import lil_lookout_affiliation as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_lookout_v1984 import DOC, MAP, ACTUAL
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Lookout_release_v1985')
PROFILE = 'all-routes-unified-v1986'
CONFIG = 'translations/lil_lookout_affiliation_release_v1.json'
PARENT = Path('out/all_routes_combined_v1971_candidate.nds')
RESEARCH = Path('work/analysis/lil_Lookout_relocation_v1980/lil_Lookout_V1971_derived_RESEARCH_ONLY.nds')

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(CONFIG).exists()
    assert sha(PARENT.read_bytes()) == 'c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20'
    assert sha(RESEARCH.read_bytes()) == 'f2dcb4cc4d688e1cd40a22367180841d27d06e540edbd16927f784b2cfcb50ca'
    base_path = Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base_path.read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image, baseline, clean = map(NdsImage.open,(PARENT,base_path,'work/clean.nds'))
    doc, mapping = map(read,(DOC,MAP))
    files = {str(p) for p in (DOC,MAP,ACTUAL,Path(__file__),Path('dk4tool/patch/lil_lookout_affiliation.py'),
        Path('work/analysis/lil_Lookout_approval_v1984/approval_receipt.json'),
        Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/codec.py'),Path('dk4tool/dialogue/layout.py'),
        Path('dk4tool/dialogue/profiles.py'),Path('dk4tool/dialogue/review.py'))}
    files.update(mapping['evidence'])
    config = dict(format='dk4-lil-lookout-affiliation-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        source_SC2_sha256=sha(image.read_file(owned.PATH)),target_SC2_sha256=sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        canonical_SC2_sha256=sha(baseline.read_file(owned.PATH)),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_SC2_sha256=sha(clean.read_file(owned.PATH)),
        required_runtime_arm9_sha256=sha(image.read_file('/__arm9__.bin')),tested_research_ROM_sha256=sha(RESEARCH.read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(files)})
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = registry_path.read_bytes(), builder.read_bytes()
    registry = read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v1492'
    assert b"profile_config.get('lil_lookout_affiliation')" not in before
    stage = b'''    lil_lookout_affiliation = profile_config.get('lil_lookout_affiliation')
    if lil_lookout_affiliation:
        from dk4tool.patch.lil_lookout_affiliation import apply_release as apply_lil_lookout_affiliation

        lookout_report = apply_lil_lookout_affiliation(candidate, baseline, lil_lookout_affiliation)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in lookout_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_lookout_affiliation'] = {
            'release_config': lil_lookout_affiliation,
            'release_config_sha256': sha256(Path(lil_lookout_affiliation).read_bytes()),
            'proof': lookout_report}
        lookout_batch = Path(lookout_report['manuscript'])
        if lookout_batch in release_batches:
            raise ValueError('Lookout correction must run after the complete frozen cumulative stages')
        release_batches.append(lookout_batch)

'''
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    at = before.index(anchor)
    after = before[:at]+stage+before[at:]
    compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(CONFIG,config)
    report = owned.apply_release(image,baseline)
    assert len(report['changed_records']) == 1 and report['blocks'][0]['block'] == 23
    assert report['blocks'][0]['growth_bytes'] == -12
    assert image.read_file(owned.PATH) == NdsImage.open(RESEARCH).read_file(owned.PATH)
    save(ROOT/'native_source_release_plan.json',report)
    negatives = []
    def reject(label, target, cfgpath=CONFIG):
        previous = target.read_file(owned.PATH)
        try: owned.apply_release(target,baseline,cfgpath)
        except ValueError as error:
            assert target.read_file(owned.PATH) == previous
            negatives.append(dict(case=label,error=str(error),no_partial_SC2_mutation=True))
        else: raise AssertionError('Invalid Lookout release accepted: '+label)
    reject('repeat-application',image)
    for label,path in (('wrong-runtime','/__arm9__.bin'),('wrong-source',owned.PATH)):
        target = NdsImage.open(PARENT)
        changed = bytearray(target.read_file(path))
        changed[0x100] ^= 1
        target.replace_file(path,bytes(changed))
        reject(label,target)
    tests = ('incomplete-map','missing-command','wrong-command-target','wrong-relative-span','wrong-relative-destination','missing-relative-site',
        'unreviewed-formatting','changed-prose','changed-speaker','authored-padding','wrong-consumer','wrong-source-index','wrong-current-index',
        'wrong-Japanese','false-actual','invented-macro')
    for label in tests:
        kind = 'reference_map' if label in tests[:6] else 'manuscript'
        value, bad = deepcopy(mapping if kind == 'reference_map' else doc), deepcopy(config)
        if label == 'incomplete-map': value['external_references_complete'] = False
        elif label == 'missing-command': value['mapped_native_commands'].pop()
        elif label == 'wrong-command-target': value['mapped_native_commands'][3]['new_offset'] += 2
        elif label == 'wrong-relative-span': value['relative_skip_fixups'][0]['target_span'] += 2
        elif label == 'wrong-relative-destination': value['relative_skip_fixups'][0]['matched_skip_target'] += 2
        elif label == 'missing-relative-site': value['relative_skip_fixups'].pop()
        elif label == 'unreviewed-formatting': value['records'][0]['review']['formatting'] = False
        elif label == 'changed-prose': value['records'][0]['english'] += ' Extra words.'
        elif label == 'changed-speaker': value['records'][0]['english'] = value['records'][0]['english'].replace('SPEAKER:09','SPEAKER:02')
        elif label == 'authored-padding': value['records'][0]['english'] += '{PAD}'
        elif label == 'wrong-consumer': value['records'][0]['native_display_consumer'] = 'original_FE_modal_5473C_mode1'
        elif label == 'wrong-source-index': value['records'][0]['source_record_index'] = 141
        elif label == 'wrong-current-index': value['records'][0]['record_index'] = 142
        elif label == 'wrong-Japanese': value['records'][0]['source_hex'] = value['records'][0]['source_hex'][:-2]+'20'
        elif label == 'false-actual':
            false_actual = deepcopy(read(ACTUAL))
            false_actual['changed_Lookout_two_holds_complete_native_actual_ink'] = False
            actual_path = ROOT/'false_actual_proof.json'
            save(actual_path,false_actual)
            value['actual_visual_review'] = str(actual_path)
            bad['dependencies'][str(actual_path)] = sha(actual_path.read_bytes())
        else: value['records'][0]['english'] += '{MACRO:FI}'
        path = ROOT/(label+'.json')
        save(path,value)
        bad[kind] = str(path)
        bad['dependencies'][str(path)] = sha(path.read_bytes())
        cfgpath = ROOT/(label+'_config.json')
        save(cfgpath,bad)
        reject(label,NdsImage.open(PARENT),cfgpath)
    assert len(negatives) == 19
    profile = deepcopy(registry['profiles']['all-routes-unified-v1971'])
    profile.update(lil_lookout_affiliation=CONFIG,status='experimental',
        description='Complete V1971 stack plus one faithful Lookout affiliation wording correction after64-entry fresh lesson review.',
        note='Only SC2 B23 shrinks12bytes. All55commands/12relative spans,120native cases,onechanged/twoadjacent actual panels,sixfull holds,46original results andnormal Brugesreturn pass. Other63entries retain source-reviewed wording andexact inherited display evidence. Patch/startup pending;V1492 stays promoted.')
    registry['profiles'][PROFILE] = profile
    assert registry_path.read_bytes() == raw and builder.read_bytes() == before
    pending = registry_path.with_name('release_stack_v1985_pending.json')
    assert not pending.exists()
    save(pending,registry)
    builder.write_bytes(after)
    os.replace(pending,registry_path)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1) == before
    save(ROOT/'registration_provenance.json',dict(profile=PROFILE,source_profile='all-routes-unified-v1971',
        source_parent=str(PARENT),source_parent_sha256=sha(PARENT.read_bytes()),
        all_previous_profiles_accepted_layers_and_promotion_preserved=True,
        registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(after),release_config_sha256=sha(Path(CONFIG).read_bytes()),
        negative_cases=negatives,source_compiler_exact_to_research_SC2=True,new_registered_candidate_not_yet_built=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(profile=PROFILE,negative_release_cases=19,source_compiler_equals_research=True,accepted_layers=114))
