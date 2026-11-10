"""Prepare exact B47 research-reference andnative loader successors;no registered promotion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_reference_tools_v7994')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/create_Rafael_B46_reference_v7941.py','scripts/create_Rafael_B47_reference_v7994.py',{
        'Rafael_B46_reference_v7941':'Rafael_B47_reference_v7994',
        'Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json':
            'Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json',
        'Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json':
            'Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json',
        'Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json':
            'Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json',
        'Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json':
            'Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json',
        'all_routes_combined_v7911':'all_routes_combined_v7964',
        'all-routes-unified-v7911':'all-routes-unified-v7964',
        "len(manifest['batches'])==633":"len(manifest['batches'])==635",
        'all24_native_ink_planes_exact_to_already_viewed':'all15_native_ink_planes_exact_to_already_viewed',
        "len(view['directly_viewed_sheets'])==5":"len(view['directly_viewed_sheets'])==4",
        "len(controls['final_dispatches'])==24":"len(controls['final_dispatches'])==15",
        '==[46]':'==[47]','sha(b[46])':'sha(b[47])',
        'complete24-speech/two-choice research reference from currentV7911,exact inverses/four relocated spans/all stored/native checks. OnlyB46 changes.':
            'complete15-speech/16-page research reference from currentV7964,exact inverses/24 relocated spans/all stored/native checks. OnlyB47 changes.',
        'only_changed_blocks=[46]':'only_changed_blocks=[47]',
        'Pinned B46 research reference. OnlySC0 B46 changes;342 others/allotherfiles/components exact. CurrentV7911/mainV4701 unchanged.':
            'Pinned B47 research reference. OnlySC0 B47 changes;342others/allotherfiles/components exact. CurrentV7964/mainV4701 unchanged.',
    }))
    results.append(derive('scripts/verify_Rafael_B46_loaders_v7942.py','scripts/verify_Rafael_B47_loaders_v7995.py',{
        'scripts.create_Rafael_B46_reference_v7941':'scripts.create_Rafael_B47_reference_v7994',
        'Rafael_B46_loaders_v7942':'Rafael_B47_loaders_v7995',
        'Rafael_B46_reference_v7941':'Rafael_B47_reference_v7994',
        'exact_B46_header_andall_mapped_targets_fit_original_0x2400_cache':
            'exact_B47_header_andall_mapped_targets_fit_original_0x2400_cache',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',results)
    print('Prepared B47 reference and343-load/686-parent-mode tools;no ROM,registry orcredit mutation yet.')
