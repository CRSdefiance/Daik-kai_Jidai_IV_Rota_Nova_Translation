"""Preserve the failed offset-assumption attempt and select exact native-proof identities."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save

if __name__ == '__main__':
    out = Path('translations/rafael351_registered_successor_spec_v2.json')
    assert not out.exists()
    doc = load('translations/rafael351_registered_successor_spec_v1.json')
    doc.update(profile='all-routes-rafael867-v2-20261105', module='dk4tool.patch.rafael_story_b121_b140_release_v2',
        config='translations/rafael_B121_B140_editorial_release_v2.json',
        stage_configs=[p.replace('_Rafael867_release_v1.json','_Rafael867_release_v2.json') for p in doc['stage_configs']])
    doc['dependencies'] += ['dk4tool/patch/rafael_story_b121_b140_release_v2.py',str(Path(__file__))]
    save(out,doc)
    print('Wrotev2:exact complete menu proof identities bridgeclean/current offsets;no text, controls, native inputs orchecks weakened.')
