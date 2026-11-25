"""Verify the351 append, all681 registered entries and exact clean-input reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/verify_rafael516_registered_release_v1.py').read_text(encoding='utf-8'),{
    "    assert m['profile'] == terminal['profile'] == prep['profile'] == qualification['profile']":
        """    assert m['profile'] == terminal['profile'] == prep['profile'] == qualification['profile']
    from scripts.registered_canonical_extension_resume_v2 import qualify,stage_source,STAGES
    resume_path=Path(registry['profiles'][m['profile']]['canonical_checkpoint_resume'])
    resume_config=load(resume_path);resume=m['canonical_checkpoint_resume']
    assert terminal['registered_source_bound_extension_andfresh_original_final_contracts']
    assert sha(resume_path.read_bytes())==prep['canonical_checkpoint_resume_sha256']==resume['configuration_sha256']
    assert resume['configuration']==str(resume_path) and resume['qualification']==qualify(resume_config,registry)
    assert resume['explicit_versioned_prefix_reuse_not_a_new_full_canonical_builder_run']
    assert resume['appended_registered_extensions']==prep['new_extension_specs']
    assert sha(Path(resume['original_manifest']).read_bytes())==resume['original_manifest_sha256']
    assert sha(Path(resume['original_ROM']).read_bytes())==resume['original_ROM_sha256']
    assert sha(Path(resume['original_builder']).read_bytes())==resume['original_builder_sha256']
    raw=Path(resume['original_builder']).read_text(encoding='utf-8')
    tail=raw[raw.index('    # Lexically valid "% o"'):raw.index('\\n\\nif __name__ == "__main__":')]
    assert sha(tail.encode('utf-8'))==resume['executed_original_final_contract_source_sha256']
    assert resume['stage_source_derivations']=={s:sha(stage_source(s).encode('utf-8')) for s in STAGES}
    cq=Path(qualification['checkpoint_qualification'])
    assert sha(cq.read_bytes())==qualification['checkpoint_qualification_sha256']
    assert len(load(cq)['negative_cases'])==10 and all(r['rejected_before_publication'] for r in load(cq)['negative_cases'])""",
    "len(prep['configs']) == len(prep['new_extension_specs']) == 2": "len(prep['configs']) == len(prep['new_extension_specs']) == 1",
    "== 680": "== 681",
    "profile['late_editorial_extensions'][-2:]": "profile['late_editorial_extensions'][-1:]",
    "    assert scenes[0]['target_ROM_sha256'] == scenes[1]['parent_ROM_sha256']":
        "    assert scenes[0]['parent_ROM_sha256']==pm['production_pipeline']['canonical_stage_sha256']",
    "len(set(owned)) == len(owned) == 29": "len(set(owned)) == len(owned) == 18",
    "[44,81,82,83,84,106,107]": "[44,81,82,83,84,106,107,130,131]",
    "== 516": "== 351",
    "== (246,270)": "== (201,150)",
    "== (504,18,118,121,380)": "== (344,10,132,134,209)",
    "== scenes[1]['clean_ROM_sha256']": "== 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'",
    "complete_stack_entries=680": "complete_stack_entries=681",
    "new_contextual_records=516": "new_contextual_records=351",
    "native_andviewed_body_pages=504,typed_choice_labels=18": "native_andviewed_body_pages=344,typed_choice_labels=10",
    "observed_actual_source_speeches=118,observed_actual_body_pages=121,observed_actual_choices=18,offline_only_source_speeches=380":
        "observed_actual_source_speeches=132,observed_actual_body_pages=134,observed_actual_choices=10,offline_only_source_speeches=209",
    "Preserve registered516 cumulative/intermediate/clean reconstruction.": "Preserve registered867 cumulative/intermediate/clean reconstruction.",
    "680 entries/516 five-gate reviews/504 pages": "681 entries/351 new five-gate reviews/344 pages",
})

if __name__=='__main__':exec(compile(source,__file__+'::all-original-release-guards-one351-append-explicit-prefix-provenance','exec'),globals())
