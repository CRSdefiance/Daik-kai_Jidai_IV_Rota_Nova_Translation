"""Bind source identities while reusing unchanged native consumers; do not approve prose."""
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
NEW = Path('work/analysis/Hodram_B131_B150_release_verified_20261102')
OLD = Path('work/analysis/Hodram_B111_B130_release_verified_20261102')
FRESH = Path('work/analysis/Hodram_B151_B170_new_names_20261102/names.json')


def main():
    target = ROOT / 'native_identity_and_item_checkpoint_v1.json'
    assert not target.exists()
    current = RegisteredRuntime(NEW / 'registered_release_verification.json', NEW / 'own_registered_startup_verification.json')
    previous = RegisteredRuntime(OLD / 'registered_release_verification.json', OLD / 'own_registered_startup_verification.json')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    proposal = Path('work/analysis/Hodram_B131_B150_name_fields_20261102/owned_fields_proposal_v2.json')
    expected, inverse = plan_arm9_name_fields(previous.arm, load(proposal), clean)
    assert current.arm == expected and inverse['owned_span_bytes'] == 4
    assert current.actor_root == previous.actor_root and current.actor_bytes == previous.actor_bytes
    assert current.common == previous.common
    assert current.image.read_file('/GRP/KANJI.FNT') == previous.image.read_file('/GRP/KANJI.FNT')
    table = struct.unpack_from('<I', current.arm, 0xCDAC0)[0] - 0x02000000
    source = load(ROOT / 'clean_name_fields.json')
    means = load(ROOT / 'all634_clean_meanings_before_English_v1.json')
    actors = [r['actor_ID'] for r in source['records']]
    assert len(actors) == 36
    changed_owners = {o['actor'] for f in load(proposal)['fields'] for o in f['owners']}
    assert not changed_owners.intersection(actors)
    fresh = load(FRESH)
    assert fresh['runtime'] == current.receipt() and len(fresh['actors']) == 13
    paths = [Path('work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json'),
             Path('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json'),
             *[Path(f'work/analysis/{p}/names.json') for p in ['Hodram_B81_B90_new_names_20261101', 'Hodram_B91_B110_new_names_20261101', 'Hodram_B111_B130_new_names_20261101', 'Hodram_B131_B150_new_names_20261102']],
             Path('work/analysis/Hodram_B91_B110_name_native_20261101/native_name_fields_verification_reviewed.json'), FRESH]
    proofs = {}
    for path in paths:
        doc = load(path)
        if 'versions' in doc:
            rows = next(v['names']['rows'] for v in doc['versions'] if v['version'] == 'proposed')
            key = 'versions[proposed].names.rows'
        else:
            key = next(k for k in ['current_names', 'names', 'fresh_thirtytwo_progressive_andfull_current_getters'] if k in doc)
            rows = doc[key]['rows']
            key += '.rows'
        for actor in {r['actor_ID'] for r in rows}:
            proofs[actor] = (path, key, [r for r in rows if r['actor_ID'] == actor])
    rows = []
    for source_row in source['records']:
        actor = source_row['actor_ID']
        path, key, consumers = proofs[actor]
        assert {r['consumer'] for r in consumers} == {'progressive-nameplate', 'full-catalogue'}
        fields = []
        for col in [0, 4, 8]:
            at = table + 32 * actor + col
            pointer = struct.unpack_from('<I', current.arm, at)[0]
            # Registered pool strings live in the candidate's own initialized snapshot.
            if pointer:
                start = pointer - 0x02000000
                end = current.raw.index(0, start)
                raw = current.raw[start:end]
                value = dict(text=raw.decode('cp932'), hex=raw.hex(), pointer=pointer, terminated_hex=(raw + b'\0').hex())
            else:
                value = dict(text=None, hex='', pointer=0, null_component_not_empty_text=True)
            fields.append(dict(column=col, field_offset=at, field_hex=current.arm[at:at + 4].hex(), **value))
        assert current.arm[table + 32 * actor:table + 32 * (actor + 1)] == previous.arm[table + 32 * actor:table + 32 * (actor + 1)]
        rows.append(dict(actor_ID=actor, clean_fields=source_row['fields'], current_fields=fields,
                         current_consumers=[dict(consumer=r['consumer'], text=r['text'], text_hex=r['text_hex']) for r in consumers],
                         prior_native_proof=str(path), prior_native_proof_sha256=sha(path.read_bytes()), prior_native_key=key,
                         fresh_native=actor in fresh['actors'], exact_parent_32byte_metadata_unchanged=True,
                         context_record_ids=[r['id'] for r in means['records'] if r['source_selector'] == actor],
                         regional_metadata_not_biography=True, scoped_localization_and_visual_name_review_pending=True))
    # Mentioned Mivor is not an additional B161 speaker or evidence of kinship.
    clean_table = struct.unpack_from('<I', clean, 0xCDAC0)[0] - 0x02000000
    mention = dict(actor_ID=79, source_mention='ミヴォール', established_given='Mivor', appearance_not_claimed=True,
                   relationship_not_inferred=True, fields=[])
    for col in [0, 4, 8]:
        a, b = clean_table + 32 * 79 + col, table + 32 * 79 + col
        mention['fields'].append(dict(column=col, source=string(clean, struct.unpack_from('<I', clean, a)[0]),
                                      current=string(current.arm, struct.unpack_from('<I', current.arm, b)[0])))
    assert mention['fields'][0]['source']['text'] == 'ミヴォール' and mention['fields'][0]['current']['text'] == 'Mivor'
    asset_path = Path('translations/all_item_names_arm9_v1.json')
    asset = load(asset_path)
    items = []
    for ident, ja, en in [(175, '模様入りの布', 'Patterned Cloth'), (180, '儀式用の小刀', 'Ceremonial Knife'),
                          (182, '真鍮のランプ', 'Brass Lamp'), (187, '太陽紋の鞘', 'Sun-Crest Sheath')]:
        row = next(r for r in asset['records'] if r['id'] == f'DK4_ITEM_POINTER_{ident:03d}')
        at = row['offset']
        assert clean[at:at + 4] == bytes.fromhex(row['source_hex'])
        # The registered runtime pool can relocate the approved asset's pointer.
        # Bind the final native pointer and complete string, not the earlier insertion address.
        assert current.arm[at + 4:at + 24] == clean[at + 4:at + 24]
        source_name = string(clean, struct.unpack_from('<I', clean, at)[0])
        pointer = struct.unpack_from('<I', current.arm, at)[0]
        start = pointer - 0x02000000
        end = current.raw.index(0, start)
        raw = current.raw[start:end]
        assert source_name['text'] == ja and raw.decode('cp932') == row['english'] == en
        items.append(dict(item_ID=ident, approved_record=row, exact_clean_name=source_name, current_pointer=pointer,
                          current_pointer_field_hex=current.arm[at:at + 4].hex(),
                          complete_current_name_hex=raw.hex(), current_name=en, current_own_snapshot=True,
                          final_registered_pointer_bound_after_pool_relocation=True, all20_nonname_metadata_bytes_exact=True))
    zeros = [r for r in means['records'] if r['source_selector'] == 0]
    assert len(zeros) == 9 and {r['block'] for r in zeros} == {168}
    assert all(r['source_complete_preamble_hex'] == '0040ffff0000' and r['source_hex'].startswith('00') for r in zeros)
    save(target, dict(runtime=current.receipt(), previous_runtime=previous.receipt(), complete_ARM9_inverse=inverse,
                      whole_actual_actor_model_COMMON_font_exact=True, records=rows, ordinary_actor_bindings=36,
                      fresh_actors=13, reused_actors=23, fresh_clean_and_current_getter_calls_each=26,
                      reused_getters_not_reexecuted=True, mentioned_name=mention, approved_item_names=items,
                      item_asset=str(asset_path), item_asset_sha256=sha(asset_path.read_bytes()),
                      Rafael_actor0_complete_preamble_records=[dict(id=r['id'], source_reference=r['source_reference'], complete_preamble_hex=r['source_complete_preamble_hex']) for r in zeros],
                      Rafael_actor0_context_and_native_identity_bound_actual_B168_unvisited=True,
                      established_prior_identity_chain='work/analysis/Hodram_B131_B150_clean_20261102/native_identity_reuse_checkpoint.json',
                      prior_corrected_Fernando_andSamwell_consumers_preserved=True,
                      incidental_legacy_dialogue_exposure=[dict(id='DK4_MES_B151_R0005', path='scripts/materialize_hodram_deep_route_v9.py', reason='A terminology search returned this one legacy generator line after all642 clean meanings were saved; not current-ROM extraction or a prior-English conversation pass.')],
                      prior_English_conversation_comparison_not_started=True, no_new_global207_approval=True,
                      B156_cinematic_FE_geometry_andother_nonname_terms_pending=True, new_credit=0,
                      evidence={str(p):sha(p.read_bytes()) for p in [*paths, proposal, ROOT/'clean_name_fields.json', ROOT/'all634_clean_meanings_before_English_v1.json', Path(__file__)]}))
    print('Bound36 ordinary identities:13 fresh/23 reused;four exact items,Mivor andnine Rafael preambles. No prose/display approval,ROM orcredit.')


if __name__ == '__main__':
    main()
