"""Record editorial/native progress without claiming a new ROM or scene pass."""

from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/refit_editorial_v830_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V830 Refit help source and native review')


def main():
    assert not DOC.exists(), 'Do not double count a checkpoint'
    manuscript, proof, ledger = read(MANUSCRIPT), read(ROOT / 'native_font_verification.json'), read(LEDGER)
    assert len(manuscript['records']) == len(proof['records']) == 31
    assert proof['candidate_sha256'] == manuscript['current_candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    validate_natural_dialogue_batch(manuscript)
    assert proof['native_pixels_compared'] == 562464
    for row, native in zip(manuscript['records'], proof['records'], strict=True):
        compiled, lines = compile_paragraph(row['english'])
        assert compiled.hex() == native['compiled_hex'] and lines == native['lines']
        assert len(lines[-1].split()) > 1
        assert sha(Path(native['native_preview']).read_bytes()) == native['native_preview_sha256']
    for sheet in proof['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    proof['visual_review_pending'] = False
    proof['visual_review'] = {
        'all_four_current_complete_sheets_opened': True,
        'all31_native_body_planes_inspected': True,
        'all_line_starts_left_aligned_complete_first_and_final_letters': True,
        'no_single_word_final_rows': True,
        'first_draft_short_tail_findings': [1251, 1275, 1280, 1281],
        'no_authored_alignment_or_line_breaks': True,
        'scope': 'Controlled native body planes, not final composited gameplay screenshots.'}
    save(ROOT / 'native_font_verification.json', proof)
    save(ROOT / 'editorial_ledger_before_V830.json', ledger)
    assert ledger['records_editorially_completed'] == 603
    assert ledger['records_with_source_and_prose_pass'] == 606
    assert ledger['reviewed_but_incomplete_COMMON_IDs'] == [750, 751, 752]
    ids = [r['message_id'] for r in manuscript['records']]
    decisions = {k: [r['message_id'] for r in manuscript['records'] if r['editorial_decision'] == k]
                 for k in ('revise', 'retain')}
    assert len(decisions['revise']) == 18 and len(decisions['retain']) == 13
    entry = {
        'documentation': str(DOC), 'manuscript': str(MANUSCRIPT),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'source_context_packet': str(ROOT / 'source_context_packet.json'),
        'source_context_packet_sha256': sha((ROOT / 'source_context_packet.json').read_bytes()),
        'controlled_native_proof': str(ROOT / 'native_font_verification.json'),
        'controlled_native_proof_sha256': sha((ROOT / 'native_font_verification.json').read_bytes()),
        'native_message_IDs': ids, 'editorial_decisions': decisions,
        'status': '31-source-prose-and-controlled-native-reviewed-release-and-actual-scene-pending',
        'no_completed_entry_credit': True, 'current_integrated_ROM_unchanged': str(ROM),
        'new_ROM_or_patch_not_generated': True,
        'remaining_gates': ['Source-locked late COMMON integration preserving all unselected native selections and cache bounds',
                            'Registered combined ROM and exact clean-input patch',
                            'Actual revised help-panel composition, entry/exit and ordinary startup regression'],
        'graphics_and_all18_plaques_remain_separately_unfinished': True,
        'full_goal_complete': False}
    ledger['refit_help_editorial_v830'] = entry
    ledger['research_checkpoints'].append({'id': 'V830-Refit-help-editorial-and-native-review', **entry})
    ledger['records_with_source_and_prose_pass'] = 637
    ledger['records_with_source_prose_drafts'] = 637
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] = 636
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted([750, 751, 752, *ids])
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': ledger['reviewed_but_incomplete_COMMON_IDs'],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '3-older-context-unmapped-and31-Refit-integration-actual-display-pending',
        'note': 'The52 ceremony entries were completed in V829 and are no longer active drafts. Their earlier metadata is preserved in the V830 before-ledger snapshot. Refit31 has fresh source/prose and controlled native-font coverage, not new gameplay or completed-entry credit.'}
    ledger['latest_checkpoint'] = (
        'V830 freshly reviews all31 Refit room/equipment help paragraphs against clean Japanese and current V829 selections:18 proposed revisions and13 justified retentions. '
        'All31 current native font executions match complete independent168x108 planes (562464 pixels), preserve guards/ABI and leave heading/detail rows untouched. '
        'All four sheets are visually reviewed;four initial stranded-word tails are corrected without manual spacing or breaks. '
        'Current integrated release remains V829. Source-locked COMMON integration, registered ROM/patch, actual revised panel compositions and entry/exit/startup tests remain pending. '
        'Ledger:603 completed,637 source/prose reviewed,34 reviewed entries incomplete. Ceremony52 is removed from stale active-draft metadata. '
        'The complete editorial goal and separate graphics/all18-plaque audit remain unfinished.')
    ledger['findings'].append({'id': 'COMMON-Refit-help31-V830-editorial',
                               'file': '/COMMON/MESFILE.DK4', 'native_message_IDs': ids,
                               'status': entry['status'], 'proof': str(ROOT / 'native_font_verification.json'),
                               'detail': 'Corrected cure-versus-treat, fatigue prose, following-wind specificity, alternative stern fittings, square-sail identity and four short-tail layouts. All room limits and directional placement rules retained.',
                               'no_completion_credit': True})
    assert ledger['records_revised_and_integrated'] == 438
    assert ledger['retained_wordings_editorially_completed'] == 165
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 637
    save(LEDGER, ledger)
    DOC.write_text('''# V830: Refit help editorial and native-font review

All31 help entries (1247-1255 and1268-1289) have a fresh editorial review against
the clean Japanese and exact current V829 selections, with surrounding1245-1290
records saved as context. Spoken1256-1267 and HELP articles remain separate.
The manuscript contains18 proposed revisions and13 justified retained wordings.

The revisions preserve the doctor's ability to cure ailments, separate resource
conservation from slower sailor fatigue, clarify following winds, restore the
stern gun/jigger spanker alternative and the final sail's square-sail identity,
and preserve the four-room/five-hold limits and sail placement restrictions.

## Formatting evidence

All31 paragraphs execute through the current original font painter using a
captured help object and a supplied9072-byte allocation. Complete independent
168x108 masks match all562464 pixels, every first/final letter, blank cells and
guard buffers. Body ink stays within the first60 rows; the following heading and
detail regions remain untouched. All four sheets were opened and reviewed.
Four initial single-word tails (1251,1275,1280,1281) were corrected through natural
prose; no manual alignment or line breaks were authored. The first draft is
preserved under `work/analysis/refit_editorial_v830_first_draft`.

These are controlled native-font tests, not31 new gameplay observations. Earlier
V712 actual23 help compositions cover13 messages; those retain their original
scope and do not establish the new wording's final GPU composition.

## Remaining release work

V829 remains the current integrated experimental ROM. No new ROM/patch is claimed.
Next: source-locked late COMMON integration; preserve all unselected strings,
opaque spans, cache bounds and existing renderers; build through a registered
combined profile and verify its exact clean-input patch; exercise revised help
panels, entry/exit and ordinary startup in the actual emulator. Do not modify an
old frozen stage or relax its original full-input guards.

Ledger:603 completed (438 revised/165 retained),637 source/prose reviewed,
34 reviewed entries incomplete (three older750-752 plus31 Refit). The already
completed52 ceremony entries are removed from stale active-draft metadata.
The full editorial goal, raw-source coverage revisit and separate graphics audit,
including all18 plaques, remain unfinished. No donor saves were modified.
''', encoding='utf-8')
    paragraph = '\n\n## V830: Refit help editorial/native review\n\n' + ledger['latest_checkpoint'] + ' See [V830 evidence](refit_editorial_v830_checkpoint.md).\n'
    for path in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md'):
        with Path(path).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    archive_current()
    print('V830 recorded:603 completed,637 source/prose,34 pending. Current ROM V829;archive hashes verified.', flush=True)


def archive_current():
    sources = [MANUSCRIPT, LEDGER, DOC, Path(__file__),
               Path('scripts/prepare_refit_editorial_v830.py'), Path('scripts/verify_refit_editorial_v830.py'),
               *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('native_previews/*.png')]
    for path in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md')):
        sources.append(path)
    manifest = []
    for path in sources:
        # Preserve the logical work/analysis path across its E: junction.
        relative = path.absolute().relative_to(Path.cwd())
        dest = ARCHIVE / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        copy2(path, dest)
        assert sha(path.read_bytes()) == sha(dest.read_bytes())
        manifest.append({'source': str(path), 'archive': str(dest), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': manifest,
                                         'all_copies_hash_verified': True,
                                         'not_guide_screenshots': 'Controlled native font sheets; final gameplay captures pending.'})
    copy2(ROOT / 'archive_manifest.json', ARCHIVE / 'archive_manifest.json')


if __name__ == '__main__':
    main()
