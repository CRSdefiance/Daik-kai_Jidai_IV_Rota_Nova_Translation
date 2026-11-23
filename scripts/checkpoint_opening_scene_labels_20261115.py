"""Bind the remaining opening-label drafts to observed title artwork where possible."""

from hashlib import sha256
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_opening_scene_labels_20261115 as replay
from scripts.seal_shared_text_source_v1 import reference


base, current = replay.base, replay.current
MANUSCRIPT = Path('translations/common_scene_labels_manuscript_v2.json')
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/opening_scene_labels_20261115_v1.json')
MOVIE = '/FLS/M28.fls'
IDS = set(range(3570, 3607))
GROUPS = (
    ((3570, 3573), (168, 169), 'Closing flash and ensemble artwork. Both stored finale variants remain distinct.'),
    ((3571,), (1, 2, 3), 'Sunlight on the sea at the beginning of the title movie.'),
    ((3572, 3593), range(7, 11), 'Rafael picks up and holds a tomato. The two stored labels are identical.'),
    ((3574, 3592), (23, 24), 'Shipboard members and Hodram’s face in his title-movie section.'),
    ((3575, 3576), (47, 48), 'Port approach and the painting of Lil running with Camille.'),
    ((3579,), (73,), 'Armed riders and burning buildings in the village sequence.'),
    ((3580, 3606), range(74, 78), 'Sera’s face, headpiece and hair. The two Gallery portraits confirm her identity.'),
    ((3581, 3582), range(78, 84), 'Maria beside the rose across the focus change and matching side strips.'),
    ((3583,), range(84, 149), 'The figures appear one by one in the group portrait over a map.'),
    ((3584,), (149,), 'Irene stands beside the shelves in the study.'),
    ((3585,), (150,), 'A single dagger lies on a wooden surface. The asset supplies no personal ownership.'),
    ((3586,), (151,), 'Close-up of the map after the dagger. No region is named in the label.'),
    ((3587,), range(152, 156), 'The anchor emerges from the water next to the hull.'),
    ((3588,), (156,), 'The canvas unfurls before the departure view.'),
    ((3589,), (157,), 'The vessel sails out.'),
    ((3590,), (158, 159), 'The ship against an orange sky before the move to night.'),
    ((3591,), (160, 161), 'The ship beneath a moonlit sky, with a matching side strip.'),
    ((3598, 3599, 3600), (4, 5), 'The main logo and Rota Nova subtitle have their own texture planes. Three labels do not identify two exact variants.'),
    ((3601, 3602), range(11, 23), 'Rafael Castor appears progressively, ending on texture 22.'),
    ((3603, 3604), range(25, 47), 'Hodram Joakim Bergstrom appears progressively, ending on texture 46.'),
    ((3605,), range(49, 73), 'Lil Argot and Camille Overijssel have a shared animated name plane, ending on texture 72.'),
)


def sha(data):
    return sha256(data).hexdigest()


def captures(case, release, historical):
    folder = replay.ROOT / case
    report_path = folder / 'capture/capture_report.json'
    inputs, frames, end, _, _ = replay.schedule(case)
    report = base.load(report_path)
    trace = base.load(folder / 'requests.json')
    assert report['ROM_sha256'] == release['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert not report['callback_errors'] and report['scripted_input_schedule'] == inputs
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    requests = trace['source_requests']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert trace['callbacks'] == len(requests) and not any(row['message_ID'] in IDS for row in requests)
    assert base.digest(folder / 'source_contract.json') == trace['source_contract_sha256']
    assert base.digest(historical['path']) == historical['sha256']
    older = {row['frame']: row for row in base.load(historical['path'])['frames_captured']}
    now = {row['frame']: row for row in report['frames_captured']}

    def upper(row):
        assert base.digest(row['path']) == row['PNG_sha256']
        with Image.open(row['path']) as image:
            return image.convert('RGB').crop((0, 0, 256, 192)).tobytes()

    comparisons = []
    for n in frames:
        pixels = upper(now[n])
        comparisons.append(dict(frame=n, current=now[n], historical=older.get(n),
            match=None if n not in older else pixels == upper(older[n])))
    expected = frames if case == 'title' else [2908, 3000, 3141]
    assert [row['frame'] for row in comparisons if row['match']] == expected
    if case == 'rafael':
        assert [(row['message_ID'], row['PC']) for row in requests] == [(120, 0x0205528C), (120, 0x020534F4)]
        assert requests[0]['frame'] == requests[1]['frame'] == 1800
    return dict(control_only=True, frames=end, exact_historical_upper_frames=expected,
        held_frames=comparisons, requests=requests, target_requests=0, source_contract=trace['source_contract_sha256'],
        evidence={str(path): base.digest(path) for path in
                  (report_path, folder / 'requests.json', folder / 'terminal.json')})


def main():
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    arm_path, common = current.stage.ARM, current.stage.COMMON
    source_arm, arm = clean.read_file(arm_path), active.read_file(arm_path)
    source = common_message_entries(clean.read_file(common), source_arm)
    current_rows = owned_entries(active.read_file(common), arm, sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    scene = FlsArchive(clean.read_file(MOVIE))
    animation = FlsArchive(active.read_file(MOVIE))
    assert scene.count == animation.count == 170
    changed = set()
    for index in range(scene.count):
        assert scene.records[index][:4] == animation.records[index][:4]
        before, after = scene.texture(index), animation.texture(index)
        assert (before.width, before.height, before.palette) == (after.width, after.height, after.palette)
        if before.indices != after.indices:
            changed.add(index)
    pre = replay.TITLE.with_name('preflight.json')
    route_pre = replay.ROUTES.with_name('preflight.json')
    proof_path = replay.TITLE.with_name('opening_composition_proof.json')
    route_proof = replay.ROUTES.with_name('route_opening_movie_proof.json')
    old_proof, route = map(base.load, (proof_path, route_proof))
    assert base.digest(replay.TITLE) == old_proof['results_sha256']
    assert changed == set(map(int, base.load(replay.TITLE)['opaque_English_boundary_controls']))
    asset_hashes = {path: sha(active.read_file(path)) for path in (MOVIE, '/FLS/M20.fls')}
    assert asset_hashes[MOVIE] == base.load(pre)['opening_movie_sha256']
    assert asset_hashes['/FLS/M20.fls'] == base.load(route_pre)['movies']['/FLS/M20.fls']
    title = captures('title', release, old_proof['reports']['baseline'])
    rafael = captures('rafael', release, route['reports']['rafael']['baseline'])
    frame_by_asset = replay.title_frames()
    pairs = {ident: (list(indices), note) for ids, indices, note in GROUPS for ident in ids}
    assert set(pairs) == IDS - {3577, 3578, 3594, 3595, 3596, 3597}
    manuscript = base.load(MANUSCRIPT)['records']
    book = manuscript[-len(IDS):]
    assert {row['message_ID'] for row in book} == IDS
    rows = []
    for row in book:
        number = row['message_ID']
        original, stored = source[number], current_rows[number]
        assert original.text == stored.text == bytes.fromhex(row['source_hex'])
        assert row['source_reference'] == reference(original)
        indices, context = pairs.get(number, ([], 'An individual asset match remains unproved.'))
        assets = None if not indices else dict(path=MOVIE, related_texture_indices=indices,
            exact_label_to_texture_pointer_proven=False, visual_basis=context,
            current_representative_frames=sorted({frame_by_asset[n] for n in indices if n in frame_by_asset}))
        rows.append(dict(message_ID=number, source_reference=reference(original), current_reference=reference(stored),
            current_hex=stored.text.hex(), source_Japanese=row['source_Japanese'], English_draft=row['english'],
            artwork_association=assets, original_title_and_Rafael_COMMON_requests=0,
            recommendation='retain draft', reason=row['localization_note'],
            review=row['review'], other_display_owners_open=True))

    for path in ('/evstill/evstill016.pxl', '/evstill/evstill044.pxl'):
        source_row = next(row for row in manuscript if row['artwork'] and row['artwork']['path'] == path)
        assert sha(clean.read_file(path)) == source_row['artwork']['sha256'] == sha(active.read_file(path))
        asset_hashes[path] = source_row['artwork']['sha256']
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        alternate_visible_assets=asset_hashes, retained_movie_localization_indices=sorted(changed),
        ordinary_emulator_runs={'title': title, 'rafael': rafael},
        observed_runtime_scope='Startup movie and Rafael New Game through the opening card and transition.',
        labels_with_artwork_association=len(pairs), unbound_label_ids=sorted(IDS - set(pairs)), records=rows,
        global_absence_claim=False, new_editorial_credit=0, common_records_remaining=276, hardware=False,
        evidence={str(path): base.digest(path) for path in
                  (MANUSCRIPT, proof_path, route_proof, pre, route_pre, replay.TITLE, Path(__file__))}))
    print('37 source/current labels, 31 visual artwork associations, 29 exact upper frames, and zero target requests.')


if __name__ == '__main__':
    main()
