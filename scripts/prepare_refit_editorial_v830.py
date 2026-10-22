"""Fresh source/current editorial packet for the complete Refit help family."""

from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_editorial_v830')
MANUSCRIPT = Path('translations/refit_help_editorial_manuscript_v3.json')
ROM = Path('out/all_routes_combined_v829_candidate.nds')

# Unpositioned prose. The captured Refit consumer owns every line break.
REVISIONS = {
    1247: 'Officers here recover their health and morale.',
    1249: "A ship's doctor can cure ailments affecting officers and sailors.",
    1250: 'A chief cook conserves food and water and makes sailors tire more slowly.',
    1251: 'Officers here recover their morale and make sailors tire more slowly.',
    1253: "A missionary relieves sailors' discontent and lets you distribute trade goods in the square.",
    1268: 'A split sail improves square sail performance, increasing speed with a following wind.',
    1272: 'A bow gun lets you fire ahead of the ship, but its shots are weak.',
    1273: 'A stern gun lets you fire behind the ship, but its shots are inaccurate.',
    1275: 'A marine captain boosts boarding attack power. You can add up to four rooms of this type.',
    1276: 'A gunner speeds up cannon fire. You can add up to four of these rooms.',
    1277: "This room holds the ship's food and water.",
    1278: 'Cargo holds carry trade goods. You can add up to five holds.',
    1280: 'Fit a ram or bow gun here. Medium and larger ships can also carry a split sail.',
    1281: 'Fit extra armor here.',
    1282: 'You can fit a stern gun here, or a jigger spanker on large ships.',
    1286: 'A topsail improves square sail performance, increasing speed with a following wind.',
    1287: 'Square sails work well with a following wind. You cannot put a lateen sail ahead of one.',
    1289: 'This is a square sail with improved fore-and-aft and square sail performance.',
}

NOTES = {
    1247: 'Here refers to the selected room. Retain both physical recovery and mood recovery; morale is the existing help-family rendering of mood. Remove redundant location phrasing, not either effect.',
    1248: 'Retain: a carpenter enables repair of damaged ships. No repair rate, free repair or prevention of damage is promised.',
    1249: 'The source says can cure, not merely treat. Ailments covers abnormal health conditions without restricting the explanation to disease or inventing named conditions.',
    1250: 'Preserve two separate benefits: conserving both resources and slowing sailor fatigue. More slowly is clearer than less quickly; no immediate fatigue recovery or causal connection between the two benefits is asserted.',
    1251: 'Preserve the officers versus sailors distinction and the separate mood and fatigue effects. Slower fatigue does not mean restored fatigue or complete prevention.',
    1252: 'Retain the established animal keeper term and the natural explanation of slower food depletion. Do not extend the benefit to water.',
    1253: 'Relieves preserves the source resolution of discontent more closely than eases. Retain trade goods, the square and the additional distribution ability.',
    1254: 'Retain the strategist requirement, planning action and tavern location. No particular scheme is introduced.',
    1255: 'Retain the established bargain/corner-markets terminology for the two purser-enabled actions. The clean source uses buying up stock, also seen in COMMON1184; no guaranteed profit or new stock quantity is added.',
    1268: 'Following wind explicitly preserves the favorable-wind condition. Keep the split sail, square-sail performance and speed benefit separate from the adverse-wind sail descriptions.',
    1269: 'Retain both fore-and-aft performance and speed against the wind, with the established jigger spanker name.',
    1270: 'Retain increased durability and the explicitly slight speed penalty. Do not turn the tradeoff into a free upgrade.',
    1271: 'Retain the named second armor upgrade and further durability gain, plus the slight speed penalty.',
    1272: 'Weak shots is natural help prose for low attack power. Keep forward fire distinct from rearward accuracy in1273.',
    1273: 'Inaccurate shots preserves the source low hit rate. Do not replace this limitation with low power from1272.',
    1274: 'Retain the ram requirement and side-of-enemy-ship collision target. Do not imply that a normal collision without the fitting has this ability.',
    1275: 'The four-room limit belongs to this selected room type, not four officers or four rooms of every type combined. Add these rooms reads naturally in a refit interface.',
    1276: 'Preserve faster cannon fire and this room type limit of four. Avoid implying higher damage or accuracy.',
    1277: 'Retain storage of both food and water. The ship reference is the established Refit context, not a new effect.',
    1278: 'Retain trade goods and the five-hold maximum. Add is natural for creating a room in the refit interface.',
    1279: 'Retain the positional cargo-hold option and its slight speed penalty. Do not confuse the added-room penalty with the separate trade-goods description.',
    1280: 'A natural location instruction preserves the ram/bow-gun options and the medium-or-larger restriction on the split sail. This is a location tooltip, not a general sail effect. No stacking of alternative fittings is promised.',
    1281: 'Use a natural instruction for this location-specific armor option. No quantity or benefit beyond fitting extra armor is invented.',
    1282: 'Japanese matawa marks alternatives. Use or to distinguish the stern gun from the large-ship jigger spanker option; do not imply that both can occupy the selected position simultaneously.',
    1283: 'Retain the ownership requirement and selected mounting location. Do not imply a figurehead is supplied for free.',
    1284: 'Retain changing the installed cannon type, not a promise to add another gun or improve its performance.',
    1285: 'Retain the lateen sail adverse-wind advantage and the prohibition on a square sail behind it. Do not reverse bow/stern ordering.',
    1286: 'Following wind preserves the favorable-wind condition. Retain the topsail square-sail performance and speed benefit.',
    1287: 'Following wind makes the wind direction explicit. Keep the prohibition on a lateen sail ahead of this square sail, consistent with1285.',
    1288: 'Retain the staysail name, fore-and-aft improvement and adverse-wind speed benefit. Do not substitute the favorable-wind effect.',
    1289: 'The source describes a square sail with both kinds of performance improved. Restore that square-sail connection omitted by this sail improves both; do not invent a numerical bonus.',
}


def reference(entry):
    return {key: getattr(entry, key) for key in (
        'message_id', 'block', 'table_offset', 'block_offset', 'copy_end',
        'record_index', 'start', 'end')}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not MANUSCRIPT.exists(), 'Do not overwrite a reviewed manuscript'
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '641d4a9dfd4dee5ca66fc89fe242cc36f9f3373d773510011b6f5898af45e66d'
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    entries = current_entries(common, arm)
    original = read('translations/refit_help_manuscript_v2.json')
    manuscript = deepcopy(original)
    manuscript.update(status='source-prose-reviewed-current-native-and-release-pending',
                      current_candidate=str(ROM), current_candidate_sha256=sha(ROM.read_bytes()),
                      current_common_sha256=sha(common), current_arm9_sha256=sha(arm),
                      editorial_goal_family='COMMON-Refit-help-31',
                      scope_note='Fresh editorial review of all31 selected Refit help messages. Spoken1256-1267 and HELP articles are separate consumers. No completion or integration credit yet.')
    assert {r['message_id'] for r in manuscript['records']} == set(NOTES)
    layouts = []
    for row in manuscript['records']:
        i = row['message_id']
        assert row['clean_source_hex'] == source[i].text.hex()
        before = entries[i].text.decode('ascii')
        assert ' '.join(before.split()) == row['english']
        row.update(current_text_hex=entries[i].text.hex(), current_English=before,
                   clean_reference=reference(source[i]), current_reference=reference(entries[i]),
                   english=REVISIONS.get(i, row['english']),
                   editorial_decision='revise' if i in REVISIONS else 'retain',
                   localization_note=NOTES[i],
                   context='Original Refit room/equipment explanation selected by stable COMMON ID. The original168x108 surface provides five body rows; heading and three detail rows occupy separate later rows. Spoken1256-1267 are excluded.',
                   review={'source': True, 'context': True, 'localization': True,
                           'naturalness': True, 'formatting': False})
        compiled, lines = compile_paragraph(row['english'])
        layouts.append({'message_id': i, 'English': row['english'], 'lines': lines,
                        'compiled_hex': compiled.hex(), 'single_word_last_row': len(lines[-1].split()) == 1})
    save(MANUSCRIPT, manuscript)
    save(ROOT / 'source_context_packet.json', {
        'clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()),
        'current_ROM_sha256': sha(ROM.read_bytes()),
        'source_and_current_neighbors': [
            {'message_id': i, 'Japanese': source[i].text.decode('cp932'),
             'clean_hex': source[i].text.hex(), 'clean_reference': reference(source[i]),
             'current_hex': entries[i].text.hex(), 'current_reference': reference(entries[i])}
            for i in range(1245, 1291)],
        'source_reviewed_entries': len(NOTES), 'proposed_revisions': len(REVISIONS),
        'justified_retained_wordings': len(NOTES) - len(REVISIONS),
        'earlier_actual_context_evidence': 'work/analysis/refit_help_v712/display_proof.json',
        'earlier_actual_scope': '23 help compositions cover13 distinct messages; not31 ordinary visits.',
        'new_actual_scene_sample_pending': True, 'full_goal_complete': False})
    save(ROOT / 'generated_layouts.json', layouts)
    print(f'Fresh31-entry Refit source/prose packet:{len(REVISIONS)} revisions,{len(NOTES)-len(REVISIONS)} retentions;native/release gates pending.', flush=True)


if __name__ == '__main__':
    main()
