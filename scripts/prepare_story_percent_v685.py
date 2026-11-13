"""Four clean-source percent records, complete context and canonical batches."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety import story_percent_findings
from dk4tool.script.mesfile import iter_mesfile_records
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/story_percent_v685')
OLD = Path('out/all_routes_combined_v678_candidate.nds')
TARGETS = {0: ('DK4_MES_B177_R0180',), 2: ('DK4_MES_B133_R0136',),
           3: ('DK4_MES_B33_R0137', 'DK4_MES_B135_R0325')}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    stack = read('translations/release_stack.json')
    clean, canonical, current = [NdsImage.open(p) for p in (
        'work/clean.nds', stack['canonical_baseline']['path'], OLD)]
    review = {
        'DK4_MES_B133_R0136': {
            'speaker': 'Lil Argot',
            'context': 'Lil checks the proposed exchange after the other trader rejects a one-for-one share exchange because Lisbon is larger and strategically placed.',
            'source_meaning': 'Lil asks whether giving up two percent in Nantes means receiving one percent in Lisbon in exchange.',
            'paragraph': 'So we give you 2 percent of Nantes for 1 percent of Lisbon?',
            'localization_note': 'Keeps both amounts, cities and exchange direction in a natural confirmation question. Writes percent as a word because ASCII percent-space-o becomes an octal conversion; no manual breaks.'},
        'DK4_MES_B33_R0137': {
            'speaker': 'Ian Dukov',
            'context': 'Maria asks for a report on coastal port contracts. Ian reports successful bribery and explains the agreed sales cut and foreign-ship disguise.',
            'source_meaning': 'They reached an agreement to pay three percent of sales; officials will pretend not to see them if their ships are disguised as foreign vessels.',
            'paragraph': 'They agreed to 3 percent of sales. Officials will look the other way if we pose as foreign ships.',
            'localization_note': 'Preserves the sales cut and the disguise condition. Pose as foreign ships is an idiomatic collective reference to their fleet. Percent is written out to avoid the observed native octal read.'},
        'DK4_MES_B135_R0325': {
            'speaker': 'Manuel Almeida',
            'context': 'Maria route trade tutorial, before the advice to buy a ship once increased market share allows buying larger quantities. Source presentation byte0D is retained.',
            'source_meaning': 'While adding contracted ports and expanding routes there is no need to buy ships; a one-percent contract limits purchases of each trade good to one through five units.',
            'paragraph': "There's no need for new ships as we add ports to our routes. A 1 percent share lets us buy one to five units of each good.",
            'localization_note': 'Adding ports to our routes conveys contract-driven expansion. Keeps the temporary advice, one-percent share and one-to-five-unit limit. Percent avoids a native string conversion from percent-space-s.'}}
    review['DK4_MES_B177_R0180'] = dict(review['DK4_MES_B135_R0325'],
        context='Rafael route trade tutorial: the exact same original Japanese paragraph as Maria B135 R0325. Advice precedes buying ships once market share supports larger purchases.')
    packets, batches, files = [], [], {}
    for route, ids in TARGETS.items():
        path = f'/data/SC{route}.DK4'
        source, base, active = [r.read_file(path) for r in (clean, canonical, current)]
        records = [{r.row_id: r for r in iter_mesfile_records(data, include_non_japanese=True)}
                   for data in (source, base, active)]
        entries = []
        for key in ids:
            original, parent, older = [r[key] for r in records]
            assert original.raw_bytes == parent.raw_bytes
            row = review[key]
            neighbors = [r for r in records[0].values() if r.block_index == original.block_index
                         and 0 < abs(r.segment_index - original.segment_index) <= 9
                         and any('\u3040' <= c <= '\u9fff' for c in r.text)]
            packets.append({'route': route, 'id': key, 'source_hex': original.raw_bytes.hex(),
                'clean_Japanese': original.text, 'source_meaning': row['source_meaning'],
                'neighbors': [{'id': r.row_id, 'Japanese': r.text} for r in neighbors],
                'current_hex_for_version_guard_only': older.raw_bytes.hex(),
                'original_control': original.raw_bytes[:1].hex()})
            entries.append({'id': key, 'english': '{SPEAKER:' + f'{original.raw_bytes[0]:02X}' + '}' + row['paragraph'] + '{PAD}',
                **{k: row[k] for k in ('speaker', 'context', 'source_meaning', 'localization_note')},
                'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
        route_name = {0: 'rafael', 2: 'lil', 3: 'maria'}[route]
        batch_path = Path(f'translations/{route_name}_literal_percent_v2.json')
        save(batch_path, {'format': 'dk4-ilnk-translation-batch-v1', 'file_path': path,
            'source_file_sha256': sha(base), 'encoder': 'dialogue-fixed-v1',
            'dialogue_profile': {0: 'raphael-story-percent-live', 2: 'lil-story-deep-route-live', 3: 'maria-story-percent-live'}[route],
            'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
            'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
            'scope': 'Clean-source literal percentages rewritten as natural words; original allocations and controls retained.',
            'records': entries})
        batches.append(str(batch_path))
        files[path] = {'current_sha256': sha(active), 'canonical_sha256': sha(base),
                       'batch': str(batch_path), 'batch_sha256': sha(batch_path.read_bytes()), 'ids': list(ids)}
    findings = {f'/data/SC{i}.DK4': story_percent_findings(clean.read_file(f'/data/SC{i}.DK4'),
        current.read_file(f'/data/SC{i}.DK4')) for i in range(4)}
    assert [[r['id'] for r in findings[f'/data/SC{i}.DK4']] for i in range(4)] == [list(TARGETS[0]), [], list(TARGETS[2]), list(TARGETS[3])]
    save(ROOT / 'source_context_review.json', {'records': packets, 'all_four_route_findings': findings,
        'clean_first_source_gloss_and_adjacent_dialogue_review_before_localization': True})
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {'source_candidate': str(OLD), 'source_candidate_sha256': sha(OLD.read_bytes()),
        'source_registry': stack, 'source_registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'canonical_baseline': stack['canonical_baseline'], 'accepted_layers': stack['accepted_layers'],
        'files': files, 'batches': batches, 'profile': 'all-routes-unified-v685',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V684 complete Maria opening reveals real native percent corruption;298 archive files verified',
        'full_goal_complete': False})
    (ROOT / 'release_stack_before.json').write_bytes(Path('translations/release_stack.json').read_bytes())
    print('V685 exactly four source-bound percent hazards and natural paragraphs prepared.', flush=True)


if __name__ == '__main__':
    main()
