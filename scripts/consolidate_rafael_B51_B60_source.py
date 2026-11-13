"""Bind the next245 source meanings to exact names and source event membership."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

RELEASE = Path('work/analysis/Rafael_B36_B41_release_verified_20261104/registered_release_verification.json')
OLD = Path('work/analysis/Hodram_B191_B210_clean_20261104/native_identity_checkpoint_v1.json')
FRESH = Path('work/analysis/Rafael_B51_B60_new_name_bindings_20261104/names.json')
TUTORIAL = Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json')
RAFAEL = Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json')


def cstring(raw, pointer):
    if not pointer:
        return b''
    start = pointer - 33554432
    assert 0 <= start < len(raw)
    return raw[start:raw.index(0, start)]


if __name__ == '__main__':
    output = ROOT / 'B51_B60_source_identity_checkpoint_v1.json'; assert not output.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'), captain=0)
    old, fresh, tutorial, prior = map(load, [OLD, FRESH, TUTORIAL, RAFAEL])
    previous = RegisteredRuntime(old['runtime']['release_proof'], old['runtime']['startup_proof'], captain=1)
    assert previous.receipt() == old['runtime'] and previous.arm == ctx.arm and previous.common == ctx.common
    assert previous.image.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')
    assert previous.actor_root == ctx.actor_root
    for doc in [fresh, tutorial, prior]:
        assert doc['runtime']['ARM9_sha256'] == sha(ctx.arm) and doc['runtime']['COMMON_sha256'] == sha(ctx.common)
    candidates = {r['actor_ID']: (r['current_consumers'], OLD) for r in old['records']}
    for doc, key, path in [(prior, 'current_names', RAFAEL), (fresh, 'current_names', FRESH)]:
        for actor in doc['actors']:
            candidates[actor] = ([r for r in doc[key]['rows'] if r['actor_ID'] == actor], path)
    for actor in {r['actor_ID'] for r in tutorial['consumer_bindings']}:
        candidates[actor] = ([r for r in tutorial['consumer_bindings'] if r['actor_ID'] == actor], TUTORIAL)
    paths = [ROOT / 'B51_B59_146_clean_meanings_v1.json', ROOT / 'B60_99_clean_meanings_v1.json']
    rows = [r for p in paths for r in load(p)['records']]
    assert len(rows) == 245 and len({r['id'] for r in rows}) == 245
    actors = sorted({r['source_selector'] for r in rows} - {254})
    clean = NdsImage.open('work/clean.nds'); clean_arm = clean.read_file('/__arm9__.bin')
    clean_table, table = [struct.unpack_from('<I', arm, 0xCDAC0)[0] - 33554432 for arm in [clean_arm, ctx.arm]]
    bindings = []
    for actor in actors:
        consumers, path = candidates[actor]
        assert len(consumers) == 2 and {r['consumer'] for r in consumers} == {'progressive-nameplate', 'full-catalogue'}
        if path == OLD:
            start = 4 + 32 * actor
            assert ctx.actor_bytes[start:start + 32] == previous.actor_bytes[start:start + 32]
        fields = []
        for column in [0, 4, 8]:
            at, clean_at = table + 32 * actor + column, clean_table + 32 * actor + column
            pointer, clean_pointer = struct.unpack_from('<I', ctx.arm, at)[0], struct.unpack_from('<I', clean_arm, clean_at)[0]
            value, source = cstring(ctx.raw, pointer), cstring(clean_arm, clean_pointer)
            if path == OLD:
                assert value == cstring(previous.raw, pointer)
            fields.append(dict(column=column, current_field=at, current_pointer=pointer, current_hex=value.hex(),
                source_field=clean_at, source_pointer=clean_pointer, source_hex=source.hex(), source_text=source.decode('cp932')))
        bindings.append(dict(actor_ID=actor, current_consumers=[{k:r[k] for k in ['consumer','text','text_hex']} for r in consumers],
            source_andcurrent_fields=fields, native_proof=str(path), native_proof_sha256=sha(path.read_bytes()),
            new_native=path == FRESH, full_catalogue_UI_unvisited=True))
    events_bytes = clean.read_file('/data/EV0.DK4'); events = parse_events(events_bytes)
    events_bound = []
    for block in range(51, 61):
        selected = [r for r in events if r['script_block'] == block]
        dependencies = {v for r in selected for v in r['must_be_completed'] + r['must_not_be_completed'] if v != 65535}
        events_bound.append(dict(block=block, events=selected, prerequisites=[r for r in events if r['event_ID'] in dependencies],
            numeric_block_order_not_chronology=True, natural_activation_unvisited=True))
    save(output, dict(runtime=ctx.receipt(), records=rows, actors=actors, name_bindings=bindings,
        fresh_actors=7, fresh_clean_andcurrent_consumers_each=14, qualified_reused_actors=11,
        prior_captain1_only_used_for_intrinsic_names_with_complete_ARM9_COMMON_font_andscoped_actor_objects_andfield_inputs_equal=True,
        whole_actor_array_not_assumed_equal_across_different_protagonists=True,
        current_captain0_context_exact=True, source_event_context=events_bound, source_EV0_sha256=sha(events_bytes),
        source_meanings=245, current_story_English_unconsulted=True, native_controls_branches_display_andlocalization_pending=True,
        no_global_name_approval_orROM_orcompletion_credit=True, new_credit=0, guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RELEASE, RELEASE.with_name('own_registered_startup_verification.json'),
            OLD, FRESH, TUTORIAL, RAFAEL, *paths, Path(__file__)]}))
    print('Bound245 clean meanings/18 source identities:7 fresh and11 exact-reused actors;events bound,zero credit.')
