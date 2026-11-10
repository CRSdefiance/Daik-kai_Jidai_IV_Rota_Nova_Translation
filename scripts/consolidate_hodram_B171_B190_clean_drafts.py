"""Seal435 logical drafts and a small source-fidelity refinement before current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_hodram_B171_B190_drafts import ROOT

PARTS = ['B171_B173_131', 'B174_B175_74', 'B176_B179_98', 'B180_B190_130']
REFINEMENTS = {
    'DK4_MES_B172_R0026': (
        "Oh, that's not why you're here? He's famous around here for how much he knows.",
        'Express the source reputation for knowledge without understating it as a little of everything.'),
    'DK4_MES_B172_R0070': (
        "Ah, that's a peppercorn. It grows on a tropical tree. Grind it up, and you have a spice.",
        'Preserve Mikhail\'s actual claim about a tropical tree rather than silently broadening it to plant.'),
    'DK4_MES_B172_R0122': (
        "You know a great deal, Mikhail. I am {MACRO:FI} {MACRO:FA}. I command a fleet.",
        'Use a natural formal introduction. Preserve both name substitutions and fleet command without introducing the distinct rank Fleet Admiral.'),
    'DK4_MES_B174_R0039': (
        "I slipped away from my master. If I'm found, I'll be taken straight back!",
        'The source does not gender the master or specify who will catch her; preserve the passive consequence naturally.'),
    'DK4_MES_B174_R0054': (
        "My master caught me skipping practice and gave me an earful. Such a stick-in-the-mud!",
        'Preserve the scolding and complaint about rigidity without inventing the master\'s gender.'),
    'DK4_MES_B174_R0057': (
        "So I've made up my mind! I'll travel the world, keep training, and show my master what I can do! Pretty admirable, huh?",
        'Keep her defiance and continued training; replace the unsupported gendered pronoun with the actual relationship.'),
    'DK4_MES_B174_R0123': (
        "...My own master once told me to go to sea. That advice made me who I am today...",
        'Preserve Hodram\'s former mentor and life-changing advice without assigning an unstated gender.'),
}


if __name__ == '__main__':
    final_path = ROOT / 'all435_clean_English_drafts_v2.json'
    assert not final_path.exists()
    meanings_path = ROOT / 'complete_clean_meanings_before_English.json'
    meanings = load(meanings_path)
    source_rows = {r['id']: r for r in meanings['records']}
    files = [ROOT / (p + '_clean_English_drafts_v1.json') for p in PARTS]
    rows = [r for p in files for r in load(p)['records']]
    assert len(rows) == len({r['id'] for r in rows}) == 433
    choice_source_path = ROOT / 'clean_choice_objects.json'
    choice_source = load(choice_source_path)
    captions = []
    for row, english, note in zip(choice_source['records'], ['Listen.', 'No, thanks.'], [
        'Choose to hear the offered lesson; no invented future promise or reward.',
        'Decline naturally and politely; this is not a promise to listen later.'], strict=True):
        captions.append(dict(**row, english=english, logical_English=english, speaker='Player choice',
            context=row['exchange_context'], localization_note=note,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            current_ROM_English_conversation_comparison_pending=True, current_reference_pending=True,
            native_provider_caption_visual_stored_andgameplay_checks_pending=True, new_credit=0))
    captions_path = ROOT / 'two_clean_caption_English_drafts_v1.json'
    assert not captions_path.exists()
    save(captions_path, dict(records=captions, choices=2, objects=1, no_current_English_exposure=True,
        source=str(choice_source_path), source_sha256=sha(choice_source_path.read_bytes()), new_credit=0))
    initial = dict(format='dk4-complete-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        file_path='/data/SC1.DK4', blocks=list(range(171, 191)), records=rows + captions,
        ordinary_speeches=433, typed_captions=2, total_editorial_objects=435,
        all_current_ROM_English_conversation_comparisons_pending=True, all_fifth_formatting_gates_false=True,
        no_authored_ordinary_breaks_alignment_orpadding=True,
        earlier_user_tea_screenshot_incidental_exposure_disclosed=True,
        no_blanket_meaning_or_draft_before_any_prior_English_claim=True,
        no_current_ROM_English_extraction=True, new_credit=0, new_ROMs=0,
        evidence={str(p): sha(p.read_bytes()) for p in [meanings_path, choice_source_path, *files, captions_path, Path(__file__)]})
    initial_path = ROOT / 'all435_clean_English_drafts_v1.json'
    assert not initial_path.exists()
    save(initial_path, initial)
    refined = deepcopy(initial)
    refinements = []
    by_id = {r['id']: r for r in refined['records']}
    for ident, (english, reason) in REFINEMENTS.items():
        row = by_id[ident]
        assert row['source_hex'] == source_rows[ident]['source_hex']
        old = row['english']
        assert old != english
        assert all(old.count('{MACRO:' + m + '}') == english.count('{MACRO:' + m + '}') for m in ['FI', 'FA', 'FO'])
        refinements.append(dict(id=ident, old_English=old, English=english, reason=reason,
            source_reference=row['source_reference'], source_Japanese=row['source_Japanese']))
        row.update(english=english, logical_English=english, localization_note=reason,
            source_first_refinement=dict(previous=old, reason=reason))
    assert len(refined['records']) == len(by_id) == len(source_rows) == 435 and set(by_id) == set(source_rows)
    for row in refined['records']:
        assert row['source_hex'] == source_rows[row['id']]['source_hex']
        assert not any(t in row['english'] for t in ['\n', '{LB', '{ALIGN', '{PAD}', '  '])
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        row['english'].encode('cp932')
    refined.update(source_first_refinements=refinements, previous_drafts=str(initial_path),
        previous_drafts_sha256=sha(initial_path.read_bytes()), all435_drafts_saved_before_current_ROM_dialogue_extraction=True,
        scoped_Proofs_consistency_does_not_close_wider_terminology_question=True)
    save(final_path, refined)
    # Reusable current-binding input contains only clean meanings, not prior English.
    compatibility = ROOT / 'ordinary_meanings_for_current_binding.json'
    save(compatibility, dict(records=[r for r in meanings['records'] if 'source_selector' in r], meanings=433,
        all435_drafts_sealed=str(final_path), all435_drafts_sha256=sha(final_path.read_bytes()),
        current_ROM_English_unconsulted=True, incidental_user_screenshot_exposure_disclosed=True))
    save(ROOT / 'source_draft_checkpoint_v1.json', dict(total_objects=435, speech_drafts=433, caption_drafts=2,
        complete_blocks=20, current_English_comparisons=0, draft_source_fidelity_refinements=7,
        all435_drafts_saved_before_current_ROM_dialogue_extraction=True, all_fifth_gates_still_pending=True,
        final_drafts=str(final_path), final_drafts_sha256=sha(final_path.read_bytes()),
        initial_drafts=str(initial_path), initial_drafts_sha256=sha(initial_path.read_bytes()),
        native_identities='native_identity_and_term_checkpoint_v1.json',
        no_new_editorial_credit=True, new_credit=0, full_goal_complete=False, guide_photos=False))
    print('Sealed435 source-first logical drafts;seven fidelity refinements preserve all originals. Current comparison/display remain.')
