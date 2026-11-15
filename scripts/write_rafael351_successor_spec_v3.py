"""Use the already validated research adapter for duplicate current-index metadata."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save

if __name__ == '__main__':
    out=Path('translations/rafael351_registered_successor_spec_v3.json')
    assert not out.exists()
    doc=load('translations/rafael351_registered_successor_spec_v2.json')
    doc.update(profile='all-routes-rafael867-v3-20261105',module='dk4tool.patch.rafael_story_b121_b140_release_v3',
        config='translations/rafael_B121_B140_editorial_release_v3.json',
        stage_configs=[p.replace('_Rafael867_release_v2.json','_Rafael867_release_v3.json') for p in doc['stage_configs']])
    doc['dependencies'] += ['dk4tool/patch/rafael_story_b121_b140_release_v3.py',str(Path(__file__)),
        'scripts/rebuild_rafael_B121_B140_reviewed_v2.py']
    save(out,doc)
    print('Wrotev3:exact current-reference indices supplied as inalready validated research rebuild;all native/source checks retained.')
