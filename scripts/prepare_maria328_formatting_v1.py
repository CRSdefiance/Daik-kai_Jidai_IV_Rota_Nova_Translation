"""Prepare full-width mixed-consumer layouts;reuse exact native macro proofs withqualified dynamic assertions."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

PROSE = Path('translations/maria_B73_B95_contextual_review_v1.json')


def main():
    out = ROOT/'formatting_v1'
    assert not out.exists()
    current_path = ROOT/'current_v1/current_effective.json'
    reference_path = ROOT/'scoped_names_macros_reference_v1.json'
    roles_path = ROOT/'dynamic_roles_current_v1.json'
    old_path = Path('work/Maria_B58_B70_clean_20261109/formatting_v3/native_macro_measurements.json')
    doc,current,reference,roles,prior = map(load,[PROSE,current_path,reference_path,roles_path,old_path])
    runtime = current['runtime']
    assert runtime == doc['runtime'] == reference['runtime'] == roles['runtime']
    now = RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    old = RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=3)
    assert now.receipt() == runtime and old.receipt() == prior['runtime']
    assert digest('translations/release_stack.json') == now.release['registry_sha256']
    assert now.arm == old.arm and now.common == old.common
    assert now.actor_root == old.actor_root and now.actor_bytes == old.actor_bytes
    assert now.raw[0x7f244:0x7f248] == old.raw[0x7f244:0x7f248] == b'\x03\0\0\0'
    assert now.image.read_file('/GRP/KANJI.FNT') == old.image.read_file('/GRP/KANJI.FNT')
    expected = {r['token']:r['text'] for r in reference['default_macro_cases']}
    assert {t:v['text'] for t,v in prior['defaults'].items()} == expected == dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    assert prior['default_macro_all_four_alignment_cases_pass'] and prior['FE_null_actor_FI_four_alignment_cases_pass']
    adapter = checked_text(prior['source_owned_progressive_adapter'], {
        'assert identity==prefix and captain==3': 'assert captain==3 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])',
    })
    rows, tokens = [], 0
    for original in doc['records']:
        row = deepcopy(original)
        assert row['review'] == dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English'] = row['english']
        row['english'] = re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english']) == row['editorial_logical_English']
        for token,count in row['source_macros'].items():
            assert row['english'].count('{MACRO:'+token+'}') == count
            tokens += count
        if row['kind'] != 'typed-choice-label':
            assert isinstance(row['source_record_index'],int)
            row['planned_English_markup'] = '{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison'] = row['english'] if row['decision']=='retention' else None
            if row.get('native_object_kind') == '4100-style-alternative':
                row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text'] = True
                assert row['source_choice_object_hex'] == row['source_object_hex']
        rows.append(row)
    assert len(rows) == 328 and sum(r['kind']=='progressive' for r in rows) == 286
    assert sum(r['kind']=='system-FE' for r in rows) == 27 and sum(r['kind']=='typed-choice-label' for r in rows) == 15 and tokens == 2
    out.mkdir()
    macro_path = out/'native_macro_measurements.json'
    save(macro_path,{**prior,'runtime':runtime,'source_owned_progressive_adapter':adapter,
        'reused_original_runtime':prior['runtime'],'prior_native_measurements':str(old_path),'prior_native_measurements_sha256':digest(old_path),
        'exact_dependency_reuse':dict(complete_ARM9=True,complete_COMMON=True,complete_font=True,actor_root=True,
            complete_actor_model_block=True,captain3_word=True,all_four_default_expansions=True),
        'native_assertion_only_dynamic_identity_extension':dict(role_proof=str(roles_path),role_proof_sha256=digest(roles_path),
            no_original_instruction_orABI_change=True,per_record_native_expansion_alignment_still_required=True),
        'no_native_default_macro_cases_reexecuted':True,'fresh_formatted_record_alignment_andpixels_still_pending':True,
        'evidence':{**prior['evidence'],**{str(p):digest(p) for p in [PROSE,current_path,reference_path,roles_path,old_path,Path(__file__)]}}})
    save(out/'role_bindings.json',roles)
    save(out/'formatting_input.json',{**doc,'records':rows,'current_archive_sha256':current['current_archive_sha256'],
        'physical_speech_objects':313,'ordinary_speech_objects':289,'style_physical_speech_objects':24,'style_command_objects':4,
        'typed_choice_objects':15,'typed_choice_commands':5,'source_full_manuscript':str(PROSE),'source_full_manuscript_sha256':digest(PROSE),
        'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,'macro_proof_sha256':digest(macro_path),
        'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(out/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared313 bodies/15 captions/two FI tokens;exact20 default macro proofs reused;fresh formatting remains pending.')


if __name__ == '__main__':
    main()
