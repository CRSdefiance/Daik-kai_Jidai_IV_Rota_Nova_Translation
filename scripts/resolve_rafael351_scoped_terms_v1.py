"""Finish scoped prose localization using saved identity/term bindings; leave display gates open."""
from copy import deepcopy
from pathlib import Path
from collections import Counter

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

PARENT = Path('translations/rafael_B121_B140_contextual_comparison_v1.json')
IDENTITY = Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
TERMS = Path('work/analysis/Rafael351_item_UI_terms_v1_20261105/term_bindings.json')
OUT = Path('translations/rafael_B121_B140_contextual_prose_review_v2.json')
ROOT = Path('work/analysis/Rafael351_scoped_terms_resolved_v1_20261105')

# Complete-exchange decisions retain all earlier source glosses and findings.
# These successors correct only terms resolved by the exact clean/current bindings.
UPDATES = {
(128,23): ("Full sail lets the ship move at top speed. But as captain, you must direct the sail handlers yourself.", 'Describe the source sailing state naturally; do not claim an unverified literal Full Sail menu caption.'),
(128,26): ("You can stay at half sail while you're learning. Assign a sail handler to each mast, and they'll trim the sails for you.", 'Preserve the one-handler-per-mast condition and automatic trimming; half sail describes the source state.'),
(128,29): ("At full sail, the ship may be too fast to handle easily. Half sail can be more useful in battle, too.", 'Keep both qualified recommendations and describe sailing states, without inventing visible mode captions.'),
(128,32): ("Anchoring can help regroup your fleet when the ships have spread out, or let you lie in wait for an enemy.", 'Describe anchoring and both source uses as ordinary spoken English, without inventing an Anchor UI caption.'),
(128,50): ("At full sail, press B to switch to half sail and slow down.", 'Keep the exact B-driven full-to-half transition and its speed effect; sailing states are descriptive.'),
(128,53): ("At half sail, press B to anchor and stop in place.", 'Keep the exact B-driven half-to-anchored transition and stationary result.'),
(128,56): ("While anchored, press A to set half sail. At half sail, press A to set full sail.", 'Keep both exact A-driven transitions, without treating descriptive sailing terms as verified literal captions.'),
(128,60): ("Remember, even at half sail, you'll have to direct the sails yourself if you don't have enough sail handlers.", 'Retain the insufficient-handler exception; use the same descriptive half-sail terminology as the surrounding exchange.'),
(129,30): ("Build funds through trade among Lisbon, Ceuta, and Madeira. Then secure Las Palmas and Verde.", 'Use Verde, the exact current city-table name corresponding to source ヴェルデ, rather than expanding it to Cape Verde.'),
(129,33): ("They connect Africa with the Mediterranean. Verde yields many goods for little investment.", 'Keep the gateway and investment advantages; match the exact existing city name Verde.'),
(135,43): ("Take Sakura in Osaka. They say you can buy the Snow-Silk Robe she wants in a town somewhere on the North Sea.", 'Match 細雪のローブ to the registered Snow-Silk Robe item name, replacing the inconsistent Snowfall Robe. Preserve the reported availability and unspecific North Sea town.'),
(137,60): ("When everything looks right, choose Finish to complete the deal. Now, give it a try.", 'The existing X-button transaction-completion caption is Finish; Select is a different A-button action. Replace the unsupported Confirm instruction.'),
(138,18): ("Now, let's see how many turn up when you choose Recruit Crew.", 'Match source 水夫を集める to its actual current Recruit Crew pointer; a village Recruit Sailors caption is a different consumer.'),
(138,21): ("Next, assign your sailors. If you have only one ship, the Flagship option will do.", 'Match source 旗艦重視 to its actual current Flagship caption, preserving the one-ship qualification without inventing Flagship Priority as a visible label.'),
(139,30): ("With a Captain and Surveyor assigned on the Deck screen, you can use Auto Move along an established route.", 'Use the exact existing Auto Move command, distinct from the Auto Sail sailing-status caption. Preserve both assigned roles and the established-route condition.'),
(139,34): ("Auto Move?", 'Keep Rafael\'s brief echo question while matching the actual Auto Move command rather than the earlier Auto Travel wording.'),
(139,42): ("At the port, choose Auto Move, then select your destination on the Route Map.", 'Use Auto Move for the departure command and Route Map for the accepted common-menu caption; the shorter internal Map heading is a different consumer.'),
(140,5): ("If you want to raise a town's Arms rating against enemy attacks, invest at the palace or governor's residence.", 'Arms rating matches the existing town-defense terminology. Preserve both investment locations and the defensive purpose.'),
(140,12): ("Thanks to the building techniques developed there, we should be able to raise a town's Arms rating with less military investment than other nations need.", 'Keep the source building-technique cause, qualified expected advantage and military-investment comparison; Arms rating makes the existing label natural in speech.'),
}

TERM_NOTES = {
(123,109): 'Source サン＝ジョルジェ matches the current city-table Sao Jorge. Preserve the bandit question without adding a new political or personal identity.',
(123,165): 'Proofs is the established artifact term. Keep the source great-powers/pretext/partitioning connection; no new item or motive is invented.',
(123,207): 'Keep the established singular Proof reference and the source uncertainty about a connection. The hidden object is not assigned an unsupported name.',
(124,18): 'India is explicit in the source. No Ganges or particular building name is given, so neither is supplied.',
(126,10): 'The source says this small knife. Keep the generic knife reference; the separately bound Tlaloc Knife and Ceremonial Knife do not establish this object\'s identity.',
(127,80): 'Retain Route Map: bank4 of the accepted, byte-identical common radial resource uses that exact caption. The southeast direction is explicit in the source.',
(132,13): 'Valdes is the established family-name address for actor31 Pedro de Valdes, already included in the scoped native identity review.',
(134,15): 'Source ヴェルス is the exact given-name field of actor61, currently Vels. Preserve Claudio\'s alarm at the recognized pirate flag without adding a rank.',
(137,48): 'Trade house is the natural facility noun for source 交易所. Keep the unclaimed-share condition and both investment locations, without claiming a new literal menu caption.',
(139,71): 'Source 六分儀 matches the existing Sextant item. The common noun sextant is natural in this purchase instruction; the following exchange still requires equipping Julio himself.',
}


def main():
    assert not OUT.exists() and not ROOT.exists()
    parent, identity, terms = map(load, [PARENT,IDENTITY,TERMS])
    assert parent['source_objects'] == len(parent['records']) == 351
    assert identity['runtime'] == terms['runtime']
    assert parent['current_ROM_sha256'] == terms['runtime']['candidate_sha256']
    public = {r['actor_ID']:r for r in identity['name_bindings']}
    roles = {r['source_selector']:r for r in identity['dynamic_roles']}
    doc = deepcopy(parent); changes = []; holds = []
    applied = set(); noted = set()
    for row in doc['records']:
        before = deepcopy(row)
        key = (row['block'],row['source_reference'].get('record_index'))
        notes = []
        selector = row.get('source_selector')
        if selector is None:
            assert row['kind'] == 'typed-choice-label'
            notes.append('Source-bound player choice; no speaker name or role is invented.')
        elif selector == 254:
            notes.append('Preserve the source system/tutorial presentation selector254.')
        elif selector < 207:
            binding = public[selector]
            assert row['speaker'] == next(r['text'] for r in binding['current_consumers'] if r['consumer']=='progressive-nameplate')
            notes.append(f"Scoped source/current actor{selector} identity and public name are bound by the saved 22-name review; full-catalogue particle defects remain separate.")
        else:
            assert row['native_dynamic_role'] == roles[selector]
            notes.append(f"Preserve source selector{selector}/runtime role{roles[selector]['role_index']}; the own-startup fallback does not assign the original conditional speaker.")
        if key in UPDATES:
            row['english'], note = UPDATES[key]; notes.append(note); applied.add(key)
        if row['block'] == 136 and 'Staff of Guidance' in row['english']:
            row['english'] = row['english'].replace('Staff of Guidance','Guiding Staff')
            notes.append('Match 善導のステッキ to the exact registered Guiding Staff item name; preserve the character\'s uncertainty or legend qualification in this complete exchange.')
        if key in TERM_NOTES:
            notes.append(TERM_NOTES[key]); noted.add(key)
        # Every intake hold is an identity/role hold or one of the explicit term cases.
        if not before['review']['localization']:
            assert selector in public or selector in roles or selector == 254
            holds.append(row['id'])
        row['review']['localization'] = True
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        row['scoped_binding_resolution'] = ' '.join(notes)
        row['localization_note'] = before['localization_note']+' '+row['scoped_binding_resolution']
        row['source_name_term_control_binding_pending'] = False
        row['source_names_roles_terms_anddynamic_bindings_pending'] = False
        row['native_scoped_identity_proof'] = str(IDENTITY)
        row['native_scoped_identity_proof_sha256'] = sha(IDENTITY.read_bytes())
        row['scoped_term_proof'] = str(TERMS)
        row['scoped_term_proof_sha256'] = sha(TERMS.read_bytes())
        row['decision'] = 'retention' if row['english'] == row['current_English'] else 'revision'
        if row['english'] != before['english']:
            row['finding'] = before['finding']+' '+' '.join(notes[1:])
            row['previous_comparison_English'] = before['english']
            changes.append(dict(id=row['id'], source_reference=row['source_reference'], current_reference=row['current_reference'],
                prior_proposal=before['english'], reviewed_English=row['english'], reason=' '.join(notes[1:]),
                previous_decision=before['decision'], decision=row['decision']))
        if row['decision']=='retention':
            row['retention_reason'] = row['finding']+' '+row['scoped_binding_resolution']
        else:
            row.pop('retention_reason',None)
        assert row['english'].isascii() and not any(x in row['english'] for x in ['\n','\r','{LB','{PAD}','{ALIGN'])
        for macro,count in row['source_macros'].items(): assert row['english'].count(macro) == count
        assert row['new_credit'] == 0
    assert applied == set(UPDATES) and noted == set(TERM_NOTES)
    assert len(holds) == 126
    counts = Counter(r['decision'] for r in doc['records'])
    doc.update(proposed_revisions=counts['revision'], justified_retentions=counts['retention'],
        four_gate_passes=351, pending_name_term_IDs=[], all351_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True, source_context_localization_formatting_gates_pending=True,
        no_original_conditional_activation_or_new_gameplay_claim=True,
        scoped_names_andterms_bound_for_prose=True, two_full_catalogue_particle_corrections_still_pending=True,
        scoped_identity_proof=str(IDENTITY), scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()),
        scoped_term_proof=str(TERMS), scoped_term_proof_sha256=sha(TERMS.read_bytes()),
        scoped_name_review=identity['scoped_name_review'], scoped_name_review_sha256=identity['scoped_name_review_sha256'],
        current_comparison_parent=str(PARENT), current_comparison_parent_sha256=sha(PARENT.read_bytes()),
        new_credit=0, full_goal_complete=False)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [PARENT,IDENTITY,TERMS,Path(__file__)]})
    ROOT.mkdir(parents=True)
    save(OUT,doc)
    save(ROOT/'prose_resolution.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        individual_four_gate_passes=351,previous_intake_holds_resolved=holds,proposed_revisions=counts['revision'],
        justified_retentions=counts['retention'],proposal_wording_changes=changes,
        formatting_native_page_contact_sheet_gameplay_andintegration_pending=True,
        two_full_catalogue_particles_still_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PARENT,IDENTITY,TERMS,Path(__file__)]}))
    print(dict(four_prose_gates=351,resolved_intake_holds=len(holds),revisions=counts['revision'],
        retentions=counts['retention'],proposal_wording_changes=len(changes),formatting_pending=351,new_credit=0))


if __name__ == '__main__': main()
