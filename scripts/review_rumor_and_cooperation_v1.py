"""Bind the false-letter, bribery, and rumor replies to their original exchanges."""

import struct
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.checkpoint_mutiny_review_v1 import arm_immediate, pointer_aliases
from scripts.checkpoint_sailing_alert_review_v1 import BASE, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_shark_encounter_v1 import RELEASE
from scripts.register_shared_notices_v1 import CONTEXT, LEDGER
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


OUTPUT = ROOT / 'rumor_and_cooperation_context_v1.json'
IDS = tuple(range(2770, 2814))
GROUPS = (
    (0x1169C0, 0x927D8, ((0x92654, 0x9265C),), (2770, 2771, 2772, 2773, -1, -1, -1, -1), ('town',),
        'The recipient reacts to a report of a new local product before deciding whether to send a fleet.'),
    (0x116A60, 0x927DC, ((0x92684, 0x9268C),), (2774, 2775, -1, 2776, -1, -1, -1, -1), ('town',),
        'The recipient reacts to a report of an enemy merchant fleet before deciding whether to send a fleet.'),
    (0x116AC0, 0x927E0, ((0x92724, 0x92728),), (2777, 2778, 2779, 2780, -1, -1, -1, -1), (),
        'The recipient orders a fleet sent in response to the report. The native result then names the destination.'),
    (0x116B20, 0x927EC, ((0x927B4, 0x927B8),), (2781, -1, 2782, 2783, -1, -1, -1, -1), (),
        'The recipient doubts the report and dismisses it instead of sending a fleet.'),
    (0x116F00, 0x92554, ((0x922E4, 0x922E8),), (2784, -1, 2785, 2786, -1, -1, -1, -1), ('faction',),
        'A false document presents a named faction’s supposed demand for submission. The recipient reacts before deciding if it is genuine.'),
    (0x117020, 0x92558, ((0x922FC, 0x92300),), (2787, -1, 2788, 2789, 2790, -1, -1, -1), (),
        'The recipient believes the supposed demand and rejects it angrily. The following system result changes relations.'),
    (0x117100, 0x92564, ((0x92358, 0x9235C),), (2791, 2792, 2793, 2794, 2795, -1, -1, -1), (),
        'The recipient identifies the false document and dismisses it. The same table is reused in a second forged-document branch.'),
    (0x117200, 0x92198, ((0x91F30, 0x91F34),), (2806, 2807, 2808, 2809, 2810, 2811, 2812, 2813), ('faction', 'town'),
        'The defending faction is the player’s. The game selects an available crew member to report that the rival’s rumor scheme was countered.'),
)
DIRECT = {
    2796: (0x91FD4, (0x921A0,), ('faction',), 'Local patron',
        'When the planted rumor takes hold, the town’s patron repeats the smuggling allegation about the named faction.'),
    2797: (0x91FD4, (0x9219C,), ('faction',), 'Local patron',
        'An alternate planted rumor claims the named faction is ruthless. The same patron can deliver it.'),
    2798: (0x92000, (0x921A4,), ('faction',), 'Town representative',
        'The native town representative follows the patron’s rumor with doubts about trading with the named faction.'),
    2799: (0x920B4, (0x921B0,), ('faction',), 'Local patron',
        'When the rumor fails to take hold, the patron dismisses the smuggling claim and the native result says the rumor was disregarded.'),
    2800: (0x920B4, (), ('faction',), 'Local patron',
        'When the rumor fails to take hold, the patron treats the ruthlessness accusation as hearsay.'),
    2801: (0x91ADC, (0x91D90,), ('gold amount', 'faction'), 'Trader',
        'The town trader can cut the named rival’s share for a fee even though the town is too crowded with trading partners to secure a share directly. The price comes first.'),
    2802: (0x91AF8, (0x91D94,), ('gold amount',), 'Trader',
        'The town trader names the fee on the cooperation path that has a share available. The system asks whether to pay.'),
    2803: (0x91CC8, (0x91DAC,), (), 'Trader',
        'The transaction stops without acceptance. The same original exit handles both insufficient funds and a declined payment.'),
    2804: (0x91B4C, (0x91D98,), (), 'Trader',
        'The player accepts the fee. The trader responds before the original charge and share change.'),
    2805: (0x91CE8, (0x91DB0,), (), 'Trader',
        'The original cooperation check fails. The trader refuses before the fee and payment prompt.'),
}
DATA = {
    2770: ('A new product in %s?', 'Asks if a new product has appeared in the named town.', 'Use an immediate reaction. The report is still unconfirmed.'),
    2771: ('%s has a new product?', 'Asks in surprise whether the named town has a new product.', 'Retain the direct question and the town substitution.'),
    2772: ("There's a new product in %s?", 'Repeats the report that the named town has a new product.', 'Retain the conversational question in this voice.'),
    2773: ('Huh? A new product in %s?', 'Expresses surprise and repeats the new-product report.', 'Retain the audible surprise and the short follow-up.'),
    2774: ('An enemy merchant fleet has appeared at %s?', 'Asks whether an enemy merchant fleet has appeared at the named town.', 'Put the report ahead of the location for natural English. Keep merchant fleet.'),
    2775: ('An enemy merchant fleet showed up at %s?', 'Asks if an enemy merchant fleet has shown up at the named town.', 'Use the more conversational verb in this voice.'),
    2776: ('Huh? An enemy merchant fleet at %s?', 'Expresses surprise at a report of an enemy merchant fleet at the named town.', 'Retain the short reaction. The preceding report supplies the situation.'),
    2777: ("Good. Let's send a fleet right away.", 'Approves and proposes sending a fleet immediately.', 'Retain the approval and the immediate action.'),
    2778: ('Send a fleet at once!', 'Orders that a fleet be sent immediately.', 'Retain the sharp order and its urgency.'),
    2779: ("Let's send a fleet right away!", 'Energetically proposes sending a fleet immediately.', 'Preserve the inclusive proposal and enthusiastic delivery.'),
    2780: ("Let's send a fleet at once.", 'Proposes sending a fleet without delay.', 'Use a natural contraction while retaining the measured delivery.'),
    2781: ('That sounds suspicious... Could be a false report. Ignore it.', 'Suspects the report could be false and tells the listener to disregard it.', 'Keep the uncertainty, pause, and order. Replace the old mismatched I.'),
    2782: ('Can we really trust that report...? Never mind. Just leave it alone.', 'Questions whether the report can be trusted and decides to leave it alone.', 'Retain the tentative question and understated dismissal.'),
    2783: ('Something sounds off... It must be a false report. Ignore it.', 'Finds the report suspicious, decides it must be false, and orders it ignored.', 'Keep the stronger certainty of this reaction.'),
    2784: ("They're demanding we submit to %s?!", 'Reacts in indignation to the supposed demand to come under the named faction’s authority.', 'Make the demand explicit without treating it as genuine.'),
    2785: ('They say we should submit to %s?!', 'Repeats the purported demand to submit to the named faction in disbelief.', 'Retain the conversational reaction and its surprised emphasis.'),
    2786: ('They expect us to submit to %s?!', 'Repeats the supposed demand in disbelief.', 'Use an incredulous question that keeps the named faction in the same role.'),
    2787: ("I tried being accommodating, and now they're pushing their luck!", 'The speaker says they dealt deferentially with the other side and that the other side is getting carried away.', 'Keep the indignation and the link between conciliatory behavior and perceived arrogance.'),
    2788: ('The nerve of them! Absolutely not!', 'Angrily rejects the supposed demand as outrageous.', 'Use a direct expression of outrage instead of sounding amused.'),
    2789: ('They must be joking!', 'Indignantly says the demand must be a joke.', 'Retain the concise disbelief as a forceful rejection.'),
    2790: ("Who do they think they are? I won't stand for this!", 'Angrily calls out the supposed affront and refuses to stand for it.', 'Retain both parts of the rebuke without asserting a specific act of mockery.'),
    2791: ('This is a forgery... Just ignore it.', 'Recognizes a forged document and advises ignoring it.', 'Retain the calm recognition and short dismissal.'),
    2792: ("It's a forgery. Pay it no mind.", 'Recognizes the forgery and says it can be disregarded.', 'Keep the firm dismissal and distinguish this voice from the uncertain one that follows.'),
    2793: ("I think... this is a forgery. Let's ignore it.", 'Suspects the letter is a forgery and proposes ignoring it.', 'Retain the deliberate hesitation and replace the mismatched I.'),
    2794: ("Heh... This is a forgery. Let's just ignore it.", 'Recognizes the forgery with a short laugh and suggests ignoring it.', 'Retain the knowing amusement and shared decision.'),
    2795: ("It's a forgery. Ignore it.", 'Recognizes the forged document and orders that it be ignored.', 'Keep the terse certainty and short instruction.'),
    2796: ('I hear %s is involved in smuggling.', 'The patron reports hearing that the named faction is involved in smuggling.', 'Retain the hearsay and precise allegation. Use the ordinary capital I.'),
    2797: ('They say %s is utterly ruthless.', 'The patron repeats a rumor that the named faction or its leader is heartless and cruel.', 'Retain the hearsay and a description that reads naturally with a faction name.'),
    2798: ('Hmm... Is %s really the kind of trading partner we want for our town?', 'The town representative questions whether the named faction is a suitable trading partner for the town.', 'Give the doubts a natural speaking rhythm. Leave the decision open.'),
    2799: ("%s, smuggling? That's got to be a lie.", 'The patron questions the smuggling allegation and dismisses it as a false rumor.', 'Make the disbelief and dismissal sound conversational.'),
    2800: ("%s, heartless? Well, it's only a rumor. Who knows if it's true?", 'The patron says the charge of heartlessness is hearsay and the truth is unknown.', 'Keep the difference from the more certain smuggling denial.'),
    2801: ("I can't get you a share with this many trading partners in town. For %s gold, I'll cut %s's share.",
        'The town has too many trading partners to secure a share for the player. For the supplied fee in gold, the trader offers to reduce the named rival’s share.',
        'Keep the failed direct request and the conditional counteroffer. Preserve the original fee-then-faction argument order.'),
    2802: ("You want my help? Well... I'll need %s gold to set it up.",
        'The trader asks about the requested cooperation and names the gold fee for making arrangements.',
        'Let the hesitation lead naturally into the fee. The later payment prompt still makes the decision.'),
    2803: ("You can't pay? Then the deal is off.", 'The trader asks if the player cannot pay and calls off the deal.', 'Retain the brusque withdrawal. The native caller supplies the result.'),
    2804: ('All right. Leave it to me.', 'The trader agrees and tells the player to leave it to them.', 'Retain the short acceptance before the actual charge.'),
    2805: ("You want my help? Sorry, but I can't do that.", 'The trader acknowledges the request and apologetically refuses.', 'Retain the direct refusal and replace the mismatched I.'),
    2806: ('%s tried to spread malicious rumors in %s, but we managed to stop them.',
        'The named faction attempted to spread bad rumors in the named town. The speaker says they managed to stop it.',
        'Retain the attempt and the measured description of stopping it.'),
    2807: ('%s was about to spread malicious rumors in %s. We stopped them in time.',
        'The named faction was trying to spread bad rumors in the named town. The speaker says the plan was stopped before it took effect.',
        'Preserve preemption and the formal voice.'),
    2808: ("Looks like %s tried to spread nasty rumors in %s. Don't worry. We've got it covered.",
        'It appears the faction tried to spread bad rumors in the town. The speaker reassures the player that the response is in hand.',
        'Use an easy spoken opening and keep both reassurance beats.'),
    2809: ("%s has been spreading nasty rumors in %s. Of course we aren't falling for that.",
        'The faction spread bad rumors in the town. The speaker says they will of course see through the trick.',
        'Keep the reported spreading and the confident dismissal distinct from an attempt intercepted in advance.'),
    2810: ("%s spread nasty rumors in %s. As if we'd fall for that trick!",
        'The faction spread bad rumors in the town. The speaker scoffs that such a trick could ever work.',
        'Retain the rougher voice and the scoffing reply.'),
    2811: ('Seems %s is spreading nasty rumors in %s. We know better than to fall for that.',
        'The faction appears to be spreading bad rumors in the town. The speaker says they will not fall for it.',
        'Keep the qualified opening and the seasoned, familiar reply.'),
    2812: ("Looks like %s is trying to spread nasty rumors in %s. Don't worry, Admiral. The townspeople are on your side!",
        'The faction appears to be trying to spread bad rumors in the town. The speaker reassures the admiral that the townspeople support them.',
        'Preserve the young speaker’s reassurance and the admiral address. Keep both original names and the townspeople’s support.'),
    2813: ('%s was trying to spread malicious rumors in %s, so we took precautions.',
        'The faction was trying to spread bad rumors in the town, so the speaker made arrangements in advance.',
        'Retain the formal report and the preventive action.'),
}
SPANS = ((0x91934, 0x919B8), (0x91A68, 0x91BEC), (0x91CB0, 0x91D0C),
         (0x91E98, 0x920D4), (0x92298, 0x92370), (0x92634, 0x927CC), (0x92A34, 0x92A44))


def original_groups(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = [(n, runtime.actor_root + (0x19E4 if n == 3 else 4 + 32 * n)) for n in range(207)]
    voices = {n: get(0x7E988, ptr) for n, ptr in roster}
    groups, rows = [], {}
    for table, literal, sites, slots, args, context in GROUPS:
        assert struct.unpack_from('<8i', clean, table) == struct.unpack_from('<8i', runtime.arm, table) == slots
        aliases = [literal, 0x92B70] if table == 0x117100 else [literal]
        assert pointer_aliases(clean, BASE + table) == pointer_aliases(runtime.arm, BASE + table) == aliases
        calls = [caller_binding(clean, runtime.arm, pc, call, literal, BASE + table, 0x53F0C) for pc, call in sites]
        if table == 0x117100:
            calls.append(caller_binding(clean, runtime.arm, 0x92A3C, 0x92A40, 0x92B70, BASE + table, 0x53F0C))
        matches = {}
        for actor, ptr in roster:
            voice = voices[actor]
            result = get(0x53F4C, ptr, BASE + table)
            assert result == (slots[voice] if slots[voice] != -1 else slots[0])
            matches.setdefault(result, []).append(actor)
        assert get(0x53F4C, 0, BASE + table) == slots[0] and set(matches) == set(slots) - {-1}
        speaker = 'Original defending crew member' if table == 0x117200 else 'Original recipient faction leader'
        groups.append(dict(table=BASE + table, table_slots=slots, original_actor_IDs_by_result=matches,
                           original_arguments=args, native_callers=calls, context=context))
        for voice, n in enumerate(slots):
            if n >= 0:
                rows[n] = dict(speaker=speaker, context=context, original_substitutions=args,
                    voice_slot=voice, original_table=BASE + table, representative_actor_ID=matches[n][0],
                    original_consumer=0x02053F0C, native_callers=calls)
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups, rows


def main():
    assert not OUTPUT.exists()
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    source = NdsImage.open(CLEAN)
    clean, arm = source.read_file(ARM), runtime.arm
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in SPANS)
    jp = common_message_entries(source.read_file(COMMON), clean)
    en = owned_entries(runtime.common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    groups, bindings = original_groups(runtime, clean)
    for n, (pc, literals, args, speaker, context) in DIRECT.items():
        assert branch_target(clean, pc) == 0x02053FE4
        assert all(word(clean, at) == word(arm, at) == n for at in literals)
        if n == 2800:
            assert arm_immediate(word(clean, 0x9207C)) == n
        bindings[n] = dict(speaker=speaker, context=context, original_substitutions=args, original_consumer=0x02053FE4,
            native_callers=[dict(call_PC=BASE + pc, literal_addresses=[BASE + at for at in literals],
                                 code_window_hex=clean[pc - 24:pc + 4].hex())])
    assert sorted(bindings) == list(IDS)
    ledger = load(LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(row['file_path'], row['id']) for row in ledger[CONTEXT]['integrated_record_keys']}

    def source_row(n):
        a, b = jp[n], en[n]
        return dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, message_ID=n, source_reference=reference(a),
            current_reference=reference(b), source_hex=a.text.hex(), current_hex=b.text.hex(),
            clean_Japanese=a.text.decode('cp932'), current_English=b.text.decode('cp932'))

    records = []
    for n, (english, meaning, note) in DATA.items():
        row = source_row(n) | bindings[n]
        assert (COMMON, row['id']) not in credited
        assert english.count('%s') == row['clean_Japanese'].count('%s') == len(row['original_substitutions'])
        old = ' '.join(row['current_English'].replace('Ｉ', 'I').split())
        records.append(row | dict(english=english, source_meaning=meaning, localization_note=note,
            decision='retention' if english == old else 'revision',
            current_wide_glyphs=wide_letters(row['current_English']),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert tuple(row['message_ID'] for row in records) == IDS
    neighbors = [source_row(n) for n in range(2757, 2770)]
    prior_results = [source_row(n) for n in range(369, 381)]
    assert all((COMMON, row['id']) in credited for row in prior_results)
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        registered_input=runtime.receipt(), original_portrait_tables=groups, adjacent_submission_context=neighbors,
        previously_credited_system_results=prior_results,
        exact_code_spans=[dict(start=BASE + lo, end=BASE + hi, clean_current_hex=clean[lo:hi].hex()) for lo, hi in SPANS],
        source_rom_sha256=release['clean_input_sha256'], new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, Path(__file__))}))
    print('Reviewed 44 source-bound false-letter, rumor, and cooperation records in their complete exchanges.')


if __name__ == '__main__':
    main()
