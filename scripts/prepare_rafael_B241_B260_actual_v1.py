"""Create initialized scene fixtures with an independently proven name correction."""
from pathlib import Path

from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.assemble_rafael_B241_B260_offline_v1 import FRANCISCA, NAMES, ROOT, digest
from scripts.audit_story_glyph_consistency import load, save
from scripts.prepare_rafael_B221_B240_actual_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B241_B260_contextual_v1 import LABELS


PROPOSAL = ROOT / 'Francisca_name_field_v1/owned_fields_proposal.json'
EXPECTED_NAMES = ROOT / 'focused_name_planes_v1.json'

source = checked_text(previous, {
    "    inventory, _, _ = scoped_inventory()": """    name_proposal, name_proof = map(load, (PROPOSAL, FRANCISCA))
    assert name_proof['proposal_sha256'] == sha(PROPOSAL.read_bytes())
    corrected, owned_proof = plan_arm9_name_fields(arm, name_proposal, NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert owned_proof == name_proof['name_data_plan']
    assert sha(corrected) == name_proof['versions'][1]['ARM9_sha256']
    inventory, _, _ = scoped_inventory()""",
    "        assert all(fixture.read_file(p) == v for p, v in image.iter_components())": """        assert all(fixture.read_file(p) == v for p, v in image.iter_components())
        correct_name = any(b['selector'] == 186 for b in bindings)
        if correct_name:
            fixture.replace_file('/__arm9__.bin', corrected)
            assert [p for p, v in image.iter_components() if fixture.read_file(p) != v] == ['/__arm9__.bin']""",
    "        inverse.replace_file(path, archive)": """        inverse.replace_file(path, archive)
        if correct_name:
            assert inverse.read_file('/__arm9__.bin') == corrected
            inverse.replace_file('/__arm9__.bin', arm)""",
    "            not_registered_candidate_or_natural_activation=True": """            verified_Francisca_field_applied=correct_name,
            Francisca_name_proof_sha256=sha(FRANCISCA.read_bytes()) if correct_name else None,
            not_registered_candidate_or_natural_activation=True""",
    'ORDINARY,args.roles,Path(\'scripts/prepare_reviewed_dialogue_fixtures_v2.py\'),Path(__file__)':
        "ORDINARY,args.roles,PROPOSAL,FRANCISCA,Path('scripts/prepare_reviewed_dialogue_fixtures_v2.py'),Path(__file__)",
})


def expected_names():
    assert not EXPECTED_NAMES.exists()
    original, francisca, decisions = map(load, (NAMES, FRANCISCA, LABELS))
    assert len(original['planes']) == 19 and len(decisions['records']) == 20
    plane = next(r for r in francisca['planes'] if r['version'] == 'proposed' and r['style'] == 11)
    assert plane['text'] == 'Francisca' and digest(plane['plane']) == plane['plane_sha256']
    assert plane['complete_glyphs_bounds_andindependent_pixels_pass']
    planes = original['planes'] + [dict(text=plane['text'], native_plane=plane['plane'],
        native_plane_sha256=plane['plane_sha256'], preview=plane['preview'], preview_sha256=plane['preview_sha256'])]
    save(EXPECTED_NAMES, {**original, 'planes': planes, 'Francisca_only_from_exact_proposed_owned_field': True,
        'name_decisions': str(LABELS), 'name_decisions_sha256': digest(LABELS),
        'evidence': {str(p): digest(p) for p in (NAMES, FRANCISCA, LABELS, Path(__file__))}})


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--expected-names']:
        expected_names()
    else:
        exec(compile(source, __file__+'::exact-fixture-with-exclusive-name-field', 'exec'), globals())
