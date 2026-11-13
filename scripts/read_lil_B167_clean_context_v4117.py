"""Fresh complete-exchange glosses from clean Japanese before predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_clean_context_v4117')
SOURCE = Path('work/analysis/lil_B167_clean_v4116/complete_clean27_speeches_two_choice_labels_before_English.json')
CONTEXT = '''A rough-spoken man, source actor109, hails an admiral and asks whether she wants to hear his sailing-ship lecture. Lil is puzzled. He admits that he has been unbearably bored lately and asks her to think of listening as doing him a favor. No payment, commercial lesson, job title or relationship is supplied. The two player labels accept or decline the offer. Preserve the casual invitation, Lil's short incredulous response and the man's frankly self-interested plea without adding a fee or lesson reward.
The source stores a refusal exchange before the accepted lecture; native choice ownership must be bound independently. Actor4 politely objects to being underestimated, and actor23 agrees. An actor13 membership query gates a further formal claim that there is no need to hear about ships at this late stage. The man gives up because they seem knowledgeable and says he will wait for a more novice-looking audience. This refusal has its own earlier end. Do not concatenate it with the accepted lecture, or treat declining as refusing recruitment. Source actor23 is the previously source-bound Manuel and actor13 Cesare, but their exact current consumers and actor4/109 names still require fresh binding. No rank, kinship or role should be inferred from a raw speaker byte.
On acceptance the man approvingly says the admiral has the right attitude and will go far. This is flattery, not a guaranteed award or future plot fact. He calls sails a sailing ship's lifeblood and explains square versus triangular/lateen sails. Square sails are set across the vessel's direction of travel and cannot turn fore-and-aft; they work well with a following wind but cannot reach the optimal angle against the wind. Triangular sails, which those in the know call lateen sails, run fore-and-aft and cannot turn athwart the vessel. They can achieve the right angle against the wind but are less fast with a following wind. Preserve this character's game-specific explanation without adding new real-world qualifications, correcting the game's mechanics or inventing speeds. The check for understanding is rhetorical; the source supplies no second menu there.
He then covers four supplementary sails. Topsails are small square sails at the top of each mast. Staysails are small fore-and-aft sails ahead of each mast and cannot be fitted in front of lateens, because fore-and-aft sails would overlap. The source bow-sail name is スプリットセイル; bind its reviewed UI spelling rather than copying an unverified English loanword. It is a square sail at the bow and cannot be fitted to small ships. The stern sail, also called ジガースパンカー, is fore-and-aft, effectively adds a small mast and fits only large ships. Preserve both size restrictions, the installation positions and the causal overlap/additional-mast explanations. Do not substitute ship classes, numeric capacities, mast counts or economic facts not given here. Bind square/lateen, topsail/staysail and bow/stern names to the exact reviewed Help/Refit terminology before authoring English.
Finally he asks whether they know that ships with two or more masts sail faster with a somewhat oblique wind than with one directly behind. He invites an answer from a specific companion; actor23 explains that the masts are arranged fore-and-aft. The man agrees: directly following wind reaches only the rear mast, leaving the forward masts ineffective. Wind from diagonally behind is fastest, provided the sail angle is adjusted to match. Actor4 understands. A second actor13 membership query gates a surprised admission that he had not paid much attention to this and now understands. That conditional realization is on the lecture path, while his already-know-it objection is on the alternative refusal path; no invented same-exchange humiliation or callback is needed. The speaker thanks everyone for keeping him company and says he will get back to work. The nature of his work is not stated. Source resource words and the two ends must be preserved without inferring payment, recruitment, natural event eligibility or a source port. No runtime FI/FA/FO substitutions occur in this block. All29 objects remain uncredited until contextual/native/reference/release requirements pass. The full wider editorial objective, separate graphics work and later older-record technical re-audit remain open.'''
MEANINGS = {
    5: 'Actor109 casually hails the admiral and asks whether she wants to listen to his sailing-ship lecture. Preserve the direct Admiral address and optional invitation without inventing a paid course or professional title.',
    8: 'Lil gives a short puzzled or incredulous response. Do not invent an acceptance, refusal or elaborated question.',
    12: 'The man says he has been unbearably bored lately and asks her to think of listening as helping someone out. Keep the self-interested, informal plea; it is not a request for money or rescue.',
    30: 'On the refusal exchange, actor4 politely but firmly says they must not be underestimated. Bind the current actor identity and voice; no new rank or expertise credential is supplied.',
    33: 'Actor23 agrees with the preceding objection in a thoughtful, older-sounding manner. Keep the brief agreement without inventing technical detail.',
    45: 'Conditional actor13 says, with emphatic formal phrasing, that there is no need to hear about ships now. Preserve the confident objection on this refusal branch, not as an opening to the lecture.',
    51: 'The man concedes there is no helping it, says they seem knowledgeable about ships and decides to wait for more novice-looking listeners. Do not add a fee, transaction or insult beyond the dismissive, informal observation.',
    62: 'On acceptance he approves of the admiral\'s attitude and predicts she will become a person of consequence. Preserve friendly flattery rather than a literal rank promotion or guaranteed future event.',
    65: 'He opens by saying that, as the name sailing ship implies, sails are the ship\'s life. Keep the metaphor and conversational introduction.',
    68: 'He announces that he will first explain the difference between square and triangular sails. Preserve the sequence and the two basic types.',
    71: 'A square sail is also called a square sail in the loanword terminology and is a transverse sail spread across the ship\'s direction of travel. English need not mechanically repeat an identical borrowed term, but must retain the orientation/type definition.',
    75: 'Because it is a transverse sail, it cannot be set fore-and-aft. It works well with a following wind but cannot be set to the optimal angle against the wind. Preserve both wind conditions and the explanation as this character\'s game lesson.',
    78: 'Triangular sails, called lateen sails by those in the know, are set fore-and-aft, unlike square sails, and cannot be turned across the ship\'s direction. Preserve the knowing aside and the opposite orientation limitation.',
    81: 'This explains why lateens can reach a suitable angle against the wind but do not produce as much speed with a following wind. He checks whether they follow so far. This is not an actual additional choice prompt.',
    84: 'He moves on to supplementary sails that can be fitted. Preserve the transition without inventing a complete equipment catalogue claim.',
    88: 'The upper sail, properly termed topsail in the loanword explanation, is a small square sail fitted atop each mast. Preserve its size, square/transverse type and position on each mast.',
    92: 'A staysail is a small fore-and-aft sail fitted ahead of each mast. It cannot be fitted in front of a lateen because the fore-and-aft sails would overlap. Preserve the fit restriction and its reason without generalizing to an unrelated ship-wide rule.',
    95: 'The bow sail is named スプリットセイル in the source; the man urges proper seafaring terminology. It is a square sail at the bow and cannot be fitted to a small ship. Bind the reviewed UI name before authoring; do not drop the size restriction or invent a new mast.',
    98: 'The stern sail is also called ジガースパンカー. Although fore-and-aft, fitting it effectively adds a small mast, so it can be fitted only to large ships. Keep the cause and restriction; bind the reviewed name.',
    101: 'He asks whether they know that ships with two or more masts can go faster with somewhat diagonal wind than with wind directly from behind. Preserve the at-least-two condition and comparison; no exact angle or speed is supplied.',
    105: 'He asks one of the listeners whether he knows why. The following answer comes from actor23; do not arbitrarily redirect this question to Lil or invent a name before native actor binding.',
    109: 'Actor23 thoughtfully answers that the masts are arranged one behind another, fore-and-aft. Preserve the reason, not merely agreement that there are multiple masts.',
    112: 'The man agrees and explains that with wind directly behind, only the rear mast receives the wind and the forward masts are ineffective. Preserve the fore/rear distinction and causal explanation without adding percentages.',
    115: 'Therefore wind from diagonally behind makes the ship fastest, provided the sails are adjusted to the matching angle. Keep both the conclusion and the explicit adjustment condition.',
    119: 'Actor4 expresses understanding. Keep the short realization, with identity and voice to be freshly bound.',
    131: 'Conditional actor13 is surprised, admits he had not paid much attention to this and says he now sees why. This is an optional lecture-path reaction, not a direct continuation of his refusal-path boast.',
    138: 'The man thanks them for keeping him company and says he will return to work. Do not invent what his work is or imply a lesson fee or recruitment.',
}
CHOICE_MEANINGS = {
    0: 'Lil casually accepts the invitation to hear the sail lecture. This is consent to listen, not recruitment or payment.',
    1: 'Lil casually declines the invitation to hear the sail lecture. Do not add dismissal, refusal to recruit or a payment consequence.',
}

if __name__ == '__main__':
    assert not ROOT.exists()
    source = read(SOURCE)
    rows,choices = deepcopy(source['block']['records']),deepcopy(source['typed_choice_records'])
    assert len(rows) == len(MEANINGS) == 27 and {r['source_record_index'] for r in rows} == set(MEANINGS)
    assert len(choices) == 2 and {r['option_index'] for r in choices} == {0,1}
    for row in rows:
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    for row in choices:
        row.update(fresh_source_gloss=CHOICE_MEANINGS[row['option_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'all29_complete_B167_exchange_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        whole_exchange_context=CONTEXT,records=rows,typed_choice_records=choices,all29_clean_first_glosses_before_predecessor_English=True,
        source_macro_counts=source['source_macro_counts'],sail_terminology_UI_binding_pending=True,
        source_five_actor_current_name_voice_bindings_pending=True,choice_refusal_and_acceptance_paths_require_native_confirmation=True,
        two_Cesare_membership_queries_and_source_entry_effect_end_binding_pending=True,
        source_native_fonts_actual_registered_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(source['source_transcript']),Path(__file__)]},full_goal_complete=False))
    print('B167:27 speech+two choice clean-first glosses recorded;all29 uncredited;predecessor English not yet exposed.')
