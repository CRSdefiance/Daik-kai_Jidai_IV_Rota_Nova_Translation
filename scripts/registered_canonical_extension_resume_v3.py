"""Compile the indented original extension block inside a function before deriving it."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/registered_canonical_extension_resume_v2.py').read_text(encoding='utf-8'),{
    'scripts.registered_canonical_extension_resume_v2 import resume_checkpoint':
        'scripts.registered_canonical_extension_resume_v3 import resume_checkpoint',
    "'scripts/resume_extended_release_with_'+prior+'_v2.py'":
        "'scripts/resume_extended_release_with_'+prior+'_v3.py'",
    "    assert prep['registry_sha256'] == config['previous_registry_sha256']":
        """    prepared_bytes=Path(config['prepared_registry']).read_bytes()
    assert prep['registry_sha256']==config['prepared_registry_sha256']==sha(prepared_bytes)
    prepared_stack=json.loads(prepared_bytes)
    assert prepared_stack['accepted_layers']==previous['accepted_layers']
    assert all(previous[k]==v for k,v in prepared_stack.items() if k!='profiles')
    assert all(previous['profiles'][k]==v for k,v in prepared_stack['profiles'].items())""",
    '    extension = checked_text(BUILDER_STAGE, {':
        "    extension = checked_text('def source_block():\\n'+BUILDER_STAGE, {",
    '    namespace = runpy.run_path(str(builder),run_name=\'immutable_canonical_final_contract_functions\')':
        "    extension=extension.split('\\n',1)[1]\n    namespace = runpy.run_path(str(builder),run_name='immutable_canonical_final_contract_functions')",
})
exec(compile(source,__file__+'::same-qualified-extension-andnative-guards-valid-snippet-compilation','exec'),globals())
