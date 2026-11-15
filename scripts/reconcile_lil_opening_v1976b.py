"""Successor binds six later reinforcement messages instead of whole COMMON equality."""
from pathlib import Path

SOURCE = Path('scripts/reconcile_lil_opening_v1976.py')

if __name__ == '__main__':
    assert not Path('work/analysis/lil_opening_contextual_retention_v1976').exists()
    text = SOURCE.read_text(encoding='utf-8')
    old = "    assert image.read_file('/COMMON/MESFILE.DK4') == previous.read_file('/COMMON/MESFILE.DK4')"
    new = """    from dk4tool.patch import reinforcement_faction_prose as common_layer
    common_before = previous.read_file('/COMMON/MESFILE.DK4')
    common_current = image.read_file('/COMMON/MESFILE.DK4')
    common_report = common_layer.apply_release(previous,NdsImage.open('out/raphael_natural_v2_accepted_base.nds'))
    assert previous.read_file('/COMMON/MESFILE.DK4') == common_current
    assert [r['message_ID'] for r in common_report['changed_records']] == list(range(1911,1917))
    assert common_report['all3668_native_offsets_and_copy_spans_exact']
    assert common_report['all3662_unselected_strings_and_all_unowned_block_bytes_exact']
    assert common_report['no_runtime_font_graphic_story_macro_or_RNG_changes']
    common_scope = dict(original_COMMON_sha256=sha(common_before),current_COMMON_sha256=sha(common_current),
        exact_registered_late_layer=common_layer.CONFIG,changed_message_IDs=list(range(1911,1917)),
        unrelated_battle_reinforcement_barks_only=True,not_claimed_whole_COMMON_equal=True,
        all_other3662_messages_and_all_native_offsets_copy_spans_exact=True,report=common_report)
    common_scope_path = ROOT/'COMMON_delta_scope.json'"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    changes = {
        'lil_opening_contextual_retention_v1976':'lil_opening_contextual_retention_v1976b',
        'Exact B22,ARM9 andCOMMON inheritance fromV1711':
            'Exact B22/ARM9 inheritance plus the source-locked six-reinforcement-message COMMON delta fromV1711',
        'ExactB22/runtime/COMMON checked.':'ExactB22/runtime plus six unrelated reinforcement-only COMMON changes checked.',
        'exactB22/ARM9/COMMON checks.':'exactB22/ARM9 plus reinforcement-only COMMON delta checks.',
        'CurrentB22/ARM9/COMMON matchV1711 exactly;':
            'CurrentB22/ARM9 matchV1711 exactly;COMMON differs only in six unrelated reinforcement announcements with unchanged native offsets/copy spans;',
        "    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())":
            "    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())\n    save(common_scope_path,common_scope)",
        "inherited_native_and_actual_evidence_bound_to_unchanged_bytes=True,narrow_physical_line_count_warning_IDs=waivers":
            "inherited_native_and_actual_evidence_bound_to_unchanged_B22_runtime_and_scoped_COMMON=True,COMMON_difference_scope=common_scope,narrow_physical_line_count_warning_IDs=waivers",
        "evidence={str(OLD):sha(OLD.read_bytes()),**old['proofs']}":
            "evidence={str(OLD):sha(OLD.read_bytes()),**old['proofs'],str(common_scope_path):sha(common_scope_path.read_bytes()),common_layer.CONFIG:sha(Path(common_layer.CONFIG).read_bytes()),str(SOURCE):sha(SOURCE.read_bytes())}",
    }
    for old,new in changes.items():
        assert old in text,old
        text = text.replace(old,new)
    # Preserve the initial failed assertion as historical source; only this
    # successor emits review/ledger files after proving the exact late delta.
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__,'SOURCE':SOURCE})
