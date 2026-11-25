"""Combine disjoint owned blocks; qualify existing local native proofs without rerendering prose."""
import gc
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael516_combined_research_v1_20261105')
A = Path('work/analysis/Rafael261_rebased678_20261105/reconstruction.json')
B = Path('work/analysis/Rafael255_rebuilt678_v2_20261105/reconstruction.json')
REVIEW = Path('translations/rafael_B101_B120_contextual_final_review_v1.json')
FINAL = Path('translations/rafael_B101_B120_cumulative516_refs_v1.json')
PLAN = Path('work/analysis/Rafael255_checked_v2_20261105/release_plans.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists()
    a, b, doc, plan = map(load, [A, B, REVIEW, PLAN])
    assert a['parent_sha256'] == b['parent_sha256'] == 'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'
    assert not set(a['reviewed_blocks']) & set(b['reviewed_blocks'])
    for r in [a, b]:
        assert sha(Path(r['research_ROM']).read_bytes()) == r['research_ROM_sha256']
        assert sha(Path(r['target_archive']).read_bytes()) == r['target_archive_sha256']
        assert r['all_other_files_components_exact']
    parent = NdsImage.open(a['research_ROM'])
    verified = NdsImage.open(b['parent'])
    own = NdsImage.open(b['research_ROM'])
    path = doc['file_path']; before = parent.read_file(path)
    blocks, oldblocks, targets = [IlnkContainer.parse(raw).blocks for raw in
        [before, verified.read_file(path), own.read_file(path)]]
    assert len(blocks) == len(oldblocks) == len(targets) == 343
    assert sha(before) == a['target_archive_sha256']
    receipts = []
    for group in b['groups']:
        n = group['block']
        assert blocks[n] == oldblocks[n] and sha(blocks[n]) == group['current_sha256']
        assert sha(targets[n]) == group['target_sha256']
        receipts.append(dict(block=n, current_block_sha256=sha(blocks[n]), target_block_sha256=sha(targets[n]),
                             all_owned_offsets_commands_relatives_andnative_input_bytes_exact=True))
    for n in b['changed_blocks']:
        blocks[n] = targets[n]
    combined = IlnkContainer(blocks).to_bytes()
    assert [n for n, (x,y) in enumerate(zip(oldblocks, blocks, strict=True)) if x != y] == sorted(a['changed_blocks']+b['changed_blocks'])
    inverse = list(blocks)
    for n in b['changed_blocks']:
        inverse[n] = oldblocks[n]
    assert IlnkContainer(inverse).to_bytes() == before
    for n in range(343):
        assert blocks[n] == (targets[n] if n in b['changed_blocks'] else IlnkContainer.parse(before).blocks[n])
    for resource in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT']:
        assert parent.read_file(resource) == verified.read_file(resource) == own.read_file(resource)
    ROOT.mkdir(parents=True)
    archive = ROOT/'combined_SC0.DK4'; archive.write_bytes(combined)
    parent.replace_file(path, combined)
    assert [p for _,p,v in verified.iter_files() if parent.read_file(p) != v] == [path]
    assert all(parent.read_file(p) == v for p,v in verified.iter_components())
    rom = ROOT/'combined_RESEARCH_ONLY.nds'; parent.save(rom)
    restored = NdsImage.open(rom); restored.replace_file(path, before)
    assert bytes(restored.rom.save()) == Path(a['research_ROM']).read_bytes()
    restored.replace_file(path, verified.read_file(path))
    assert bytes(restored.rom.save()) == Path(b['parent']).read_bytes()
    del restored, own, verified, parent
    gc.collect()
    for row in doc['records']:
        ref = row['planned_integrated_reference']
        assert ref['target_archive_sha256'] == b['target_archive_sha256']
        raw = bytes.fromhex(ref['exact_stored_hex']); at = ref['offset']
        assert blocks[row['block']][at:at+len(raw)+1] == raw+b'\0'
        ref['target_archive_sha256'] = sha(combined)
    doc.update(research_review_before_rebase=str(REVIEW), research_review_before_rebase_sha256=sha(REVIEW.read_bytes()),
               current_comparison_stays_bound_to_verified678_owned_blocks=True,
               only_whole_archive_reference_digest_changed_no_new_prose_layout_orcoverage=True)
    validate_natural_dialogue_batch(doc); save(FINAL, doc)
    plan.update(manuscript=str(FINAL), manuscript_sha256=sha(FINAL.read_bytes()))
    save(ROOT/'release_plans.json', plan)
    rebased = deepcopy(b)
    rebased.update(parent=a['research_ROM'], parent_sha256=a['research_ROM_sha256'],
        source_archive_sha256=sha(before), target_archive=str(archive), target_archive_sha256=sha(combined),
        research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()),
        manuscript=str(FINAL), manuscript_sha256=sha(FINAL.read_bytes()),
        plan=str(ROOT/'release_plans.json'), plan_sha256=sha((ROOT/'release_plans.json').read_bytes()),
        original_storage_reconstruction=str(B), original_storage_reconstruction_sha256=sha(B.read_bytes()),
        parent_is_qualified_unregistered261_research_not_a_registered_release=True,
        registered_predecessor_is_verified678=True)
    save(ROOT/'reconstruction.json', rebased)
    save(ROOT/'dependency_reuse.json', dict(original_reconstruction=str(B), original_reconstruction_sha256=sha(B.read_bytes()),
        rebased_reconstruction=str(ROOT/'reconstruction.json'), rebased_reconstruction_sha256=sha((ROOT/'reconstruction.json').read_bytes()),
        previous261_reconstruction=str(A), previous261_reconstruction_sha256=sha(A.read_bytes()),
        original_review=str(REVIEW), original_review_sha256=sha(REVIEW.read_bytes()),
        rebased_review=str(FINAL), rebased_review_sha256=sha(FINAL.read_bytes()),
        exact_all20_owned_source_andtarget_blocks=receipts, unchanged_control_only_blocks=[106,107],
        complete_ARM9_COMMON_font_own_context_macro_andname_dependencies_exact=True,
        all_original_local_display_storage_catalogue_andload_inputs_identical=True,
        all_other_files_components_andtwo_complete_serialized_inverses_exact=True,
        no_new_native_execution_gameplay_coverage_orcompletion_credit=True, new_credit=0))
    print('Combined261+255 owned blocks;all20 local255 source/target blocks andruntime dependencies exact. No prose ordisplay tests repeated. Research only;registered preparation pending.')
