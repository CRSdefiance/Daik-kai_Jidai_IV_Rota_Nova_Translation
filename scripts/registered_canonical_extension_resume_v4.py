"""Verify the predecessor's declared prefix size and keep the original stage bodies."""
from scripts.registered_canonical_extension_resume_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v3 import resume_checkpoint':
        'scripts.registered_canonical_extension_resume_v4 import resume_checkpoint',
    "'scripts/resume_extended_release_with_'+prior+'_v3.py'":
        "'scripts/resume_extended_release_with_'+prior+'_v4.py'",
    "    assert all(prefix['checks'].values()) and len(prefix['batches']) == 672":
        """    assert all(prefix['checks'].values())
    assert len(prefix['batches'])==config['expected_prefix_entries']==release['complete_stack_entries']-len(KEYS)
    assert prep['expected_manifest_entries']==release['complete_stack_entries']+1""",
    'full_verified672_entry_canonical_prefix_exact=True':
        "full_verified_canonical_prefix_exact=True,verified_prefix_entries=config['expected_prefix_entries']",
    "len(manifest['batches']) == 673":"len(manifest['batches']) == config['expected_prefix_entries']+1",
    'Exact canonical prefix plus351 registered transaction':'Exact verified canonical prefix plus the registered transaction',
})
exec(compile(source,__file__+'::same-source-and-stage-guards-verified-prefix-size','exec'),globals())
