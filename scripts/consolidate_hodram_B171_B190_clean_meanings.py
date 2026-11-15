"""Seal all435 source meanings; preserve the disclosed screenshot and pending context."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')


if __name__ == '__main__':
    target = ROOT / 'complete_clean_meanings_checkpoint_v1.json'
    assert not target.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    source = {r['id']: r for g in packet['groups'] for r in g['records']}
    parts = [ROOT / name for name in ['B171_B172_clean_meanings_before_English.json',
        'B173_clean_meanings_before_English.json', 'B174_B175_clean_meanings_before_English.json',
        'B176_B178_clean_meanings_before_English.json', 'B179_B183_clean_meanings_before_English.json',
        'B184_B190_clean_meanings_before_English.json']]
    rows = [r for path in parts for r in load(path)['records']]
    assert len(rows) == len({r['id'] for r in rows}) == len(source) == 433
    assert {r['id'] for r in rows} == set(source)
    for row in rows:
        old = source[row['id']]
        assert all(row[k] == old[k] for k in ['source_hex', 'source_reference', 'source_Japanese', 'source_complete_preamble_hex', 'source_selector'])
        assert row['complete_exchange_clean_context_read'] and row['source_meaning'].strip()
    choices_path = ROOT / 'clean_choice_objects.json'
    choices = load(choices_path)
    assert len(choices['records']) == 2 and choices['source_caption_meanings_saved'] == 2
    combined = ROOT / 'complete_clean_meanings_before_English.json'
    save(combined, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        records=rows + choices['records'], speech_records=433, caption_records=2, complete_blocks=20,
        no_current_ROM_English_dialogue_extraction=True, no_localized_drafts=True,
        incidental_earlier_user_screenshot_exposure=load(parts[-1])['incidental_exposure'],
        no_blanket_meaning_or_draft_before_any_English_exposure_claim=True,
        source_context_research_still_required=['Shared ruin/crown-discovery encounter preceding B178.',
            'Exact pirate identity/sword context and all native names,roles,goods,city anditem consumers.',
            'Broader established English terminology for 覇者の証 remains an editorial question; do not decide it from one isolated line.'],
        source_parts={str(p): sha(p.read_bytes()) for p in parts},
        all_localization_current_comparison_anddisplay_gates_still_pending=True, new_credit=0))
    save(target, dict(total_editorial_objects=435, ordinary_speeches=433, typed_caption_records=2,
        typed_choice_objects=1, physical_style_objects=0, source_meanings_saved=435,
        remaining_ordinary_meanings=0, remaining_caption_meanings=0, localized_drafts=0,
        current_English_comparisons=0, complete_clean_meanings=str(combined),
        complete_clean_meanings_sha256=sha(combined.read_bytes()),
        scope='All20 clean blocks read as exchanges; native identity/term bindings and linked ruin context remain before localized approval.',
        earlier_user_tea_screenshot_incidental_exposure_disclosed=True,
        no_current_ROM_English_extraction=True, no_all_prior_English_exposure_claim=True,
        new_credit=0, full_goal_complete=False, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [packet_path, choices_path, *parts, combined, Path(__file__)]}))
    print('Sealed435 clean meanings from20 blocks;no current English ordrafts;linked context/identities/terms/localization still pending.')
