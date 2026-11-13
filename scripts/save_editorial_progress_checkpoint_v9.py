"""Keep the checkpoint guards and replace documents through verified sibling files.

This avoids the observed Windows EINVAL while directly opening a compressed
handoff. Before/after plans, backups, zero-credit and ledger guards are unchanged.
"""
from scripts import save_editorial_progress_checkpoint_v8 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "        path.write_text(content, encoding='utf-8', newline='\\n')":
        """        sibling=path.with_name(path.name+'.'+mutation.name+'.pending')
        assert not sibling.exists()
        sibling.write_bytes(content.encode('utf-8'))
        assert sha(sibling.read_bytes())==entry['after_sha256']
        assert (sha(path.read_bytes()) if path.exists() else None)==entry['before_sha256']
        os.replace(sibling,path)""",
})
env={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-checkpoint-contract-verified-sibling-document-replacements','exec'),env)
checkpoint=env['checkpoint']
