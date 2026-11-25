"""Bind B171 names,training/address terms and new facts against exact completed B170."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_terms_v4318b')
SOURCE = Path('work/analysis/lil_B171_source_v4311/all37_clean_current_complete_context.json')
NAMES = Path('work/analysis/lil_B171_names_v4316/six_original_name_consumers_and_owned_scratch_paths.json')
CONTROL = Path('work/analysis/lil_B171_dispatches_v4313/all37_source_current_dispatches_FI1_FO0_and8_control_leaves.json')
EARLIER = Path('translations/lil_B170_contextual_final_review_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source, names, control, earlier = map(read, [SOURCE, NAMES, CONTROL, EARLIER])
    assert names['source_context_sha256'] == control['source_context_sha256'] == sha(SOURCE.read_bytes())
    image, clean = NdsImage.open(source['current_ROM']), NdsImage.open('work/clean.nds')
    current, jp = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image, clean]]
    bindings = []
    for index in [82,90,94,97,100,104,108,111,114,125]:
        row = next(r for r in earlier['records'] if r['source_record_index'] == index)
        sr, ref = row['source_reference'], row['integrated_reference']
        raw, value = bytes.fromhex(row['source_hex']), bytes.fromhex(row['integrated_hex'])
        assert row['block'] == ref['block'] == 170 and row['file_path']=='/data/SC2.DK4'
        assert jp[170][sr['offset']:sr['offset'] + len(raw)] == raw and jp[170][sr['offset'] + len(raw)] == 0
        assert current[170][ref['offset']:ref['offset'] + len(value)] == value and current[170][ref['offset'] + len(value)] == 0
        assert all(row['review'].values())
        if index in [90,100]:
            assert '道術' in row['source_Japanese'] and 'Taoist arts' in row['english']
        bindings.append(dict(final_review=str(EARLIER), final_review_sha256=sha(EARLIER.read_bytes()), id=row['id'],
            clean_reference=sr, clean_hex=raw.hex(), clean_Japanese=row['source_Japanese'], current_reference=ref,
            current_hex=value.hex(), reviewed_English=row['english'], source_meaning=row['source_meaning'], localization_note=row['localization_note']))
    by = {r['source_record_index']: r for r in source['records']}
    for index, phrases in {29:['イファの兄弟子','サンヒョン'],48:['我が国','国外','禁じられて'],55:['国禁','当道場','破門'],
                           61:['幼少','実の兄妹のごとく'],114:['山を下りる','術を使って'],122:['修行を怠るな','お師匠様のいいつけ'],
                           133:['サンヒョン兄さん','がんばって修行'],137:['船の仕事が先','修行はその次']}.items():
        assert all(phrase in by[index]['source_Japanese'] for phrase in phrases), index
    assert names['progressive_nameplate_values'] == names['full_catalogue_values'] == {'2':'Lil Argot','25':'Yifa Sol','81':'Sanghyeon Kan'}
    assert names['approved_prose_names'] == {'2':'Lil','25':'Yifa','81':'Sanghyeon'}
    ROOT.mkdir(parents=True)
    save(ROOT / 'current_Taoist_arts_Sanghyeon_training_bond_and_new_facts_reconciliation.json', dict(
        candidate=source['current_ROM'], candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE), source_context_sha256=sha(SOURCE.read_bytes()), exact_completed_B170_bindings=bindings,
        approved_B171_prose_names={'2':'Lil','25':'Yifa','81':'Sanghyeon'}, native_full_names_preserved={'2':'Lil Argot','25':'Yifa Sol','81':'Sanghyeon Kan'},
        Kan_not_added_to_source_spoken_introduction=True, source51_is_static_actor81_not_Q=True,
        anideshi_meaning='senior fellow disciple/student under the same teacher;male seniority in training,not biological brother or the teacher',
        siblinglike_childhood_bond_explicit_biological_kinship_or_romance_not_established=True,
        source_niisan_address_localized_with_approved_name_and_affection_not_new_rank=True,
        source_dono_courtesy_not_feudal_title=True, chosen_discipline_term='Taoist arts;contextual arts where source shortens to術',
        dojo_meaning='their training school;expulsion is loss of membership,not invented loss of powers or a further national punishment',
        teacher_translation='teacher', teacher_gender_and_name_unspecified=True,
        country_not_named_and_not_inferred_from_name_culture=True,
        source_national_travel_ban_Yifa_ignorance_and_school_expulsion_newly_stated_here=True,
        no_new_B171_information_retroactively_added_to_completed_B170=True,
        source_Lil_only_relays_training_and_teacher_requests_to_Yifa_not_ban_or_expulsion=True,
        dream_visit_Lil_uncertainty_and_Yifa_arts_explanation_remain_distinct_perspectives=True,
        no_named_spell_telepathy_ghost_physical_crossborder_travel_or_earned_event_state_asserted=True,
        no_other_route_scene_relationship_rank_or_school_name_imported=True,
        names_proof=str(NAMES), names_proof_sha256=sha(NAMES.read_bytes()), source_FI1_preserved=True,
        later_older_record0D_reaudit_stays_open=True,
        evidence={str(p): sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,EARLIER,Path(__file__)]},
        new_emulator_runs=0, source_prose_or_completion_credit_added=0, no_ROM_registry_ledger_change=True, full_goal_complete=False))
    print('B171 names/bond/new facts and training terms bound to exact source plus10 completed B170 references. Predecessor B171 English still unexposed;no credit.')
