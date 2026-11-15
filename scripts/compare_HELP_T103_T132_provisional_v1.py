"""Record individual contextual decisions; native term/control binding and all display gates remain open."""
import re
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')
REVISE = {
    103: ('These commands are available both in town and at sea. Press X on either screen to open the menu. See [[104|Route Map]], [[105|Deck]], [[134|Info]], [[138|Items]], [[139|Assign Sailors]] and [[140|Functions]].',
          'Use town for the full source scope rather than suggesting only City-level settlements. Keep the existing recognizable destinations; X still requires native binding for this consumer.'),
    104: ('The Route Map shows the current sea region and faction names. In a region containing cities you have not visited, only [[145|City-level settlements]] are shown. Select a city or fleet to view its data. Lines between cities are routes; you can use Auto Move along red routes. To view another sea region, press Y to zoom out to the world map, then select the region.',
          'Retain the accurate explanation and restore the omitted source zoom-out button, provisionally Y. Verify the current native map consumer before approval.'),
    106: ('You can assign officers to jobs automatically. Press X on the Deck screen, then select [[107|Exploration]], [[108|Trade]] or [[109|Naval Battle]].',
          'Restore the source instruction for opening automatic assignments, provisionally X; current Choose Auto may describe an equivalent native menu action, so resolve that consumer before final approval.'),
    119: ("The fleet's accounts are managed here. Officers assigned here become Pursers and need Finance 100 or higher. A Purser may get you lower prices at the Trade House. You may also be able to buy up all available stock by paying twice the price, but you cannot sell at twice the price.",
          'The source benefit applies at the Trade House, not the separate Market Info service. Retain the conditional discount/buyout wording and explicit inability to sell for twice the price.'),
    121: ("This office is for the Captain's assistant. Officers assigned here become First Mates and need Speech 100 or higher. A First Mate lets you [[27|Send Letter]] from the Guild and slows the increase in crew fatigue. In battles against cities, they demand the city's surrender.",
          'Keep the accurate role and effects; use the already reviewed Send Letter command caption so players can find it. Bind the remaining room/skill/role names before final approval.'),
    127: ("The ship's holds are divided into five types according to their purpose. You can assign officers to the Quarters and Gun Batteries. See [[128|Quarters]], [[129|Gun Batteries]], [[130|Rowers' Quarters]], [[131|Supply Hold]] and [[132|Cargo Hold]].",
          'Use source-bound native Quarters for the same room already bound in the boarding tutorial, replacing Marine Barracks. Preserve the five types, two assignable types and link order; other hold labels remain to be bound.'),
    128: ('The boarding crew waits here. A ship can have up to four Quarters. Officers assigned here become Boarding Leaders and need Swords 90 or higher. A Boarding Leader improves your strength in [[98|boarding battles]] and takes part in [[99|duels]].',
          'Use native Quarters and avoid implying a new formal Marine rank. Boarding Leader and Swords are already source-bound; preserve four rooms, the 90 threshold and both combat effects.'),
}
REASONS = {
    105: 'Clear assignment sequence, room-to-job relationship, prerequisite exclusion and stronger-skill effect; all three related destinations are intact.',
    107: 'Naturally explains exploration priorities without claiming every officer receives a job or inventing a numeric skill threshold.',
    108: 'Concise trade-assignment explanation preserves priority for skilled officers and the source focus on trade-related jobs.',
    109: 'Readable battle-assignment policy preserves the priority rule without inventing a formation or battle bonus.',
    110: 'All sixteen original workroom/position destinations are present in order; the short introduction serves the navigation hub clearly.',
    111: 'Physical condition and mood convey both source recovery categories without inventing a specific HP or fatigue effect.',
    112: 'Correctly separates reduced crew-fatigue buildup from recovery of the assigned officer\'s fatigue and mood.',
    113: 'Preserves Survey130, sailing repairs and lower shipyard costs; does not promise instant or free repair.',
    114: 'Preserves Observe150 and all three medical benefits, including enabling curative items; disease prevention stays probabilistic.',
    115: 'Preserves Aim70 and slower consumption of both food and water, plus slower fatigue buildup.',
    116: 'Preserves Vigor130 and production of food during voyages without inventing water production.',
    117: 'Preserves Speech160, fatigue benefit, the goods-to-trend link and belief-based refusal without assigning an invented religion.',
    118: 'Clear conditional inspiration, possible prevention of enemy schemes and inn-triggered intelligence gathering; no guaranteed scheme or invented report.',
    120: 'Preserves the clean source\'s protagonist-only assignment, Captain role, fatigue benefit and Auto Move prerequisite.',
    122: 'Preserves Sailing60, easier turning and faster automatic travel without claiming a manual top-speed bonus.',
    123: 'Preserves Survey120, skilled position reporting, mandatory Auto Move role and skill-dependent automatic speed.',
    124: 'Preserves Observe70 and discoveries/nearby information; high Aim only may snipe an admiral, and success captures that ship.',
    125: 'Preserves Sailing80, sail handling and automatic speed; automatic adjustment explicitly requires every mast staffed and Half Open sails.',
    126: 'Preserves Vigor30, boarding strength and easier leveling together with severe fatigue; natural practical advice.',
    129: 'Preserves Aim90 and more cannon shots without inventing range, damage or reload values.',
    130: 'Clearly distinguishes sailors rowing from officer assignments and restricts the room to row-powered ships.',
    131: 'Preserves both food and water capacity, increased capacity with more holds and the prohibition on assigning officers.',
    132: 'Preserves trade cargo, the five-hold maximum and the prohibition on assigning officers.',
}

def plain(text):
    return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]', r'\1', text).split())

def logical_body(text):
    # Remove legacy physical wrapping; preserve original logical link objects.
    return ' '.join(text.split('\n',1)[1].split())

if __name__ == '__main__':
    out = ROOT/'whole_article_comparisons_provisional_v1.json'
    assert not out.exists() and set(REVISE) | set(REASONS) == set(range(103,133))
    draft_path, current_path = ROOT/'clean_meanings_andfull_drafts_v1.json', ROOT/'current_full_articles_verified_parent_v1.json'
    draft, current = map(load, [draft_path,current_path])
    old_by_id = {r['topic_id']:r for r in current['records']}
    rows = []
    for source in draft['records']:
        n = source['topic_id']
        old = old_by_id[n]
        assert source['source_hex'] == old['source_hex'] and not old['complete_current_continuations']
        row = deepcopy(source)
        retained = n in REASONS
        english = logical_body(old['current_English_with_link_IDs']) if retained else REVISE[n][0]
        ids = [int(t) for t in re.findall(r'\[\[(\d+)\|',english)]
        assert ids == old['current_link_IDs']
        if retained:
            assert plain(english) == plain(old['current_English_with_link_IDs'].split('\n',1)[1])
        finding = REASONS[n] if retained else REVISE[n][1]
        row.update(heading=old['current_English_with_link_IDs'].split('\n',1)[0].strip(), english=english,
            current_reference=old['current_reference'], current_hex=old['current_hex'], current_English=old['current_English_with_link_IDs'],
            original_link_IDs=old['current_link_IDs'], complete_current_continuations=[], decision='retention' if retained else 'revision',
            finding=finding, retention_reason=finding if retained else None, localization_note=finding,
            review=dict(source=True,context=True,localization=False,naturalness=True,formatting=False),
            native_term_orcontrol_binding_pending=True, provisional_decision_may_change_after_binding=True, new_credit=0)
        rows.append(row)
    assert sum(r['decision']=='revision' for r in rows) == 7
    save(out,dict(format='dk4-help103-132-provisional-contextual-comparisons-v1', records=rows, records_count=30,
        proposed_revisions=7, justified_wording_retention_candidates=23, all_source_context_andnaturalness_reviews_recorded=True,
        first_four_gates_passed=0, all_localization_gates_pending_native_binding=True, all_fifth_gates_pending=True,
        source_draft=str(draft_path), source_draft_sha256=sha(draft_path.read_bytes()), current_packet=str(current_path), current_packet_sha256=sha(current_path.read_bytes()),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        retain_candidates_word_exact_after_removing_legacy_wraps=True, all_binding_formatting_gameplay_andregistered_integration_pending=True,
        new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('30 contextual comparisons: seven proposed revisions, 23 exact-wording retention candidates; localization binding and display gates remain open.')
