"""Carry the exact previously reviewed Sailor plane into the fixture expectations."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.prepare_rafael_B241_B260_actual_v1 import EXPECTED_NAMES, ROOT, digest


PRIOR = Path('work/analysis/Rafael_B221_B240_current2952_20261106/scoped_name_planes_v1/native_name_planes.json')
NAMES = ROOT / 'focused_name_planes_v2.json'
DECISIONS = ROOT / 'focused_name_decisions_v1.json'
ROLES = ROOT / 'roles.json'


def main():
    assert not NAMES.exists() and not DECISIONS.exists()
    names, prior, roles = map(load, (EXPECTED_NAMES, PRIOR, ROLES))
    source_decisions = Path(names['name_decisions'])
    decisions = load(source_decisions)
    assert digest(source_decisions) == names['name_decisions_sha256']
    assert names['runtime'] == roles['runtime']
    assert all(names['runtime'][key] == prior['runtime'][key] for key in ('ARM9_sha256', 'COMMON_sha256'))
    role = next(r for r in roles['native_roles']['rows'] if r['source_selector'] == 208)
    assert role['resolved_actor_ID'] == 151 and role['source_voice_class'] == 4
    actor = next(row for row in prior['actors'] if row['actor_ID'] == role['resolved_actor_ID'])
    plane = next(row for row in prior['planes'] if row['text'] == actor['text'])
    assert actor['text'] == 'Sailor' and digest(plane['native_plane']) == plane['native_plane_sha256']
    save(DECISIONS, {**decisions, 'records': decisions['records'] + [dict(actor_ID=151, english=actor['text'],
        prior_contextual_retention=True, source_reference=actor['source_reference'],
        current_reference=actor['current_reference'])]})
    save(NAMES, {**names, 'planes': names['planes'] + [plane], 'name_decisions': str(DECISIONS),
        'name_decisions_sha256': digest(DECISIONS), 'native_Sailor_role_exact_reuse': True,
        'evidence': {**names['evidence'], **{str(p): digest(p) for p in (PRIOR, ROLES, DECISIONS, Path(__file__))}}})


if __name__ == '__main__':
    main()
