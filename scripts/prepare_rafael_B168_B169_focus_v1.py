"""Select complete source commands for both page turns and the Ian scene’s display risks."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B168_B169_display_v1 as display
from scripts import write_rafael_B169_contextual_v1 as b169
from scripts.audit_story_glyph_consistency import load, save


ROOT = display.ROOT
MANUSCRIPT = ROOT / 'formatting_manuscript_v2.json'
SELECT = ROOT / 'focused_selection_v1.json'
NAME_PROOF = ROOT / 'offline_display_v2/native_name_planes.json'
DECISIONS = ROOT / 'focused_name_decisions_v1.json'
NAMES = ROOT / 'focused_name_planes_v1.json'
PRIOR_LABELS = Path('translations/rafael_B166_B167_scoped_names_review_v1.json')
BLOCKS = {
    168: (5, 14, 26, 30, 45, 50, 55, 85, 93, 110, 114, 130, 134, 154, 171, 174, 182, 186, 190, 193, 211, 214, 220),
    169: (7, 11, 16, 20, 24, 28, 39, 52, 55, 66, 70, 74, 90, 110, 114, 118, 154, 158, 161, 169, 181, 184, 198,
          202, 207, 212, 227, 241, 254, 266, 274, 279, 283, 286, 291),
}


def main():
    assert not any(p.exists() for p in (SELECT, DECISIONS, NAMES))
    doc, current_names, earlier_names, name_planes = map(load, (MANUSCRIPT, b169.LABELS, PRIOR_LABELS, NAME_PROOF))
    ids = {f'DK4_MES_B{block}_R{record:04d}' for block, entries in BLOCKS.items() for record in entries}
    selected = [r for r in doc['records'] if r['id'] in ids]
    assert {r['id'] for r in selected} == ids and len(ids) == 58
    actors = {r['source_selector'] for r in selected}
    angelo = next(r for r in earlier_names['records'] if r['actor_ID'] == 15)
    all_names = sorted([*current_names['records'], angelo], key=lambda r: r['actor_ID'])
    assert actors == {r['actor_ID'] for r in all_names} == {r['actor_ID'] for r in name_planes['actors']}
    save(DECISIONS, dict(records=all_names, existing_native_names_preserved=True, actual_observation_pending=True, new_credit=0))
    save(NAMES, {**name_planes, 'evidence': {**name_planes['evidence'], str(DECISIONS): sha(DECISIONS.read_bytes())}})
    save(SELECT, dict(fixtures=[dict(name='angelo_trade_and_ian_recruitment', speech_ids=[r['id'] for r in selected],
        purpose='Check both trade page turns, Rafael’s name substitution, complete portraits and nameplates, source punctuation, Ian’s intervention and recruitment with ordinary A inputs.')],
        only_selected_speech_commands_after_source_initializers=True, original_conditions_location_and_hardware_unvisited=True,
        no_state_or_condition_overrides=True, new_credit=0))


if __name__ == '__main__':
    main()
