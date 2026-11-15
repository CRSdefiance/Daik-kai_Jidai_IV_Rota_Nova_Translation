"""Bind32 scoped actors; reuse18 exact consumers and add14 already qualified actors."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
RELEASE = Path('work/analysis/Hodram_B151_B170_release_verified_20261102/registered_release_verification.json')
PRIOR = Path('work/analysis/Hodram_B151_B170_clean_20261102/native_identity_and_item_checkpoint_v1.json')
FRESH = Path('work/analysis/Hodram_B171_B190_new_names_20261102/names.json')


def cstring(raw, pointer):
    start = pointer - 0x02000000
    assert 0 <= start < len(raw)
    end = raw.index(0, start)
    return raw[start:end]


if __name__ == '__main__':
    output = ROOT / 'native_identity_and_term_checkpoint_v1.json'
    assert not output.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'))
    prior, fresh, source = map(load, [PRIOR, FRESH, ROOT / 'clean_name_fields.json'])
    assert fresh['runtime'] == ctx.receipt() and len(fresh['actors']) == 14
    previous_release = Path(prior['runtime']['release_proof'])
    previous = RegisteredRuntime(previous_release, Path(prior['runtime']['startup_proof']))
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    static_proof = load('work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json')
    expected, inverse = plan_static_labels(previous.arm, load(static_proof['proposal']), clean)
    assert ctx.arm == expected and ctx.actor_root == previous.actor_root and ctx.actor_bytes == previous.actor_bytes
    assert ctx.common == previous.common and ctx.image.read_file('/GRP/KANJI.FNT') == previous.image.read_file('/GRP/KANJI.FNT')
    older_path = Path('work/analysis/Hodram_B81_B90_new_names_20261101/names.json')
    older_doc = load(older_path)
    older = RegisteredRuntime(older_doc['runtime']['release_proof'], older_doc['runtime']['startup_proof'])
    assert older.actor_root == ctx.actor_root and older.actor_bytes == ctx.actor_bytes and older.common == ctx.common
    assert older.image.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')
    # This conservatively checks the complete original code/library prefix and
    # all staged runtime bytes, rather than replaying unchanged name getters.
    assert older.arm[:0x120000] == ctx.arm[:0x120000]
    old_section = bytes(MainCodeFile(older.arm, 0x02000000).sections[3].data)
    new_section = bytes(MainCodeFile(ctx.arm, 0x02000000).sections[3].data)
    stage_offset = ctx.arm.find(new_section)
    assert stage_offset >= 0 and older.arm.find(old_section) == stage_offset
    manifest_path = Path(ctx.release['manifest'])
    assert sha(manifest_path.read_bytes()) == ctx.release['manifest_sha256']
    registered = load(manifest_path)['relocations']['/__arm9__.bin']
    fields = [registered['owned_name_glyph']['proof']]
    fields += [f for key in ['owned_name_fields', 'owned_name_fields_next', 'owned_name_fields_grouped']
        for f in registered[key]['proof']['fields']]
    restored_payload = bytearray(old_section[:-48])
    staged_name_repairs = []
    for field in fields:
        offset = field['physical_offset'] - stage_offset
        if not 0 <= offset < len(restored_payload):
            continue
        old_bytes, new_bytes = bytes.fromhex(field['old_hex']), bytes.fromhex(field['new_hex'])
        assert len(old_bytes) == len(new_bytes)
        assert restored_payload[offset:offset + len(old_bytes)] in (old_bytes, new_bytes)
        restored_payload[offset:offset + len(old_bytes)] = new_bytes
        staged_name_repairs.append(dict(physical_offset=field['physical_offset'], old_hex=field['old_hex'], new_hex=field['new_hex']))
    assert bytes(restored_payload) == new_section[:-48]
    meanings = load(ROOT / 'complete_clean_meanings_before_English.json')
    prior_rows = {r['actor_ID']: r for r in prior['records']}
    table = struct.unpack_from('<I', ctx.arm, 0xCDAC0)[0] - 0x02000000
    rows = []
    for original in source['records']:
        actor = original['actor_ID']
        if actor in fresh['actors']:
            consumers = [r for r in fresh['current_names']['rows'] if r['actor_ID'] == actor]
            proof, proof_key, old = FRESH, 'current_names.rows', ctx
        elif actor in prior_rows:
            consumers = prior_rows[actor]['current_consumers']
            proof, proof_key, old = PRIOR, 'records[actor_ID].current_consumers', previous
        else:
            assert actor in [4, 26, 167]
            consumers = [r for r in older_doc['current_names']['rows'] if r['actor_ID'] == actor]
            proof, proof_key, old = older_path, 'current_names.rows', older
        assert len(consumers) == 2 and {r['consumer'] for r in consumers} == {'progressive-nameplate', 'full-catalogue'}
        at = table + 32 * actor
        assert ctx.arm[at:at + 32] == old.arm[at:at + 32]
        fields = []
        for column in [0, 4, 8]:
            field = at + column
            pointer = struct.unpack_from('<I', ctx.arm, field)[0]
            value = cstring(ctx.raw, pointer) if pointer else b''
            assert not pointer or value == cstring(old.raw, pointer)
            fields.append(dict(column=column, field_offset=field, pointer=pointer,
                field_hex=ctx.arm[field:field + 4].hex(), text=value.decode('cp932') if pointer else None, hex=value.hex()))
        rows.append(dict(actor_ID=actor, clean_fields=original['fields'], current_fields=fields,
            current_consumers=[dict(consumer=c['consumer'], text=c['text'], text_hex=c['text_hex']) for c in consumers],
            fresh_native=actor in fresh['actors'], native_proof=str(proof), native_proof_sha256=sha(proof.read_bytes()), native_key=proof_key,
            complete_current_actor_model_name_inputs_andcode_dependencies_exact=True,
            context_record_ids=[r['id'] for r in meanings['records'] if r.get('source_selector') == actor],
            scoped_name_localization_anddisplay_review_still_pending=True, regional_metadata_not_biography=True))
    assert len(rows) == 32 and sum(r['fresh_native'] for r in rows) == 14
    # Bound exact current labels without reading translated story paragraphs.
    labels = []
    for ja, field in [('新羅の金冠', 0x11EEE8), ('武寧王陵', 0x11BC60), ('京城', 0x123F34),
        ('杭州', 0x123DD8), ('スプリットセイル', 0x114E4C), ('ジガースパンカー', 0x114E50)]:
        source_pointer, pointer = [struct.unpack_from('<I', arm, field)[0] for arm in [clean, ctx.arm]]
        original = string(clean, source_pointer)
        assert original['text'] == ja
        raw = cstring(ctx.raw, pointer)
        labels.append(dict(source_Japanese=ja, field_offset=field, clean_pointer=source_pointer,
            clean_text_hex=original['hex'], current_pointer=pointer, current_complete_hex=raw.hex(), current_label=raw.decode('cp932'),
            static_native_pointer_input_binding_not_new_widget_gameplay=True))
    save(output, dict(runtime=ctx.receipt(), previous_runtime=previous.receipt(), older_three_actor_runtime=older.receipt(),
        complete_latest_static_data_inverse=inverse, all32_actor_inputs_models_COMMON_font_andname_consumer_dependencies_match=True,
        older_payload_diff_is_only_registered_owned_name_data=staged_name_repairs,
        all_other123264_staged_bytes_andoriginal_code_prefix_exact=True,
        records=rows, ordinary_actors=32, fresh_actors=14, reused_actors=18, current_native_consumer_bindings=64,
        fresh_clean_andcurrent_getters_each=28, exact_existing_consumers_reused_not_replayed=36,
        source_literal_terms=labels, FE254_not_an_ordinary_named_actor=True,
        B179_FE_woman_not_named_in_this_exchange_no_identity_orromance_invented=True,
        source_scoped_terms_andnames_still_require_editorial_decisions=True,
        prior_English_story_dialogue_unconsulted=True, no_new_global207_name_approval=True,
        new_credit=0, new_ROMs=0, new_emulator_runs=0,
        evidence={str(p): sha(p.read_bytes()) for p in [PRIOR, FRESH, older_path, ROOT / 'clean_name_fields.json',
            ROOT / 'complete_clean_meanings_before_English.json', ROOT / 'linked_B89_crown_context_v1.json', Path(__file__)]}))
    print('Bound32 actors:14 fresh/18 reused;64 current consumers andsix exact labels. No prior story English,ROM orglobal name approval.')
