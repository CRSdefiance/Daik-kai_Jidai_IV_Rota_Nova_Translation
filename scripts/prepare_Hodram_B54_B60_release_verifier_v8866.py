"""Retain complete manifest/prefix/ROM/patch inverse and original runtime guards for the cumulative release."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_release_verifier_tools_v8866');assert not root.exists()
    verifier=derive('scripts/verify_Hodram_B31_B53_release_v8779.py','scripts/verify_Hodram_B54_B60_release_v8866.py',{
      'Verify registered B52 cumulative output':'Verify registered B54-B60 cumulative output',
      'Hodram_B31_B53_release_v8779':'Hodram_B54_B60_release_v8866',
      'out/all_routes_combined_v8778_candidate.nds':'out/all_routes_combined_v8865_candidate.nds',
      'out/all_routes_combined_v8704_candidate.nds':'out/all_routes_combined_v8778_candidate.nds',
      'translations/hodram_B31_B53_editorial_release_v2.json':'translations/hodram_B54_B60_editorial_release_v2.json',
      'Hodram_B31_B53_registration_v8777':'Hodram_B54_B60_registration_v8864',
      'Hodram_B31_B53_atomic_positive_v8770':'Hodram_B54_B60_atomic_positive_v8857',
      'Hodram_B31_B53_build_v8778':'Hodram_B54_B60_build_v8865',
      'Hodram_B31_B53_regressions_v8778':'Hodram_B54_B60_regressions_v8865',
      "'all-routes-unified-v8778'":"'all-routes-unified-v8865'",
      "registry['profiles']['all-routes-unified-v8704']":"registry['profiles']['all-routes-unified-v8778']",
      "==647 and len(manifest['checks'])":"==648 and len(manifest['checks'])",
      'len(old_extensions)==1':'len(old_extensions)==2',
      "len(proof['changed_records'])==3":"len(proof['changed_records'])==82",
      'hodram-b31-b53':'hodram-b54-b60',
      'if a!=b]==[31,53]':'if a!=b]==[54,55,56,57,58,59,60]',
      'Registered cumulative B31/B53 after wholeV8704;647batches/114accepted/18checks/110regressions;main4701 unchanged.':'Registered cumulative B54-B60 after wholeV8778;648batches/114accepted/18checks/110regressions;main4701 unchanged.',
      'Exact clean-input patch reconstruction ofregisteredV8778':'Exact clean-input patch reconstruction ofregisteredV8865',
      'manifest_batches=647':'manifest_batches=648',
      'all647_manifest_batches_and114_accepted_layers_present':'all648_manifest_batches_and114_accepted_layers_present',
      'only_SC1_B31_B53_change_323_otherblocks_andall_other_files_components_exact':'only_SC1_B54_B60_change_318_otherblocks_andall_other_files_components_exact',
      'batches=647':'batches=648',
    })
    root.mkdir(parents=True);save(root/'source_locked_release_verifier.json',dict(verifier=verifier,all_original_complete_registry_inverse_manifest_batches_prior_extension_prefix_full_changedrecord_report_runtime_payload_byteidentity_andcleanpatch_reconstruction_guards_preserved=True,only7_SC1blocks_change_and318unownedblocks_all_other_files_components_exact_required=True,no_verifier_run_before_registered_build_andregressions_pass=True,no_ROM_registry_orcredit_change_by_preparer=True,full_goal_complete=False))
