"""Review the entire Tavern Help family against its original menu labels."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import register_recruit_crew_20261120 as parent
from scripts import stage_palace_help_20261120 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base, HELP, ARM, CLEAN = parent.base, earlier.HELP, earlier.ARM, earlier.CLEAN
ROOT = Path('work/tavern_help_20261120')
ROM, PROOF, PLAN = ROOT / 'Tavern_Help_RESEARCH_ONLY.nds', ROOT / 'native_help_pages.json', ROOT / 'plan.json'
CHILDREN = {}
GATES = earlier.GATES
MENU = Path('translations/tavern_scheme_labels_v1.json')
ARTICLES = {
    12: ('Tavern', (
        "Recruit crew and gather news at the Tavern. Many towns in Arab cultural regions have no tavern for religious "
        "reasons. It's harder to find sailors there, so think twice before starting a battle. See [[13|Order Drink,]] "
        "[[14|Treat Everyone,]] [[15|Recruit Crew,]] and [[16|Schemes.]]",),
        'Keep the regional and religious context, the advice about battle and all four original menu links.'),
    14: ('Treat Everyone (Tavern)', (
        "Buy a round for everyone in the Tavern. You'll hear news about nearby towns and other factions, and you may "
        "get a tip about an item. Buying a round before you choose [[15|Recruit Crew]] makes it easier to find sailors.",),
        'Use the current menu name. Buying a round preserves the sense of treating the room, including its recruiting benefit.'),
    15: ('Recruit Crew (Tavern)', (
        "Recruit sailors for your fleet. Towns with higher Growth offer more recruits at once, but the fee is higher. "
        "Any extra recruits are dismissed on the spot. Buy a round first to improve turnout. Then use [[139|Assign Sailors]] "
        "to place the new recruits on your ships.",),
        'Use the original English menu names for recruitment and assignment. Keep the cost, turnout and dismissal rules.'),
    16: ('Schemes (Tavern)', (
        "If your [[118|Strategist]] has an idea, you can scheme against a rival. Each attempt costs 1,000 gold and can fail. "
        "You need another faction in this region. Except for Forge Papers, you must have visited a town where another "
        "faction has [[150|market share.]] See [[17|Lure Fleet,]] [[18|Forge Papers,]] "
        "[[19|Bad Rumors,]] and [[20|Bribe.]]",),
        'Use the original action names and keep the 1,000-gold cost, possible failure and Forge Papers exception.'),
    17: ('Lure Fleet', (
        "Draw another faction's fleet to a town you choose in the current sea region.",),
        'The action and the target are singular. Town preserves the broader Japanese settlement term.'),
    18: ('Forge Papers', (
        "Choose two other factions and forge papers to turn them against each other. You need at least two other factions "
        "to use this scheme.",),
        'Use the original menu name and keep the need for two other factions and the specific purpose of the papers.'),
    19: ('Bad Rumors', (
        "Spread damaging rumors about another faction in a town in the current sea region. This lowers that faction's "
        "market share there. Your Strategist must be skilled enough to think of this scheme.",),
        'Name the market-share loss and keep the Strategist prerequisite without implying a numeric threshold.'),
    20: ('Bribe', (
        "Choose a town in the current sea region where another faction operates. Bribe a broker there to take some of "
        "that faction's market share. Your Strategist must be skilled enough to think of this scheme.",),
        'Match Bribe and make the original town, broker, faction and market-share relationship clear.'),
    118: ('Tactics Room', (
        "Strategists plan your schemes here. An officer needs Guile 120 or higher to take the job. When your Strategist "
        "has an idea, choose [[16|Schemes]] at the Tavern. They may foil enemy schemes. They also gather news about "
        "other factions when you stay at an Inn.",),
        'Use Schemes where it links back to the Tavern, and keep the separate plan, defense and intelligence duties.'),
}
RETAIN = {
    11: 'Town Commands names the Tavern and gives the intended building and City-only navigation.',
    13: 'The price and two news topics read clearly, and the City link and the women’s item tips carry their source meaning.',
    139: 'Assign Sailors uses the current heading and keeps the displayed count fields, controls and three policies on its linked pages.',
}


def plan_pages(manuscript, raw):
    compiler = earlier.compiler
    source = checked_text(compiler.SOURCE, {
        'topics!=(set(range(133,202))-{181,184})': f'topics!={set(ARTICLES)!r}',
        'Exact remaining67 Help articles': 'Exact Tavern Help articles',
    })
    scope = compiler.plan_articles.__globals__.copy()
    wrap = scope['wrap']
    phrases = [['sea', 'region'], ['market', 'share'], ['higher', 'Growth'], ['1,000', 'gold'],
               ['Forge', 'Papers'], ['Arab', 'cultural', 'regions']]
    scope['wrap'] = FunctionType(wrap.__code__, wrap.__globals__ | {'PHRASES': [*wrap.__globals__['PHRASES'], *phrases]})
    exec(compile(source, __file__ + '::tavern-help-compiler', 'exec'), scope)
    return scope['plan_articles'](manuscript, *raw.values(), require_formatting=False)


def menu_matches(path, source, arm):
    records = base.load(path)['proof']['records']
    menu = {r['field']: (r['japanese'], r['english']) for r in records}
    menu.update({0x118BA4: ('飲み物をたのむ', 'Order Drink'), 0x118BB4: ('みんなにおごる', 'Treat Everyone'),
                 0x118BC4: ('水夫を集める', 'Recruit Crew'), 0x1FD14: ('水夫を編成して下さい', 'Assign Sailors')})
    matches = []
    for field, expected in menu.items():
        pointers = [unpack_from('<I', data, field)[0] for data in (source, arm)]
        raw = [data[p - 0x02000000:p - 0x02000000 + 80].split(b'\0', 1)[0]
               for data, p in zip((source, arm), pointers, strict=True)]
        assert tuple(value.decode('cp932') for value in raw) == expected, (hex(field), raw, expected)
        assert any(expected[1] in (' '.join(body) + title) for title, body, _ in ARTICLES.values())
        matches.append(dict(pointer_field=0x02000000 + field, source_pointer=pointers[0], current_pointer=pointers[1],
                            source_hex=raw[0].hex(), current_hex=raw[1].hex(), english=expected[1]))
    return matches


source = getsource(earlier.main)
start, end = source.index('    menu_path = '), source.index('    records = []')
source = source[:start] + '    menu_path = MENU\n    menu_labels = menu_matches(menu_path, stock_arm, arm)\n' + source[end:]
source = checked_text(source, {
    '([213] if topic == 25 else [])': '([210] if topic == 139 else [])',
    "context='Palace commands and the original linked Help articles on contracts, letters and Arms.'":
        "context='Tavern Help and its linked Tactics Room and crew assignment pages.'",
    'Palace Help decisions': 'Tavern Help decisions',
})
env = vars(earlier) | globals()
exec(compile(source, __file__ + '::stage-tavern-help', 'exec'), env)


if __name__ == '__main__':
    env['main']()
