"""Review the complete Seoul Square encounter and stage its dialogue amendments."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from scripts import register_market_conversation_20261115 as parent
from scripts import stage_maria_final_wraps_20261114 as prior_story
from scripts import stage_rafael_early_wraps_20261111 as sheet_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_release_baseline import files


base, prior = parent.base, prior_story.prior
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
FILE, BLOCK = '/data/SC3.DK4', 140
IlnkContainer = prior_story.IlnkContainer
ROOT = Path('work/seoul_recruitment_20261115_v1')
ROM, STORED = ROOT / 'Seoul_Recruitment_RESEARCH_ONLY.nds', ROOT / 'staged.json'
HISTORY = Path('translations/maria335_B137_B151_integrated_final_review_v1.json')
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/seoul_recruitment_20261115_v1.json')
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
AMENDMENTS = {
    18: ("She's followed us for a bit, but...", 'Keep his observation about being followed and his trailing hesitation in one natural sentence.', ()),
    22: ("I didn't expect a girl like her...", 'Give Yukihisa a natural reaction as he sees the person he caught. Keep the unfinished thought.', ()),
    30: (None, 'Keep Maria’s order to let Yifa go and the short pause before her full question.', ('Why were you following us?',)),
    37: (None, 'Keep the company substitution and Yifa’s complete demand to come aboard.', ('Take me aboard!',)),
    41: ("That's rather forward of her. Has she no manners?", 'Xien comments on the abrupt demand and then rebukes her. The second sentence keeps his older voice.', ('Has she no manners?',)),
    45: ("You can't just show up and demand a place aboard. Why do you want to come?", 'Keep Maria’s objection to the demand before she gives Yifa a chance to explain.', ('demand a place aboard.', 'Why do you want to come?')),
    49: ("I want to travel the world! I'll train as I go, get stronger, and show my master what I can do!", 'Keep Yifa’s goal, her plans to train along the way and improve, and her determination to show her master what she can do.',
         ("I'll train as I go,", 'get stronger,', 'show my master what I can do!')),
    52: ('Training? In what discipline?', 'Yukihisa’s measured question takes her training seriously and asks which art she hopes to master.', ()),
    101: ('Not bad. Closing in on Yukihisa that fast is impressive.', 'Maria praises how quickly Yifa closed the distance. She stops short of confirming the spell.', ('on Yukihisa', 'that fast')),
    105: ('Footwork and spacing like that take martial training.', 'Yukihisa recognizes martial training from her footwork and how she judged the distance.', ('martial training.',)),
    108: ('You really mean to see the world?', 'Let Maria check the seriousness of Yifa’s original request before hearing her motivation again.', ()),
    112: ('I want to prove my master wrong! Please, take me to see the world!', 'Keep the reason for training and her plea to travel. Both belong to her answer to Maria’s question.', ('prove my master wrong!', 'to see the world!')),
    116: (None, 'Keep Maria’s acceptance of the motive, followed by the question about Yifa’s name.', ('prove someone wrong', "What's your name?")),
    124: (None, 'Keep Maria’s condition that Yifa work as an equal and give the no-special-treatment sentence a complete line.',
          ('aboard my ship', 'you work as an equal.', 'Expect no special treatment.')),
    135: ('Heh. Can you beat my Taoist art?', 'Bring back Yifa’s smug laugh and challenge as her answer to Yukihisa’s introduction.', ()),
}
RETENTIONS = {
    6: 'Yukihisa’s abrupt challenge fits his suspicion and the surprise of catching a follower.',
    10: 'Yifa’s short cry answers the sudden capture before Maria knows what happened.',
    14: 'Maria’s brief question keeps her initial confusion and hesitation.',
    26: 'Yifa’s sharp demand to be let go answers Yukihisa’s suspicion before Maria gives the same order.',
    33: 'Yifa starts with a polite request for a favor before stating her much bolder demand.',
    56: 'Her enthusiastic invitation to watch keeps the art she is about to demonstrate.',
    59: 'Yukihisa’s echo identifies his surprise at the unfamiliar art.',
    63: 'Yifa gives the specific sword instruction and immediately starts her demonstration.',
    67: 'Yukihisa’s brief grunt suits the response to her challenge.',
    71: 'The drawn-out shout preserves the sound of her demonstration.',
    75: 'The standalone question mark conveys Yukihisa waiting for an effect.',
    79: 'The current Huh preserves Maria’s private puzzlement as she waits for a visible effect.',
    82: 'Yifa spots an opening and exploits it. The short attack cry belongs to the same action.',
    87: 'Yukihisa’s startled dodge comes directly after her attack.',
    91: 'Keep her burst of praise before she proudly identifies her binding spell.',
    94: 'Yukihisa offers the ordinary explanation that he let his guard down. The complete phrase stays together, and he leaves room for her claim.',
    97: 'The laugh and rhetorical question keep her pleased teasing after Yukihisa voices doubt.',
    120: 'Yifa’s proud one-word introduction answers Maria’s direct question.',
    128: 'Yifa welcomes the condition eagerly. Her brief answer keeps the quick rhythm before Yukihisa introduces himself.',
    132: 'Yukihisa gives his name and promises to keep his guard up, setting up Yifa’s last challenge.',
}
CONTEXT = ('Yukihisa catches Yifa following the crew. She asks to join them so she can train abroad and prove herself '
           'to her master. She attacks during a distraction. Maria and Yukihisa acknowledge her technique, and Maria '
           'takes her aboard as an equal. The speakers’ forms of address carry familiarity without establishing kinship.')


def digest(raw):
    return sha256(raw).hexdigest()


def scene(image):
    return IlnkContainer.parse(image.read_file(FILE)).blocks[BLOCK]


def bind(source, image):
    historical = {int(row['id'].split('_R')[-1]): row for row in base.load(HISTORY)['records'] if row['block'] == BLOCK}
    inventory, _, _ = prior.scoped_inventory()
    (ja_cmd, ja), (en_cmd, en) = [prior.raw_speeches(rom.read_file(ARM), scene(rom), inventory) for rom in (source, image)]
    assert [r['word'] for r in ja_cmd] == [r['word'] for r in en_cmd]
    assert len(ja) == len(en) == len(historical) == 35
    assert set(AMENDMENTS).isdisjoint(RETENTIONS) and AMENDMENTS.keys() | RETENTIONS.keys() == historical.keys()
    rows = []
    for original, current in zip(ja, en, strict=True):
        n = original['record_index']
        old = historical[n]
        assert original['selector'] == current['selector'] == old['source_selector']
        assert original['complete_preamble_hex'] == current['complete_preamble_hex']
        assert original['raw_hex'] == old['source_hex']
        rows.append((n, original, current, old))
    return rows


def compile_changes(source, image, pairs):
    selected, editor = [], {}
    for n, original, current, old in pairs:
        if n in AMENDMENTS:
            text, reason, phrases = AMENDMENTS[n]
            editor[BLOCK, n] = old['speaker'], text, old['source_meaning'], reason, phrases
            selected.append(((BLOCK, n), original, current))
    compiled = FunctionType(prior_story.compile_rows.__code__, prior_story.compile_rows.__globals__ | {
        'get_exchanges': lambda *_: ([{'file_path': FILE, 'block': BLOCK}], selected), 'DECISIONS': editor,
    })
    _, records = compiled(image, source)
    return {row['source_reference']['record_index']: row for row in records}


def stage():
    assert not any(p.exists() for p in (ROM, STORED, MANUSCRIPT))
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(CLEAN)
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    image = ctx.image
    pairs = bind(clean, image)
    amended = compile_changes(clean, image, pairs)
    rows, changed, previews = [], [], []
    _, paint = prior.precedent.planners(ctx.arm)
    for n, original, current, old in pairs:
        if n not in amended:
            rows.append(dict(id=old['id'], file_path=FILE, speaker=old['speaker'], source_reference=original,
                current_reference=current, source_meaning=old['source_meaning'], context=CONTEXT,
                english=' '.join(bytes.fromhex(current['raw_hex'])[1:].decode('ascii').split()),
                localization_note=RETENTIONS[n], decision='retention', review=dict.fromkeys(GATES, True)))
            continue
        row = amended[n]
        assert row['current_hex'] != row['target_hex']
        for label, field in (('before', 'current_hex'), ('after', 'target_hex')):
            body = bytes.fromhex(row[field])[1:]
            result = prior_story.native(ctx, row['source_selector'], body, paint)
            page, = result['pages']
            assert page['first_visible_origin'] == [0, 0]
            row[label + '_native'] = result
            previews.append((f'B140 R{n} {label}', bytes.fromhex(page['native_plane_hex'])))
        row['context'] = CONTEXT
        row['decision'] = 'wrap revision' if AMENDMENTS[n][0] is None else 'revision'
        rows.append(row)
        changed.append(row)
    (path, archive), = prior.transform(image, changed)
    assert path == FILE and len(changed) == 15
    before = files(image)
    old_block = scene(image)
    image.replace_file(FILE, archive)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {FILE}
    inventory, _, _ = prior.scoped_inventory()
    commands, text = prior.raw_speeches(ctx.arm, scene(image), inventory)
    old_commands, _ = prior.raw_speeches(ctx.arm, old_block, inventory)
    controls = ('offset', 'word', 'native_extent', 'ancestor_0100_offsets')
    assert [[r[k] for k in controls] for r in commands] == [[r[k] for k in controls] for r in old_commands]
    for row, old, new in zip(rows, pairs, text, strict=True):
        assert row.get('target_hex', old[2]['raw_hex']) == new['raw_hex']
        assert old[2]['complete_preamble_hex'] == new['complete_preamble_hex']
        row['staged_reference'] = new
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    image.replace_file(FILE, before[FILE])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheet_writer = FunctionType(sheet_tools.contact_sheets.__code__, sheet_tools.contact_sheets.__globals__ | {'ROOT': ROOT})
    sheets = sheet_writer(previews)
    candidate = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(GATES), candidate_sha256=candidate, previous_sha256=release['candidate_sha256'], records=rows))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(ctx.arm), target_SC3_sha256=digest(archive), original_command_count=len(commands),
        sheets=sheets, manuscript_sha256=base.digest(MANUSCRIPT), changed_records=[r['id'] for r in changed],
        source_review_sha256=base.digest(HISTORY), whole_parent_inverse=True))
    for row in changed:
        print(row['id'], row['automatic_layout']['lines'])
    print('Staged the complete 35-line Yifa recruitment review with 15 scoped revisions.')


if __name__ == '__main__':
    stage()
