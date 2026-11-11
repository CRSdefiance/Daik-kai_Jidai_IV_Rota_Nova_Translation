"""Bind the current actor inventory and review a group of shared nameplates."""

from contextlib import redirect_stdout
from hashlib import sha256
from inspect import getsource
from io import StringIO
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.script.common_message_table import common_message_entries
from scripts import prove_lil_B167_names_v4124b as original_names
from scripts import register_visible_gallery_captions_v1 as current
from scripts.audit_native_given_name_table import ordinary_getter, string
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
TRANSLATIONS = Path('translations')
CHECKPOINT = TRANSLATIONS / 'editorial_checkpoints/SharedText_20261110_v1'
INVENTORY = CHECKPOINT / 'actor_name_inventory_current_v1.json'
MANUSCRIPT = CHECKPOINT / 'shared_occupational_nameplates_context_v1.json'
BINDINGS = Path('work/shared_occupational_nameplates_20261111_v1')
TABLE = 0x120B80
GETTERS = (('progressive-nameplate', 0x7ED88), ('full-catalogue', 0x7EDD4))
GATES = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
TOWN = TRANSLATIONS / 'primary_town_services_contextual_final_review_v1.json'
SAILOR = TRANSLATIONS / 'hodram_B61_B70_speaker_name_review_v1.json'
PREVIOUS = (
    TRANSLATIONS / 'square_shopkeeper_labels_contextual_final_review_v1.json',
    TRANSLATIONS / 'generic_speaker_labels_manuscript_v2.json',
    TRANSLATIONS / 'shady_man_label_manuscript_v2.json',
)
DECISIONS = (
    (range(92, 95), '酒場の親父', 'Barkeep', 'The tavern keeper who greets customers, takes drink orders and bills for drinks.',
     'Barkeep is a natural occupational label that matches both the formal and casual greetings. The familiar Japanese form carries no family relationship.', tuple(range(50, 62))),
    (range(104, 109), '交易所の親父', 'Trader', 'The trading-house proprietor who greets customers, bargains and confirms the transaction.',
     'Trader identifies the person handling the deal. The trading-house screen supplies the location. The Japanese address implies no kinship.', tuple(range(8, 27))),
    (range(113, 120), '出港所の兄貴', 'Port Worker', 'The departure-dock attendant who warns about shortages or damage and offers resupply.',
     'Port Worker fits the attendant’s duties across the departure and resupply branches. The familiar Japanese label supplies no evidence of rank or a sibling relationship.', tuple(range(27, 50))),
)


def native_clean_roles(arm):
    cpu = machine_for(arm)
    root = unpack_from('<I', arm, 0xCB18C)[0]
    for ident in range(82, 207):
        ordinary_getter(arm, ident, cpu)
        actor = root + 4 + ident * 32
        results = []
        for consumer, offset in GETTERS:
            cpu.reg_write(UC_ARM_REG_R0, actor)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_LR, STOP)
            cpu.emu_start(BASE + offset, STOP, count=1000)
            assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
            result = string(arm, cpu.reg_read(UC_ARM_REG_R0))
            assert result['status'] == 'printable-static-string'
            results.append(result | dict(consumer=consumer, getter=BASE + offset))
        yield ident, results


def current_getters(ctx):
    source = checked_text(getsource(original_names.names), {
        'for ident in [2,4,13,23,109]:': 'for ident in range(207):',
        'actor = root+4+32*ident': 'actor = root+0x19E4 if ident==3 else root+4+32*ident',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact=True':
            'all_414_original_consumers_and_owned_or_readonly_memory_paths_exact=True',
    })
    env = vars(original_names).copy()
    exec(compile(source, __file__ + '::exact-all-actor-getters', 'exec'), env)
    with redirect_stdout(StringIO()):
        proof = ctx.execute(env['names'])
    assert len(proof['rows']) == 414 and proof['all_414_original_consumers_and_owned_or_readonly_memory_paths_exact']
    return proof


def bind_context(clean, town):
    refs = {row['message_id']: row for row in base.load(TOWN)['records']}
    results = []
    for ident in town:
        row = refs[ident]
        entry = clean[ident]
        assert entry.text.hex() == row['source_hex']
        assert row['message_id'] in row['full_exchange_native_IDs']
        results.append(dict(id=row['id'], source_reference=row['source_reference'], source_hex=row['source_hex'],
            source_Japanese=entry.text.decode('cp932')))
    return results


def main():
    assert not any(path.exists() for path in (INVENTORY, MANUSCRIPT, BINDINGS))
    release = base.load(current.RELEASE)
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(current.CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(current.CLEAN)
    arm = clean.read_file(current.ARM)
    assert unpack_from('<I', arm, 0xCDAC0)[0] == unpack_from('<I', ctx.arm, 0xCDAC0)[0] == BASE + TABLE
    assert arm[0x7ED88:0x7EE08] == ctx.arm[0x7ED88:0x7EE08]
    clean_roles = dict(native_clean_roles(arm))
    proof = current_getters(ctx)
    runtime = ctx.receipt()
    fields = ('primary', 'secondary', 'middle')
    rows = []
    for ident in range(207):
        offset = TABLE + ident * 32
        names = proof['rows'][ident * 2:ident * 2 + 2]
        assert all(name['actor_ID'] == ident and name['text'].isascii() and name['text'].isprintable() for name in names)
        source_fields = []
        for index, field in enumerate(fields):
            at = offset + index * 4
            src, target = (unpack_from('<I', data, at)[0] for data in (arm, ctx.arm))
            assert not src or string(arm, src)['status'] == 'printable-static-string'
            source_fields.append(dict(field=field, ARM9_pointer_field_offset=at, clean=string(arm, src) if src else None,
                                      current_pointer=target))
        rows.append(dict(actor_ID=ident, clean_actor_table_fields=source_fields,
                         clean_ordinary_role_consumers=clean_roles.get(ident), current_consumers=names))

    previous = []
    for path in PREVIOUS:
        for record in base.load(path)['records']:
            ident = record['actor_ID']
            row = rows[ident]
            assert all(record['review'].values())
            assert {n['text'] for n in row['current_consumers']} == {record['english']}
            assert {n['text'] for n in row['clean_ordinary_role_consumers']} == {record['source_Japanese']}
            assert row['clean_actor_table_fields'][0]['clean']['pointer'] == record['source_reference']['pointer']
            previous.append(dict(actor_ID=ident, name=record['english'], historical_review=path.as_posix(),
                                 historical_record=record['id'], historical_review_sha256=base.digest(path)))
    assert len(previous) == 14
    common = common_message_entries(clean.read_file(current.COMMON), arm)
    contexts, reviewed = {}, []
    for ids, japanese, english, meaning, note, context_ids in DECISIONS:
        key = english.lower().replace(' ', '_')
        contexts[key] = dict(file_path=current.COMMON, whole_context=bind_context(common, context_ids), review=TOWN.as_posix())
        for ident in ids:
            row = rows[ident]
            assert [n['text'] for n in row['clean_ordinary_role_consumers']] == [japanese] * 2
            assert [n['text'] for n in row['current_consumers']] == [english] * 2
            reviewed.append(dict(id=f'ACTOR_{ident}_OCCUPATIONAL_LABEL', actor_ID=ident, english=english, speaker=english,
                source_meaning=meaning, context=key, localization_note=note, decision='retention', review=GATES.copy(),
                source_reference=row['clean_ordinary_role_consumers'], current_consumers=row['current_consumers']))
    sailor = next(row for row in base.load(SAILOR)['records'] if row['actor_ID'] == 154)
    contexts['sailor_and_retainer'] = dict(file_path='/data/SC1.DK4', sample_exchange_block=63,
        exact_actor154_occurrences=sailor['source_dialogue_occurrences'], review=SAILOR.as_posix(),
        other_variants='The same native override spans actors 151–159; no shared scene role is assigned beyond the Japanese names.')
    for ident in range(151, 160):
        row = rows[ident]
        assert [n['text'] for n in row['clean_ordinary_role_consumers']] == ['水夫', '配下']
        assert [n['text'] for n in row['current_consumers']] == ['Sailor', 'Retainer']
        reviewed.append(dict(id=f'ACTOR_{ident}_SAILOR_AND_RETAINER', actor_ID=ident, english='Sailor', speaker='Sailor',
            source_meaning='The progressive header identifies a sailor. The catalog describes a retainer.', context='sailor_and_retainer',
            localization_note='Sailor reads naturally above a speaker’s dialogue. Retainer preserves the separate catalog description of a person in another’s service. Neither adds a rank or a personal identity.',
            catalogue_english='Retainer', decision='retention', review=GATES.copy(),
            source_reference=row['clean_ordinary_role_consumers'], current_consumers=row['current_consumers']))
    assert len(reviewed) == 24
    for row in reviewed:
        row['current_reference'] = dict(candidate_sha256=release['candidate_sha256'], ARM9_sha256=sha256(ctx.arm).hexdigest())
    dependencies = {path.as_posix(): base.digest(path) for path in (TOWN, SAILOR, *PREVIOUS, Path(__file__))}
    base.save(INVENTORY, dict(runtime=runtime, clean_ARM9_sha256=sha256(arm).hexdigest(), actor_count=len(rows),
        current_original_getter_count=414, clean_original_ordinary_role_getter_count=len(clean_roles) * 2,
        current_executed_instruction_addresses=proof['current_executed_instruction_addresses'], records=rows,
        historical_label_reviews_reconciled=previous, prior_name_review_credit_unchanged=True,
        context_scope='Current getters use the exact registered startup snapshot with Maria as the player. Clean role getters use ordinary constructed actor fixtures.',
        all_414_current_default_name_outputs_printable_ASCII=True, aliases_and_custom_names_separate=True, new_gameplay=False))
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), runtime=runtime, records=reviewed, contexts=contexts,
        inventory=INVENTORY.as_posix(), inventory_sha256=base.digest(INVENTORY), evidence=dependencies,
        catalog_layout_gameplay_unvisited=True, new_dialogue_credit=0, full_goal_complete=False))
    BINDINGS.mkdir()
    base.save(BINDINGS / 'display_bindings.json', dict(runtime=runtime, records=[
        dict(actor_ID=row['actor_ID'], current_consumers=row['current_consumers']) for row in reviewed]))
    print('Bound 414 current names and 250 clean role labels. Reconciled 14 prior labels and recorded 24 current contextual retentions.')


if __name__ == '__main__':
    main()
