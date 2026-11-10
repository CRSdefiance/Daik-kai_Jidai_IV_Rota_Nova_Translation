"""Record the complete source-context role review before changing shared labels."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/square_shopkeeper_contexts_v6974')
SCOPE = Path('work/analysis/square_shopkeeper_scope_v6972/ten_source_identical_roles_current_owners_alias_fields_and_whole_clean_story_contexts.json')
NATIVE = Path('work/analysis/square_shopkeeper_baseline_v6973/all414_current_getters207_voices_and_all36_owner_pointer_values.json')
MANUSCRIPT = Path('translations/square_shopkeeper_label_manuscript_v2.json')

# Each group has been read as complete clean Japanese exchanges, including the
# surrounding protagonists, alternative branches and the final replies/notices.
# The groups bind identical roles, not identical prose or naturally visited events.
GROUPS = [
    ([(0,54)], 'The local shopkeeper reports Silveira defeating Espinosa and the reported move of the governorate; Rafael departs abruptly. The speaker is a local informant, not the governor or a newly named official.'),
    ([(0,56)], 'The shopkeeper and port worker thank Rafael after the oppressive merchants, explain the townspeople pooling money to obtain a fragment and entrust it to him. Civic gratitude does not change the speaker into an official or faction leader.'),
    ([(0,74)], 'The female shopkeeper contributes a brief warning about gathering fleets among several townspeople discussing the coming Seville confrontation. Shopkeeper remains accurate without displaying gender metadata or conferring military rank.'),
    ([(0,81),(1,84),(3,56)], 'The shopkeeper appears among the bullfight audience, heckling and cheering before the protagonist recruits Emilio rather than the expected matador. The occupation remains a useful role label while the speaker is a spectator; no announcer or bullfighter identity is implied.'),
    ([(0,84),(3,59)], 'The shopkeeper gives Janus a cryptic hint about Gerhardt, then backs away from explaining; the party finds and speaks to the retired admiral. The shopkeeper is the local information source, not the admiral, his retainer or a new relative.'),
    ([(0,195),(1,187),(2,183),(3,156)], 'After customers dispute paintings and leave, the shopkeeper vents about arguments inside the shop, describes the collecting fad and jokes privately with the sailor. Direct references to the shop, customers and shopkeeper establish the occupation; Square adds an unnatural standalone modifier.'),
    ([(0,199),(1,191),(2,187),(3,160)], 'In the complete coughing/almond exchange the shopkeeper checks on a sailor, reports a remembered remedy and offers to look for it. The role does not become physician, pharmacist, spouse or relative merely because of the advice.'),
    ([(0,201),(1,193),(2,189),(3,162)], 'The shopkeeper and guildmaster praise a ceramics purchase and complain about indiscriminate collecting; two other men reveal the pair bought worthless ceramics at an absurd price. Shopkeeper preserves the occupation through the ironic reversal without inventing art expertise or a personal name.'),
    ([(0,203),(1,195),(2,191),(3,164)], 'The shopkeeper hesitates over purchasing dye while the sailor insists competitors will buy it up, then reluctantly agrees. The familiar oyaji-san address does not prove fatherhood; the occupational label needs no age, kinship or employer-specific title.'),
    ([(0,228),(1,219),(2,216),(3,189)], 'The shopkeeper angrily tells Vivian to leave because she disrupts business; the protagonist then hears her Arthur/Excalibur/Avalon message and asks companions about information. The occupational label explains the initial complaint without identifying this person as a guard or an Arthurian figure.'),
    ([(0,233),(1,224),(2,221),(3,194)], 'The shopkeeper stops the protagonist in the square, challenges a favorable European account of the Crusades, expresses local anger about distorted history and champions Saladin; Al explains his humane reputation and the missing armor rumor. Shopkeeper identifies the ordinary local speaker without inventing historian, religious office, ethnicity or rank; the claims remain character viewpoints.'),
    ([(1,58)], 'The shopkeeper and other townspeople confront Espinosa about their losses; after Hodram entrusts his fate to them, the shopkeeper proposes a Solomon-related test before offering an undisclosed reward. The changing respectful and angry voice does not establish a civic office, judge, priest or new personal name.'),
    ([(1,59)], 'When Hodram returns, the shopkeeper recognizes the object and entrusts the fragment from Espinosa, hoping for peace and prosperity. Entrusting a fragment does not make this occupational speaker a ruler or faction official.'),
    ([(1,172),(2,168),(3,139)], 'The shopkeeper introduces Mikhail as a knowledgeable local and warns about bringing women; the party observes his knowledge and harassment before the recruitment and item-information notices. The shopkeeper is a local informant, not Mikhail, a family member, the woman or a new crew member.'),
    ([(2,34)], 'Lil encounters the distressed merchant and offers medicine; the shopkeeper explains the addictive drug, escalating prices and ruin, then warns against challenging Espinosa. Shopkeeper retains the local merchant role without assigning medical authority or transferring the distressed merchant identity to this speaker.'),
    ([(2,35)], 'The shopkeeper celebrates Espinosa falling, discusses the harm and recovery, recognizes Lil on the alternative path and offers the unexplained object. Customer and merchant language directly support Shopkeeper; the familiar uncle/old-man address does not establish kinship or require an age label.'),
    ([(2,36)], 'After Lil prohibits Espinosa selling drugs, the shopkeeper thanks her on both recognition paths and offers the unexplained object. The thankful community member remains a shopkeeper, without invented government authority or a relationship to Lil.'),
    ([(3,47)], 'The shopkeeper joins the public confrontation of Espinosa, asks to handle him and entrusts the fragment to Maria; the crew then observes her joyful response to the townspeople. Participation in public justice does not change the source occupational identity to magistrate or faction officer.'),
    ([(3,278)], 'Amid the disguised-missionary sting and the impostor official performance, this shopkeeper briefly tells the governor the forces have already left. The later revelation of the acting ruse does not turn the answering shopkeeper into the actor, county magistrate, governor or military officer.'),
]

ACTOR_REASONS = {
    82: 'Business interference, ceramics collecting, local hints and bullfight spectatorship all retain the same shopkeeper role. The plain occupation works in each setting and avoids the awkward Square modifier.',
    83: 'The one located static story utterance reports assembling fleets among townspeople. The clean primary label supplies the occupation; separate female/European metadata is not a displayed surname, age or rank.',
    84: 'Across the Africa plot exchanges the shopkeeper acts as merchant, witness, civic informant and grateful donor. Neither gratitude nor a test/reward confers an official title. Shopkeeper remains natural across the different tones.',
    85: 'The art-shop proprietor and the angry local Crusades/Saladin speaker share the same occupational label. Shopkeeper fits both complete exchanges without implying a historian or religious office.',
    86: 'The dye-purchasing exchange supports a shopkeeper weighing a commercial decision. The sailor\'s familiar address does not establish fatherhood; no age or regional suffix is added.',
    87: 'The almond-remedy conversation and Mikhail introduction use this shopkeeper as a local informant. Neither remedy hearsay nor local gossip changes the occupation to physician or guide as a new office.',
    88: 'The brief reply within Maria\'s complete Macao sting identifies a local bystander who knows the forces departed. Preserve the source shopkeeper role without promoting the speaker to an official or exposing the actor\'s identity.',
    89: 'No static SC0-SC3 preamble was found in the explicitly bounded census. The exact clean primary label independently and unambiguously means a shop proprietor in the square; Shopkeeper is the same natural role label. Korean metadata is not appended. Shared/dynamic behavior remains a separate validation gate, not an invented story visit.',
    90: 'No static SC0-SC3 preamble was found in the explicitly bounded census. The exact clean primary label is the same occupation; Shopkeeper localizes it without appending Japanese metadata or inventing an age, rank or biography. Shared/dynamic validation and representative display remain pending.',
    91: 'No static SC0-SC3 preamble was found in the explicitly bounded census. The exact clean primary label is the same occupation; Shopkeeper keeps that function without turning the unused Indio metadata into a displayed identity or ethnicity. No conditional dialogue visit is claimed.',
}

if __name__ == '__main__':
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    scope, native = read(SCOPE), read(NATIVE)
    assert scope['current_ROM_sha256'] == native['current_ROM_sha256']
    assert scope['source_context_count'] == 42 and scope['raw_static_story_hit_count'] == 216
    decisions = {key: reason for keys, reason in GROUPS for key in keys}
    assert len(decisions) == 42
    clean = NdsImage.open('work/clean.nds')
    banks = {r: IlnkContainer.parse(clean.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
    contexts = []
    for context in scope['story_contexts']:
        route = int(context['file_path'][8])
        key = route, context['block']
        block = banks[route][context['block']]
        assert sha(block) == context['source_block_sha256'] and block.hex() == context['source_block_hex']
        role_speeches = [r for r in context['whole_clean_transcript'] if r['source_selector'] in range(82,92)]
        for row in context['whole_clean_transcript']:
            ref = row['source_reference']
            assert block[ref['offset']:ref['offset']+ref['bytes']].hex() == row['source_hex']
            assert bytes.fromhex(row['source_hex'])[1:].decode('cp932') == row['Japanese']
        contexts.append(dict(file_path=context['file_path'], block=context['block'],
            source_block_sha256=sha(block), complete_source_exchange=context['whole_clean_transcript'],
            role_speech_references=[r['source_reference'] for r in role_speeches],
            role_actor_IDs=sorted({r['source_selector'] for r in role_speeches}),
            complete_exchange_read=True, source_role_context_and_localization_reason=decisions[key],
            review_scope='speaker-role localization only; no new approval or revision of the surrounding dialogue',
            actual_gameplay_visit_claimed=False, new_dialogue_credit=0))
    assert sum(len(c['role_speech_references']) for c in contexts) == 216
    ROOT.mkdir(parents=True)
    proof = ROOT / 'all42_complete_clean_contexts_ten_individual_role_decisions.json'
    save(proof, dict(contexts=contexts, exact_source_unique_blocks=len({r['source_block_sha256'] for r in contexts}),
        exact_source_duplicate_reuse_by_whole_block_hash=True,
        no_predecessor_English_dialogue_used_to_determine_source_role=True,
        decision='Propose Shopkeeper for the ten source-identical primary role labels.',
        rationale='Shopkeeper is natural American English for the occupation. The town-square qualifier locates the shop rather than naming the person; scene and dialogue retain that location. Omitting it from the header does not relocate the shop or turn the speaker into another profession. Do not replace it with Market Vendor because a stall or market-vendor specialization is not established in every exchange.',
        actor_reasons=ACTOR_REASONS,
        absent_static_story_actor_IDs=[89,90,91],
        no_closed_global_dynamic_consumer_census_or_natural_conditional_visit_claim=True,
        no_name_asset_change_and_no_duplicate_dialogue_review_credit=True,
        shared_consumers_native_target_glyphs_representative_capture_registered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SCOPE,NATIVE,Path(__file__)]},
        full_goal_complete=False))
    rows=[]
    for actor in scope['actors']:
        ident=actor['actor_ID']; field=actor['fields'][0]
        assert field['Japanese']=='広場の店主' and field['current_English']=='Square Shopkeeper'
        rows.append(dict(id=f'DK4_ACTOR_{ident:03d}_PRIMARY_LABEL',actor_ID=ident,
            target_locale='en-US',source_Japanese=field['Japanese'],current_English=field['current_English'],
            english='Shopkeeper',speaker='Shopkeeper',editorial_decision='revise',
            source_meaning='The proprietor of a shop in the town square; an occupational speaker label.',
            context=ACTOR_REASONS[ident],localization_note=ACTOR_REASONS[ident]+' Use a natural occupational header; the scene and spoken context preserve the square location. Do not append unused metadata or invent a personal identity.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            source_reference=dict(source_file='/__arm9__.bin',pointer_field=field['pointer_field'],pointer=field['source_pointer'],storage_offset=field['source_storage_offset'],terminated_hex=field['source_terminated_hex']),
            current_reference=dict(source_file='/__arm9__.bin',pointer_field=field['pointer_field'],runtime_pointer=field['current_pointer'],file_offset=field['current_storage_offset'],terminated_hex=field['current_terminated_hex']),
            all_three_source_current_name_fields=actor['fields'],
            complete_clean_exchange_references=[dict(file_path=c['file_path'],block=c['block'],source_block_sha256=c['source_block_sha256']) for c in contexts if ident in c['role_actor_IDs']],
            exact_current_two_getters=[r for r in native['ten_role_twenty_getters'] if r['actor_ID']==ident],
            formatting_and_shared_consumer_validation_pending=True,new_dialogue_completion_credit=0))
    save(MANUSCRIPT,dict(format='editorial-role-label-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_ROM=scope['current_ROM'],current_ROM_sha256=scope['current_ROM_sha256'],current_ARM9_sha256=scope['current_ARM9_sha256'],
        context_review=str(proof),context_review_sha256=sha(proof.read_bytes()),records=rows,
        all_ten_four_prose_gates_true_formatting_false=True,
        proper_names_Rafael_Hodram_Joakim_Maria_Camille_and_all_other_actor_fields_preserved=True,
        no_ROM_or_registry_or_ledger_change=True,no_duplicate_dialogue_or_name_completion_credit=True,
        full_goal_complete=False))
    print(dict(complete_source_contexts=42,unique_source_blocks=34,role_utterances=216,
        proposed_role_revisions=len(rows),formatting_pending=True,assets_changed=0,credit=0))
