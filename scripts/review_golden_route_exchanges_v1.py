"""Review and bind the original Golden Route discovery, report and reward exchange."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import prepare_common_golden_route_manuscript as historical
from scripts import register_sailing_hazards_and_dolphins_v1 as parent
from scripts import review_sailing_hazards_and_dolphins_v1 as previous


prior = previous.prior
BASE, ARM, COMMON, CLEAN = previous.BASE, previous.ARM, previous.COMMON, previous.CLEAN
OUTPUT = prior.ROOT / 'golden_route_exchanges_context_v1.json'
CAPTAIN, ROLE, ACTOR, MODAL = previous.CAPTAIN, previous.ROLE, 0x53FE4, 0x546B8
CAPTAINS = ('Rafael', 'Hodram', 'Lil', 'Maria')
GROUPS = (
    (3320, 3327, 0x1172E0, 0xDB02C, 0xDB078, 0xDB120, ROLE, 1, 'good',
     'The First Mate or fallback notices a large profit on the named trade good. This is the first route in the native pending-discovery queue. They suggest, or predict confidently, that it qualifies.'),
    (3328, 3331, 0x116690, 0xDB030, 0xDB080, 0xDB124, CAPTAIN, None, None,
     'The captain reacts to the name Golden Route, opening the way for the First Mate to explain.'),
    (3332, 3339, 0x1178A0, 0xDB084, 0xDB08C, 0xDB128, ROLE, 1, None,
     'The First Mate tells the captain what they have heard about the guild looking for profitable trade routes.'),
    (3340, 3347, 0x117C20, 0xDB090, 0xDB098, 0xDB12C, ROLE, 1, None,
     'The same officer continues with the Golden Route definition and what the guild reportedly pays to an informant. The actual payment terms come later at the guild.'),
    (3348, 3351, 0x116580, 0xDB09C, 0xDB0A0, 0xDB130, CAPTAIN, None, None,
     'The captain reacts with admiration to the reward and explanation.'),
    (3352, 3359, 0x1189E0, 0xDB0A4, 0xDB0AC, 0xDB134, ROLE, 1, None,
     'The First Mate proposes reporting the discovery as soon as they reach the next port that has a guild.'),
    (3360, 3363, 0x116600, 0xDB0B0, 0xDB0B4, 0xDB138, CAPTAIN, None, None,
     'The captain agrees to report the discovery.'),
    (3364, 3367, 0x116540, 0xDB0E0, 0xDB0E4, 0xDB13C, CAPTAIN, None, 'good',
     'For another pending discovery, the captain observes a large profit on this good as well and asks whether it qualifies. The good can differ from the earlier discovery.'),
    (3368, 3375, 0x116B40, 0xDB0E8, 0xDB0F0, 0xDB140, ROLE, 1, None,
     'The First Mate agrees and predicts that the guild will recognize this additional route, with certainty varying by voice.'),
    (3376, 3379, 0x116450, 0xDB0F4, 0xDB0F8, 0xDB144, CAPTAIN, None, None,
     'The captain proposes reporting the additional route promptly at the next port with a guild.'),
    (3380, 3380, None, 0xDAE84, 0xDAE8C, 0xDAFD4, ACTOR, None, None,
     'The guild representative is surprised that the captain found one Golden Route and asks whether it is true.'),
    (3381, 3384, 0x1167D0, 0xDAEF4, 0xDAEFC, 0xDAFE0, CAPTAIN, None, 'town_good',
     'The captain explains the profitable deal. The original getter supplies the purchase town first, then the good bought there.'),
    (3385, 3385, None, 0xDAF2C, 0xDAF34, 0xDAFE4, ACTOR, None, 'good_amount',
     'The guild representative promises gold in the named good’s arrival months for two years. The original caller supplies the good name and the recorded profit in that order.'),
    (3386, 3386, None, 0xDAF3C, 0xDAF44, 0xDAFE8, ACTOR, None, None,
     'The guild representative is surprised to hear that the captain discovered several Golden Routes.'),
    (3387, 3390, 0x1167F0, 0xDAFAC, 0xDAFB4, 0xDAFEC, CAPTAIN, None, 'town_good',
     'The captain presents a written report of lucrative deals. The two arguments are one example, with the purchase town before its trade good.'),
    (3391, 3391, None, 0xDAFBC, 0xDAFC0, 0xDAFF0, ACTOR, None, None,
     'The guild representative accepts the report and offers a generous reward for two years. In the month each good comes in, its own recorded profit sets the amount.'),
    (3392, 3392, None, 0xDADB8, 0xDADBC, None, MODAL, None, 'amount',
     'The system notification follows collection. The original monthly code totals the qualifying reported route profits and uses the amount as the only substitution.'),
)
ARGUMENT_COUNTS = {None: 0, 'good': 1, 'town_good': 2, 'good_amount': 2, 'amount': 1}

# A missing replacement keeps the working logical paragraph, with the individual reason.
DECISIONS = {
    3320: (None, 'Keep the clear statement of profit and the tentative question.'),
    3321: (None, 'Keep the short observation and restrained prediction.'),
    3322: ("We made a good profit on %s! I'm sure this will count as a Golden Route!", 'Restore the excited certainty and make the trading good the object of the profit.'),
    3323: ("We did well on %s this time. Do you think this could be a Golden Route?", 'Use a conversational question and keep the result provisional.'),
    3324: (None, 'Keep the emphatic profit and direct question for this voice.'),
    3325: ("We made a handsome profit on %s this time. Hmm... This may be a Golden Route.", 'Keep the older voice’s pause and treat qualification as possible.'),
    3326: ("Look how much we made on %s! This has to be a Golden Route!", 'Keep the younger voice enthusiastic and confident.'),
    3327: (None, 'Keep the complete profit report and the courteous suggestion.'),
    3328: (None, 'Keep the captain’s quick echo of the unfamiliar term.'),
    3329: (None, 'Keep the captain’s more pointed echo.'),
    3330: (None, 'Keep the direct request for an explanation.'),
    3331: (None, 'Keep the direct question that leads into the explanation.'),
    3332: (None, 'Keep the natural hearsay and what the guild wants.'),
    3333: ("Apparently, the guild is looking for profitable trade routes.", 'Keep the qualified report in the measured voice.'),
    3334: ("I hear the guild's looking for tips on profitable trade routes.", 'Use a spoken contraction and preserve that the guild wants information.'),
    3335: (None, 'Keep the quieter hearsay and the guild’s interest in lucrative routes.'),
    3336: (None, 'Keep the rough voice’s “Word is” and the specific request.'),
    3337: ("I'm told the guild is looking for information on profitable trade routes.", 'Give the older voice a measured report that still attributes the information.'),
    3338: (None, 'Keep the youthful excitement and the report rather than a claim of direct knowledge.'),
    3339: ("From what I hear, the guild is looking for information on profitable trade routes.", 'Keep the careful introduction and the original hearsay.'),
    3340: ("They call routes that could bring in a lot of money Golden Routes. I hear they pay well for a tip.", 'Keep the potential for a large profit and the reported reward in spoken English.'),
    3341: ("They call routes with high potential profit margins Golden Routes. I hear they pay well for that information.", 'Keep the distinct reference to a profit margin and the reported reward.'),
    3342: ("They call routes that could make a lot of money Golden Routes. Tell the guild about one and, from what I hear, you get a big reward.", 'Keep the conversational explanation and qualify the reward as hearsay.'),
    3343: ("They call promising trade routes Golden Routes. I hear anyone who reports one gets a big reward.", 'Make the spoken explanation flow into the reported reward.'),
    3344: ("If a trade route looks like it'll bring in a fortune, they call it a Golden Route. Word is, they pay a hefty reward for a tip.", 'Keep the rough voice and the prospect of especially large profits.'),
    3345: ("They call the most promising trade routes Golden Routes. I hear the guild pays a handsome sum to anyone who tells them about one.", 'Keep the older voice and the reward attributed to what they have heard.'),
    3346: ("They call them Golden Routes. I hear the guild will pay a big reward if you tell them about a trade route that could make a lot of money.", 'Lead with the term and keep the younger voice’s account of the rumor.'),
    3347: ("I'm told the guild calls especially promising trade routes Golden Routes. They say there's a substantial reward for reporting one.", 'Keep the more formal account and both hearsay qualifications.'),
    3348: (None, 'Keep the captain’s quick, impressed reaction.'),
    3349: (None, 'Keep the captain’s restrained admiration.'),
    3350: (None, 'Keep the brief, enthusiastic reaction.'),
    3351: (None, 'Keep the short impressed response in the parallel captain slot.'),
    3352: ("Let's report it as soon as we reach a port with a guild.", 'Keep the urgency and the requirement to find a guild.'),
    3353: ("Next port with a guild, let's tell them right away.", 'Keep the short spoken proposal and the immediate timing.'),
    3354: ("We've got to tell them as soon as we reach a port with a guild.", 'Keep this voice’s eagerness and the guild-port condition.'),
    3355: ("We should tell them the moment we reach a port with a guild.", 'Keep the urge to tell the guild promptly in a conversational voice.'),
    3356: ("Soon as we reach a port with a guild, let's tell them!", 'Keep the informal voice and urgency in the two clauses.'),
    3357: ("We'd best tell them as soon as we reach a port with a guild.", 'Keep the older voice’s sense of duty and the guild condition.'),
    3358: ("Let's tell them the minute we reach a port with a guild!", 'Keep the eager offer and immediate timing.'),
    3359: ("Let's make sure to tell them as soon as we reach a port with a guild.", 'Keep the polite proposal and the practical guild condition.'),
    3360: (None, 'Keep the easy agreement to report the discovery.'),
    3361: (None, 'Keep the captain’s decisive assent.'),
    3362: ("Sure, I'll do that.", 'Keep the captain speaking for herself while making the assent natural.'),
    3363: (None, 'Keep the polite collective agreement.'),
    3364: ("We made a good profit on %s, too. Could this be another Golden Route?", 'Keep the additional discovery without implying a repeat sale of the same good.'),
    3365: (None, 'Keep the profitable trade and the question about another Golden Route.'),
    3366: ("We made quite a profit on %s, too. Think this is another Golden Route?", 'Keep the added good and use the captain’s brisk question.'),
    3367: ("We did quite well on %s, too. I wonder if this is another Golden Route.", 'Keep the reflective question and the reference to an additional trade.'),
    3368: ("I think the guild will recognize this one, too.", 'Make the reply refer clearly to the additional route.'),
    3369: (None, 'Keep the calm agreement and the probabilistic prediction.'),
    3370: ("Yes. I'm sure the guild will recognize this one, too.", 'Keep the confident prediction about this additional route.'),
    3371: (None, 'Keep the confident reply, with the guild’s approval still in the future.'),
    3372: ("Yeah, I think the guild will go for this one, too.", 'Keep the rough voice and tentative prediction.'),
    3373: (None, 'Keep the older voice’s formal assent and measured prediction.'),
    3374: (None, 'Keep the enthusiasm and confident expectation.'),
    3375: ("Yes, I'm sure the guild will recognize this one, too.", 'Keep the polite confidence and the reference to the additional route.'),
    3376: ("Then let's report it as soon as we reach a port with a guild.", 'Keep the conclusion and the first opportunity to report it.'),
    3377: (None, 'Keep the decisive agreement and next guild-port condition.'),
    3378: ("Then let's report it the moment we reach a port with a guild.", 'Keep the proposal and immediate timing in a direct sentence.'),
    3379: ("Then let's tell the guild as soon as we reach a port that has one.", 'Name the recipient and preserve the condition on where to report.'),
    3380: ("You found a Golden Route? Is that true?", 'Use a spoken double take while the guild representative waits for details.'),
    3381: ("If you buy in %s, you can make a fortune selling %s.", 'Keep the spoken cause and effect and the original town-then-good order.'),
    3382: ("Buy it in %s, and you'll turn a huge profit selling %s!", 'Give the explanation a forceful delivery and preserve both inputs.'),
    3383: ("Buy it in %s and you can make a fortune selling %s.", 'Make the trade recommendation direct while retaining both parts of the deal.'),
    3384: ("If you buy in %s, you'll make quite a profit when you sell %s.", 'Use the measured voice’s conditional and both original substitutions.'),
    3385: ("All right. For two years, in the months when %s comes in, I'll pay you %s gold as a reward.", 'Keep the assent, exact amount, arrival-month condition and two-year duration.'),
    3386: ("You found several Golden Routes? That's remarkable!", 'Preserve the plural discovery and natural surprise.'),
    3387: ("I've written up the trades that could make us a fortune. One example from %s is %s.", 'Keep the written report, large potential profits, and one named example.'),
    3388: ("I've written up the profitable deals, starting with a purchase in %s: %s.", 'Keep the report and the first example with the original argument order.'),
    3389: ("I've put together a report on the most profitable deals. Take %s, for example. We bought %s there.", 'Use the conversational voice and give the town and good as one example from the report.'),
    3390: ("I've written up some very profitable deals. One example is a purchase in %s, where we bought %s.", 'Keep the written summary and specify that the town is where the good was bought.'),
    3391: ("So this is your report! I'll pay well. For two years, each month a good comes in, I'll match its profit in gold.", 'Keep the written report acknowledgment and the full payment rule for each good.'),
    3392: ("The guild paid you %s gold for discovering a Golden Route.", 'Put the amount and source of the system payment into a direct notice.'),
}


def arguments(runtime):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)

    def word(address):
        return unpack_from('<I', cpu.mem_read(address, 4))[0]

    def text(address):
        return bytes(cpu.mem_read(address, 80)).split(b'\0', 1)[0]

    def names(root_getter, stride, count):
        root = get(root_getter) + 4
        entries = []
        for index in range(count):
            actor = root + stride * index
            getter = word(word(actor) + 8)
            name = text(get(getter - BASE, actor))
            assert name and name.isascii()
            entries.append(dict(index=index, original_getter=getter, display=name.decode('ascii'), hex=name.hex()))
        return entries

    goods, towns = names(0xCB124, 16, 77), names(0xCB178, 108, 90)
    amounts = []
    for value in (1, 57, 1000, 99999, 99999999, 2147483647):
        raw = text(get(0xABF50, value))
        assert normalize('NFKC', raw.decode('cp932')) == str(value)
        amounts.append(dict(value=value, original_hex=raw.hex(), ASCII_hex=str(value).encode().hex()))
    assert max(map(lambda item: len(item['display']), goods)) == max(map(lambda item: len(item['display']), towns)) == 13
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return dict(goods=goods, towns=towns, gold=amounts)


def main():
    assert not OUTPUT.exists()
    release = prior.load(parent.RELEASE)
    assert parent.base.digest(parent.base.REGISTRY) == release['registry_sha256']
    assert prior.digest(CLEAN) == release['clean_input_sha256']
    runtime = prior.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    image = parent.base.NdsImage.open(CLEAN)
    clean = image.read_file(ARM)
    source = common_message_entries(image.read_file(COMMON), clean)
    current = owned_entries(runtime.common, runtime.arm, sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    assert set(DECISIONS) == set(range(3320, 3393)) == set(historical.TEXT)
    ledger = prior.load(parent.base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {row['id'] for row in ledger[parent.base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert not credited.intersection(f'COMMON_MESSAGE_{n}' for n in DECISIONS)
    argument_samples = arguments(runtime)
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in actors.items()}
    groups, records = [], []
    for first, last, table, load, call, pool, consumer, role, kind, context in GROUPS:
        if pool is None:
            assert consumer == MODAL and first == last == 3392
            assert clean[load:call + 4].hex() == '350da0e33de6fdeb'
            assert clean[load:call + 4] == runtime.arm[load:call + 4]
            binding = dict(load_PC=BASE + load, call_PC=BASE + call, literal_value=first,
                           consumer=BASE + consumer, clean_and_current_hex=clean[load:call + 4].hex())
        else:
            binding = prior.caller_binding(clean, runtime.arm, load, call, pool, BASE + table if table else first, consumer)
        slots, selected = (first,), []
        if table is not None:
            count = 4 if consumer == CAPTAIN else 8
            assert clean[table:table + count * 4] == runtime.arm[table:table + count * 4]
            slots = unpack_from(f'<{count}i', clean, table)
            assert slots == tuple(range(first, last + 1))
            if consumer == CAPTAIN:
                selected = [(index, None, number) for index, number in enumerate(slots)]
            else:
                selected = [(i, voices[i], get(0x53F4C, actor, BASE + table)) for i, actor in actors.items()]
                assert all(number == slots[voice] for _, voice, number in selected)
        groups.append(dict(first_ID=first, last_ID=last, table=BASE + table if table else None, slots=slots,
            native_callers=[binding], original_voice_choices=selected, original_role_argument=role,
            argument_kind=kind, context=context))
        for number in range(first, last + 1):
            jp, old = source[number], current[number]
            text = old.text.decode('cp932')
            paragraph = ' '.join(normalize('NFKC', text).split())
            revision, reason = DECISIONS[number]
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split())
            assert (english != paragraph) == bool(revision), number
            count = ARGUMENT_COUNTS[kind]
            assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == count
            assert '%' not in english.replace('%s', '')
            speaker = {ROLE: 'First Mate or original fallback', ACTOR: 'Guild representative', MODAL: 'System notice'}
            records.append(dict(id=f'COMMON_MESSAGE_{number}', message_ID=number, file_path=COMMON,
                source_reference=prior.reference(jp), current_reference=prior.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=text, english=english, context=context, native_group_first_ID=first,
                original_slots=[i for i, selected_number in enumerate(slots) if number == selected_number],
                speaker=CAPTAINS[slots.index(number)] if consumer == CAPTAIN else speaker[consumer],
                source_meaning=historical.TEXT[number][1], localization_note=reason,
                decision='revision' if revision else 'retention', inherited_fullwidth_Latin=prior.wide_letters(text),
                original_substitution_count=count, review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert len(records) == 73 and len(groups) == 17
    counts = Counter(row['decision'] for row in records)
    prior.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=prior.GATES, records=records,
        registered_input=runtime.receipt(), source_ROM_sha256=release['clean_input_sha256'],
        native_context=groups, initialized_argument_samples=argument_samples,
        original_offline_actor_selections=sum(len(group['original_voice_choices']) for group in groups),
        counts=dict(counts), formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} decisions {dict(counts)} across {len(groups)} original call groups.')


if __name__ == '__main__':
    main()
