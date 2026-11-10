"""Read all seven clean source blocks before prior English; meanings only, no localized approval."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_next_clean_gloss_v8786')
SOURCE=Path('work/analysis/Hodram_next_clean_v8785/complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json')
GLOSSES={
54:{
6:'The unfamiliar speaker asks whether the addressee is a newcomer.',
10:'The captain is puzzled, then answers yes.',
14:'The speaker acknowledges the answer, tells the newcomer to do his best, and gives a low, suppressed chuckle. The repetition and laugh can suggest an unsettling or mocking undertone; the motive is not stated.',
18:'The captain remains puzzled, with only a question reaction.',
},
55:{
6:'The casual speaker checks whether the addressee is the military man called FA or something like that, then says the man at the guild was asking for him in the town named ヴェラクルス. FA is an original runtime substitution, not the literal letters of a name.',
},
56:{
7:'The captain asks what the addressee will do and whether she will go along with everyone else.',
10:'The source system-panel text labels the silent response as coming from a foreign girl and shows an ellipsis. The caption and silence are both part of the source text; FE is the separate presentation selector.',
13:'The captain recalls that she alone belongs to a different ethnic group from the other captives and advises her to have the people of this town look after or shelter her for a while.',
},
57:{
7:'The hesitant speaker begins to address FI, the original runtime name substitution.',
11:'The captain notices and asks what it is.',
15:'She hesitantly says thank you, struggling to put the newly learned words together.',
19:'The captain reacts with surprise that she has learned the language or words.',
23:'She nods and says she has learned a little, with hesitant, broken delivery.',
27:'The captain acknowledges this and praises her ability to learn quickly.',
31:'She addresses FI again and repeats her thanks, still speaking haltingly.',
35:'The captain is briefly taken aback, then tells her not to worry about it or not to mention it.',
},
58:{
6:'The frightened man stammers and demands to know what the others are doing.',
10:'A rough speaker orders him to come over.',
14:'The captain is startled to recognize the man as エスピノサ.',
18:'A respectful speaker addresses FA and thanks or praises the addressee for defeating this scoundrel.',
21:'The captured man protests that the others cannot expect to get away with treating him this way.',
24:'The rough speaker tells him to shut up.',
28:'The man cries out in pain. The words establish pain; any specific visible blow, attacker or animation must be bound separately to native controls.',
32:'The rough speaker says the man has been doing whatever he pleased for a long time.',
35:'The man nervously asks what the accusation is about.',
39:'The accuser refuses to let him pretend to have forgotten: his father was deceived, the house and farmland were taken, and the family went missing. The source supports an actual father and missing family; it does not say they are all dead.',
42:'The respectful accuser says his friend tried to report the man\'s corruption to the home country, and the man killed that friend while making it look like an accident.',
46:'Another speaker says many villagers from her home have been taken away to various places and forced to work while barely being fed.',
58:'A companion condemns the man with the image of a demon wearing human skin.',
64:'The accused disclaims knowledge and blames foolish subordinates for doing everything on their own.',
68:'An angry speaker bursts out at the man, without completing a longer argument.',
80:'Another companion says the man is corrupt through and through and there are no grounds for leniency.',
93:'The captain asks セラ whether she knows this man.',
97:'She quietly answers yes.',
101:'The man reacts with shocked recognition of her.',
105:'In halting speech, she says this man ordered that she be sold for a high price and sent to the home country. Preserve the accusation and the broken delivery; the source does not identify that country in this line.',
108:'The man begins an alarmed protest.',
112:'The captain is silent.',
116:'The man asks them to wait, claims mistaken identity, and calls the accusation false.',
120:'She accuses this man of killing her younger brother and her companions, repeating the reference to him in intense distress. The younger-brother relationship is explicit in the source.',
124:'The man tries to stop her, curses her, and blurts out that he should have killed her along with the others at the time, before a cut-off cry. This undermines his denial; no later punishment is stated here.',
127:'The captain concludes that the man apparently cannot talk his way out of this now.',
137:'The respectful accuser calls him inhuman, then asks FA what the addressee plans to do with him.',
141:'The captain leaves the decision about the man\'s treatment or disposition to the local speakers.',
145:'The rough speaker tells the others they heard that, orders the man to come, and says they will make him pay fully for his crimes. A specific sentence, execution or enslavement is not stated.',
148:'The man begs to be saved.',
152:'The captain is silent.',
164:'She is silent.',
168:'The captain tells セラ to remember that the reality is that Westerners like that man are still throwing their weight around throughout the world.',
172:'The captain adds self-critically that he himself may not be very different from them.',
175:'In limited speech, she rejects that comparison and says FI is different.',
179:'The captain cautions her against putting too much trust in people. This is a warning about overtrust, not an absolute order never to trust anyone.',
186:'The respectful speaker addresses FA again.',
190:'The speaker regrets seeming to test the group but says there is an object he very much wants them to find and bring back.',
194:'The captain gives a puzzled reaction.',
198:'The speaker addresses the admiral and asks whether he has heard rumors about the legend of King Solomon.',
202:'According to the old account, the great King Solomon\'s powers extended even to commanding the demon king. This is presented as legend, not independently established historical fact.',
206:'Rumor says a weapon associated with that demon king was sealed away on an icy island far to the northwest of here.',
210:'The speaker says the weapon is said to be held only by someone qualified to be an overlord, then begins a conditional offer if the group can bring it back.',
213:'The captain asks what will happen if they bring it back.',
217:'The speaker says he intends to give them a certain object.',
220:'The captain asks what the object is.',
224:'The speaker declines to say for now and suggests leaving it as something to look forward to after their safe return.',
228:'The captain considers the prospect of the demon king\'s weapon.',
239:'A companion repeats the description of an icy island far to the northwest and wonders whether it means Iceland. This remains a suggestion, not a confirmed destination.',
},
59:{
5:'The respectful speaker reacts with surprise and asks whether the object has been found.',
9:'After considering it, he says there is no mistake and that he will entrust something to the group.',
13:'He respectfully offers a fragment of a map.',
19:'The captain asks what it is.',
23:'The speaker says エスピノサ had it and had also long been seeking Africa\'s 覇者の証; the speaker\'s group had been praying that it would somehow stay out of his hands. The distinction between his former possession of the fragment and his search for the larger named objective matters.',
26:'He declares that the addressee is the one who ought to become the dominant figure of this sea region and wishes for the addressee to find the treasure shown on the map promptly and bring peace and prosperity to the land.',
30:'The captain says so much expectation puts him in an awkward position, but gratefully accepts the gift.',
},
60:{
5:'A companion addresses the admiral and says there is nothing as unforgivable as slave traders.',
8:'The captain gives a puzzled reaction.',
12:'The companion recalls visiting サン＝ジョルジェ as a ship\'s carpenter in a Portuguese fleet bound for India, contracting an epidemic illness, and leaving the ship.',
15:'He says local residents saved him then and nursed him with great care.',
19:'He learned that Portuguese people had treated them very badly, yet they treated him as a sick person deserving care and worried about him as though he were family. This is a comparison, not actual kinship.',
22:'The captain responds with interest.',
26:'The companion says the experience made him feel the Lord\'s teaching to love one\'s neighbor deeply and personally; since then this place has become his second home.',
29:'He says he then swore that someday he would fight the vile, unscrupulous traders who conduct slave raids in Africa.',
33:'He urges the admiral to make sure they defeat エスピノサ.',
36:'The captain firmly agrees.',
},
}

NOTES={
54:'Read all four reactions together. Preserve the newcomer question, brief baffled answer, repeated acknowledgment and low chuckle. Do not invent a name, faction, rank, hidden scheme or relationship for actor119 from this exchange alone.',
55:'Read the identity check and guild message together. 軍人 does not by itself establish a commissioned rank; 親父 in this guild-role reference must not invent a father relationship. Preserve FA and verify its native referent and approved ヴェラクルス term before final English.',
56:'The silent FE caption belongs to a distinct native consumer. Different 民族 means ethnic identity, not automatically nationality, language or gender. 捕虜 requires surrounding event15 context before choosing a more specific English category. The source suggests temporary local protection, not permanent residence, adoption or an invented institution.',
57:'Follow the progression from tentative address to thanks, surprise, nod, praise, renewed thanks and modest deflection. Reproduce newly learned, hesitant speech with care and dignity; do not create comic caricature, stuttering across all future dialogue, an invented age, romance or family relationship. FI remains an exact runtime substitution.',
58:'Read all49 utterances and the source command/ancestor inventory together. Queries and relative controls mean the entire printed list is not proof of one attainable path; bind alternative companion comments and the quest continuation before localized dialogue. Preserve distinct allegations, explicit kinship, missing versus dead relatives, coercion and hunger, the denial and revealing outburst, local disposition left unspecified, the captain\'s self-criticism, qualified trust and the conditional legendary quest. Keep the colonial/Western identity reference and religious/cultural legend without imposing external biography. Do not name the demon weapon, promised object or country, confirm Iceland, invent a punishment, or assign opaque animation semantics from text alone.',
59:'The map fragment, former holder, ongoing search for 覇者の証, hoped-for exclusion, offered trust and the captain\'s guarded gratitude form one exchange. Bind the original event/action and any item-control object before final item terminology. Numbered adjacency to58 does not establish actual trigger order or earned progress.',
60:'Read the full personal recollection and vow. Preserve slavery and slave raids explicitly, local kindness despite prior Portuguese abuse, serious illness, ship\'s-carpenter role in that past voyage, the Christian love-of-neighbor reference, second-home metaphor and shared commitment. Do not invent death, an exact disease, denomination, rank, a voyage date, nationality from unused metadata or actual family relationship from ように.',
}

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert not packet['inventory_failures'] and packet['source_only_no_current_English_exposed_orused']
    groups=deepcopy(packet['groups']);assert [g['block'] for g in groups]==list(GLOSSES)
    count=0
    for g in groups:
        number=g['block'];assert [r['source_record_index'] for r in g['records']]==list(GLOSSES[number])
        assert not any(c['word']==0x2100 for c in g['commands'])
        for r in g['records']:
            assert r['source_decode_error'] is None and not r['already_contextually_completed'] and r['current_English_body_unread']
            r.update(first_clean_source_gloss=GLOSSES[number][r['source_record_index']],source_context_note=NOTES[number],
                whole_clean_block_andall_neighboring_utterances_read_before_current_English=True,
                current_English_dialogue_still_unconsulted=True,source_meaning_only_not_localized_orformatting_approval=True,
                names_native_consumers_macros_branch_paths_actual_andrelease_still_pending=True,no_source_prose_counter_orcompletion_credit=True)
            count+=1
    assert count==82 and sum(r['source_selector']==254 for g in groups for r in g['records'])==1
    ROOT.mkdir(parents=True);save(ROOT/'82_first_clean_glosses_context_andcultural_fidelity_before_current_English.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],
        groups=groups,source_speech_objects=82,typed_choice_objects=0,source_FE_objects=1,
        all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English=True,
        source_only_numbered_blocks_not_assumed_chronological_orone_continuous_exchange=True,
        B58_alternative_native_paths_andcompanion_membership_require_binding=True,
        limited_language_ethnic_identity_actual_kinship_colonial_slavery_andChristian_legend_context_reviewed=True,
        complete_source_references_preambles_commands_andEV1_context_preserved=True,
        source_Japanese_names_are_evidence_not_approved_new_romanizations=True,
        every_localization_formatting_actual_frozen_policy_andregistered_gate_still_pending=True,
        B31_B53_registered_builder_patch_startup_andcredit_are_separate_incomplete_work=True,
        no_new_ROM_emulator_run_current_English_read_orcounter_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [SOURCE,Path(__file__)]}))
    print('Clean-first:82utterances/seven whole source blocks/one FE/no menu glossed withindividual meanings andwhole-block context. Older English unread;all native/localization/release gates pending;zero credit.',flush=True)
