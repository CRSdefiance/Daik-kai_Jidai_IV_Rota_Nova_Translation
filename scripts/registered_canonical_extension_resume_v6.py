"""Bind the canonical percent check to exact relocated source speaker records."""
from scripts.registered_canonical_extension_resume_v5 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

def derive_tail(tail):
    return checked_text('def final_safety_contracts():\n'+tail,{
        '    from dk4tool.script.format_safety import reject_story_percent_commands':
            '    from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard\n'
            '    reject_story_percent_commands = bind_registered_story_percent_guard(percent_relocation_guard)',
    }).split('\n',1)[1]

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v5 import resume_checkpoint':
        'scripts.registered_canonical_extension_resume_v6 import resume_checkpoint',
    "'scripts/resume_extended_release_with_'+prior+'_v5.py'":
        "'scripts/resume_extended_release_with_'+prior+'_v6.py'",
    '    prefix = load(config[\'canonical_manifest\'])\n    assert prefix':
        "    from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard\n"
        "    bind_registered_story_percent_guard(config['percent_relocation_guard'])\n"
        "    prefix = load(config['canonical_manifest'])\n    assert prefix",
    "    code='def complete_registered_checkpoint():\\n'+extension+tail":
        """    original_tail=tail
    tail=derive_tail(tail)
    namespace['percent_relocation_guard']=config['percent_relocation_guard']
    code='def complete_registered_checkpoint():\\n'+extension+tail""",
    "executed_original_final_contract_source_sha256=sha(tail.encode('utf-8')),":
        """original_final_contract_source_sha256=sha(original_tail.encode('utf-8')),
        executed_final_contract_source_sha256=sha(tail.encode('utf-8')),
        source_bound_story_percent_guard=config['percent_relocation_guard'],""",
})
exec(compile(source,__file__+'::same-final-checks-exact-story-source-record-mapping','exec'),globals())
