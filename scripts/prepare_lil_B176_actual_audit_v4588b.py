"""Resolve the observer's pending entry-row references without rerunning either boot."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

tool=derive('scripts/audit_lil_B176_actual_v4588.py','scripts/audit_lil_B176_actual_v4588b.py',{
    "        for pending in trace['unreturned_at_capture_end']:assert pending['source']['block']!=22":
    """        following_pending=[]
        for pending in trace['unreturned_at_capture_end']:
            assert set(pending)=={'player','entry_row'}
            entry=rows[pending['entry_row']]
            assert entry['kind']=='before_command' and entry['player']==pending['player']
            assert entry['source']['block']!=22
            following_pending.append(dict(entry_row=pending['entry_row'],player=pending['player'],
                block=entry['source']['block'],offset=entry['source']['instruction_offset'],start=entry['frame'],
                original_payload_exact_ROM=entry['source']['whole_resident_payload_exact_ROM']))""",
    "following_observed_blocks=sorted({r['block'] for r in pairs if r['block']!=22})":
    "following_unreturned_commands_at_capture_end=following_pending,following_observed_blocks=sorted({r['block'] for r in pairs if r['block']!=22})",
})
save(Path('work/analysis/lil_B176_actual_tools_v4588/pending_entry_reference_successor.json'),dict(tool=tool,
    correction='Pending observer rows contain player/entry_row references,not copied source objects. Resolve and validate the original before-command row;both pending rows are following B120 offset606,not B176 fixture commands.',
    initial_audit_failed_before_output_or_metadata_write=True,no_new_boot_or_retiming=True,
    both_terminal_jobs_preserved=True,full_goal_complete=False))
