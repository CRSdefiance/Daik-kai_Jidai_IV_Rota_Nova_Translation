"""Review the original ram, town attack, defeat and special-target messages."""

from inspect import getsource
from struct import unpack_from

from scripts import register_pirate_and_retreat_reports_v1 as parent
from scripts import review_city_combat_notices_v1 as city
from scripts import review_fleet_reports_v1 as fleet
from scripts.source_locked_derivation_v5118 import checked_text


prior = city.prior
BASE, ARM, COMMON, CLEAN = city.BASE, city.ARM, city.COMMON, city.CLEAN
OUTPUT = prior.ROOT / 'battle_commands_and_outcomes_context_v1.json'
DIRECT, MODAL, QUEUED = 0x53F0C, 0x53CB0, 0x53D44
MODELS = (
    (149, '化魚', '化魚', 'Monster Fish'),
    (150, '大イカ', '大イカ', 'Giant Squid'),
    (151, 'サメ', 'サメ', 'Shark'),
    (152, '白鯨', '白鯨', 'White Whale'),
    (153, '幽霊船', 'Ghost', 'Ghost Ship'),
)
GROUPS = (
    (2106, 2113, 0x117CA0, 0x733BC, 0x733E8, 0x733EC, 0x734EC, DIRECT, None,
     'The ramming maneuver has hit an enemy ship. The short reactions are alternatives for the native selected actor. '
     'Only the rough alternative specifies the side of the enemy ship. The hit does not establish a sinking.'),
    (2122, 2129, 0x117D20, 0x6ED54, 0x6ED78, 0x6ED80, 0x6EE88, MODAL, 'town',
     'The original First Mate or fallback asks for permission to attack the selected town. The displayed name comes '
     'from the town object. The original confirmation allows the player to proceed or cancel; the attack is still pending.'),
    (2179, 2186, 0x1182E0, 0x71874, 0x718C8, 0x718D0, 0x71964, QUEUED, 'company',
     'The original battle-result branch reports the named faction’s flagship was lost in combat and says our side lost. '
     'The original role-1 selection preserves voice. Only voice 1 explicitly reports that the flagship sank.'),
    (2187, 2191, 0x1183C0, 0x71D74, 0x71DB4, 0x71DBC, 0x71F04, QUEUED, 'special',
     'The original special-target result gets the vessel or creature name through virtual slot 4 on the mobile '
     'attached to the fixed encounter fleet. These are victory announcements followed by the native result flow.'),
)
DECISIONS = {
    2106: ('The ram hit the enemy ship!', 'A crew member reports the ram hit the enemy ship.', 'Add the article for natural speech.'),
    2107: ('Ram hit the enemy ship.', 'A clipped confirmation of the hit on the enemy ship.', 'Keep the terse report and restore the stated target.'),
    2108: (None, 'The speaker says their ram hit the enemy ship.', 'Keep the immediate, conversational report.'),
    2109: (None, 'The speaker exclaims that their ram hit the enemy ship.', 'Keep the clear, emphatic report with “struck.”'),
    2110: (None, 'The speaker exclaims that the ram struck the enemy ship squarely in the side.', 'Keep the only stated impact location and rough emphasis.'),
    2111: ('We rammed the enemy ship!', 'The speaker confirms their ram hit the enemy ship.', 'Use an idiomatic active exclamation.'),
    2112: ('We hit the enemy ship with the ram!', 'The speaker excitedly announces the hit.', 'Keep the uncomplicated excitement and the explicit ram.'),
    2113: (None, 'The speaker emphatically reports the ram strike.', 'Keep the measured voice and exact target.'),
    2122: (None, 'The speaker politely asks whether to attack the named town.', 'Keep the complete, natural confirmation question.'),
    2123: ('Attack %s?', 'The speaker names the attack target and asks for confirmation.', 'Keep the clipped confirmation in a single question.'),
    2124: ('Should we attack %s?', 'The speaker casually checks whether to attack the town.', 'Use a full conversational question in place of a tag.'),
    2125: ('Do you want us to attack %s?', 'The speaker asks if the player agrees to attack the town.', 'Keep the courteous request for consent together.'),
    2126: ('Are we going after %s?', 'The speaker bluntly asks for assent to the town attack.', 'Use the familiar, direct phrasing of this voice.'),
    2127: ('Are we to attack %s?', 'The speaker asks for confirmation of the town attack.', 'Keep the older voice’s measured formality in one question.'),
    2128: ("So we're attacking %s?", 'The speaker informally checks that they should attack the town.', 'Keep the familiar confirmation without an isolated tag.'),
    2129: (None, 'The speaker courteously asks permission to attack the town.', 'Keep the existing full question and polite cadence.'),
    2179: (None, 'The speaker reports the named faction’s flagship was defeated and their side lost.', 'Keep the formal announcement and its result.'),
    2180: (None, 'The speaker reports the named flagship actually sank and their side lost.', 'Keep “sunk” because this voice explicitly says it.'),
    2181: ("They took out %s's flagship! We lost!", 'The speaker says the named flagship was defeated and their side lost.', 'Use active battle speech and preserve the collective first person.'),
    2182: ("They got %s's flagship. We've lost!", 'The speaker laments the named flagship’s defeat and their side’s loss.', 'Use a dismayed first beat before the outcome.'),
    2183: ("They got %s's flagship! We lost the fight!", 'The speaker says the flagship was beaten and their side lost.', 'Keep the rough and direct admission.'),
    2184: ("Looks like %s's flagship is out of action. We've lost!", 'The speaker says it appears the named flagship was knocked out and their side lost.', 'Restore the tentative observation without implying a sinking.'),
    2185: ("They got %s's flagship! We lost!", 'The speaker blurts out that the flagship was beaten and their side lost.', 'Keep the young voice’s short, disappointed delivery.'),
    2186: ("%s's flagship is out of action. We've lost!", 'The speaker formally reports the flagship was defeated and their side lost.', 'Use a measured report without inventing a sinking.'),
    2187: (None, 'The speaker announces that they defeated the named target.', 'Keep the complete victory call and its original target name field.'),
    2188: (None, 'The speaker gives a terse report that the target was defeated.', '“Down” works as a clipped battle call and does not specify a sinking.'),
    2189: (None, 'The speaker announces that the named target was defeated.', 'Keep the short victory call matching the compact Japanese.'),
    2190: (None, 'The speaker announces that the named target was defeated.', 'Keep the shared brisk wording for the identical Japanese report.'),
    2191: (None, 'The speaker exclaims that they defeated the named target.', 'Keep the plain and enthusiastic victory report.'),
}


def argument_samples(runtime, source):
    towns = city.argument_samples(runtime, source)['town']
    companies = fleet.argument_samples(runtime, source)['company']
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    models = get(0xCB148) + 4
    fields = []
    for index, japanese, inherited, english in MODELS:
        obj = models + index * 140
        getter = unpack_from('<I', cpu.mem_read(unpack_from('<I', cpu.mem_read(obj, 4))[0] + 4, 4))[0]
        pointer = get(getter - BASE, obj)
        field = 0x11E134 + 44 * (index - MODELS[0][0])
        rom_pointer = unpack_from('<I', source, field)[0]
        assert rom_pointer == unpack_from('<I', runtime.arm, field)[0]
        clean = japanese.encode('cp932') + b'\0'
        current = inherited.encode('cp932') + b'\0'
        assert source[rom_pointer - BASE:rom_pointer - BASE + len(clean)] == clean
        assert runtime.arm[rom_pointer - BASE:rom_pointer - BASE + len(current)] == current
        assert getter == 0x0201A4E0 and pointer == obj + 8
        assert bytes(cpu.mem_read(pointer, len(current))) == current
        fields.append(dict(model_ID=index, source_pointer=rom_pointer, pointer_field=BASE + field,
            model_name_getter=getter, model_name_address=pointer, source_Japanese=japanese,
            source_hex=clean[:-1].hex(), current_English=inherited, current_hex=current[:-1].hex(),
            english=english, arguments=[english.encode('ascii').hex()]))
    runtime.calls.clear()
    return dict(town=towns, company=companies, special=fields)


def main():
    source = checked_text(getsource(city.main), {
        'set(range(2580, 2615))': 'set(SELECTED)',
        'prefix, load, call, pool, kind, context': 'prefix, load, call, pool, wrapper, kind, context',
        'BASE + table, DIRECT)': 'BASE + table, wrapper)',
        'original_role_argument=None': 'original_role_argument=1 if wrapper != DIRECT else None',
        '== english.count(\'%s\') == 1': "== english.count('%s') == int(kind is not None)",
        'original_substitution_count=1': "original_substitution_count=int(kind is not None), source_collective_IC=b'IC' in jp.text",
        "speaker='Fleet captain selected by the original battle dispatcher'":
            "speaker='Original role-1 officer or native fallback' if wrapper != DIRECT else 'Original ram officer'",
        '== list(range(2580, 2615))': '== SELECTED',
        'native_context=groups, initialized_argument_samples=arguments,':
            'native_context=groups, initialized_argument_samples=arguments, '
            'credited_surrender_context=dict(message_ID=2192, source_reference=prior.reference(source[2192]), '
            'current_reference=prior.reference(current[2192]), source_hex=source[2192].text.hex(), '
            "current_hex=current[2192].text.hex(), new_credit=0),",
    })
    selected = [*range(2106, 2114), *range(2122, 2130), *range(2179, 2192)]
    env = vars(city) | globals() | {'SELECTED': selected}
    exec(compile(source, __file__ + '::source-bound-battle-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
