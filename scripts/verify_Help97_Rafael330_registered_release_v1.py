"""Bind the original 678-entry build to qualified ordered plans and exact clean patch.

Reuse the sealed native/visual/gameplay proofs via their exact dependencies. Do
not turn composite Help observations or initialized story fixtures into claims
of a natural playthrough of the final ROM.
"""
import argparse
import os
import struct
import sys
from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.verify_release_baseline import main as verify_baseline
from scripts.verify_rafael_B51_B60_registered_release import KEYS, PIPELINES

PARENT = Path('work/analysis/Sea22_Fleet66_release_verified_20261105/registered_release_verification.json')
QUAL = Path('work/analysis/Help97_Rafael330_release_qualification_20261105/qualification.json')
BUILD = Path('work/analysis/Help97_Rafael330_registered_build_20261105')
FILES = ['/COMMON/HELP.DK4', '/data/SC0.DK4']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['candidate', 'preparation', 'out']:
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists() and not args.candidate.with_suffix('.xdelta').exists()
    prep, parentproof, qualification = map(load, [args.preparation, PARENT, QUAL])
    terminal = load(BUILD/'completion.json')
    assert terminal['terminal'] and terminal['driver_completed_without_exception']
    assert terminal['all_original_driver_andregistry_bytes_unchanged']
    assert not terminal['garbage_collection']['errors']
    assert terminal['registry_sha256'] == prep['registry_sha256']
    assert terminal['original_locked_ROM_core_sha256'] == sha(Path('dk4tool/rom/nds.py').read_bytes())
    for path, digest in terminal['driver_andcanonical_bytes'].items():
        assert sha(Path(path).read_bytes()) == digest
    registry_path = Path('translations/release_stack.json')
    registry = load(registry_path)
    profile = registry['profiles'][prep['profile']]
    manifest_path = args.candidate.with_suffix('.manifest.json')
    manifest = load(manifest_path)
    parentpath = Path(parentproof['candidate'])
    pm = load(parentpath.with_suffix('.manifest.json'))
    assert sha(registry_path.read_bytes()) == prep['registry_sha256'] == manifest['release_stack_sha256']
    assert manifest['profile'] == prep['profile'] == terminal['profile']
    assert len(manifest['checks']) == 26 and all(manifest['checks'].values())
    assert all(manifest['checks'][k] == v for k, v in pm['checks'].items())
    assert manifest['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    stagepaths = [Path(profile[k]) for k in KEYS]
    assert stagepaths == [Path(prep['preserved_stage_configs'][k]) for k in KEYS]
    stagespecs = list(map(load, stagepaths))
    extensionpaths = list(map(Path, prep['configs']))
    extensions = list(map(load, extensionpaths))
    assert len(extensions) == 3 and profile['late_editorial_extensions'][-3:] == prep['new_extension_specs']
    manuscripts = [str(Path(c['manuscript'])) for c in extensions]
    assert manifest['batches'] == [*pm['batches'][:-8], *manuscripts, *map(str, stagepaths)]
    assert len(manifest['batches']) == prep['expected_manifest_entries'] == 678
    assert manifest['required_batches'] == pm['required_batches']
    assert qualification['preparation_sha256'] == sha(args.preparation.read_bytes())
    assert qualification['registry_sha256'] == prep['registry_sha256']
    assert qualification['direct_prepublication_andshared_targets_equal']
    assert len(qualification['changed_scope_andordering_rejections']) == 11
    assert qualification['unchanged_eight_final_stage_contracts_compared_exactly']
    assert qualification['all_inputs_unowned_files_components_andcomplete_inverses_preserved']
    assert qualification['seven_FE_and15_menu_negative_native_proofs_reused']
    for spec, conf, proof in zip(prep['new_extension_specs'], extensions, qualification['positive_ordered_shared_plans'], strict=True):
        assert sha(Path(spec['config']).read_bytes()) == spec['config_sha256'] == proof['release_config_sha256']
        assert sha(Path(*spec['module'].split('.')).with_suffix('.py').read_bytes()) == spec['module_sha256'] == proof['module_sha256']
        assert proof['parent_ROM_sha256'] == conf['parent_ROM_sha256']
        assert proof['target_ROM_sha256'] == conf['target_ROM_sha256']
        assert proof['one_complete_NDS_object_commit_after_all_gates']
    for conf in [*extensions, *stagespecs]:
        for path, digest in conf.get('dependencies', {}).items():
            assert sha(Path(path).read_bytes()) == digest, path
    original = load(Path(prep['previous_preparation']).parent/'release_stack_before.json')
    assert registry['accepted_layers'] == original['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert all(registry['profiles'][k] == v for k, v in original['profiles'].items())
    present = {str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present for r in registry['accepted_layers'])
    baseline = Path(registry['canonical_baseline']['path'])
    assert manifest['base_sha256'] == sha(baseline.read_bytes()) == registry['canonical_baseline']['sha256']
    assert sha(parentpath.read_bytes()) == parentproof['candidate_sha256'] == pm['candidate_sha256']
    assert sha(args.candidate.read_bytes()) == manifest['candidate_sha256'] == prep['target_ROM_sha256']
    assert args.candidate.read_bytes() == Path(prep['final_ROM']).read_bytes()
    states = [Path(manifest[a][b]) for a, b in PIPELINES]+[args.candidate]
    assert sha(states[0].read_bytes()) == extensions[-1]['target_ROM_sha256']
    for i, (path, conf) in enumerate(zip(stagepaths, stagespecs, strict=True)):
        assert sha(states[i].read_bytes()) == conf['parent_ROM_sha256']
        assert sha(states[i+1].read_bytes()) == conf['target_ROM_sha256']
        sm = load(states[i+1].with_suffix('.manifest.json'))
        assert sm['release_stack_sha256'] == prep['registry_sha256']
        assert sm['candidate_sha256'] == conf['target_ROM_sha256'] and all(sm['checks'].values())
        assert str(path) in sm['batches']
    parent, candidate = map(NdsImage.open, [parentpath, args.candidate])
    assert [p for _, p, v in parent.iter_files() if candidate.read_file(p) != v] == FILES
    assert all(candidate.read_file(p) == v for p, v in parent.iter_components())
    helpraw, storyraw = [candidate.read_file(p) for p in FILES]
    assert sha(helpraw) == extensions[1]['target_HELP_sha256']
    assert helpraw == Path(extensions[1]['target_resource']).read_bytes()
    rebuild = load(extensions[2]['reconstruction'])
    assert sha(storyraw) == rebuild['target_archive_sha256']
    beforeblocks, storyblocks = [IlnkContainer.parse(raw).blocks for raw in [parent.read_file(FILES[1]), storyraw]]
    assert len(beforeblocks) == len(storyblocks) == 343
    assert [i for i, (a, b) in enumerate(zip(beforeblocks, storyblocks, strict=True)) if a != b] == [81, 82, 83, 84]
    for group in rebuild['groups']:
        assert sha(storyblocks[group['block']]) == group['target_sha256']
    helpblocks = IlnkContainer.parse(helpraw).blocks
    assert len(helpblocks) == 217 and helpblocks[203] == b'\0'
    bindings = []
    helpstats = dict(native_pages=0, observed_pages=0, offline_only_pages=0, observed_articles=0)
    for conf in extensions[:2]:
        doc = load(conf['manuscript'])
        for row in doc['records']:
            assert all(row['review'].values())
            pages = []
            for ref in row['planned_stored_pages']:
                b = ref['block']
                raw = bytes.fromhex(ref['exact_stored_hex'])
                offset = struct.unpack_from('<I', helpraw, 8+4*b)[0]
                assert helpraw[offset:offset+len(raw)] == helpblocks[b] == raw
                assert sha(Path(ref['native_preview']).read_bytes()) == ref['native_preview_sha256']
                if 'actual_frame' in ref:
                    assert sha(Path(ref['actual_capture']).read_bytes()) == ref['actual_capture_sha256']
                pages.append({**deepcopy(ref), 'archive_offset': offset, 'target_archive_sha256': sha(helpraw),
                    'source_page_proof': conf['actual'], 'source_page_proof_sha256': sha(Path(conf['actual']).read_bytes())})
            observed = sum('actual_frame' in p for p in pages)
            helpstats['native_pages'] += len(pages)
            helpstats['observed_pages'] += observed
            helpstats['offline_only_pages'] += len(pages)-observed
            helpstats['observed_articles'] += int(bool(observed))
            bindings.append(dict(id=row['id'], file_path=FILES[0], source_reference=row['source_reference'], source_hex=row['source_hex'],
                current_reference=row['current_reference'], current_hex=row['current_hex'], registered_pages=pages,
                decision=row['decision'], finding=row['finding'], retention_reason=row.get('retention_reason'), review=row['review'],
                new_source_credit_eligible=row['topic_id'] != 33))
    assert helpstats == dict(native_pages=103, observed_pages=56, offline_only_pages=47, observed_articles=51)
    storydoc = load(extensions[2]['manuscript'])
    for row in storydoc['records']:
        assert all(row['review'].values())
        ref = row['planned_integrated_reference']
        raw, block, at = bytes.fromhex(ref['exact_stored_hex']), storyblocks[row['block']], ref['offset']
        assert block[at:at+len(raw)+1] == raw+b'\0' and ref['target_archive_sha256'] == sha(storyraw)
        if row['kind'] != 'typed-choice-label':
            assert block[ref['header_offset']:at+1].hex() == row['source_complete_preamble_hex']
        bindings.append(dict(id=row['id'], file_path=FILES[1], block=row['block'], source_reference=row['source_reference'], source_hex=row['source_hex'],
            current_reference=row['current_reference'], current_hex=row['current_hex'], registered_reference=ref,
            decision=row['decision'], finding=row['finding'], retention_reason=row.get('retention_reason'), review=row['review'], new_source_credit_eligible=True))
    assert len(bindings) == 428 and len({(r['file_path'], r['id']) for r in bindings}) == 428
    new = [r for r in bindings if r['new_source_credit_eligible']]
    assert (len(new), sum(r['decision'] == 'revision' for r in new), sum(r['decision'] == 'retention' for r in new)) == (427, 191, 236)
    actual = load(extensions[2]['actual'])
    assert (actual['source_speeches_observed'], actual['native_commands_observed'], actual['native_body_pages_observed'], actual['actual_choice_labels'], actual['offline_only_source_speeches']) == (75, 77, 86, 5, 250)
    inverse = deepcopy(candidate)
    for path in FILES:
        inverse.replace_file(path, parent.read_file(path))
    assert bytes(inverse.rom.save()) == parentpath.read_bytes()
    oldargv = sys.argv
    try:
        sys.argv = ['verify_release_baseline', str(baseline), str(args.candidate)]
        for path in manifest['changed_paths']:
            sys.argv += ['--allow-path', path]
        verify_baseline()
    finally:
        sys.argv = oldargv
    args.out.mkdir(parents=True)
    patch = args.candidate.with_suffix('.xdelta')
    reconstruction = args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    clean = Path(extensions[0]['clean_ROM'])
    assert sha(clean.read_bytes()) == extensions[0]['clean_ROM_sha256']
    make_xdelta(clean, args.candidate, patch)
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == args.candidate.read_bytes()
    bound = args.out/'exact_integrated_record_bindings.json'
    save(bound, dict(candidate=str(args.candidate), candidate_sha256=manifest['candidate_sha256'], records=bindings,
        all428_exact_source_current_target_refs_andindividual_five_gates_bound=True,
        source_owned_FE_child_commands_bound_by_exact_whole_reconstruction_andqualified_consumer_proofs=True, new_credit=0))
    coverage = args.out/'composite_page_coverage.json'
    save(coverage, dict(candidate=str(args.candidate), candidate_sha256=manifest['candidate_sha256'],
        proof_groups=[dict(manuscript=c['manuscript'], actual=c['actual'], actual_sha256=sha(Path(c['actual']).read_bytes())) for c in extensions],
        help=helpstats, story=dict(native_source_speeches=325, native_commands=327, native_body_pages=336, typed_labels=5,
            observed_source_speeches=75, observed_commands=77, observed_body_pages=86, observed_choices=5, offline_only_source_speeches=250),
        exact_dependency_qualified_existing_native_visual_andactual_evidence_reused=True,
        no_old_RAM_orcaptures_relabelled_as_final_ROM=True, all_content_observed_on_one_final_ROM=False,
        actual_full_story_playthrough=False, natural_story_activation=False, hardware=False, new_credit=0))
    save(args.out/'registered_release_verification.json', dict(candidate=str(args.candidate), candidate_sha256=manifest['candidate_sha256'],
        manifest=str(manifest_path), manifest_sha256=sha(manifest_path.read_bytes()), profile=manifest['profile'], registry_sha256=prep['registry_sha256'],
        canonical_base=str(baseline), canonical_sha256=manifest['base_sha256'], parent=str(parentpath), parent_sha256=parentproof['candidate_sha256'],
        changed_internal_files=FILES, changed_components=[], target_HELP_sha256=sha(helpraw), target_SC0_sha256=sha(storyraw),
        only_HELP_andSC0_B81_B84_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent=True,
        complete_stack_entries=678, accepted_layers=114, passing_release_checks=26, all_eight_registered_final_stages_preserved=True,
        Fernan_name_field_proof=manifest['relocations']['/__arm9__.bin']['owned_Fernan_name_field']['proof'],
        new_contextual_records=427, prose_revisions=191, justified_retentions=236, previously_credited_amendments=[33],
        all427_exact_integrated_references_bound=True, exact_record_bindings=str(bound), exact_record_bindings_sha256=sha(bound.read_bytes()),
        composite_page_coverage=str(coverage), composite_page_coverage_sha256=sha(coverage.read_bytes()),
        byte_exact_to_reviewed_research_image=True, patch=str(patch), patch_sha256=sha(patch.read_bytes()), clean_input_sha256=sha(clean.read_bytes()),
        exact_clean_reconstruction=str(reconstruction), reconstructed_sha256=sha(reconstruction.read_bytes()), clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True, experimental_not_promoted=True, full_goal_complete=False, new_credit=0,
        preparation=str(args.preparation), preparation_sha256=sha(args.preparation.read_bytes()), qualification=str(QUAL), qualification_sha256=sha(QUAL.read_bytes()),
        original_registered_terminal=str(BUILD/'completion.json'), original_registered_terminal_sha256=sha((BUILD/'completion.json').read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path = Path('translations/rom_retention_pins.json')
    beforebytes = pins_path.read_bytes()
    pins = load(pins_path)
    (args.out/'pins.before.json').write_bytes(beforebytes)
    for rom in [args.candidate, reconstruction, *Path('work/h97r330').rglob('*.nds')]:
        if not any(Path(r['path']).resolve() == rom.resolve() for r in pins):
            pins.append(dict(path=str(rom.resolve()), reason='Preserve678 cumulative build/intermediate/clean reconstruction. SHA256 '+sha(rom.read_bytes())))
    pending = pins_path.with_name('rom_retention_pins.Help97_Rafael330_verified.pending.json')
    assert not pending.exists()
    save(pending, pins)
    assert pins_path.read_bytes() == beforebytes
    os.replace(pending, pins_path)
    print('678 entries/114 layers/eight stages/427 new objects/one amendment/exact clean patch pass. Own registered RAM binding pending.')


if __name__ == '__main__':
    main()
