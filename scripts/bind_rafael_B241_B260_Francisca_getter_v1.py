"""Bind the preserved Francisca field proposal to both original name getters."""
import inspect

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B241_B260_contextual_v1 import ROOT


def main():
    source = ROOT / 'names_and_terms_v1.json'
    field = ROOT / 'Francisca_name_field_v1'
    target = field / 'native_getter_binding.json'
    assert not target.exists()
    binding = load(source)
    proposal = load(field / 'owned_fields_proposal.json')
    assert proposal['runtime'] == binding['runtime']
    assert [row['actor'] for row in proposal['fields']] == [186]
    actor = next(row for row in binding['name_bindings'] if row['actor_ID'] == 186)
    consumers = actor['current_consumers']
    assert {row['consumer'] for row in consumers} == {'progressive-nameplate', 'full-catalogue'}
    assert all(row['text'] == 'Ｆrancisca' for row in consumers)
    adapter = checked_text(inspect.getsource(names), {'for ident in [2,4,13,23,109]:': 'for ident in ACTORS:'})
    save(target, dict(runtime=proposal['runtime'], current_names=dict(rows=consumers),
        source_owned_current_adapter=adapter, source_name_binding=str(source),
        source_name_binding_sha256=sha(source.read_bytes()), new_credit=0))


if __name__ == '__main__':
    main()
