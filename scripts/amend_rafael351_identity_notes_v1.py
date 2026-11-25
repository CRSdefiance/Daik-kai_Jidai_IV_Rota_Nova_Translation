"""Correct two draft rationale names usingthe alreadybound native fields;rerun no getters."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

OLD = Path('work/analysis/Rafael351_identity_qualification_v2_20261105/qualified_names_roles_andparticle_findings.json')
NAMES = Path('translations/rafael_B121_B140_scoped_names_review_v1.json')
NEW = Path('translations/rafael_B121_B140_scoped_names_review_v2.json')
ROOT = Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105')

if __name__ == '__main__':
    assert not NEW.exists() and not ROOT.exists()
    old, names = map(load,[OLD,NAMES]); before = deepcopy(names)
    assert old['scoped_name_review_sha256'] == sha(NAMES.read_bytes())
    expected = {20:('Fernando Dias','Retain Fernando Dias fromthe exact earlier scoped proof;the rough battle response addsno nationality orrank.'),
        26:('Julian Lopes','Retain Julian Lopes fromthe exact earlier scoped proof. Theflirtation advice isa character’s joking justification,notan invented biography orrelationship.')}
    for actor,(label,reason) in expected.items():
        row = next(r for r in names['records'] if r['actor_ID'] == actor)
        binding = next(r for r in old['name_bindings'] if r['actor_ID'] == actor)
        assert row['english'] == label == next(r for r in binding['current_consumers'] if r['consumer']=='progressive-nameplate')['text']
        for key in ['finding','retention_reason','localization_note']:
            row[key] = reason
    for a,b in zip(before['records'],names['records'],strict=True):
        allowed = {'finding','retention_reason','localization_note'} if a['actor_ID'] in expected else set()
        assert {k:v for k,v in a.items() if k not in allowed} == {k:v for k,v in b.items() if k not in allowed}
    names.update(prior_notes=str(NAMES),prior_notes_sha256=sha(NAMES.read_bytes()),
        two_stale_rationale_names_corrected_to_actual_native_public_labels=True,no_name_data_orprose_change=True)
    save(NEW,names);ROOT.mkdir()
    result = deepcopy(old)
    result.update(scoped_name_review=str(NEW),scoped_name_review_sha256=sha(NEW.read_bytes()),
        original_qualification=str(OLD),original_qualification_sha256=sha(OLD.read_bytes()),
        all_source_fields_consumers_dynamic_roles_andparticle_proposals_exact_reused=True,
        no_new_native_execution=True)
    result['evidence'].update({str(p):sha(p.read_bytes()) for p in [OLD,NAMES,NEW,Path(__file__)]})
    save(ROOT/'qualified_names_roles_andparticle_findings.json',result)
    print('Corrected onlytwo rationale names toFernando Dias/Julian Lopes;all22 actual English labels/native proofs/role contracts andtwo particle findings unchanged. No ROM change ornewtests.')
