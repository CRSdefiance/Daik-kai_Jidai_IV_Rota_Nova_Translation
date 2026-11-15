"""Register only a fresh successor;preserve failed8459/currentbuilder anduse corrected explicitconfigv3."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B49_registration_tools_v8475')
if __name__=='__main__':
    assert not ROOT.exists();path=Path('scripts/register_Hodram_B49_v8458.py');text=path.read_text('utf8')
    a=text.index("    assert len(read(PARENT.with_suffix");b=text.index('    profile=deepcopy(',a)
    plan='''    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==642
    assert before==Path('work/analysis/Hodram_B49_builder_v8452/planned_builder.bin').read_bytes() and sha(before)==guard['planned_builder_sha256']
    assert before.count(STAGE_V5.encode())==before.count(STAGE_B49_V2.encode())==1 and before.count(anchor.encode())==1
    assert validate_builder_bytes(before,digest)['corrected_B49_stage_version']==2
    historical_before=Path('work/analysis/Hodram_B49_registration_v8458/build_integrated_release.py.before').read_bytes()
    assert before.replace(STAGE_B49_V2.encode(),b'',1).replace(STAGE_V5.encode(),STAGE_V3.encode(),1)==historical_before
    assert registry['profiles']['all-routes-unified-v8459']==read('work/analysis/Hodram_B49_registration_v8458/release_stack.planned.json')['profiles']['all-routes-unified-v8459']
    pin_binding=read('work/analysis/Hodram_B49_pin_semantics_v8465b/semantic_binding.json')
    assert pin_binding['prior14_semantic_cases_reused_not_rerun'] and pin_binding['new_lifecycle_rejection_count']==3 and pin_binding['all_current_protected_files_hash_exact']
    after=before
'''
    c=text.index('    ROOT.mkdir(parents=True);');d=text.index("    with rp.open('r+b')",c)
    backups='''    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(historical_before)
    (ROOT/'live_builder.at_registration.bin').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
'''
    result=derive(path,'scripts/register_Hodram_B49_v8475.py',{
        text[a:b]:plan,text[c:d]:backups,
        'Hodram_B49_registration_v8458\')':'Hodram_B49_registration_v8475\')',
        "PROFILE='all-routes-unified-v8459'":"CONFIG=Path('translations/hodram_B49_editorial_release_v3.json')\nPROFILE='all-routes-unified-v8475'",
        'Hodram_B49_atomic_positive_v8456':'Hodram_B49_atomic_positive_v8465',
        'owned.CONFIG':'CONFIG','editorial_handoff_verification_v8430':'editorial_handoff_verification_v8474',
        'every_unowned_builder_byte_andprior_registry_value_inverts_exactly=True':'every_unowned_builder_byte_andprior_registry_value_inverts_exactly=True,live_builder_not_modified_by_successor_registration=True,historical_builder_before_first_B49_attempt_preserved=True,failed_V8459_profile_preserved_exact=True,pin_semantic_binding="work/analysis/Hodram_B49_pin_semantics_v8465b/semantic_binding.json"',
        'Registered experimental V8459':'Registered experimental V8475',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_prior_source_native_semantic_andregistration_gates_preserved=True,only_corrected_explicit_config_successor_profile_andknown_live_builder_lifecycle_changed=True,no_unowned_builder_orprior_profile_mutation=True,new_credit=0,full_goal_complete=False))
