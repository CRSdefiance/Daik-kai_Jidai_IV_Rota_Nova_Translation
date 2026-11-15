"""Bind ordered full-scene body calls before attributing repeated short replies."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original = Path('scripts/analyze_hodram_B171_B190_actual.py')
source = checked_text(original.read_text(encoding='utf-8'), {
    "Path('work/analysis/Hodram_B171_B190_actual_pixels_20261104')":
        "Path('work/analysis/Hodram_B171_B190_actual_pixels_v2_20261104')",
    "        if key in ['town', 'pirate']:\n            assert [r['text_hex'] for r in target_paints] == [r['expected_expanded_body_hex'] for r in fixture['selected_records']], key":
    """        ordered_ids = {}
        if key in ['town', 'pirate']:
            assert [r['text_hex'] for r in target_paints] == [r['expected_expanded_body_hex'] for r in fixture['selected_records']], key
            assert len({r['frame'] for r in target_paints}) == len(target_paints)
            ordered_ids = {paint['frame']: record['id'] for paint, record in zip(target_paints, fixture['selected_records'], strict=True)}""",
    "            candidates = allowed[active['text_hex']]":
    """            candidates = allowed[active['text_hex']]
            if ordered_ids:
                candidates = [item for item in candidates if item[0] == ordered_ids[active['frame']]]
                assert candidates
            # This attribution also uses all copied sequential commands and the
            # exact ordered native body calls; identical pixels alone do not
            # establish the source occurrence.""",
    "                live_modal_frame=active['frame'], live_modal_body_hex=active['text_hex'],":
    """                live_modal_frame=active['frame'], live_modal_body_hex=active['text_hex'],
                ordered_fixture_record_id=ordered_ids.get(active['frame']),
                occurrence_evidence='complete ordered native body sequence and byte-exact sequential copied scene commands' if ordered_ids else 'native body and pixel equivalence',""",
    "        direct_visual_review_pending=True, new_credit=0,":
    """        earlier_equivalence_only_analysis='work/analysis/Hodram_B171_B190_actual_pixels_20261104/focused_actual_pixels.json',
        earlier_town_first_last_contact_labels_superseded_by_ordered_attribution=True,
        direct_visual_review_pending=True, new_credit=0,""",
})
exec(compile(source, __file__ + '::strict-ordered-scene-attribution-same-captures', 'exec'), globals())
