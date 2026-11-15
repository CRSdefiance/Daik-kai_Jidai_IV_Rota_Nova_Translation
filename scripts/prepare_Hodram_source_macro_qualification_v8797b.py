"""Qualify the two registered F/I literal guards, keeping them live during the read-only trace."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_macro_tools_v8797b');assert not root.exists()
    old="    start,end=0x53914,0x53AC4;assert arm[start:end]==clean[start:end]"
    qualified="""    start,end=0x53914,0x53AC4
    from ndspy.code import MainCodeFile
    from dk4tool.patch.common_literal_prefix import guard,POOL
    manifest=read(Path(inp['current_ROM']).with_suffix('.manifest.json'))
    registered=manifest['relocations']['/__arm9__.bin']['common_literal_prefix']
    config=Path(registered['release_config']);assert sha(config.read_bytes())==registered['release_config_sha256']
    copies=[r for r in registered['changes'] if start<=r['offset']<end];assert len(copies)==2
    restored=bytearray(arm);packed=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);hook_bindings=[]
    for row,prefix in zip(copies,['F','I'],strict=True):
        at=row['offset'];before,after=[int.from_bytes(data[at:at+4],'little') for data in [clean,arm]]
        assert (before,after)==(row['before'],row['after'])
        helper=registered['helpers'][prefix];blob=guard(helper['entry'],prefix);offset=helper['entry']-POOL
        assert len(blob)==helper['bytes'] and offset>=0 and packed[offset:offset+len(blob)]==blob
        restored[at:at+4]=clean[at:at+4]
        hook_bindings.append(dict(prefix=prefix,offset=at,source_word=before,registered_live_word=after,helper=helper,complete_helper_sha256=sha(blob)))
    assert bytes(restored[start:end])==clean[start:end]
    assert all(m in registered['recognized_F_tokens_preserved'] for m in ['FI','FA'])
"""
    receipt=derive('scripts/trace_Hodram_B54_B60_source_macros_v8797.py','scripts/trace_Hodram_B54_B60_source_macros_v8797b.py',{
        'Hodram_B54_B60_source_macros_v8797':'Hodram_B54_B60_source_macros_v8797b',old:qualified,
        "entire_original_macro_parser_span=dict(start=start,end=end,sha256=sha(arm[start:end]))":"entire_macro_parser_span=dict(start=start,end=end,clean_sha256=sha(clean[start:end]),current_sha256=sha(arm[start:end]),two_registered_literal_guards=hook_bindings,restoring_only_owned_words_in_unexecuted_comparison_copy_recovers_full_clean_span=True)",
        "all_original_macro_ABI_scratch_ring_input_output_unowned_memory_guards_preserved=True":"all_original_macro_ABI_scratch_ring_input_output_unowned_memory_guards_preserved=True,two_registered_F_I_literal_guards_remain_live_with_complete_helper_payloads_exact=True,unexecuted_comparison_copy_never_loaded_into_CPU_orROM=True",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,stopped_original_macro_span_assumption_preserved_no_partial_trace_receipt_was_written=True,
        source_current_differences_exactly_two_already_registered_literal_prefix_guards_verified_by_manifest_words_full_helpers_andwhole_span_inverse=True,
        actual_trace_runs_unchanged_current_ROM_andown_current_snapshot_no_guard_disabled_orcomparison_copy_executed=True,
        all_original_ABI_source_native_ownership_andmemory_guards_preserved=True,new_credit=0,full_goal_complete=False))
