"""Exact cumulative name-layer and clean-input patch verification successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/shady_man_release_verifier_tools_v6271')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/verify_generic_speaker_labels_release_v5895.py','scripts/verify_shady_man_release_v6271.py',{
      'generic_speaker_labels_release_v1':'shady_man_label_release_v1','generic_speaker_labels_release_v5895':'shady_man_label_release_v6271','generic_speaker_labels_build_v5891':'shady_man_label_build_v6270','generic_speaker_labels_registration_v5890':'shady_man_label_registration_v6269',
      'v5891':'v6270','v5872':'v6220','V5872':'V6220','generic_speaker_labels_v5881':'shady_man_label_v6260',
      'generic_speaker_labels':'shady_man_label','==587':'==595','all587_manifest_batches114_accepted_layers18_checks_present':'all595_manifest_batches114_accepted_layers18_checks_present',
      'only_three_owned_primary_label_prefixes_changed_from_V5872':'only_one_owned_primary_label_prefix_changed_from_V6220',
      'original_five_sections_code_pointers_allocations123040_staged_extent_wrapper_and_cache_plan_preserved':'original_five_sections_code_pointers_allocations123264_staged_extent_wrapper_and_cache_plan_preserved',
    })
    ROOT.mkdir(parents=True);save(ROOT/'cumulative_verifier_source_locked_derivation.json',proof);print('Exact one-label cumulative ancestry and clean-input reconstruction verifier prepared.')
