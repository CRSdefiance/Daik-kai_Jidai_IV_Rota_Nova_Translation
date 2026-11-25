"""Record qualified shared-reader completion and preserve both stopped audit preparations."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_checkpoint_tools_v8774b');assert not root.exists()
    receipt=derive('scripts/checkpoint_Hodram_B31_B53_v8774.py','scripts/checkpoint_Hodram_B31_B53_v8774b.py',{
        'work/analysis/Hodram_B31_B53_shared_extension_v8773/shared_extension_validation.json':'work/analysis/Hodram_B31_B53_shared_extension_v8773c/shared_extension_validation.json',
        'Preserve the stopped seal preparer8769:':'Shared reader8773 completed its positive case before stopping on a Windows-versus-literal path key. Successor preparation8773b stopped on a duplicate separator before creating its target. Qualified8773c reuses the exact completed positive by hash and runs only the missing late-target failure, preserving all original guards and stopped files. No completed positive, native or actual capture is replayed.\n\nPreserve the stopped seal preparer8769:',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,every_full_ledger_scope_document_counter_andprotected_ROM_inverse_preserved=True,
        qualified_shared_reader_andcompleted_positive_reuse_bound_stopped_readers_preserved=True,new_credit=0,full_goal_complete=False))
