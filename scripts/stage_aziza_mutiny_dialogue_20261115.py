"""Review the pirate names and stage the ambiguous mutiny orders."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_port_supply_dialogue_20261115 as parent
from scripts import stage_rafael_early_wraps_20261111 as layout
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_town_role_labels_20261115 import scoped_inventory, raw_speeches, story_context
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files

base, IlnkContainer, sha = parent.base, layout.IlnkContainer, layout.sha
ARM, CLEAN, GATES = parent.stage.ARM, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/aziza_mutiny_dialogue_20261115_v2')
ROM = ROOT / 'Aziza_Mutiny_Dialogue_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
REVIEW = names.CHECKPOINT / 'aziza_mutiny_dialogue_20261115_v2.json'
ROUTES = ((12, 26, 187), (3, 17, 179), (3, 12, 175), (5, 19, 145))
LABELS = {
    183: ('Angel', 'エンジェル', 'Angel is the pirate’s nickname. He voices the crew’s grievances and orders the attack.'),
    184: ('Snake', 'スネーク', 'Snake is the pirate’s nickname. He mocks Aziza and names her real reason for pursuing the fleet.'),
    185: ('Dandy', 'ダンディー', 'Dandy is the pirate’s nickname. He begins with a restrained reply to Aziza and later questions or bargains with her rescuers.'),
}
ORDER = "None of your business! Take out Aziza and this guy!"
GRIEVANCE = "We keep losing. No money coming in. You're gonna answer for that."
REVISIONS = {
    (0, 26, 92): (ORDER, ('None of your business!', 'Take out Aziza and this guy!'),
                  'Name Aziza and the man who just intervened as separate targets of the same order. The old construction could make Aziza sound like his accomplice.'),
    (1, 17, 41): (GRIEVANCE, ('We keep losing. No money coming in.', "You're gonna answer for that."),
                  'Keep the losses, the lack of earnings and the threat. The clipped complaints and blunt accusation fit the pirate who has just told Aziza he no longer takes her orders.'),
    (1, 17, 95): (ORDER, ('None of your business!', 'Take out Aziza and this guy!'),
                  'Keep Angel’s answer to Al and make both attack targets explicit, as the Japanese does.'),
}
RETAINED_ORDERS = {
    (2, 12, 91): '“Take him and Aziza out together” already names both targets. The blunt pivot follows Al’s intervention.',
    (3, 19, 92): '“Both him and Aziza” already names the two targets and preserves the escalation as Al stands up to the mutineers.',
}
ORDER_JA = 'てめえにゃ関係ねえ！\n…この際だ、アズィーザもこいつも\nまとめて片付けろ！'
RESCUE = 'Aziza’s crew turns on her after a defeat, blaming the losses and her pursuit of the fleet that has her father’s sword. Al intervenes. The confrontation leads to a settlement and Aziza explains what the sword means to her.'


def sheet(pictures):
    export = FunctionType(layout.contact_sheets.__code__, layout.contact_sheets.__globals__ | {'ROOT': ROOT})
    return export(pictures)


def pirate_names(ctx, clean):
    getter = names.original_names
    code = checked_text(getsource(getter.names), {
        'for ident in [2,4,13,23,109]:': 'for ident in (183, 184, 185):',
    })
    env = vars(getter).copy()
    exec(compile(code, __file__ + '::three-pirate-getters', 'exec'), env)
    getters = ctx.execute(env['names'])['rows']
    clean_arm = clean.read_file(ARM)
    inventory = base.load(names.INVENTORY)
    assert inventory['clean_ARM9_sha256'] == sha(clean_arm)
    rows = []
    for actor, (en, ja, note) in LABELS.items():
        known = inventory['records'][actor]
        source = known['clean_ordinary_role_consumers']
        current = [row for row in getters if row['actor_ID'] == actor]
        assert [row['text'] for row in source] == [ja, ja]
        assert [row['text'] for row in current] == [en, en]
        assert [row['text_hex'] for row in current] == [row['text_hex'] for row in known['current_consumers']]
        rows.append({'id': f'ACTOR_{actor}_PIRATE_NAME', 'actor_ID': actor, 'speaker': en, 'english': en,
                     'Japanese': ja, 'source_meaning': 'The pirate’s nickname.', 'localization_note': note,
                     'context': RESCUE, 'decision': 'retention', 'review': dict.fromkeys(GATES, True) | {'formatting': False},
                     'source_reference': source, 'current_reference': current})
    return rows


def plan(clean, ctx, manifest):
    arm, clean_arm = ctx.arm, clean.read_file(ARM)
    inventory, _, _ = scoped_inventory()
    summaries = {}
    for route, (encounter, rescue, later) in enumerate(ROUTES):
        summaries[route, encounter] = 'Aziza prepares for the encounter. Snake, Angel and Dandy answer her in their own voices.'
        summaries[route, rescue] = RESCUE
        summaries[route, later] = 'The former crew confronts Aziza again. The labels distinguish who threatens the party and who reacts when the threat turns against them.'
    contexts, occurrences = story_context(clean, ctx, summaries, LABELS)
    assert len(contexts) == 12 and all(occurrences.values())
    all_blocks = [IlnkContainer.parse(ctx.image.read_file(f'/data/SC{route}.DK4')).blocks for route in range(4)]
    original_blocks = [list(blocks) for blocks in all_blocks]
    memo = manifest['relocations'][ARM]['reviewed_name_integration']['catalog']
    catalogue(arm, memo, all_blocks)
    decisions = []
    for route, (_, block, _) in enumerate(ROUTES):
        path = f'/data/SC{route}.DK4'
        jp = IlnkContainer.parse(clean.read_file(path)).blocks[block]
        en = all_blocks[route][block]
        commands, current = raw_speeches(arm, en, inventory)
        source_commands, source = raw_speeches(clean_arm, jp, inventory)
        assert [row['word'] for row in commands] == [row['word'] for row in source_commands]
        revised = bytearray(en)
        changed = set()
        for ordinal, (s, t) in enumerate(zip(source, current, strict=True)):
            key = route, block, s['record_index']
            if key not in REVISIONS and key not in RETAINED_ORDERS:
                continue
            source_raw, en_raw = [bytes.fromhex(row['raw_hex']) for row in (s, t)]
            assert source_raw[0] == en_raw[0] == 183
            japanese = source_raw[1:].decode('cp932')
            order = key != (1, 17, 41)
            if order:
                assert japanese == ORDER_JA
                meaning = 'Angel tells the intervening man to stay out of it, then orders both him and Aziza taken out together.'
            else:
                assert '負け続け' in japanese and 'その責任' in japanese
                meaning = 'Angel blames Aziza for their losing streak and says she must answer for the money they have failed to earn.'
            previous = ' '.join(en_raw[1:].decode('ascii').split())
            english, phrases, note = REVISIONS[key] if key in REVISIONS else (previous, (), RETAINED_ORDERS[key])
            ident = f"DK4_MES_B{block}_R{s['record_index']:04d}"
            row = {'id': ident, 'file_path': path, 'route': route, 'block': block, 'ordinal': ordinal,
                   'speaker': 'Angel', 'kind': 'progressive', 'source_selector': 183,
                   'source_hex': s['raw_hex'], 'current_hex': t['raw_hex'], 'Japanese': japanese,
                   'source_reference': s, 'current_reference': t, 'context': RESCUE, 'source_meaning': meaning,
                   'localization_note': note, 'previous_English': previous,
                   'english': f'{{SPEAKER:B7}}{english}', 'review': dict.fromkeys(GATES, True) | {'formatting': False},
                   'decision': 'revision' if key in REVISIONS else 'retention'}
            if key in REVISIONS:
                words = english.split()
                protected = [phrase.split() for phrase in phrases]
                assert all(part in english for part in phrases) and ' '.join(words) == english
                row['protected_pairs'] = [(layout.prior.layout.norm(a), layout.prior.layout.norm(b))
                                          for phrase in protected for a, b in zip(phrase, phrase[1:])]
                compiled = layout.plan_record(row)
                assert compiled['expected_native_pages'] == 1
                assert all(d['code'] == 'line-break-count' and d['severity'] == 'warning'
                           for d in compiled['diagnostics']), compiled['diagnostics']
                if compiled['diagnostics']:
                    row['qa_waivers'] = ['line-break-count']
                    row['qa_waiver_reason'] = 'The automatic English layout fits the complete sentences on one native page.'
                assert all(any(phrase in line for line in compiled['lines']) for phrase in phrases), compiled['lines']
                target = bytes.fromhex(compiled['encoded_hex']).ljust(len(en_raw), b' ')
                assert len(target) == len(en_raw) and target[0] == en_raw[0]
                before, after = (blob + b'\0' for blob in (en_raw, target))
                assert all(bytes.fromhex(entry['key_hex']) + b'\0' not in (before, after, before[1:], after[1:])
                           for entry in memo['records'] if entry['route_mask'] & (1 << route))
                pos = t['offset']
                revised[pos:pos + len(en_raw)] = target
                row.update(target_hex=target.hex(), automatic_layout=compiled,
                           trailing_blank_bytes=len(target) - len(bytes.fromhex(compiled['encoded_hex'])))
                changed.add(ordinal)
            decisions.append(row)
        checked, result = raw_speeches(arm, bytes(revised), inventory)
        assert len(result) == len(current)
        fingerprint = ('offset', 'word', 'native_extent', 'ancestor_0100_offsets')
        assert [[r[k] for k in fingerprint] for r in checked] == [[r[k] for k in fingerprint] for r in commands]
        assert {i for i, (a, b) in enumerate(zip(current, result, strict=True)) if a != b} == changed
        inverse = bytearray(revised)
        for row in (row for row in decisions if row['route'] == route):
            ordinal = row['ordinal']
            row['staged_reference'] = result[ordinal]
            if ordinal in changed:
                start = current[ordinal]['offset']
                previous = bytes.fromhex(current[ordinal]['raw_hex'])
                inverse[start:start + len(previous)] = previous
                assert result[ordinal]['raw_hex'] == row['target_hex']
        assert bytes(inverse) == en
        all_blocks[route][block] = bytes(revised)
    assert [i for i, (a, b) in enumerate(zip(original_blocks, all_blocks, strict=True)) if a != b] == [0, 1]
    assert {p['route'] for p in decisions if p['decision'] == 'retention'} == {2, 3}
    catalogue(arm, memo, all_blocks)
    targets = {f'/data/SC{route}.DK4': IlnkContainer(all_blocks[route]).to_bytes() for route in (0, 1)}
    return targets, decisions, contexts, occurrences


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    r = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == r['registry_sha256'] and base.digest(CLEAN) == r['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, r['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    targets, records, contexts, occurrences = plan(clean, ctx, base.load(parent.MANIFEST))
    identities = pirate_names(ctx, clean)
    for row in identities:
        row['source_exchanges'] = occurrences[row['actor_ID']]
    changed = [row for row in records if row['decision'] == 'revision']
    assert len(changed) == 3 and len(records) == 5
    pictures = layout.native_validation(ctx, changed)
    assert len(pictures) == 6
    ROOT.mkdir()
    sheets = sheet(pictures)
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    for path, data in targets.items():
        image.replace_file(path, data)
    after = files(image)
    assert after.keys() == before.keys() and {p for p in before if before[p] != after[p]} == set(targets)
    image.save(ROM)
    for path in targets:
        image.replace_file(path, before[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    base.save(REVIEW, {'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                      'encoder': 'dialogue-relocatable-v1', 'review_gates': list(GATES),
                      'candidate_sha256': candidate, 'previous_sha256': r['candidate_sha256'],
                      'records': records, 'nameplates': identities, 'contexts': contexts,
                      'native_sheets': sheets})
    base.save(STORED, {'candidate_sha256': candidate, 'previous_sha256': r['candidate_sha256'],
                      'target_ARM9_sha256': sha(ctx.arm), 'route_archives': {p: sha(data) for p, data in targets.items()},
                      'whole_parent_inverse': True, 'sheets': sheets, 'review_sha256': base.digest(REVIEW)})
    print('Three revised pages, two retained orders and three nameplates bound to twelve exchanges.')


if __name__ == '__main__':
    main()
