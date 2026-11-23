"""Rebind the default name decisions and prepare nine checks in both Deck panels."""

import re
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_genoa_tomato_exchange_20261120 as head
from scripts import review_hostess_and_follower_names_20261115 as generic
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_barmaid_town_labels_20261115 import read_static
from scripts.review_town_role_labels_20261115 import story_context
from scripts.stage_town_trend_exchanges_20261115 import IlnkContainer


base = head.base
ROOT = Path('work/named_actor_catalogue_20261120')
DRAFT, BINDINGS = ROOT / 'draft.json', ROOT / 'bindings.json'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
CONSUMERS = ('progressive-nameplate', 'full-catalogue')
PATTERN = re.compile(r'(name|role).*(final|review|manifest)|(final|review|manifest).*name', re.IGNORECASE)
EXCHANGES = {
    (0, 37): 'Rafael argues for passage through Hayreddin’s waters. Salid taunts him and objects when Hayreddin decides to let him pass.',
    (0, 65): 'Charlotte questions Rafael’s plans for a village market, especially the labor, wages and materials.',
    (0, 66): 'Rafael brings the promised wood. Charlotte thanks him and commits to building the market.',
    (0, 147): 'Uddin asks Rafael to consider an alliance overnight. Ibn Niyadi directs Rafael to the accommodations Uddin arranged.',
    (0, 148): 'Uddin asks to hear Rafael’s decision. On acceptance, Ibn Niyadi acknowledges the order to show him into the reception room.',
    (1, 140): 'Escante seeks Hodram’s help against Maldonado. Jorge objects to Hodram’s tone before Escante takes over.',
}
DECISIONS = {
    32: ('Paolo Centurione', 'Keep Paolo with Centurione. It matches the original name components and distinguishes his identity '
         'from Paulo Morais. The surname also matches the established Centurione Company.'),
    45: ('Charles Gilban', 'Keep the given name and the existing Latin spelling of ギルバン. The surname distinguishes this '
         'record from Charles Rochefort. No extra middle name appears in the Japanese fields.'),
    46: ('Paulo Morais', 'Retain Paulo for パウロ and Morais for モライス. The source distinguishes the given name from Paolo, '
         'and the existing Latin spelling gives both components without expanding either.'),
    50: ('Enzo Regioni', 'Keep Enzo for エンツォ and the established Regioni for レジオーニ. Both consumers present the same '
         'personal name, with no additional source component.'),
    51: ('Salid Ajar', 'Keep Salid, the name Hayreddin uses when telling him to wait. Ajar preserves the second source '
         'component. The scene supplies his allegiance without adding a formal rank to his nameplate.'),
    54: ('Ibn Niyadi', 'Keep both parts of the source name in their stored order. The short, courteous replies identify '
         'the same person at both of Uddin’s meetings and supply no title to append.'),
    58: ('Jorge Albacete', 'Keep the two Spanish name components. The portrait label identifies the speaker of the single '
         'protective interjection while Escante and Hodram negotiate. It need not name an office or rank.'),
    77: ('Akaboo Damai', 'Keep the project spelling for アカブー and ダーマイー in both getters. The two components identify '
         'one actor. The available source fields give no additional Latin form or title.'),
    80: ('Charlotte Miller', 'Keep Charlotte, the name Rafael uses directly, and Miller for the separate source field. '
         'The market exchange establishes her practical role without turning it into a title or inventing a relationship.'),
}


def compared_forms(row):
    approved = row.get('approved_forms')
    if isinstance(approved, dict) and all(k in approved for k in CONSUMERS):
        return tuple(approved[k] for k in CONSUMERS)
    items = row.get('proposed_consumers', row.get('current_consumers', []))
    by_kind = {r.get('consumer'): r.get('text') for r in items if isinstance(r, dict)} if isinstance(items, list) else {}
    return tuple(by_kind.get(k) for k in CONSUMERS)


def field_signature(row):
    fields = row.get('source_andcurrent_fields')
    if fields is None:
        reference = row.get('source_reference')
        fields = reference.get('fields', []) if isinstance(reference, dict) else []
    if not isinstance(fields, list):
        return []
    clean = [r.get('source', r) for r in fields if isinstance(r, dict)]
    return [(r.get('field_offset'), r.get('pointer'), r.get('hex')) for r in clean if isinstance(r, dict)]


def prior_personal_decisions(forms, signatures):
    found = {}
    paths = sorted(Path('translations').glob('*.json'))
    for path in paths:
        if not PATTERN.search(path.stem):
            continue
        root = base.load(path)
        if not isinstance(root, dict) or not isinstance(root.get('records'), list):
            continue
        for row in root['records']:
            if not isinstance(row, dict):
                continue
            ident, review = row.get('actor_ID'), row.get('review')
            if type(ident) is not int or ident not in forms or ident in found or not isinstance(review, dict):
                continue
            note = row.get('localization_note', row.get('retention_reason'))
            if (all(review.get(k) is True for k in GATES) and row.get('context') and note
                    and compared_forms(row) == forms[ident] and field_signature(row) == signatures[ident]):
                found[ident] = dict(path=path.as_posix(), sha256=base.digest(path), record=row['id'],
                                    retained_or_registered_wording=note, gates={k: review[k] for k in GATES})
    return found


def main():
    assert not ROOT.exists()
    release = base.load(head.RELEASE)
    ledger = base.load(base.LEDGER)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(head.ROM) == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    clean_path = head.stage.original.CLEAN
    assert base.digest(clean_path) == release['clean_input_sha256']
    clean = base.NdsImage.open(clean_path)
    arm_path = head.stage.original.ARM
    clean_arm = clean.read_file(arm_path)
    ctx = RegisteredRuntime(head.RELEASE, release['own_registered_startup'], captain=3)
    runtime = ctx.receipt()
    inventory = base.load(names.INVENTORY)
    getters = names.current_getters(ctx)['rows']
    assert len(getters) == 414 and inventory['clean_ARM9_sha256'] == sha256(clean_arm).hexdigest()
    forms, signatures, fields = {}, {}, {}
    for ident, prior in enumerate(inventory['records']):
        assert prior['actor_ID'] == ident
        rows = getters[2 * ident:2 * ident + 2]
        assert all(r['actor_ID'] == ident for r in rows)
        fields[ident] = []
        for column, record in enumerate(prior['clean_actor_table_fields']):
            offset = names.TABLE + ident * 32 + column * 4
            assert offset == record['ARM9_pointer_field_offset']
            clean_pointer, pointer = [unpack_from('<I', arm, offset)[0] for arm in (clean_arm, ctx.arm)]
            original = read_static(clean_arm, offset) if clean_pointer else None
            assert ctx.raw[offset:offset + 4] == ctx.arm[offset:offset + 4]
            current = None
            if pointer:
                at = pointer - names.BASE
                assert 0 <= at <= len(ctx.raw) - 96
                raw = ctx.raw[at:ctx.raw.index(0, at, at + 96)]
                current = dict(pointer=pointer, hex=raw.hex(), text=raw.decode('cp932'))
            expected = record['clean']
            assert (original is None) == (expected is None)
            if original:
                assert (original['pointer'], original['hex']) == (expected['pointer'], expected['hex'])
            fields[ident].append(dict(field=record['field'], offset=offset, clean=original, current=current))
        if ident < 82:
            forms[ident] = tuple(r['text'] for r in rows)
            signatures[ident] = [(f['offset'], f['clean']['pointer'] if f['clean'] else 0,
                                  f['clean']['hex'] if f['clean'] else '') for f in fields[ident]]
    carried = prior_personal_decisions(forms, signatures)
    assert set(forms) - carried.keys() == DECISIONS.keys(), sorted(set(forms) - carried.keys())

    # Rebind the already completed role and hostess reviews to both current default getters.
    prior_generic = base.load(generic.FINAL)
    generic_decisions = generic.prior_decisions(inventory, getters)
    for row in prior_generic['records']:
        ident = row['actor_ID']
        assert ident not in generic_decisions and all(row['review'][g] for g in GATES)
        assert tuple(c['text'] for c in getters[2 * ident:2 * ident + 2]) == (row['english'],) * 2
        generic_decisions[ident] = dict(english=row['english'], catalogue_english=row['english'],
                                       precedent=str(generic.FINAL), precedent_sha256=base.digest(generic.FINAL), record=row['id'])
    assert set(generic_decisions) == set(range(82, 207))

    contexts, speaker_blocks = story_context(clean, ctx, EXCHANGES, DECISIONS)
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    actor_bytes = bytes(cpu.mem_read(ctx.actor_root, 0x1A04))
    speech_census = {i: [] for i in DECISIONS}
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        for block, raw in enumerate(IlnkContainer.parse(clean.read_file(path)).blocks):
            for ident in DECISIONS:
                marker = bytes.fromhex('0040ffff00') + bytes([ident])
                count = raw.count(marker)
                if count:
                    speech_census[ident].append(dict(file_path=path, block=block, matching_preambles=count))
    draft = []
    for ident, (english, note) in DECISIONS.items():
        assert forms[ident] == (english, english)
        ref = fields[ident]
        segments = [f['clean']['text'] for f in ref if f['clean']]
        assert len(segments) == 2
        actual_sources = speaker_blocks.get(ident, [])
        faction = get(0x7E958, ctx.actor_root + 4 + ident * 32)
        scope = (' '.join(contexts[key]['summary'] for key in actual_sources) if actual_sources else
                 'The original actor getter supplies this name. No exact static speech preamble for this actor was found '
                 'in the four retail archives. The source identifies them without a dialogue assignment in this search.')
        draft.append(dict(id=f'ACTOR_{ident:03d}_DEFAULT_NAME', actor_ID=ident, speaker=english, english=english,
                          source_meaning=' / '.join(segments), context=scope, decision='retention',
                          localization_note=note, review=dict.fromkeys(GATES, True) | {'formatting': False},
                          current_reference={'candidate_sha256': runtime['candidate_sha256'], 'file_path': arm_path},
                          fields=ref, current_consumers=getters[2 * ident:2 * ident + 2], default_faction_index=faction,
                          representative_complete_exchanges=actual_sources, static_source_speech_census=speech_census[ident]))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == actor_bytes and not provider.reads
    ROOT.mkdir()
    base.save(DRAFT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), runtime=runtime, records=draft,
        earlier_personal_name_decisions=carried, earlier_role_and_hostess_decisions=generic_decisions,
        clean_and_current_actor_fields=fields, complete_exchanges=contexts, default_getters_verified=414))
    base.save(BINDINGS, dict(runtime=runtime, records=[dict(actor_ID=r['actor_ID'], current_consumers=r['current_consumers'])
                                                      for r in draft]))
    print('Bound 198 prior decisions and prepared nine focused native display checks.')


if __name__ == '__main__':
    main()
