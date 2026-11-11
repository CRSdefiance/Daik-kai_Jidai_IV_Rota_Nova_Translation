"""Review the oasis, Proof, figurehead and white-whale conversations."""

from inspect import getsource
from struct import unpack_from

from dk4tool.patch.tavern_continuation_runtime import REGION, REGION_TABLE
from scripts import register_crew_and_shore_reports_v1 as parent
from scripts import review_crew_and_shore_reports_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


prior = previous.prior
BASE, ARM, COMMON, CLEAN = previous.BASE, previous.ARM, previous.COMMON, previous.CLEAN
OUTPUT = prior.ROOT / 'oasis_and_whale_reports_context_v1.json'
CAPTAIN, ROLE, DIRECT = previous.CAPTAIN, previous.ROLE, 0x53F0C
GROUPS = (
    (2288, 2293, 0x116D40, 0x79288, 0x79290, 0x7930C, ROLE, 1, None,
     'The First Mate or original fallback relays the apparent discovery of an oasis and urges the party to go. The next report resolves the sighting as an oasis or a mirage.'),
    (2294, 2300, 0x116D20, 0x792C4, 0x792CC, 0x79314, ROLE, 1, None,
     'The oasis is real. The officer reacts to their good fortune or relief. This branch leads into the original fatigue decrease.'),
    (2301, 2307, 0x116D00, 0x792DC, 0x792E4, 0x79318, ROLE, 1, None,
     'The apparent oasis disappears. The officer realizes or suspects it was a mirage, or simply reacts with disappointment. The report is followed by the original fatigue increase.'),
    (2308, 2314, 0x116A20, 0x79238, 0x79240, 0x79270, ROLE, 1, None,
     'The shore expedition appears trapped in a deep bog. The degree of certainty varies by speaker. Do not infer that they sank or died.'),
    (2315, 2322, 0x116CC0, 0x791A4, 0x791AC, 0x79218, ROLE, 1, None,
     'The officer announces a possible or definite find. The original Search branch handles the discovery after this preliminary report, so no object is named here.'),
    (2323, 2330, 0x116CA0, 0x79D28, 0x79D2C, 0x79FD0, ROLE, 7, 'proof',
     'The lookout or fallback identifies a Proof of Conqueror after the expedition’s discovery. The source supplies the region first and the paired item name second. Several voices are tentative or ask for confirmation.'),
    (2331, 2336, 0x116C80, 0x73968, 0x73970, 0x74064, DIRECT, None, 'figurehead',
     'A shark has bitten off the ship’s equipped figurehead. The ship-duty actor is selected by the original caller and the lost item supplies its full name. No crew member or vessel is the object of the bite.'),
    (2337, 2344, 0x116C60, 0x7A764, 0x7A76C, 0x7AE68, ROLE, 7, None,
     'The lookout recognizes the much-talked-about white whale and proposes defeating it. The crew cites reports of ships falling prey to it. Their accounts do not establish that every ship sank.'),
    (2345, 2351, 0x116C40, 0x7A8D0, 0x7A8D8, 0x7AE88, ROLE, 7, None,
     'When the original whale event continues and the player has not attacked, the lookout presses the admiral to act. The tone ranges from concern to anger.'),
    (2352, 2358, 0x116C20, 0x7A7D4, 0x7A7DC, 0x7AE70, ROLE, 7, None,
     'The whale escapes and the lookout notices a glint where it dived or in that direction. The original item presentation and the separately reviewed gentler reactions follow.'),
)

DECISIONS = {
    2288: (None, 'The expedition seems to have found an oasis and the officer suggests going.', 'Keep the natural invitation and the uncertainty.'),
    2289: (None, 'The officer reports an apparent oasis and urges haste.', 'Keep the measured report and prompt follow-up.'),
    2290: ('Admiral! The expedition found an oasis! Come on, hurry!', 'The officer announces the find to the admiral and urgently suggests going.', 'Use direct excited speech and the explicit discovery.'),
    2291: ("Looks like the expedition found an oasis! Come on, let's go!", 'The officer thinks the expedition found an oasis and urges them to go.', 'Keep the rough voice and use normal dialogue glyphs.'),
    2292: ('It seems the expedition found an oasis! Shall we go at once?', 'The officer reports the apparent find and suggests going right away.', 'Restore the uncertainty and the older voice’s invitation.'),
    2293: ("They say the expedition found an oasis! Let's hurry!", 'The officer relays the expedition’s find and wants to hurry.', 'Restore the hearsay and the finder.'),
    2294: (None, 'The officer marvels at finding an oasis here and calls it heaven-sent.', 'Keep the unexpected find, religious image and measured pause.'),
    2295: ("I didn't expect an oasis out here. What a relief...", 'The officer did not expect the oasis and is grateful.', 'Keep the restrained relief and standard-width opening I.'),
    2296: (None, 'The officer marvels at the oasis and says their group is lucky.', 'Keep the natural question and the collective “we” for IC plus tachi.'),
    2297: (None, 'The officer calls the unexpected oasis good luck for their group.', 'Keep the short, pleased response.'),
    2298: (None, 'The officer is surprised and exclaims to the admiral that they are lucky.', 'Keep the rough voice’s direct exclamation and address.'),
    2299: ("I never thought we'd find an oasis here. Ah, I feel like myself again!", 'The officer never expected the oasis and feels restored.', 'Use a natural expression for feeling renewed in this older voice.'),
    2300: ("An oasis, out here! This is great!", 'The officer is thrilled that there is an oasis here.', 'Keep the youthful excitement and normal glyphs.'),
    2301: ('Wait, the oasis is gone... Admiral, it was a mirage.', 'The officer notices it vanish and identifies it as a mirage.', 'Keep the moment of recognition and the direct address.'),
    2302: ('Ah, the oasis... It looks like it was a mirage, Admiral.', 'The officer trails off, then tells the admiral it appears to have been a mirage.', 'Restore the hesitation, uncertainty and address.'),
    2303: ('Oh, the oasis... It was just a mirage...', 'The officer is startled and realizes it was a mirage.', 'Let the second thought sound like a realization.'),
    2304: ('Oh, the oasis disappeared... What a shame. It was a mirage.', 'The officer notices it disappear and sighs at the realization.', 'Preserve the disappointment and the realization as distinct beats.'),
    2305: (None, 'The officer sees the oasis disappear and curses the mirage.', 'Keep the strong language and clipped delivery.'),
    2306: ('The oasis has vanished. Seems it was a mirage, Admiral.', 'The officer says it disappeared and judges it to have been a mirage.', 'Preserve the older voice’s qualified judgment.'),
    2307: ('Huh? The oasis is gone... What a letdown.', 'The officer is puzzled, then disappointed when the oasis disappears.', 'Restore the surprise before the letdown. This voice does not name a mirage.'),
    2308: ('It seems the expedition got stuck in a bottomless bog!', 'The officer thinks the party is stuck in a seemingly bottomless bog.', 'Preserve the uncertain report and the specific hazard.'),
    2309: ('The expedition appears to be stuck in a bottomless bog!', 'The officer reports that the party appears trapped in a bottomless bog.', 'Keep the formal uncertainty and the specific hazard.'),
    2310: ('Looks like our party got stuck in a bottomless bog!', 'The officer thinks the party got stuck in a bottomless bog.', 'Use conversational hearsay and the specific hazard.'),
    2311: ('Admiral, trouble! I hear the expedition is stuck in a bottomless bog!', 'The officer warns the admiral and relays news that the party is trapped in a bottomless bog.', 'Keep the explicit hearsay and the urgent address.'),
    2312: ('Admiral, this is bad! Sounds like our party got stuck in a bottomless bog!', 'The officer calls to the admiral and relays the apparent danger.', 'Keep the rough opening, the depth and normal English glyphs.'),
    2313: (None, 'The officer announces trouble and reports that the party seems stuck.', 'Keep the two beats and correct the mixed-width I.'),
    2314: ('Oh no! The expedition is stuck in a bottomless bog!', 'The officer cries out that the expedition is stuck.', 'Put the party first in the urgent report.'),
    2315: ('It looks like the expedition found something!', 'The officer reports an apparent find.', 'Restore uncertainty before the discovery is identified.'),
    2316: ('The expedition appears to have found something!', 'The officer announces a probable discovery.', 'Keep the brisk and somewhat formal voice.'),
    2317: (None, 'The officer exclaims that the expedition found something.', 'Keep the direct report for this certain voice.'),
    2318: ('Looks like the expedition found something!', 'The officer thinks the expedition found something.', 'Restore the natural qualification.'),
    2319: ('Sounds like our party found something!', 'The officer says it seems the expedition made a find.', 'Keep the rough voice conversational and the report provisional.'),
    2320: ('It seems the expedition turned up something!', 'The officer believes the expedition found something.', 'Restore the older voice’s measured uncertainty.'),
    2321: (None, 'The officer exclaims that the expedition found something.', 'Keep the complete, plain announcement.'),
    2322: ('It looks like the expedition has found something!', 'The officer announces that the party seems to have made a find.', 'Restore the courteous and tentative report.'),
    2323: ("Admiral! It's the Proof of Conqueror for %s. That's %s!", 'The lookout positively identifies the region’s proof and names it.', 'Preserve the official item category and the original argument order.'),
    2324: ('Admiral, look what the expedition found! Is this the Proof of Conqueror for %s? Could it be %s?', 'The lookout calls attention to the find and wonders whether it is the named proof.', 'Restore the finder and uncertainty in complete questions.'),
    2325: ('Admiral, did the expedition find the Proof of Conqueror for %s? Is that %s?', 'The lookout asks the admiral to confirm the expedition’s find.', 'Keep the curious voice and identify the two fields in order.'),
    2326: ("Admiral, the expedition brought this back! It's the Proof of Conqueror for %s. That's %s!", 'The lookout says the expedition found the named proof.', 'Keep the excited first beat and use normal glyphs in the identification.'),
    2327: ("Admiral, look what they found! That's the Proof of Conqueror for %s! Could it be %s?", 'The lookout excitedly proposes the proof’s identity and asks for confirmation.', 'Keep the rough and excited voice without a stranded tag.'),
    2328: ("Admiral, look what they found! It appears to be the Proof of Conqueror for %s. That would be %s.", 'The lookout points out the find and tentatively identifies it.', 'Restore the older voice’s inference and retain the complete item label.'),
    2329: ("Admiral, the expedition found this! Isn't this the Proof of Conqueror for %s? Is it %s?", 'The lookout eagerly asks whether the expedition found this region’s named proof.', 'Use full questions while keeping the youthful search for confirmation.'),
    2330: ("Admiral, the expedition found this. It looks like the Proof of Conqueror for %s. I believe it's %s.", 'The lookout reports the expedition’s discovery and makes a tentative identification.', 'Preserve the measured delivery and use normal glyphs in both clauses.'),
    2331: ('A shark bit off the %s!', 'The officer says a shark bit off the named figurehead.', 'Use the natural article with the exact equipped item name.'),
    2332: ('Looks like a shark bit off the %s!', 'The officer says it appears a shark bit the figurehead off.', 'Restore the source qualification and the exact item.'),
    2333: ('A shark bit our %s off!', 'The officer exclaims that a shark bit off the ship’s figurehead.', 'Keep the emphatic, familiar report.'),
    2334: ('Admiral, trouble! A shark bit off the %s!', 'The officer warns the admiral a shark bit off the figurehead.', 'Restore the precise damage and the original alarm.'),
    2335: ('A shark tore off the %s!', 'The officer exclaims that a shark tore off the figurehead with its teeth.', 'Preserve the rough emphasis without asserting it was torn into pieces.'),
    2336: ('A shark bit off our %s! What a glutton!', 'The officer reports the lost figurehead and calls the shark a glutton.', 'Keep the playful complaint after the damage report.'),
    2337: ("That's the white whale we've heard about! Countless ships have fallen prey to it. Let's take it down!", 'The lookout identifies the whale, mentions its many victims and proposes defeating it.', 'Restore the sighting and avoid asserting that all the ships sank.'),
    2338: ("So that's the white whale. It's preyed on countless ships. This is our chance to take it down!", 'The lookout recognizes the notorious whale and sees an opportunity to defeat it.', 'Restore the recognition and the opportunity.'),
    2339: ("The white whale! We've heard all about it. It's attacked a lot of ships! Let's take it down, Admiral!", 'The lookout names the famous whale and urges the admiral to fight.', 'Keep the excited voice and the threat without inventing losses.'),
    2340: ("That's the white whale we've heard about... I hear it's attacked a lot of ships. Let's take it down, Admiral!", 'The lookout recognizes the whale, relays reports of attacks and urges the admiral to defeat it.', 'Preserve the hearsay and the moment of recognition.'),
    2341: (None, 'The lookout recognizes the infamous whale, reports many attacks and proposes taking it down.', 'Keep the rough and conversational appeal with attributed attacks.'),
    2342: ("There's that white whale! They say countless ships have fallen prey to it. What say we take it down?", 'The lookout sights the reputed whale and suggests defeating it after recalling the stories.', 'Restore the older voice’s proposal and attributed report.'),
    2343: ("Wow, the white whale! It's famous! It's attacked lots of ships! Come on, let's beat it!", 'The lookout is excited to see the famous whale and wants to fight it.', 'Preserve the eager voice and ordinary English glyphs.'),
    2344: (None, 'The lookout recognizes the whale, relays its reputation and asks whether they should defeat it themselves.', 'Keep the more measured cadence, hearsay and proposal.'),
    2345: ('Admiral, what are you doing? Attack now!', 'The lookout rebukes the admiral for delaying and urges an immediate attack.', 'Restore the rebuke before the order.'),
    2346: (None, 'The lookout asks what is wrong and urges an attack.', 'Keep the startled question and imperative.'),
    2347: ("Admiral, what's the matter? Please attack, now!", 'The lookout asks the admiral what has happened and urgently asks them to attack.', 'Restore the question and respectful urgency.'),
    2348: (None, 'The lookout tells the admiral to stop stalling and attack.', 'Keep the sharp tone and clipped command.'),
    2349: (None, 'The lookout complains that the admiral is dawdling and urges an attack.', 'Keep the older voice’s irritated rebuke.'),
    2350: ("Admiral, we can't just wait! Hurry up and attack!", 'The lookout tells the admiral not to dawdle and urgently asks for an attack.', 'Restore the warning and the youthful urgency.'),
    2351: (None, 'The lookout asks the admiral what is wrong and urges an immediate attack.', 'Keep the complete question and clear order.'),
    2352: ("The white whale's getting away... Hm? Something's shining where it dived!", 'The lookout sees the whale escaping and then notices something shining where it dived.', 'Keep the continuous escape phrase and the puzzled turn toward the glint.'),
    2353: (None, 'The lookout watches the whale get away and is startled by a gleam at its diving spot.', 'Keep the sudden question and the precise location.'),
    2354: (None, 'The lookout is disappointed the whale escaped and then points out a glint over there.', 'Keep the disappointment and the informal discovery.'),
    2355: (None, 'The lookout regrets the escape and notices something shining at the whale’s diving spot.', 'Keep the two natural reactions and exact location.'),
    2356: (None, 'The lookout reacts to the escape and sees something shining where the whale dived.', 'Keep the conversational surprise and the visible glint.'),
    2357: ("Hm, looks like the white whale escaped... Wait! Something's shining where it dove!", 'The lookout thinks the whale escaped, then calls attention to a gleam where it dived.', 'Restore the qualified observation and older voice’s sudden discovery.'),
    2358: ("Aw, the white whale got away... Huh? Something's glowing where it dove!", 'The lookout is disappointed the white whale escaped and then spots a glow where it dived.', 'Restore the explicit whale and retain the youthful turn to surprise.'),
}


def arguments(runtime, source):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    assert source[0x945B4:0x945DC] == runtime.arm[0x945B4:0x945DC]
    assert source[0x79CF4:0x79D34] == runtime.arm[0x79CF4:0x79D34]
    assert source[0x55D0C:0x55DB8] == runtime.arm[0x55D0C:0x55DB8]

    def word(at):
        return unpack_from('<I', cpu.mem_read(at, 4))[0]

    def text(at):
        return bytes(cpu.mem_read(at, 64)).split(b'\0', 1)[0]

    root = get(0xCB190) + 4

    def name(index):
        obj = root + 20 * index
        getter = word(word(obj) + 8)
        value = text(get(getter - BASE, obj))
        assert value and value.isascii()
        return obj, getter, value

    full_labels = (b'the North Sea', b'the Mediterranean', b'Africa', b'the Indian Ocean',
                   b'Southeast Asia', b'East Asia', b'the New World')
    proofs = []
    for index, label in enumerate(full_labels):
        obj, getter, item = name(148 + index)
        assert get(0x4A448, obj) == 8 and get(0x4A3F0, obj) == index
        current = text(word(get(0x945B4, index)))
        region_object = get(REGION - BASE, index)
        assert region_object == REGION_TABLE + index * 4
        assert text(word(region_object)) == label
        proofs.append(dict(item_ID=148 + index, item_name_getter=getter, original_region_ID=index,
            original_region_display=current.decode('cp932'), dialogue_region_provider=REGION,
            dialogue_region_pointer=word(region_object), arguments=[label.hex(), item.hex()]))
    figures = []
    for index in range(114, 124):
        obj, getter, item = name(index)
        assert get(0x4A448, obj) == 5
        figures.append(dict(item_ID=index, name_getter=getter, arguments=[item.hex()]))
    runtime.calls.clear()
    return dict(proof=proofs, figurehead=figures)


def main():
    source = checked_text(getsource(previous.main), {
        'wrapper, role, context in GROUPS': 'wrapper, role, kind, context in GROUPS',
        '    groups, records = [], []': '    groups, records = [], []\n    samples = arguments(runtime, arm)',
        'argument_kind=None': 'argument_kind=kind',
        "assert b'%' not in jp.text and b'%' not in old.text and '%' not in english":
            "substitutions = 2 if kind == 'proof' else int(kind is not None)\n"
            "            assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == substitutions\n"
            "            assert '%' not in english.replace('%s', '')",
        "speaker='Storyline captain' if role is None": "speaker='Original ship-duty officer' if role is None",
        'original_substitution_count=0': "original_substitution_count=substitutions, source_collective_IC=b'IC' in jp.text",
        'len(records) == 56': 'len(records) == 71',
        '[*range(2217, 2222), *range(2229, 2234), 312]': '[*range(2359, 2366), *range(2462, 2469)]',
        'initialized_argument_samples={}': 'initialized_argument_samples=samples',
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::oasis-and-whale-source-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
