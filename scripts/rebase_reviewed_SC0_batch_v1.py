"""Rebase owned reviewed blocks and qualify exact offline proof reuse on a newer release.

No prose or native page bytes are changed. The original execution identity stays
explicit in each rebound proof; captures are never relabelled as new gameplay.
"""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['reconstruction', 'release', 'startup', 'identity', 'out']:
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    old = load(args.reconstruction)
    original_doc, original_native, original_plan, identity = map(load, [old['manuscript'], old['native'], old['plan'], args.identity])
    assert original_doc['file_path'] == '/data/SC0.DK4' and original_native['manuscript_sha256'] == old['manuscript_sha256'] == sha(Path(old['manuscript']).read_bytes())
    assert original_plan['manuscript_sha256'] == old['manuscript_sha256'] and not original_plan['failures']
    assert original_native['plan_sha256'] == old['plan_sha256'] == sha(Path(old['plan']).read_bytes())
    runtime = original_native['runtime']
    prior = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=0)
    current = RegisteredRuntime(args.release, args.startup, captain=0)
    assert prior.receipt() == runtime == identity['runtime']
    assert prior.arm == current.arm and prior.common == current.common
    assert prior.image.read_file('/GRP/KANJI.FNT') == current.image.read_file('/GRP/KANJI.FNT')
    assert prior.actor_root == current.actor_root and prior.actor_bytes == current.actor_bytes
    assert sha(prior.image.read_file('/GRP/KANJI.FNT')) == original_native['font_sha256']
    oldresearch = NdsImage.open(old['research_ROM'])
    assert sha(Path(old['research_ROM']).read_bytes()) == old['research_ROM_sha256']
    path = original_doc['file_path']
    previous_archive = prior.image.read_file(path)
    parent_archive = current.image.read_file(path)
    assert sha(previous_archive) == old['source_archive_sha256'] == original_doc['current_archive_sha256']
    previous_blocks, parent_blocks, reviewed_blocks = [IlnkContainer.parse(raw).blocks for raw in [previous_archive, parent_archive, oldresearch.read_file(path)]]
    assert len(previous_blocks) == len(parent_blocks) == len(reviewed_blocks)
    owned = original_doc['blocks']
    assert owned == old['reviewed_blocks'] == [g['block'] for g in old['groups']]
    for group in old['groups']:
        b = group['block']
        assert parent_blocks[b] == previous_blocks[b] and sha(parent_blocks[b]) == group['current_sha256']
        assert sha(reviewed_blocks[b]) == group['target_sha256']
        assert reviewed_blocks[b] == Path(group['target_block']).read_bytes()
    changes_between_parents = [i for i, (a, b) in enumerate(zip(previous_blocks, parent_blocks, strict=True)) if a != b]
    assert not set(changes_between_parents) & set(owned)
    target_blocks = list(parent_blocks)
    for b in owned:
        target_blocks[b] = reviewed_blocks[b]
    target_archive = IlnkContainer(target_blocks).to_bytes()
    assert [i for i, (a, b) in enumerate(zip(parent_blocks, target_blocks, strict=True)) if a != b] == old['changed_blocks']
    inverse = list(target_blocks)
    for b in owned:
        inverse[b] = parent_blocks[b]
    assert IlnkContainer(inverse).to_bytes() == parent_archive
    planned = deepcopy(current.image)
    planned.replace_file(path, target_archive)
    assert [p for _, p, v in current.image.iter_files() if planned.read_file(p) != v] == [path]
    assert all(planned.read_file(p) == v for p, v in current.image.iter_components())
    restored = deepcopy(planned)
    restored.replace_file(path, parent_archive)
    assert bytes(restored.rom.save()) == current.rompath.read_bytes()
    args.out.mkdir(parents=True)
    dependencies = args.out/'dependency_qualification.json'
    qualified = dict(current_runtime=current.receipt(), previous_runtime=runtime,
        reconstruction=str(args.reconstruction), reconstruction_sha256=sha(args.reconstruction.read_bytes()),
        exact_ARM9_COMMON_font_andcomplete_actor_array=True, actor_root=current.actor_root,
        complete_actor_array_sha256=sha(current.actor_bytes), own_current_captain0_route0_startup_verified=True,
        owned_blocks=owned, owned_source_blocks_exact=True, newer_parent_changes_preserved=changes_between_parents,
        all_newer_unowned_files_components_names_graphics_andruntime_preserved=True,
        only_owned_SC0_blocks_replaced_not_old_whole_archive=True,
        prior_native_body_name_macro_andmenu_proofs_qualified_for_exact_inputs=True,
        no_native_execution_oractual_capture_relabelled_as_new_runtime=True, new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(dependencies, qualified)
    rebound_identity = deepcopy(identity)
    rebound_identity.update(runtime=current.receipt(), original_native_execution_runtime=runtime,
        original_identity_proof=str(args.identity), original_identity_proof_sha256=sha(args.identity.read_bytes()),
        dependency_qualification=str(dependencies), dependency_qualification_sha256=sha(dependencies.read_bytes()),
        exact_qualified_identity_reuse_not_new_getter_execution=True)
    identity_path = args.out/'qualified_scoped_identity.json'
    save(identity_path, rebound_identity)
    doc = deepcopy(original_doc)
    doc.update(current_ROM=str(current.rompath), current_ROM_sha256=current.release['candidate_sha256'], current_archive_sha256=sha(parent_archive),
        original_current_comparison_ROM=original_doc['current_ROM'], original_current_comparison_ROM_sha256=original_doc['current_ROM_sha256'],
        original_current_effective_native_execution_not_relabelled=True,
        previous_manuscript=old['manuscript'], previous_manuscript_sha256=old['manuscript_sha256'],
        scoped_identity_proof=str(identity_path), scoped_identity_proof_sha256=sha(identity_path.read_bytes()),
        rebase_qualification=str(dependencies), rebase_qualification_sha256=sha(dependencies.read_bytes()),
        all_English_andindividual_prose_decisions_unchanged=True, all_fifth_formatting_gates_pending=True)
    docpath = args.out/'manuscript.json'
    save(docpath, doc)
    plan = deepcopy(original_plan)
    plan.update(manuscript=str(docpath), manuscript_sha256=sha(docpath.read_bytes()), previous_plan=old['plan'], previous_plan_sha256=old['plan_sha256'],
        exact_compiled_bytes_andnative_geometry_reused=True, dependency_qualification=str(dependencies), dependency_qualification_sha256=sha(dependencies.read_bytes()))
    planpath = args.out/'plans.json'
    save(planpath, plan)
    native = deepcopy(original_native)
    native.update(runtime=current.receipt(), manuscript=str(docpath), manuscript_sha256=sha(docpath.read_bytes()), plan=str(planpath), plan_sha256=sha(planpath.read_bytes()),
        original_native_execution_runtime=runtime, original_native_proof=old['native'], original_native_proof_sha256=old['native_sha256'],
        exact_qualified_runtime_reuse_not_new_execution=True, dependency_qualification=str(dependencies), dependency_qualification_sha256=sha(dependencies.read_bytes()))
    nativepath = args.out/'qualified_native_pages.json'
    save(nativepath, native)
    resource = args.out/'reviewed_RESEARCH_ONLY.DK4'
    resource.write_bytes(target_archive)
    rom = args.out/'reviewed_RESEARCH_ONLY.nds'
    rom.write_bytes(bytes(planned.rom.save()))
    assert NdsImage.open(rom).read_file(path) == target_archive
    reconstruction = deepcopy(old)
    rebound_compound = {}
    for key in ['menu', 'styles']:
        source = Path(old[key])
        compound = load(source)
        assert compound['runtime'] == runtime and compound['manuscript_sha256'] == old['manuscript_sha256']
        compound.update(runtime=current.receipt(), manuscript=str(docpath), manuscript_sha256=sha(docpath.read_bytes()),
            original_native_execution_runtime=runtime, original_native_proof=str(source), original_native_proof_sha256=sha(source.read_bytes()),
            exact_qualified_runtime_reuse_not_new_execution=True, dependency_qualification=str(dependencies), dependency_qualification_sha256=sha(dependencies.read_bytes()))
        if key == 'styles':
            compound.update(plan=str(planpath), plan_sha256=sha(planpath.read_bytes()))
        rebound_compound[key] = args.out/f'qualified_{key}.json'
        save(rebound_compound[key], compound)
    reconstruction.update(parent=str(current.rompath), parent_sha256=current.release['candidate_sha256'],
        source_archive_sha256=sha(parent_archive), target_archive=str(resource), target_archive_sha256=sha(target_archive),
        research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()),
        manuscript=str(docpath), manuscript_sha256=sha(docpath.read_bytes()), plan=str(planpath), plan_sha256=sha(planpath.read_bytes()),
        native=str(nativepath), native_sha256=sha(nativepath.read_bytes()),
        menu=str(rebound_compound['menu']), menu_sha256=sha(rebound_compound['menu'].read_bytes()),
        styles=str(rebound_compound['styles']), styles_sha256=sha(rebound_compound['styles'].read_bytes()),
        original_reconstruction=str(args.reconstruction), original_reconstruction_sha256=sha(args.reconstruction.read_bytes()),
        dependency_qualification=str(dependencies), dependency_qualification_sha256=sha(dependencies.read_bytes()),
        exact_owned_block_proofs_reused_all_unowned_newer_blocks_preserved=True)
    save(args.out/'reconstruction.json', reconstruction)
    pins = Path('translations/rom_retention_pins.json')
    pinlist = load(pins)
    absolute = str(rom.resolve())
    assert not any(Path(r['path']).resolve() == rom.resolve() for r in pinlist)
    pinlist.append(dict(path=absolute, reason='Owned SC0 batch rebased onto verified newer cumulative parent. Preserve for stored/gameplay/release proofs. SHA256 '+sha(rom.read_bytes())))
    save(pins, pinlist)
    print(dict(owned_blocks=len(owned), changed_blocks=len(old['changed_blocks']), newer_parent_blocks_preserved=changes_between_parents,
        native_pages_reused=native['pages'], research_ROM=str(rom), SHA256=sha(rom.read_bytes()), new_credit=0), flush=True)


if __name__ == '__main__':
    main()
