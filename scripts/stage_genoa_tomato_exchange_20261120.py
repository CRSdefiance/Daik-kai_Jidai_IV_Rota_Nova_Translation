"""Stage all four copies of the original Genoa tomato-trend exchange."""

from inspect import getsource
from pathlib import Path

from scripts import register_sailing_help_20261120 as parent
from scripts import stage_town_trend_exchanges_20261115 as original
from scripts.source_locked_derivation_v5118 import checked_text


base = parent.base
BLOCK_MAP = {150: (189, 181, 177, 150)}
ROOT = Path('work/genoa_tomato_exchange_20261120')
ROM, STORED = ROOT / 'Genoa_Tomato_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/genoa_tomato_exchange_20261120_v1.json')
CONTEXT = {150: 'The Genoa shop owner is certain tomatoes will catch on. The cook doubts her, deadpans through her romantic reminiscence, then acknowledges her orders and ends with a much less enthusiastic reply.'}
MEANINGS = {150: {
    5: 'The owner announces tomatoes twice and insists that they are about to take over. Preserve her conviction.',
    8: 'The cook politely doubts that such a vividly red food will catch on. Keep his question and mild incredulity.',
    11: 'The owner loves that red because it stirs passion and reminds her of a romance that consumed her in her youth.',
    15: 'The cook acknowledges her story and says he is glad for her. The pause and clipped reply keep the dry contrast.',
    19: 'The owner orders the cook to make tomato dishes and sell them immediately. Keep both actions and her urgency.',
    22: 'The cook acknowledges her instructions with a brief, professional response.',
    26: 'The owner says they must seize the chance offered by the tomato trend. Keep her confidence after his flat acknowledgment.',
    29: 'The cook acknowledges her again in a flatter, more casual register. Preserve the comic fall in enthusiasm.',
    33: 'The owner urges the cook to do his best and laughs theatrically. Keep the encouragement and her laugh.',
    36: 'The notice forecasts that tomatoes may catch on in Genoa. Keep the tentative phrasing and the commodity name.',
}}
RETENTION = {
    5: 'The emphatic opening already sounds like the owner announcing a new fashion.',
    8: 'The cook’s brief question already conveys his incredulity at the red food.',
    11: 'The current metaphor preserves what the color evokes and her reminiscence of love when she was young.',
    15: 'The pause and restrained reply give the cook a dry reaction to her romantic digression.',
    19: 'The current wording gives the cook both jobs and ends with the owner’s immediate deadline.',
    22: '“Understood” is a brief, professional response and sets up the more deflated reply that follows.',
    26: 'The current insistence on the craze makes a natural follow-up to the cook’s brief acknowledgment.',
    29: 'The flat acknowledgment contrasts with the owner’s enthusiasm and ends the exchange on the intended joke.',
    33: 'The current wording keeps the owner’s encouragement and her theatrical laugh.',
    36: 'The installed notice is a tentative forecast and accurately names both tomatoes and Genoa.',
}
COLOR = ("That red is the best part! It stirs the passions. Ah, it takes me back to the love that consumed me in my youth.",
         ('the best part!', 'takes me back', 'in my youth.'))
QUESTION = ('Really? Something that red?', ('Something that red?',))
ORDER = ('Make tomato dishes and sell them now!', ('tomato dishes', 'sell them now!'))
SENDOFF = ('Good luck! Ohohoho!', ('Good luck!',))
REVISIONS = {(150, 5): ("Tomatoes! They're the future!", ("They're the future!",)),
             (150, 8): QUESTION, (150, 11): COLOR, (150, 19): ORDER, (150, 33): SENDOFF}
OTHER_ROUTES = {(0, 150, 11): COLOR, (1, 150, 8): QUESTION, (1, 150, 19): ORDER,
                (1, 150, 26): ("Don't let this tomato craze pass us by!", ('this tomato craze', 'pass us by!')),
                (1, 150, 33): SENDOFF}


def source_bundle(clean_arm, originals, inventory):
    group, = BLOCK_MAP
    block = originals[3][group]
    _, speeches = original.raw_speeches(clean_arm, block, inventory)
    assert len(speeches) == 10
    return {group: {'clean_speeches': speeches, 'source_block_sha256': original.digest(block)}}


program = getsource(original.main)
start, end = program.index('    previous = '), program.index('    config = ')
program = program[:start] + program[end:]
program = checked_text(program, {
    '    clean_arm = clean.read_file(ARM)': '    clean_arm = clean.read_file(ARM)\n'
        '    previous = source_bundle(clean_arm, originals, inventory)',
    "previous[f'SC3_B{group}'], alexandria": 'previous[group], None',
    'assert len(updates) == 276': 'assert len(updates) == 40',
    "    newbanks = [IlnkContainer.parse(changed[f'/data/SC{i}.DK4']).blocks for i in range(4)]":
        "    newbanks = [IlnkContainer.parse(changed.get(path, before[path])).blocks\n"
        "                for path in (f'/data/SC{i}.DK4' for i in range(4))]",
    'across 24 town-scene copies': 'across four copies of the Genoa exchange',
})
review = checked_text(getsource(original.review_block), {
    '    if route == 3:\n        assert digest(ja) == evidence[\'source_block_sha256\']\n'
    '        if group != 159:\n            assert digest(old) == evidence[\'current_block_sha256\']':
        "    if route == 3:\n        assert digest(ja) == evidence['source_block_sha256']",
    'source_meaning=note, localization_note=note':
        'source_meaning=note, localization_note=note if revision else RETENTION[context_index]',
})
env = vars(original) | globals()
exec(compile(review, __file__ + '::genoa-contextual-review', 'exec'), env)
exec(compile(program, __file__ + '::genoa-stage', 'exec'), env)


if __name__ == '__main__':
    env['main']()
