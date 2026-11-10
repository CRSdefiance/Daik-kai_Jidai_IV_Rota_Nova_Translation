"""Prepare exact cumulative release/clean-patch verification and the new ROM's own startup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_release_tools_v8779');assert not root.exists()
    source=Path('scripts/verify_Hodram_B52_release_v8705.py').read_text('utf-8')
    a=source.index("    oldprofile=deepcopy(");z=source.index('    norm=lambda',a)
    profiles="""    oldprofile=deepcopy(registry['profiles']['all-routes-unified-v8704']);newprofile=deepcopy(profile)
    for p in [oldprofile,newprofile]:p.pop('description',None);p.pop('note',None)
    old_extensions=oldprofile.pop('late_editorial_extensions');new_extensions=newprofile.pop('late_editorial_extensions')
    assert new_extensions==old_extensions+[registration['extension_spec']] and len(old_extensions)==1
    assert oldprofile==newprofile
"""
    b=source.index('    restored=builder.replace(');e=source.index("    clean=Path(",b)
    builder="""    assert builder==oldbuilder and validate_builder_bytes(builder,guard['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
"""
    release=derive('scripts/verify_Hodram_B52_release_v8705.py','scripts/verify_Hodram_B31_B53_release_v8779.py',{
        source[a:z]:profiles,source[b:e]:builder,
        'Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
        'all_routes_combined_v8704_candidate':'all_routes_combined_v8778_candidate',
        'all_routes_combined_v8609_candidate':'all_routes_combined_v8704_candidate',
        'translations/hodram_B52_editorial_release_v3.json':'translations/hodram_B31_B53_editorial_release_v2.json',
        'Hodram_B52_registration_v8703':'Hodram_B31_B53_registration_v8777',
        'Hodram_B52_atomic_positive_v8690b':'Hodram_B31_B53_atomic_positive_v8770',
        'Hodram_B52_build_v8704':'Hodram_B31_B53_build_v8778',
        'Hodram_B52_regressions_v8704':'Hodram_B31_B53_regressions_v8778',
        'all-routes-unified-v8704':'all-routes-unified-v8778',
        "len(proof['changed_records'])==5":"len(proof['changed_records'])==3",
        'late_editorial:hodram-b52':'late_editorial:hodram-b31-b53',
        "('extension_id','hodram-b52')":"('extension_id','hodram-b31-b53')",
        '==[52]':'==[31,53]',
        '646':'647',
        'only_SC1_B52_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B31_B53_change_323_otherblocks_andall_other_files_components_exact',
        'Registered cumulative B52 after wholeV8609':'Registered cumulative B31/B53 after wholeV8704',
        'ofregisteredV8704':'ofregisteredV8778',
    })
    capture=derive('scripts/capture_Hodram_B52_registered_v8706.py','scripts/capture_Hodram_B31_B53_registered_v8780.py',{
        'B52':'B31_B53',
        'Hodram_B52_registered_context_runs_v8706':'Hodram_B31_B53_registered_context_runs_v8780',
        'Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
        'all-routes-unified-v8704':'all-routes-unified-v8778',
        'Hodram_B52_registered_route{route}_v8706_V8704':'Hodram_B31_B53_registered_route{route}_v8780_V8778',
    })
    context=derive('scripts/Hodram_B52_registered_route_context_v8707.py','scripts/Hodram_B31_B53_registered_route_context_v8781.py',{
        'V8704':'V8778','Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
        'only_SC1_B52_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B31_B53_change_323_otherblocks_andall_other_files_components_exact',
    })
    bind=derive('scripts/bind_Hodram_B52_registered_v8707.py','scripts/bind_Hodram_B31_B53_registered_v8781.py',{
        'B52':'B31_B53','V8704':'V8778',
        'Hodram_B52_registered_route_context_v8707':'Hodram_B31_B53_registered_route_context_v8781',
        'Hodram_B52_registered_binding_v8707':'Hodram_B31_B53_registered_binding_v8781',
        'Hodram_B52_registered_context_runs_v8706':'Hodram_B31_B53_registered_context_runs_v8780',
        'current_V8704_Hodram_native_v8707':'current_V8778_Hodram_native_v8781',
        'Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
        'all-routes-unified-v8704':'all-routes-unified-v8778',
    })
    view=derive('scripts/verify_Hodram_B52_registered_startup_v8708.py','scripts/verify_Hodram_B31_B53_registered_startup_v8782.py',{
        'B52':'B31_B53','V8704':'V8778',
        'Hodram_B52_registered_startup_view_v8708':'Hodram_B31_B53_registered_startup_view_v8782',
        'Hodram_B52_registered_binding_v8707':'Hodram_B31_B53_registered_binding_v8781',
        'Hodram_B51_registered_binding_v8612':'Hodram_B52_registered_binding_v8707',
        'Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(release=release,capture=capture,context=context,bind=bind,view=view,
        all_native_high_integer_constants_andmultiplicity_preserved=True,
        complete_old_registry_builder_andprofile_inverse_guards_retained_builder_now_exactly_unchanged=True,
        all647_batches114_accepted18checks110regressions_exact_reference_andclean_patch_required=True,
        own_new_registered_ROM4001frame_coldboot_captain1_pool_names_all6RGBpairs_anddirect_view_required=True,
        no_prior_capture_orproducer_replay_no_credit_by_preparer=True,full_goal_complete=False))
