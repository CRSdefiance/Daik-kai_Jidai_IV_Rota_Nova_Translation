"""Revisit the early Rafael wrap leads on the registered Sailor Info release."""

from collections import defaultdict
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_sailor_stat_labels_20261114 as parent
from scripts import stage_rafael_early_wraps_20261111 as previous


base, prior, sha = previous.base, previous.prior, previous.sha
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_charlotte_wraps_20261114_v1')
REVIEW = parent.parent.TRIAGE.with_name('rafael_charlotte_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
DECISIONS = {
    (0, 63, 14): ('Claudio', 'Claudio tells Rafael to give the other person some consideration.',
        'Open the argument with a blunt reproach. Claudio names Eirene only after Rafael asks what he means.',
        '...Try showing some consideration.', ('showing some consideration.',)),
    (0, 63, 60): ('Arcadius', 'Arcadius thinks he heard Claudio shouting a moment ago.',
        'Keep the uncertainty. Rafael worries the subject was overheard before they move to a private exchange.',
        'I thought I heard Claudio yelling...', ('heard Claudio yelling...',)),
    (0, 63, 92): ('Arcadius', 'Eirene says nobody else was around and it would have looked strange not to help while passing as a man.',
        'Keep the private explanation and the rhetorical question. The public Arcadius selector stays in place.',
        "Oh... No one else was around. Everyone thinks I'm a man. Wouldn't it have looked odd if I hadn't helped?",
        ("Everyone thinks I'm a man.", "Wouldn't it have looked odd", "if I hadn't helped?")),
    (0, 63, 108): ('Rafael', 'Rafael thought he was taking Eirene into consideration too. He thinks Claudio was unfair.',
        'Keep his hurt after Claudio storms out. The complete short complaint belongs together before Eirene apologizes.',
        None, ('looking out for you', "It's not fair...")),
    (0, 63, 175): ('Arcadius', 'Eirene agrees that Claudio will get over it, calls him simple and invites Rafael to eat.',
        'Give her fond teasing a direct reply. Claudio’s good mood after the meal confirms her reading of him.',
        "Yes. He's easy to figure out. Come on, let's eat.", ("He's easy to figure out.", "Come on, let's eat.")),
    (0, 64, 144): ('Janus', 'Janus concedes that Rafael may have handled it poorly. He reassures him that the girl surely understood he meant no harm.',
        'Preserve the qualified criticism before the reassurance. It answers Rafael’s fear that the offer sounded condescending.',
        "Maybe you went about it wrong, but I'm sure she knows you meant well.",
        ('went about it wrong,', "I'm sure she knows", 'you meant well.')),
    (0, 64, 309): ('Charlotte', 'The group discussed the offer, pooled its scant funds and decided to cross the sea.',
        'Give Charlotte the collective decision in her own words. It links the New World offer to the hopes her family took with them.',
        'We pooled our last coins and agreed to cross the sea.', ('pooled our last coins', 'cross the sea.')),
    (0, 64, 333): ('Rafael', 'Rafael asks if they ever considered returning to their country because things were so hard.',
        'Retain the well-meant but unexamined assumption about a country of their own. Charlotte’s answer turns on that word.',
        None, ("didn't you ever think", 'back to your country?')),
    (0, 64, 337): ('Charlotte', 'Charlotte echoes the word country and says the Romani have no country of their own to return to.',
        'Keep her startled echo and use a direct explanation. Her following examples explain the rejection her community experienced.',
        "...A country? We Romani have no country of our own. There's nowhere to go back to.",
        ('We Romani', 'no country of our own.', "There's nowhere", 'go back to.')),
    (0, 67, 9): ('Rafael', 'Rafael thanks Charlotte and brings up something he wants to give her.',
        'Make the handoff sound tentative and conversational. He identifies the corn seeds after she asks.',
        "Thanks. Charlotte, I've got something for you.", ("I've got something for you.",)),
    (0, 67, 165): ('Charlotte', 'Charlotte trails off, then realizes the sun is already setting.',
        'Keep the unfinished thought and the abrupt change of subject. Rafael immediately agrees that they should hurry.',
        "Nothing... Oh, the sun's going down!", ("the sun's going down!",)),
    (0, 67, 194): ('Charlotte', 'Charlotte nods. The flower is a modest thank-you for today and is all she has to offer.',
        'Keep the nod and modest thanks before Rafael’s delighted reply.',
        "(Nods) Thanks for today. It's not much.", ('Thanks for today.', "It's not much.")),
    (0, 67, 256): ('Arcadius', 'Arcadius chuckles after Claudio’s account. Besides the village developing, they have another thing to look forward to.',
        'Keep the shared anticipation understated after Claudio’s account trails off. The village’s progress remains part of her thought.',
        'I see. Hee hee. The village is coming along, and now we have something else to look forward to.',
        ('The village is coming along,', 'something else', 'to look forward to.')),
    (0, 69, 146): ('Rafael', 'Rafael downplays what he did and credits Charlotte’s hard work.',
        'Keep the generous deflection after Charlotte thanks him for restoring the villagers’ smiles.',
        'I hardly did a thing. You did the hard work, Charlotte!',
        ('I hardly did a thing.', 'the hard work, Charlotte!')),
    (0, 70, 174): ('Maria', 'Maria’s sole condition is that Rafael destroy the Kurushima pirates, a band of wako.',
        'Put Maria’s condition up front. Keep wako because Claudio immediately asks Xien what it means.',
        "One condition. Wipe out the Kurushima pirates. They're a band of wako.",
        ('One condition.', 'the Kurushima pirates.', "They're a band of wako.")),
    (0, 70, 214): ('Maria', 'Maria will hand over the Bamboo Assembly Plan once she verifies the Kurushima faction is gone.',
        'Keep the verification condition and the registered item name intact before Rafael asks about the plan.',
        "Once I know the Kurushima faction is gone, I'll give you the Bamboo Assembly Plan.",
        ('the Kurushima faction', 'is gone,', "I'll give you", 'Bamboo Assembly Plan.')),
    (0, 71, 27): ('Shopkeeper', 'The shopkeeper asks if the crew is looking for the Proof of Conquest.',
        'Keep the casual tone and the full title. Rafael confirms and asks what the shopkeeper knows.',
        'Looking for the Proof of Conquest?', ('the Proof of Conquest?',)),
}
DEFERRED = {
    (0, 63, 113): 'Eirene apologizes for the trouble caused by keeping her identity private. Preserve the personal address.',
    (0, 64, 134): 'Arcadius gently asks Rafael to stop dwelling on the incident. Preserve the personal address.',
    (0, 64, 152): 'Claudio defends Rafael and begins to blame Charlotte before stopping himself. Keep the unfinished turn and the named subject.',
    (0, 69, 143): 'Charlotte thanks Rafael for bringing smiles back to the village. Preserve the personal address and the pause.',
    (0, 70, 50): 'Rafael politely confirms his identity to Xien. Keep the full given and family name substitution together.',
}


def bind(ctx, clean):
    release = base.load(parent.parent.RELEASE)
    queue = base.load(parent.parent.TRIAGE)
    assert queue['candidate_sha256'] == release['candidate_sha256'] == base.digest(parent.parent.ROM)
    archive = ctx.image.read_file(FILE)
    original = base.NdsImage.open(parent.parent.ROM).read_file(FILE)
    assert archive == original and queue['scanned'][FILE]['archive_sha256'] == sha(archive)
    blocks = {block for _, block, _ in DECISIONS | DEFERRED}
    before = IlnkContainer.parse(archive)
    source = IlnkContainer.parse(clean.read_file(FILE))
    inventory, _, _ = prior.scoped_inventory()
    leads = defaultdict(list)
    for lead in queue['records']:
        if lead['file_path'] == FILE and lead['block'] in blocks:
            leads[lead['block']].append(lead)
    groups, deferred, identified = {}, [], set()
    for block, flags in sorted(leads.items()):
        ja_commands, ja_rows = prior.raw_speeches(clean.read_file(ARM), source.blocks[block], inventory)
        commands, en_rows = prior.raw_speeches(ctx.arm, before.blocks[block], inventory)
        assert [r['word'] for r in ja_commands] == [r['word'] for r in commands]
        pairs = {en['offset']: (ja, en) for ja, en in zip(ja_rows, en_rows, strict=True)}
        assert all(ja['complete_preamble_hex'] == en['complete_preamble_hex'] for ja, en in pairs.values())
        assert {flag['block_sha256'] for flag in flags} == {sha(before.blocks[block])}
        selected = []
        for flag in flags:
            ja, en = pairs[flag['offset']]
            ident = (0, block, ja['record_index'])
            assert en['raw_hex'][2:] == flag['stored_body_hex'] and en['selector'] == flag['source_selector']
            encoded = bytes.fromhex(en['raw_hex'])[1:]
            identified.add(ident)
            reference = dict(id=f"DK4_MES_B{block}_R{ja['record_index']:04d}", source_reference=ja,
                             current_reference=en)
            if ident in DEFERRED:
                assert b'FI' in encoded
                deferred.append(reference | dict(file_path=FILE, block=block, source_meaning=DEFERRED[ident],
                    next_check='Qualify wrap and pair phase across the native name expansions.'))
            else:
                assert ident in DECISIONS
                selected.append(reference)
        groups[FILE, block] = source.blocks[block], before.blocks[block], commands, ja_rows, en_rows, selected
    assert identified == (DECISIONS | DEFERRED).keys()
    return groups, deferred


compile_exchanges = FunctionType(previous.compile_exchanges.__code__, vars(previous) | {'DECISIONS': DECISIONS})
contact_sheets = FunctionType(previous.contact_sheets.__code__, vars(previous) | {'ROOT': ROOT})


def main(preview=False):
    assert not ROOT.exists() and not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    clean = base.NdsImage.open(CLEAN)
    if preview:
        image = base.NdsImage.open(parent.ROM)
        ctx = SimpleNamespace(image=image, arm=image.read_file(ARM))
    else:
        ctx = prior.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    groups, deferred = bind(ctx, clean)
    contexts, reviewed = compile_exchanges(groups)
    for row in reviewed:
        print(row['id'], row['automatic_layout']['lines'], row['trailing_blank_bytes'], flush=True)
    if preview:
        return
    retained = [row for row in reviewed if row['current_hex'] == row['target_hex']]
    changed = [row for row in reviewed if row['current_hex'] != row['target_hex']]
    pictures = previous.native_validation(ctx, reviewed)
    ROOT.mkdir()
    archives = {}
    for name, raw in prior.transform(ctx.image, changed):
        path = ROOT / Path(name).name
        path.write_bytes(raw)
        archives[name] = dict(path=path.as_posix(), sha256=sha(raw), source_sha256=sha(ctx.image.read_file(name)))
    sheets = contact_sheets(pictures)
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source','context','localization','naturalness','formatting'],
        candidate_sha256=release['candidate_sha256'], records=changed, unchanged_leads=retained,
        deferred_macro_leads=deferred, complete_exchange_references=contexts, zero_new_credit=True, full_goal_complete=False))
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], review_sha256=base.digest(REVIEW),
        archives=archives, sheets=sheets, blocks=[list(key) for key in groups],
        unchanged_terminators_offsets_block_extents_and_unowned_bytes=True,
        archive_inverses_exact=True, checked_complete_native_pages=len(pictures),
        checked_original_processor_alignments=8 * len(reviewed)))


if __name__ == '__main__':
    import sys

    main(preview='--preview' in sys.argv)

