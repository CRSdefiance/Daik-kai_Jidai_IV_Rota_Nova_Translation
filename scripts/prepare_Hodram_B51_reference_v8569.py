"""Source-lock independent atoms, pinned research image and original loader tests."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_reference_tools_v8569')
    assert not root.exists()
    derivations = []
    derivations.append(derive('scripts/verify_Hodram_B50_reconstruction_v8501.py', 'scripts/verify_Hodram_B51_reconstruction_v8569.py', {
        'Hodram_B50_independent_v8501': 'Hodram_B51_independent_v8569',
        'Hodram_B50_relocation_v8495': 'Hodram_B51_relocation_v8565',
        'translations/hodram_B50_editorial_manuscript_v2.json': 'translations/hodram_B51_editorial_manuscript_v2.json',
        'Hodram_B50_current_v8488': 'Hodram_B51_current_v8559',
        'container.blocks[50]': 'container.blocks[51]',
        'len(commands)==12 and len(speeches)==3': 'len(commands)==20 and len(speeches)==5',
        'len(fixups)==0': 'len(fixups)==8',
        'blocks[50]=result': 'blocks[51]=result',
        'restored.blocks[50]=old': 'restored.blocks[51]=old',
        '12 disjoint command atoms;all three six-byte preambles andnine nontext controls/fullterminal are independently reconstructed':
            '20 disjoint command atoms;five six-byte preambles,eight relative targets,two queries,four opaque controls andfullterminal are independently reconstructed',
        'Independent12-command-atom B50 reconstruction equals sparseblock/archive;zero relatives;wholeclean/current blocks andparent archive recoverexactly.NoROM/credit.':
            'Independent20-command-atom B51 reconstruction equals sparseblock/archive;eight relative targets;wholeclean/current blocks andparent archive recoverexactly.NoROM/credit.',
    }))
    derivations.append(derive('scripts/create_Hodram_B50_reference_v8502.py', 'scripts/create_Hodram_B51_reference_v8570.py', {
        'B50': 'B51', 'V8475': 'V8543', 'v8475': 'v8543',
        'Hodram_B50_reference_v8502': 'Hodram_B51_reference_v8570',
        'Hodram_B50_relocation_v8495': 'Hodram_B51_relocation_v8565',
        'Hodram_B50_independent_v8501': 'Hodram_B51_independent_v8569',
        'work/analysis/Hodram_B50_stored_v8496/stored_bodies.json': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
        'work/analysis/Hodram_B50_controls_v8497/stored_controls.json': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
        'translations/hodram_B50_editorial_manuscript_v3.json': 'translations/hodram_B51_editorial_manuscript_v2.json',
        "len(manifest['batches'])==643": "len(manifest['batches'])==644",
        "stored['all3_ink_planes_exact_to_already_viewed']": "stored['all5_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass']",
        "len(controls['final_dispatches'])==3": "len(controls['stored_dispatches'])==5",
        "doc['source_current_final_references_complete']": "len(stored['records'])==5 and all(r['source_reference'] and r['current_reference'] and r['final_reference'] for r in stored['records'])",
        "plan['research_whole_ROM_sha256']": "stored['research_whole_ROM_sha256']",
        'a!=b]==[50]': 'a!=b]==[51]',
        'three-speech research reference': 'five-speech research reference',
    }))
    derivations.append(derive('scripts/verify_Hodram_B50_loaders_v8503.py', 'scripts/verify_Hodram_B51_loaders_v8571.py', {
        'scripts.create_Hodram_B50_reference_v8502': 'scripts.create_Hodram_B51_reference_v8570',
        'Hodram_B50_reference_v8502': 'Hodram_B51_reference_v8570',
        'Hodram_B50_loaders_v8503': 'Hodram_B51_loaders_v8571',
        'fourteen-speech/two-choice B49': 'five-speech/eight-relative B51',
        'exact_B49_header_andall_mapped_targets_fit_original_0x2400_cache': 'exact_B51_header_andall_mapped_targets_fit_original_0x2400_cache',
    }))
    root.mkdir(parents=True)
    save(root / 'derivations.json', dict(derivations=derivations, all_original_native_constants_andmultiplicity_preserved=True,
        command_atom_reconstruction_independent_of_sparse_relocation_andall_original_loader_guards_retained=True,
        only_five_source_qualified_B51_speeches_andtheir_eight_native_relatives_owned=True,
        complete_registeredV8543_parent_all114_accepted_layers_and644_manifest_batches_required=True,
        research_reference_is_not_a_handoff_orregistered_release_ornew_parent=True, no_ROM_write_orcredit_by_preparer=True))
