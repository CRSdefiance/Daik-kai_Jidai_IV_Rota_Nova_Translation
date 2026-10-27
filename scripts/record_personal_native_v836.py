"""Record the native Deck encoder/letter proof without release completion credit."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_personal_fonts_v836 import ROOT, ROM, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/personal_chatter_v836_native_layout.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V836 Personal comment native fonts and phase repair')


def main():
    assert not DOC.exists()
    proof_path, phase_path = ROOT / 'native_font_proof.json', ROOT / 'phase_and_letter_controls.json'
    proof, phase, ledger, doc = read(proof_path), read(phase_path), read(LEDGER), read(MANUSCRIPT)
    assert ledger['records_editorially_completed'] == 646 and ledger['records_with_source_and_prose_pass'] == 674
    assert proof['candidate_sha256'] == phase['candidate_sha256'] == sha(ROM.read_bytes()) == ledger['current_integrated_candidate']['sha256']
    assert sha(MANUSCRIPT.read_bytes()) == proof['manuscript_sha256']
    assert len(proof['cases']) == len(proof['all25_current_wording_baselines']) == 25
    assert len(proof['all144_three_row_parity_and_edge_cases']) == 144
    assert len(phase['all25_first_and_final_glyph_erasure_controls']) == 64
    assert len(phase['invalid_authored_spacing_break_formatting_and_oversize_word_rejections']) == 7
    for key in ('review_sheet',):
        assert sha(Path(proof[key]).read_bytes()) == proof[key + '_sha256']
    assert sha(Path(phase['contrast_sheet']).read_bytes()) == phase['contrast_sheet_sha256']
    assert all(not r['review']['formatting'] for r in doc['records'])
    proof.update(visual_review_pending=False, visual_review={
        'all25_complete_native_canvases_visible_in_final2x_sheet_opened': True,
        'all_generated_boundaries_words_first_final_letters_and_uniform_line_starts_reviewed': True,
        'source_faithful_pauses_used_for_Camille_Charles_and_other_multiline_comments': True,
        'bare_LF_vs_phase_repair_contrast_opened_and_reviewed': True,
        'ink_masks_only_parent_crops_palette_GPU_actual_UI_not_approved': True})
    save(proof_path, proof)
    phase['native_font_proof_sha256'] = sha(proof_path.read_bytes())
    save(phase_path, phase)
    save(ROOT / 'editorial_ledger_before_checkpoint.json', ledger)
    remaining = [
        'Confirm parent composition,source crops,palette and absolute visible Deck comment bounds',
        'Activate normal-source Janus1365,Claudio1366 and a revised odd-row multiline sample using disclosed fixtures if needed',
        'Approve final v2 formatting gates and register the late COMMON stage with all native copies and earlier layers preserved',
        'Build combined ROM and exact clean-input patch;verify actual startup,scene return and preserved earlier content',
        'Record completed-family coverage and final guide/capture provenance']
    ledger['personal_chatter_v836'] = {
        'status': '25-native-fonts-and-generated-phase-repair-proved-parent-actual-integration-pending',
        'manuscript': str(MANUSCRIPT), 'native_proof': str(proof_path), 'phase_proof': str(phase_path),
        'documentation': str(DOC), 'all25_authored_wordings_unchanged': True,
        'remaining_gates': remaining, 'no_completed_entry_credit': True}
    ledger['personal_chatter_v835']['continued_by_native_research'] = str(DOC)
    ledger['personal_chatter_v835']['remaining_gates'] = remaining
    ledger['active_source_prose_drafts']['status'] = 'three-older-context-unmapped-and25-Deck-native-font-proved-parent-actual-release-pending'
    ledger['active_source_prose_drafts']['note'] = 'The25 actor comments have source/prose and controlled native-font/phase coverage. Parent crops/palette,actual samples and registered release remain;28 reviewed pending drafts are not the full remaining scope.'
    finding = {'id': 'Deck-personal-comment-bare-LF-first-letter-phase-v836',
        'native_message_IDs': list(range(1361, 1386)), 'status': 'generated-encoder-phase-repair-proved-not-yet-integrated',
        'detail': 'An unpublished bare-LF serialization of1375 moves S from Sneaking onto the preceding row and shifts the next row. Full byte consumption and glyph-request counts alone miss it. Machine-generated pre-LF space on odd visible rows preserves complete letters at x0. All25 independent full canvases,144 three-row parity/edge cases and64 first/final glyph controls pass. No new shipped-ROM regression or global-other-consumer safety claim.',
        'proof': str(phase_path), 'native_font_proof': str(proof_path), 'no_completion_credit': True}
    assert not any(f.get('id') == finding['id'] for f in ledger['findings'])
    ledger['findings'].append(finding)
    ledger['formatting_watchlist']['Deck_personal_comment_phase_research'] = {
        'proof': str(phase_path), 'status': finding['status'],
        'scope': 'Only the original15334/154CC embedded Deck personal-comment consumer. Parent and actual-display gates remain open.'}
    lead = {'id': 'Samwell-middle-name-Japanese-glyph-native-header-v836',
        'status': 'exact-native-name-parts-confirmed-source-Latin-decision-and-actual-display-pending',
        'detail': 'Actor22 native fields return first Samwell,last Khan and middle835F/ダ. The full native header visibly retains the Japanese middle glyph. Review the source and established Latin naming before changing it;no name edit or source/prose completion count is claimed.',
        'proof': str(ROOT / 'Samwell_middle_name_lead.json'), 'no_completion_credit': True}
    assert not any(f.get('id') == lead['id'] for f in ledger['findings'])
    ledger['findings'].append(lead)
    checkpoint = (
        'V836 maps the original Deck comment canvas252x96 and text rectanglex0/y60,width252/42 ASCII cells,height36/3 rows. '
        'Original actor selector,macro expansion,context,overlay0 clear and complete bitmap/font painting execute for all25 current and25 proposed comments. '
        'Every252x96 canvas matches independent ASCII/CP932 pixels;all25 authored words,64 first/final glyph erasure controls,7 invalid-author inputs and144 three-row phase/edge cases pass. '
        'Seven original width/height cases confirm1-126 bytes consumed and127 clipped to126. '
        'A real unpublished bare-LF encoder bug moved the S in Sneaking to the previous row;generated pre-LF phase spaces on odd rows repair it with no visible indent or wording changes. '
        'All25 native ink masks and the rejected-vs-repaired contrast are visually reviewed. '
        'Parent crop/palette/absolute bounds,actual source activity samples,v2 final format gates,registered COMMON/ROM/patch and completion credit remain. '
        'A separate exact native Samwell middle-nameダ lead is recorded without changing names or counts. '
        'V834 remains current;646 complete,674 source/prose reviewed,28 reviewed drafts pending. All wider prose/raw coverage and separate graphics/all18 plaques remain open;full goal active.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['research_checkpoints'].append({'id': 'V836-Deck-personal-comment-native-fonts',
        'native_message_IDs': list(range(1361, 1386)), 'proof': str(proof_path), 'phase_proof': str(phase_path),
        'documentation': str(DOC), 'all25_controlled_native_canvases_and144_parities_pass': True,
        'parent_actual_and_release_pending': True, 'completed_entries_added': 0})
    before = read(ROOT / 'editorial_ledger_before_checkpoint.json')
    assert ledger['current_integrated_candidate'] == before['current_integrated_candidate']
    assert ledger['unresolved_graphics_work'] == before['unresolved_graphics_work']
    assert ledger['records_editorially_completed'] == 646 and not ledger['full_goal_complete']
    save(LEDGER, ledger)
    DOC.write_text('''# V836: native Deck comment layout and phase repair

The25 reviewed comments1361-1385 now have complete controlled native rendering
coverage. V834 remains unchanged. No formatting gate is promoted to release
approval while parent bounds/palette and actual-display verification are pending.

## Exact original geometry and execution

The actual retained CDeckPersonnelView object at0218DF2C is identified by its
original vtable021314E8 in the V83515200-frame RAM capture. Its bitmap at+40
uses the original4-bit header with pitch63 and height96:252x96 pixels. The
comment begins atx0/y60 with6x12 ASCII cells,allowing42 cells and3 rows.
Native header dimensions and pixel/input bounds are retained exactly.

All25 current baselines and25 proposed comments execute the original15334
actor selector path,53914 macro expansion,154CC/D5404 draw and actual bitmap
painters. COMMON text is an explicitly injected provider after the original
numeric selector;this is not a live loader claim. Room-type5 is a declared
header fixture,not a live assignment or actual actor eligibility claim.
Every full252x96 canvas matches independent ASCII/CP932 font decoding. Proposed
body pixels are also compared independently with the authored complete words
at canonicalx0 positions,not merely with the renderer's own glyph trace.
All input bytes,bitmap/header neighbors,ABI and exact full text consumption pass.

## First-letter failure caught and repaired

The first native model omitted original overlay0 at01FFA000,6208 bytes. Bitmap
clear at01FFB2DC then ran missing code and failed before text drawing. Loading
the unchanged original overlay corrects that model precondition. No ROM changes
or passing gameplay claims came from that failed probe.

Native ASCII painting can request duplicate or trailing blank cells. Those are
retained in the proof. They are not mistaken for missing text or used to waive
letter checks;the final pixels must match independent complete words exactly.

A naive bare LF after the15-character Mmm, delicious! moved the next S onto
the preceding row and left neaking on the next row with a6-pixel offset.
The native method still consumed every input byte,showing why byte counts alone
are insufficient. The generated serializer adds one invisible phase space
before LF when the visible row has odd ASCII length. Every continuation then
starts atx0 with all letters intact. No translator-authored spacing or breaks
are introduced. All25 authored wordings remain unchanged.

The original native pixel model passes144 three-row tests covering odd/even
and near-width lengths. Seven direct width/height controls consume1,41,42,43,
84 and126 bytes completely;127 is clipped to126 at the original three-row
limit.64 first/final-glyph erasure controls detect every damaged line edge.
Seven invalid inputs reject manual alignment/double spaces/LF,arguments,macros,
non-ASCII input and over-width words. All25 native ink-mask previews and the
failed/repaired contrast were opened in the complete review sheets.

## Readability and remaining gates

Word wrapping is generated from one paragraph. Fewest rows are used,with balanced
phrases,weak-end checks and punctuation boundaries. Natural source ellipses may
end a phrase;Camille and Charles now break at those complete paused phrases.
No isolated final word or dropped leading/trailing character is waived.
These previews are ink masks,not proof of parent palette,GPU composition or
native clipping. Parent source crops and absolute visible bounds still need
mapping,and normal-source Janus/Claudio plus an odd-row multiline sample must
be captured after registered integration. This scoped encoder does not certify
all other game consumers or repair all existing manual-wrap debt.

The sheet also exposes actor22's native middle name835F/ダ between Samwell and
Khan. Exact native fields are saved as a separate lead. Source/established Latin
naming and actual display review must precede a name change;no credit is added.

''' + checkpoint + '\n', encoding='utf-8')
    paragraph = '\n\n## V836: Deck native fonts and generated phase repair\n\n' + checkpoint + ' See [V836 native evidence](personal_chatter_v836_native_layout.md).\n'
    for p in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(p).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    copy2('work/analysis/personal_chatter_v835/v836_native_probe.log', ROOT / 'native_matrix_final.log')
    sources = {Path(__file__), Path('scripts/personal_chatter_layout_v836.py'), Path('scripts/probe_personal_fonts_v836.py'),
               Path('scripts/verify_personal_phase_v836.py'), MANUSCRIPT, DOC, LEDGER,
               *ROOT.glob('*.json'), *ROOT.glob('*.png'), ROOT / 'native_matrix_final.log'}
    sources.update(map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')))
    archived = []
    for source in sorted(sources):
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archived, 'all_copies_hash_verified': True,
        'previous_goal_turn_classification': 'progress:25 source/prose reviews and75 original selector cases',
        'this_goal_turn_classification': 'progress:25 native font proofs,phase failure found/repaired,144 parity cases,parent actual integration still pending',
        'whole_goal_complete': False})
    print('V836 saved:25 native font canvases,144 parity cases and64 letter controls;current V834 and646 complete remain. Parent/actual/integration gates open.',flush=True)


if __name__ == '__main__':
    main()
