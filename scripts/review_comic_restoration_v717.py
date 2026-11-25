"""Current raw-comic source/material decisions; no new renderer or art edits."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_art_contract import region
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/comic_restoration_v717')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
BATCH = Path('translations/gallery_chase_fringe_raw_art_v8.json')
OLD = Path('work/analysis/comic_current_v506')
FILE = '/GRP/SLACKIMG.DK4'
REVIEWS = {
    'neutral-ink-erasure-protect-connected-art-v1':
        'Original portraits,bubble outlines and corner framing remain distinct from the replacement letters; no obvious glyph residue or rectangular fill seam in the opened full-frame comparison.',
    'background-aware-connected-art-v2':
        'Vertical title and bottom thanks use their original backing context; nearby artist byline is retained as attribution rather than treated as dialogue.',
    'source-white-caption-mask-local-scenery-v3':
        'Recruitment caption,credits and ending caption preserve the photograph and its border; reconstructed gray backing reads coherently around the new caption.',
    'source-chase-bubble-interior-v4':
        'Complete English stays within the original chase bubbles; bubble outlines and the underlying photo remain visually intact.',
    'source-chase-call-mask-background-v8':
        'Red refusal and call area have no visible Japanese fringe in the opened comparison; the source photo border is retained.',
    'source-chase-call-mask-background-v4':
        'The compact pursuit call retains its complete words and the source photo boundary; the surrounding sea/sky remains coherent at storage scale.',
    'source-maria-decorative-title-v6':
        'The split Ma-ri-a lettering follows the original syllable/color panels. Mode preserves the vertical/decorative treatment without replacing the surrounding character art.',
    'source-maria-chinese-bubble-v6':
        'The original bubble contour and red lettering treatment remain; the four source sentences are retained in natural English.',
    'source-reveal-comic-v7':
        'Reaction/reveal preserve the visible creature silhouette and the approved brown marks. Smaller decorated TA-DA lettering is confined above the horns; masked paper/sea remains inferred.',
}


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    current, historical, source, clean = map(NdsImage.open, (ROM,
        'out/all_routes_combined_v502_candidate.nds', 'out/raphael_natural_v2_accepted_base.nds', 'work/clean.nds'))
    block, old_block, original, clean_block = [IlnkContainer.parse(r.read_file(FILE)).blocks[19]
        for r in (current, historical, source, clean)]
    assert block == old_block and original == clean_block
    assert len(block) == len(original) == 21 * 153600
    old = read(OLD / 'proof.json')
    batch, manifest = read(BATCH), read(OLD / 'all_frames_manifest.json')
    assert sha(BATCH.read_bytes()) == old['batch_sha256']
    assert sha(original) == manifest['source_block_sha256']
    assert sha(Path(batch['font_file_path']).read_bytes()) == batch['font_sha256']
    assert len(old['cases']) == len(batch['records']) == 18
    cases = {c['id']: c for c in old['cases']}
    decisions = []
    for row in batch['records']:
        prior = cases[row['id']]
        assert row['source_text'] == prior['source_text'] and row['english'] == prior['english']
        assert sha(region(block, row['image_index'], row['box'])) == prior['word_payload_sha256']
        note = 'English preserves the original meaning and register in this illustrated context.'
        if row['id'] == 'DK4_GALLERY_CREATURE_REPLY_V1':
            note = ('Contextual inference: retain Sea cow for the illustrated marine cow joke. '
                'The Japanese umiushi normally names a sea slug; the deliberately cow-like creature motivates the visual wordplay. No new creature identity is invented.')
        elif row['id'] == 'DK4_GALLERY_CREATURE_REVEAL_V1':
            note = 'TA-DA conveys the extended reveal effect; its placement protects visible horns. It does not invent an explosion or dialogue speaker.'
        elif row['id'] == 'DK4_GALLERY_RECRUITMENT_CREDITS_V1':
            note = 'Retain the author/artist names as names and the parenthetical pen name as a romanization; no translated identity is invented.'
        elif row['id'] == 'DK4_GALLERY_MARIA_VISIT_BUBBLE_V1':
            note = 'The source here is Chinese,not Japanese. Greeting,visit request,time question and invitation upstairs are all retained.'
        decisions.append({'id': row['id'], 'frame': row['image_index'], 'box': row['box'],
            'source_text': row['source_text'], 'English': row['english'],
            'translation_review': note, 'restoration_rule': row['background_rule'],
            'visual_restoration_review': REVIEWS[row['background_rule']],
            'exact_current_region_sha256': prior['word_payload_sha256'],
            'existing_backing_proof_sha256': prior['reconstructed_backing_sha256'],
            'existing_quantized_first_final_letter_proof_carried_forward': True,
            'art_revision_required_by_this_review': False,
            'hidden_source_pixels_not_exactly_recoverable_from_lettered_art': True,
            'normal_runtime_readability_still_open': True})
    frames = []
    for row in manifest['frames']:
        n = row['frame']
        assert sha(block[n * 153600:(n + 1) * 153600]) == row['current_sha256']
        frames.append({'frame': n, 'current_sha256': row['current_sha256'],
            'unowned_source_words_and_high_bits_proof_carried_forward': True,
            'unchanged_from_source': row['untouched_frame_byte_exact']})
    marks = region(block, 6, (175, 96, 229, 136))
    assert marks == region(original, 6, (175, 96, 229, 136)) and len(marks) == 4320
    sheets = []
    for p in sorted(OLD.glob('source_current_frames_*.png')):
        sheets.append({'path': str(p), 'sha256': sha(p.read_bytes()),
            'historical_label_V502_current_art_byte_exact_V712': True, 'opened_for_full_frame_review': True})
    assert len(sheets) == 6
    release_paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'review_scope': 'Stored source/current art,translation/context and visible restoration; no normal comic viewer proof.',
        'complete_current_raw_block_sha256': sha(block), 'source_block_sha256': sha(original),
        'current_block_byte_exact_to_previously_font_verified_V502': True,
        'all21_frames': frames, 'all18_caption_translation_and_restoration_decisions': decisions,
        'six_opened_source_current_review_sheets': sheets,
        'all11_untouched_frames_and_all_unowned_source_words_carried_forward': True,
        'approved_brown_mark_bytes': len(marks), 'approved_brown_mark_sha256': sha(marks),
        'artist_signatures_existing_Latin_attribution_and_fan_art_words_retained_as_contextual_art': True,
        'source_restoration_visual_review_complete_with_documented_inference_not_hidden_pixel_recovery': True,
        'user_approval_not_claimed_for_comic_art': True,
        'ordinary_comic_consumer_geometry_alpha_loading_and_readability_still_open': True,
        'known_kind3_index19_alias_and_portrait_loop_are_completed_negative_leads_not_new_tests': [
            'docs/generic_image_dispatch_v538_checkpoint.md', 'docs/slack_caller_loop_v588_checkpoint.md'],
        'release_hashes_unchanged': {str(p): sha(p.read_bytes()) for p in release_paths},
        'previous_goal_turn_classification': 'progress: user material acceptance and completed-task queue recorded; source review now advances the remaining comic task',
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V717 current21 raw frames/18 source-context/restoration decisions bound; stored-art review closed,ordinary playback still open.', flush=True)


if __name__ == '__main__':
    main()
