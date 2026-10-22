"""Close only the reviewed stored-art scope and retain original-playback work."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.review_comic_restoration_v717 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/comic_restoration_v717_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V717 Comic source review')
KEY = 'current21_comic_frames18_caption_source_restoration_visual_review_v717'
LEDGER = Path('translations/graphics_current_work_v1.json')


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/review_comic_restoration_v717.py').read_bytes())
    assert len(proof['all21_frames']) == 21 and len(proof['all18_caption_translation_and_restoration_decisions']) == 18
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    save(ROOT / 'audits_before.json', before)
    ledger = read(LEDGER)
    save(ROOT / 'ledger_before.json', ledger)
    assert not any(r['id'] == 'stored-comic-source-restoration-review' for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': 'stored-comic-source-restoration-review',
        'task': 'All21 stored comic/art frames and18 caption source/context/restoration visual review',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Stored artwork reviewed with documented inferred backings; no user approval or original runtime readability claimed.',
        'queue_status': 'complete-not-in-active-queue'})
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'original-comic-playback-and-restoration')
    task['task'] = 'Finish original comic viewer/loading,geometry,alpha and native readability.'
    task['remaining_scope'] = '21 raw frames/18 caption regions. Stored source/context/restoration review now complete; original scene use remains open. Retain approved marks.'
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'all21_current_frames18_caption_meanings_and_visible_restoration_review_complete': True,
        'existing_quantized_glyph_and_unowned_source_proofs_carried_forward_byte_exact': True,
        'six_complete_source_current_sheets_opened_no_art_revision_required': True,
        'concealed_source_reconstruction_and_visual_pun_inferences_explicit': True,
        'original_viewer_trigger_geometry_import_alpha_native_readability_still_open': True,
        'V538_kind3_alias_and_V588_portrait_loop_not_repeated_or_claimed_as_comic_display': True,
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'ROM_patch_registry_canonical_release_pointers_and_source_art_unchanged': True,
        'no_global_unused_claim_no_new_user_approval_or_guide_capture': True,
        'all18_overall_plaques_incomplete22_historical_objects_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        p = Path('translations') / name
        d = read(p)
        assert d == before[name]
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        d[KEY] = entry
        save(p, d)
        copy(p, ARCHIVE / 'audits' / name)
    p = Path('docs/graphics_remaining_work.md')
    text = p.read_text(encoding='utf-8')
    old = ('1. **Original comic playback and restoration:** verify the original viewer,\n'
        '   loading, geometry and readability of the21 raw frames/18 caption regions;\n'
        '   finish the related covered-background review. Preserve the approved marks.')
    new = ('1. **Original comic playback:** verify the original viewer, loading, import/alpha,\n'
        '   geometry and native readability of the21 raw frames/18 caption regions.\n'
        '   Stored source/context/restoration review is complete; preserve the approved marks.')
    assert old in text
    p.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V717: stored comic source/restoration review complete; original viewer remains open'
    summary = ('All21 current raw frames are byte-exact to the previously glyph-verified art. Six complete '
        'source/current sheets and18 caption/context/restoration decisions reviewed; no visible defect '
        'requiring an art edit found. Source backing and Sea cow visual-pun inferences are explicit; '
        'signatures and4320 approved brown-mark bytes retained. Existing font/source tests carry '
        'forward rather than being repeated. The stored-art review leaves the active queue; original '
        'viewer,trigger,alpha,geometry and native readability remain open. V538 kind3 label alias and '
        'V588 portrait reader are closed leads,not new comic display proofs. All18 overall plaque '
        'objects and22 historical scopes exact; other graphics work and final acceptance open. '
        'V712 ROM/patch/registry/pointers unchanged; no new native run or guide claim. Full goal active. '
        'See [V717 checkpoint](comic_restoration_v717_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        p = Path('docs') / name
        content = p.read_text(encoding='utf-8')
        assert heading not in content
        p.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
        copy(p, ARCHIVE / 'docs' / name)
    for p in (DOC, Path(__file__), Path('scripts/review_comic_restoration_v717.py'), LEDGER,
              Path('docs/graphics_remaining_work.md')):
        copy(p, ARCHIVE / 'sources' / p.name)
    for p in ROOT.glob('*.json'):
        copy(p, ARCHIVE / 'analysis' / p.name)
    for row in proof['six_opened_source_current_review_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        copy(row['path'], ARCHIVE / Path(row['path']).name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'decoded_stored_art_not_gameplay_screenshots': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for name, original in frozen.items():
        current = read(Path('translations') / name)
        current.pop(KEY)
        assert current == before[name]
        assert current.get('historical_pending_items_retained') == original['historical_pending_items_retained']
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in proof['release_hashes_unchanged'].items())
    print('V717 source/restoration review recorded and E archive verified;8 completed scopes carried forward; original comic playback open.', flush=True)


if __name__ == '__main__':
    main()
