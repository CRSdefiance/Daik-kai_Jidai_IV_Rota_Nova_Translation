"""Resume the exact interrupted atomic credit after preserving its completed artifacts."""
from pathlib import Path
from scripts import complete_hodram_B231_B250_registered_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

source=checked_text(previous.source,{
    "    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()":
        "    assert FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()",
    '    save(FINAL,dict(format=':'    expected_final=dict(format=',
    "origin,Path(__file__)]}))":"origin,Path(__file__)]})\n    assert load(FINAL)==expected_final",
    "    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists()\n    backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before":
        "    backup=ROOT/'ledger_before_completion.json.gz';assert backup.exists()\n    assert gzip.decompress(backup.read_bytes())==before",
    "    assert not pending.exists() and ledger_path.read_bytes()==before;pending.write_bytes(encoded)":
        """    assert pending.exists() and pending.stat().st_size==0 and ledger_path.read_bytes()==before
    preserved=ROOT/'disk_full_zero_length_pending_file_preserved.json';assert not preserved.exists()
    os.replace(pending,preserved)
    pending.write_bytes(encoded)""",
})

if __name__=='__main__':
    # Keep the original deterministic final document's producer field unchanged;
    # the separate receipt below explicitly identifies this continuation.
    env={**globals(),'__name__':'__main__','__file__':previous.__file__}
    exec(compile(source,__file__+'::same-atomic-credit-resume-from-verified-zero-length-write','exec'),env)
    root=Path('work/hodram_B231_B250_release_v1')
    save(root/'completion_disk_full_resume_v2.json',dict(resume_driver=__file__,resume_driver_sha256=digest(__file__),
        original_driver=previous.__file__,original_driver_sha256=digest(previous.__file__),
        original_final_review_andcompressed_backup_verified_exact_andreused=True,
        failed_zero_length_pending_preserved=True,prior_authoritative_ledger_was_unchanged=True,
        completion=str(root/'completion_checkpoint.json'),completion_sha256=digest(root/'completion_checkpoint.json'),
        once_only_credit_added=225,no_ROM_deleted_orchanged=True,full_goal_complete=False))
