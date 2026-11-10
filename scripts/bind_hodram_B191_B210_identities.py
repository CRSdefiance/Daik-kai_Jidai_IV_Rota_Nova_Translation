"""Bind 43 scoped actors with 15 fresh checks and 28 dependency-qualified reuses."""
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.prove_lil_B167_names_v4124b import names as original_names
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')
RELEASE = Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')
LATEST = Path('work/analysis/Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json')
PREVIOUS = Path('work/analysis/Hodram_B151_B170_clean_20261102/native_identity_and_item_checkpoint_v1.json')
FRESH = [Path('work/analysis/Hodram_B191_B210_new_names_20261104/names.json'),
    Path('work/analysis/Hodram_B191_B210_actor154_current_runtime_20261104/names.json')]
OLDER = [Path('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json'),
    Path('work/analysis/Hodram_B81_B90_new_names_20261101/names.json'),
    Path('work/analysis/Hodram_B111_B130_new_names_20261101/names.json')]


def cstring(raw, pointer):
    assert 0x02000000 <= pointer < 0x02400000
    start = pointer - 0x02000000
    return raw[start:raw.index(0, start)]


if __name__ == '__main__':
    output = ROOT / 'native_identity_checkpoint_v1.json'
    assert not output.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'))
    stage = load(ctx.release['manifest'])['relocations']['/__arm9__.bin']
    fixes = [stage['owned_name_glyph']['proof']]
    fixes += [r for key in ['owned_name_fields', 'owned_name_fields_next', 'owned_name_fields_grouped'] for r in stage[key]['proof']['fields']]
    fixes += [dict(physical_offset=r['physical_offset'], old_hex=r['parent_prefix_hex'], new_hex=r['target_prefix_hex'])
        for r in stage['owned_static_text']['proof']['complete_owned_data_plan']['fields']]
    cache, dependencies = {}, []

    def compatible(receipt):
        key = receipt['candidate_sha256']
        if key not in cache:
            old = RegisteredRuntime(receipt['release_proof'], receipt['startup_proof'])
            assert old.receipt() == receipt
            assert ctx.actor_root == old.actor_root and ctx.actor_bytes == old.actor_bytes
            assert ctx.common == old.common and ctx.image.read_file('/GRP/KANJI.FNT') == old.image.read_file('/GRP/KANJI.FNT')
            normalized = bytearray(old.arm)
            for fix in fixes:
                at = fix['physical_offset']
                before, after = bytes.fromhex(fix['old_hex']), bytes.fromhex(fix['new_hex'])
                assert len(before) == len(after) and normalized[at:at + len(before)] in (before, after)
                normalized[at:at + len(before)] = after
            assert bytes(normalized) == ctx.arm
            dependencies.append(dict(previous_runtime=receipt, complete_ARM9_diff_only_registered_owned_name_andstatic_data=True,
                whole_actor_model_COMMON_font_exact=True, normalized_ARM9_sha256=sha(normalized)))
            cache[key] = old
        return cache[key]

    candidates = {}
    for path in OLDER:
        doc = load(path)
        old = compatible(doc['runtime'])
        name_key = 'current_names' if 'current_names' in doc else 'names'
        for actor in {r['actor_ID'] for r in doc[name_key]['rows']}:
            candidates[actor] = (path, name_key + '.rows', [r for r in doc[name_key]['rows'] if r['actor_ID'] == actor], old)
    # These newer checkpoints already qualify their complete inherited chains.
    # Prefer their current values, including repaired Fernando and scoped aliases.
    for path in [PREVIOUS, LATEST]:
        doc = load(path)
        old = compatible(doc['runtime'])
        for row in doc['records']:
            candidates[row['actor_ID']] = (path, 'records[actor_ID].current_consumers', row['current_consumers'], old)
    fresh_actors = set()
    for path in FRESH:
        doc = load(path)
        assert doc['runtime'] == ctx.receipt()
        fresh_actors.update(doc['actors'])
        for actor in doc['actors']:
            candidates[actor] = (path, 'current_names.rows', [r for r in doc['current_names']['rows'] if r['actor_ID'] == actor], ctx)
    source_path = ROOT / 'clean_name_fields.json'
    means_path = ROOT / 'complete_clean_meanings_before_English.json'
    source, means = map(load, [source_path, means_path])
    table = struct.unpack_from('<I', ctx.arm, 0xCDAC0)[0] - 0x02000000
    rows = []
    for original in source['records']:
        actor = original['actor_ID']
        path, key, consumers, old = candidates[actor]
        assert len(consumers) == 2 and {r['consumer'] for r in consumers} == {'progressive-nameplate', 'full-catalogue'}
        at = table + 32 * actor
        assert ctx.arm[at:at + 32] == old.arm[at:at + 32]
        fields = []
        for column in [0, 4, 8]:
            pointer = struct.unpack_from('<I', ctx.arm, at + column)[0]
            raw = cstring(ctx.raw, pointer) if pointer else b''
            assert not pointer or raw == cstring(old.raw, pointer)
            fields.append(dict(column=column, field_offset=at + column, pointer=pointer,
                field_hex=ctx.arm[at + column:at + column + 4].hex(), text=raw.decode('cp932') if pointer else None, hex=raw.hex()))
        rows.append(dict(actor_ID=actor, clean_fields=original['fields'], current_fields=fields,
            current_consumers=[dict(consumer=r['consumer'], text=r['text'], text_hex=r['text_hex']) for r in consumers],
            fresh_native=actor in fresh_actors, native_proof=str(path), native_proof_sha256=sha(path.read_bytes()), native_key=key,
            complete_native_dependencies_andboth_consumer_inputs_qualified=True,
            context_record_ids=[r['id'] for r in means['records'] if r.get('source_selector') == actor],
            regional_metadata_not_biography=True, contextual_name_localization_anddisplay_pending=True))
    assert len(rows) == 43 and sum(r['fresh_native'] for r in rows) == 15
    # One small source-selector voice batch uses the current own snapshot;
    # inherited name getters are not replayed merely to obtain voice classes.
    precedent = load('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json')
    env = dict(original_names.__globals__)
    exec(compile(precedent['source_owned_voice_function'], __file__ + '::current-voices', 'exec'), env)
    voices = ctx.execute(env['selectors'], [r['actor_ID'] for r in rows])
    save(output, dict(runtime=ctx.receipt(), ordinary_actor_bindings=43, current_name_consumer_bindings=86,
        fresh_actors=15, reused_actors=28, fresh_clean_andcurrent_getters_each=30, unchanged_getters_reused_not_replayed=56,
        actor154_fresh_reason='Its available standalone native proof predates the registered runtime-bound repair; use two fresh current consumers rather than infer compatibility from a count of executed instructions.',
        records=rows, voices=voices, dependency_reuse_proofs=dependencies,
        no_prior_current_ROM_English_story_extraction=True, no_new_name_mutation_or_global207_approval=True,
        native_checks_not_new_gameplay=True, source_context_andterm_localization_gates_pending=True,
        new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [LATEST, PREVIOUS, *FRESH, *OLDER, source_path, means_path, Path(__file__)]}))
    print('Bound 43 actors/86 consumers: 15 fresh and 28 exact reuses. Current voices checked; no prose, ROM or completion credit.')
