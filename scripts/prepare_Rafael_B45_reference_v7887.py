"""Source-lock the unregistered research reference and whole-SC0 loader checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_reference_tools_v7887');assert not root.exists();results=[]
    results.append(derive('scripts/create_Maria_confrontation_reference_v7805.py','scripts/create_Rafael_B45_reference_v7887.py',{
        'Pin the exact three-block research image for native loader andfocused scene checks.':'Pin the exact Rafael B45 research image for native loader andfocused source/English scene checks.',
        'work/analysis/maria_confrontation_reference_v7805':'work/analysis/Rafael_B45_reference_v7887',
        'work/analysis/maria_confrontation_relocation_v7802/one_block16_speeches_no_relative_fixups_exact_full_inverse.json':
        'work/analysis/Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json',
        'work/analysis/maria_confrontation_stored_v7803/16_final_stored_targets64_alignments11_zero_ink_tails16_pages.json':
        'work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json',
        'work/analysis/maria_confrontation_controls_v7804/16_final_dispatches_six_numeric_leaves_623D_resources_setup_ends.json':
        'work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json',
        'work/analysis/maria_confrontation_native_view_v7801b/16_native_pages_three_sheets_one_final_preview_viewed.json':
        'work/analysis/Rafael_B45_native_review_v7883/native_visual_review_andexact_plan_guard_rebinding.json',
        'out/all_routes_combined_v7779_candidate.nds':'out/all_routes_combined_v7857_candidate.nds',
        'out/maria_confrontation_reference_v7805_RESEARCH_ONLY.nds':'out/Rafael_B45_reference_v7887_RESEARCH_ONLY.nds',
        "candidate['profile']=='all-routes-unified-v7779'":"candidate['profile']=='all-routes-unified-v7857'",
        "len(manifest['batches'])==630":"len(manifest['batches'])==632",
        "stored['relocation_map_sha256']":"stored['relocation_sha256']",
        "stored['all16_stored_targets_equal_reviewed_complete_native_ink']":"stored['all12_native_ink_planes_exact_to_already_viewed']",
        "view['all_three_original_sheets_andone_final_changed_preview_individually_viewed'] and len(controls['final_dispatches'])==16":
        "len(view['direct_visual_review'])==2 and all(s['directly_viewed'] for s in view['direct_visual_review']) and len(controls['final_dispatches'])==12",
        "['/data/SC3.DK4']":"['/data/SC0.DK4']",
        "len(a)==len(b)==303 and [i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]==[36]":
        "len(a)==len(b)==343 and [i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]==[45]",
        'Maria SC3B36 full16-speech contextual research reference from complete V7717;exact inverse,no relative commands,16 reviewed complete native pages and11 zero-ink stored parity tails. Only B36 changes;302other SC3 blocks andallother files/components exact. Unregistered research,not a separate handoff package,new parent orpromotion. Preserve every ROM. SHA256 ':
        'Rafael SC0B45 full12-speech contextual research reference from current V7857;exact clean/predecessor inverse,five relocated relative controls,12 viewed complete native pages andseven zero-ink stored parity tails. Only B45 changes;342other SC0 blocks andallother files/components exact. Unregistered focused-test research,not the canceled separate unified test package,new parent orpromotion. Preserve every ROM. SHA256 ',
        'only_changed_blocks=[36],all302_otherSC3_blocks_andall_other_files_components_exact=True':
        'only_changed_blocks=[45],all342_otherSC0_blocks_andall_other_files_components_exact=True',
        'Pinned B36 research reference;302other SC3 blocks/allother files/components exact.CurrentV7779/mainV4701 unchanged.':
        'Pinned B45 research reference;342other SC0 blocks/allother files/components exact.CurrentV7857/mainV4701 unchanged.',
    }))
    results.append(derive('scripts/verify_Maria_confrontation_loaders_v7806.py','scripts/verify_Rafael_B45_loaders_v7888.py',{
        'Run every native load/cache path andboth parent modes in the resized Maria SC3 archive.':'Run every native load/cache path andboth parent modes in the resized Rafael SC0 archive.',
        'from scripts.create_Maria_confrontation_reference_v7805 import ROM,PARENT':'from scripts.create_Rafael_B45_reference_v7887 import ROM,PARENT',
        'work/analysis/maria_confrontation_loaders_v7806':'work/analysis/Rafael_B45_loaders_v7888',
        'work/analysis/maria_confrontation_reference_v7805/research_image_receipt.json':'work/analysis/Rafael_B45_reference_v7887/research_image_receipt.json',
        'for r in [3]};assert counts=={3:303}':'for r in [0]};assert counts=={0:343}',
        'for route in [3]:':'for route in [0]:',
        "'for route in (3,):'":"'for route in (0,):'",
        "'assert all_actions == EXPECTED_ACTIONS and loaded == 303'":"'assert all_actions == EXPECTED_ACTIONS and loaded == 343'",
        "'assert len(cases) == 606'":"'assert len(cases) == 686'",
        'whole_SC3_native_loads.json':'whole_SC0_native_loads.json',
        'whole_SC3_native_parent_modes.json':'whole_SC0_native_parent_modes.json',
        '303_whole_native_loads_cache_hits606_initial_parent_modes.json':'343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'fresh_native_whole_loads_andcache_hits=303,fresh_initial_parent_modes=606':'fresh_native_whole_loads_andcache_hits=343,fresh_initial_parent_modes=686',
        'three_exact_source_headers_andmapped_targets_fit_original_0x2400_cache=True,all_original_EV3_actions_select_block_indices_not_interior_offsets=True':
        'exact_B45_header_andall_mapped_targets_fit_original_0x2400_cache=True,all_original_EV0_actions_select_block_indices_not_interior_offsets=True',
        'Resized SC3:303 complete native loads/cache hits and606 original initial parent modes pass. No source eligibility, optional activation oractual UI claim.':
        'Resized SC0:343 complete native loads/cache hits and686 original initial parent modes pass. No source eligibility,optional activation oractual UI claim.',
    }))
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=results,
        original_native_high_constants_full_ROM_component_pin_andloader_guards_preserved=True,
        exact_current632_batch114accepted18check_stack_andmain4701_retained=True,
        only_unregistered_focused_research_reference_no_canceled_separate_unified_package=True,
        all342_other_SC0_blocks_andall_other_files_components_must_stay_exact=True,new_credit=0,full_goal_complete=False))
