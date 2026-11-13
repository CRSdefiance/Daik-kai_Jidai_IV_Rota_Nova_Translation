"""Checkpoint only the qualified source-complete host fixtures; preserve the rejected v1 selection."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/checkpoint_maria390_stored_v1.py').read_text(encoding='utf-8'),{
    'display_fixtures_v1':'display_fixtures_v2',
    "ROOT/'stored_progress_checkpoint_v1'":"ROOT/'stored_progress_checkpoint_v2'",
    "assert len(detail['original_initializers'])==7 and len(detail['source_bound_QA_host_opening_exit'])==40":
        "assert len(detail['original_initializers'])==7 and len(detail['source_bound_QA_host_opening_exit'])==40\n        assert detail['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']\n        assert all(c['duration']==16 for c in load(detail['inputs']) if c['buttons']==['A'] and c['start']>=4000)",
    'Three pinned research fixtures are created in `display_fixtures_v1/fixtures.json`,not yet run:':
        'The initial `display_fixtures_v1` used an older helper with only22 final host commands andfive-frame A pulses. The checkpoint rejected that scope before ledger mutation. Preserve those ROMs as superseded research;do not run orcredit them. The qualified full-host helper `scripts.prepare_maria270_display_fixtures_v2` creates the corrected fixtures withall40 nonspeech commands and16-frame A pulses. Three pinned research fixtures are created in `display_fixtures_v2/fixtures.json`,not yet run:',
})
if __name__=='__main__':exec(compile(source,__file__+'::same373-stored-guards-qualified-full-host-fixtures-only','exec'),globals())
