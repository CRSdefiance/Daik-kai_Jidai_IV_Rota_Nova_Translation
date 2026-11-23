"""Review Rafael's trade expansion and military investment exchanges in context."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_departure_numerals_20261119 as parent
from scripts import review_rafael_ceuta_contract_routes_20261119 as precedent
from scripts import review_rafael_sail_controls_20261119 as earlier
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
ROOT = Path('work/rafael_trade_and_arms_20261119')
SOURCE, OUTPUT = ROOT / 'paired_source_v1.json', ROOT / 'contextual_review_v4.json'
STAGED = ROOT / 'staged_v4'
ROM, PROOF = STAGED / 'Rafael_Trade_and_Arms_STAGED.nds', STAGED / 'stored_proof.json'
BLOCKS = ((129, 140), (), (), ())
CONTEXT = {
    129: 'Julio checks whether Rafael is comfortable with trading. The detailed branch grows a Portuguese trading network from Madeira outward. The other response lets Rafael make his own decisions after Julio admits that he worries.',
    140: 'Janus explains why spending on town defenses matters and how earlier Portuguese fort-building may give the fleet an advantage. Rafael takes the advice seriously.',
}
NAMES = {**precedent.NAMES, 4: 'Janus Pasar'}
TRADE = {
    5: ('Julio asks whether Rafael has learned how to make substantial profits from trade.',
        'Use a direct, familiar question that both responses answer.',
        'FI, have you learned how to make good money trading?', ('how to make good money trading?',)),
    11: ('Rafael has not learned it yet.', 'The brief answer naturally opens the explanation.', None, ()),
    13: ('Rafael says he is comfortable trading now.', 'The informal answer conveys confidence without claiming mastery.', None, ()),
    20: ('The first place to pay attention to is Madeira, a small Portuguese island southwest of Lisbon.',
        'The current directions and political affiliation are concise and accurate.', None, ()),
    24: ('Madeira is rich in local goods such as sugar and could be an important base when the company expands into Africa and the New World.',
        'Give the goods their own sentence and keep the two destinations together as part of the same expansion.',
        'Sugar is one of its local goods. It could be an important base when FO expands into Africa and the New World.',
        ('Sugar is one of its local goods.', 'Africa and the New World.')),
    27: ('If Madeira has market share available, invest as much as possible.',
        'Keep the condition and the advice to invest as much as Rafael can, without making the share sound ownerless.',
        'Any market share left in Madeira? If so, invest as much as you can.',
        ('Any market share left in Madeira?', 'invest as much as you can.')),
    30: ('Once trade among Lisbon, Ceuta and Madeira builds capital, establish positions in Las Palmas and Verde.',
        'A foothold makes the commercial advice clear and keeps the five locations and their order.',
        'Build up some capital trading among Lisbon, Ceuta, and Madeira. Then get a foothold in Las Palmas and Verde.',
        ('Lisbon, Ceuta, and Madeira.', 'Las Palmas and Verde.')),
    33: ('The two ports are gateways between Africa and the Mediterranean. Verde in particular offers many local goods for a modest investment.',
        'The connection between geography, investing and buying local goods is clear. Verde matches the port name.', None, ()),
    36: ('Go back and forth between Africa and the Mediterranean for a while and spend the proceeds on larger ships and greater market share.',
        'Restore the repeated trips and their short-term role before the later expansion.',
        'Trade back and forth for now, from Africa to the Mediterranean. Put the profits into bigger ships and more market share.',
        ('from Africa to the Mediterranean.', 'more market share.')),
    39: ('More cargo holds and more local goods to buy mean more profit per trading run.',
        'The existing line states both contributing factors and explains the benefit per trip.', None, ()),
    42: ('After that, keep extending the range of the trade network.',
        'Finish the explanation in Julio’s familiar teaching voice, with the instruction together.',
        'Then keep trading farther afield.', ('farther afield.',)),
    45: ('Investing in commerce can introduce a new local good even in towns that seem to have nothing profitable.',
        'Keep the possibility and use the name of the investment action from Help.',
        'Commercial Investment can bring out new local goods, even in towns that seem to have nothing worth trading.',
        ('Commercial Investment', 'new local goods,')),
    48: ('Go as far as the New World if resources allow. There is no need to overextend.',
        'The conditional phrasing and gentle warning suit Julio. Both thoughts already read naturally.', None, ()),
    52: ('Rafael understands and says he will make an effort.',
        'The respectful acknowledgement and resolve fit his answer to the longer lesson.', None, ()),
    58: ('Julio wonders if things will be all right and admits that older people worry needlessly.',
        'Keep his wry self-criticism and the question’s open subject. The next line gives Rafael room to decide.', None, ()),
    62: ('Julio encourages Rafael to try what he thinks best.',
        'The short encouragement follows Julio’s admission and leaves the decision with Rafael.', None, ()),
}
ARMS = {
    5: ('Invest at the palace or governor’s office to raise a town’s Arms rating ahead of enemy attacks.',
        'Lead with the Arms mechanic and use the established names of both facilities.',
        "Raise a town's Arms rating to help it withstand enemy attacks. Invest at the Palace or Governor's Office.",
        ("Raise a town's Arms rating", 'enemy attacks.', "Governor's Office.")),
    9: ('Portugal built forts in towns on the way to the Indian Ocean and used them as trading bases.',
        'The existing sentence preserves both the route and what the forts were used for.', None, ()),
    12: ('Portugal’s experience building those forts should let Rafael raise Arms using less military investment than other countries.',
        'Keep the link to Portuguese building techniques, the qualified expectation and the comparison.',
        "Those building techniques should let us raise a town's Arms rating with less military investment than other nations need.",
        ("a town's Arms rating", 'military investment')),
    16: ('Rafael understands and will remember the advice.',
        'The brief acknowledgement fits Janus’s lesson and already sounds natural.', None, ()),
}


def pair_source():
    before, release = map(base.load, (earlier.INTAKE, parent.RELEASE))
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(native.CLEAN) == before['clean_sha256'] == release['clean_input_sha256']
    rel, clean = map(base.NdsImage.open, (parent.ROM, native.CLEAN))
    path = '/data/SC0.DK4'
    source, current = (rom.read_file(path) for rom in (clean, rel))
    banks = [native.IlnkContainer.parse(arc).blocks for arc in (source, current)]
    groups = []
    for group in before['groups']:
        block = group['block']
        if block not in BLOCKS[0]:
            continue
        assert native.digest(source) == group['source_archive_sha256']
        assert [native.digest(bank[block]) for bank in banks] == [group['source_block_sha256'], group['current_block_sha256']]
        groups.append(group | dict(context=CONTEXT[block], current_archive_sha256=native.digest(current)))
    assert [g['block'] for g in groups] == list(BLOCKS[0])
    packet = before | dict(candidate_sha256=release['candidate_sha256'], profile=release['profile'],
        groups=groups, previous_exact_blocks_proof_sha256=base.digest(earlier.INTAKE))
    if SOURCE.exists():
        assert base.load(SOURCE) == packet
    else:
        ROOT.mkdir(exist_ok=True)
        base.save(SOURCE, packet)


def review():
    pair_source()
    recipe = checked_text(getsource(precedent.review), {
        'packet, release, actual = map(base.load, (SOURCE, parent.RELEASE, observed.OUTPUT))':
            'packet, release = map(base.load, (SOURCE, parent.RELEASE))',
        "packet['candidate_sha256'] == actual['candidate_sha256'] == release['candidate_sha256']":
            "packet['candidate_sha256'] == release['candidate_sha256']",
        '(CONTRACT,ROUTES)': '(TRADE,ARMS)',
        'len(records) == 32': 'len(records) == 20',
        '        ordinary_gameplay_reference=str(observed.OUTPUT),ordinary_gameplay_sha256=base.digest(observed.OUTPUT),\n': '',
    })
    scope = vars(precedent) | globals()
    exec(compile(recipe, __file__ + '::paired-review', 'exec'), scope)
    scope['review']()


def compile_lessons():
    template = earlier.workflow
    main = template.env['main']
    scope = template.env | dict(parent=parent, paired=SimpleNamespace(BLOCKS=BLOCKS),
        review=SimpleNamespace(SOURCE=SOURCE, OUTPUT=OUTPUT), ROOT=STAGED, ROM=ROM, PROOF=PROOF,
        rebuild_function=rebuild_function)
    scope['catalogue_membership'] = FunctionType(template.catalogue.catalogue_membership.__code__, scope)
    FunctionType(main.__code__, scope)()
    check = base.load(PROOF)
    assert check['whole_parent_inverse'] and check['changed_blocks'] == {'/data/SC0.DK4': [129, 140]}


def rebuild_function():
    original = earlier.workflow.rebuild_function()
    planner = original.__globals__['plan_progressive']
    recipe = checked_text(getsource(planner), {
        '.replace("{MACRO:FI}", "W" * 16)': '.replace("{MACRO:FI}", "W" * 16).replace("{MACRO:FO}", "W" * 20)',
        'for p in row["protected_phrases"])': 'for p in row["protected_phrases"]), (row["id"], plan["lines"])',
    })
    scope = planner.__globals__.copy()
    exec(compile(recipe, __file__ + '::company-planning-width', 'exec'), scope)
    owner = original.__globals__ | {'plan_progressive': scope['plan_progressive']}
    for name in ('changed_speech', 'changed_styles'):
        owner[name] = FunctionType(owner[name].__code__, owner)
    return FunctionType(original.__code__, owner)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('review', 'stage'))
    {'review': review, 'stage': compile_lessons}[parser.parse_args().action]()
