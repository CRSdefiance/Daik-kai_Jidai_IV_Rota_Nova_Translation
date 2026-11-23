"""Review and render the linked Auto Move and at-sea command Help pages."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_tavern_help_20261120 as parent
from scripts import stage_palace_help_20261120 as original
from scripts import stage_tavern_help_20261120 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base, CLEAN, HELP, ARM = earlier.base, earlier.CLEAN, earlier.HELP, earlier.ARM
ROOT = Path('work/sailing_help_20261120_v3')
ROM, PROOF, PLAN = ROOT / 'Sailing_Help_RESEARCH_ONLY.nds', ROOT / 'native_help_pages.json', ROOT / 'plan.json'
GATES, CHILDREN = earlier.GATES, {}
MODE_RECEIPT = Path('releases/all_routes_editorial_20261119_rafael_sailing_modes_candidate/verification/registered_review.json')
ARTICLES = {
    76: ('Auto Move', (
        'Choose a destination town and your fleet will sail there automatically. You need a [[120|Captain]] and a '
        '[[123|Surveyor.]] Your starting town and destination must be connected on the [[104|Route Map,]] and your '
        'faction must have [[150|market share]] in both towns and every town along the route. The map marks usable routes in red.',),
        'The source says town, with a separate City size class elsewhere. Keep the captain and surveyor requirements, '
        'the linked map and the requirement to hold market share at both ends and every stop.'),
    85: ('Info Mode (At Sea)', (
        'Press Y while sailing to pause and open Info. Move the magnifying glass over a town or fleet and press A '
        'to see its details. From Info, you can also switch to [[86|Search]] or [[87|Declare War.]]',),
        'Name the on-screen mode and add the exact target-and-confirm action taught in Rafael’s registered tutorial.'),
    86: ('Search Mode (At Sea)', (
        'In [[85|Info,]] press Y or R to switch to Search. Press A to search the area inside the frame. You may find '
        'water, food or items. If you find nothing, your sailors gain 3 fatigue. Sailors may desert or be attacked by '
        'wild animals during a search.',),
        'Keep both shortcuts, the possible finds, the three points of fatigue for the sailors and the risks. The '
        'highlighted area follows Rafael’s tutorial.'),
    87: ('Declare War Mode', (
        'To start a [[89|battle]] with a fleet or town on screen, open [[85|Info]] and press L or press Y twice. '
        'Choose a target to begin. Your faction is now [[187|at war]] with theirs, and Friendship drops sharply. '
        'Declaring war on a town limits what you can do there. You cannot use this command against an allied fleet.',),
        'Keep both shortcuts, the immediate battle and faction relationship change, the limited town commands '
        'and the specific restriction on allied fleets.'),
}
RETAIN = {
    73: 'The Port article retains the equal fill on Yes, manual proportions on No, and all three building links.',
    74: 'Depart names the three choices in the order offered at the Port.',
    75: 'Sail is concise and correctly distinguishes manual control from Auto Move.',
    77: 'The short Deck View cross-reference leads to the full Shared Commands article.',
    82: 'The At-Sea Commands index lists all nine original destinations with clear labels.',
    83: 'Manual Sailing matches the D-pad, shoulder buttons and A and B controls, the initial Half Open position '
        'and the original all-masts assignment condition.',
    84: 'The article keeps the additional DS confirmation, the ban on restarting at sea and the Eagle Figurehead exception.',
}


def plan_pages(manuscript, raw):
    compiler = original.compiler
    source = checked_text(compiler.SOURCE, {
        'topics!=(set(range(133,202))-{181,184})': f'topics!={set(ARTICLES)!r}',
        'Exact remaining67 Help articles': 'Exact Sailing Help articles',
    })
    scope = compiler.plan_articles.__globals__.copy()
    wrap = scope['wrap']
    phrases = [['press', 'Y', 'twice'], ['Route', 'Map'], ['market', 'share'], ['Declare', 'War'],
               ['magnifying', 'glass'], ['3', 'fatigue'], ['on', 'screen'],
               ['inside', 'the', 'frame'], ['Declaring', 'war']]
    scope['wrap'] = FunctionType(wrap.__code__, wrap.__globals__ | {'PHRASES': [*wrap.__globals__['PHRASES'], *phrases]})
    exec(compile(source, __file__ + '::sailing-help-compiler', 'exec'), scope)
    return scope['plan_articles'](manuscript, *raw.values(), require_formatting=False)


def mode_matches(arm):
    receipt = base.load(MODE_RECEIPT)
    headlines = receipt['current_mode_headings']['current_exact_packed_headings']
    for reference in headlines.values():
        assert reference['file_path'] == ARM
        start = reference['offset']
        assert original.sha(arm[start:start + reference['bytes']]) == reference['packed_sha256']
    tutorial = {r['id']: r['english'] for r in receipt['records']}
    assert 'magnifying glass over a town or fleet and press A' in tutorial['DK4_MES_B46_R0058']
    assert 'Press A to search the land inside the gray frame.' == tutorial['DK4_MES_B46_R0080']
    assert 'Info to Search to Declare War' in tutorial['DK4_MES_B46_R0091']
    return headlines


source = getsource(original.main)
start, end = source.index('    menu_path = '), source.index('    records = []')
source = source[:start] + '    menu_path = MODE_RECEIPT\n    menu_labels = mode_matches(arm)\n' + source[end:]
source = checked_text(source, {
    "context='Palace commands and the original linked Help articles on contracts, letters and Arms.'":
        "context='Port and at-sea Help, read together with the registered Rafael tutorial.'",
    'Palace Help decisions': 'Sailing Help decisions',
})
env = vars(original) | globals()
exec(compile(source, __file__ + '::stage-sailing-help', 'exec'), env)


if __name__ == '__main__':
    env['main']()
