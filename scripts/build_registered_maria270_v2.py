"""Keep the whole release contract and bind both newly relocated SC3 speaker controls."""
import sys
from scripts import build_registered_maria270_v1 as previous
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE25=previous.ROOT/'registered_source25_v1/qualification.json'
SOURCE25_SPEC=dict(path=str(SOURCE25),sha256=previous.env['digest'](SOURCE25))
stage_source=checked_text(previous.stage_source,{
    "bind_registered_story_percent_guard(old_manifest['story_percent_contract']['exact_relocation_receipt'])":
        "bind_registered_story_percent_guard(SOURCE25_SPEC)",
    "assert percent == old_manifest['story_percent_contract']":
        """old_percent=old_manifest['story_percent_contract']
    assert {k:v for k,v in percent.items() if k in old_percent and k!='exact_relocation_receipt'}=={k:v for k,v in old_percent.items() if k!='exact_relocation_receipt'}
    assert percent['exact_prior_relocation_receipt']==old_percent['exact_relocation_receipt']
    assert percent['additional_exact_source_bound_relocated_leading25_count']==2 and percent['total_exact_source_bound_relocated_leading25_count']==7""",
})
register_source=checked_text(previous.register_source,{
    'profile.update(verified_market_goods_info_predecessor=predecessor, maria270_late_dialogue=str(CONFIG),':
        'profile.update(source25_multiarchive_guard=SOURCE25_SPEC,verified_market_goods_info_predecessor=predecessor, maria270_late_dialogue=str(CONFIG),',
    'final_four_archive_percent_check_reexecuted=True)':
        "final_four_archive_percent_check_reexecuted=True,exact_source25_multiarchive_guard=SOURCE25_SPEC,source25_guard_module='dk4tool/script/format_safety_relocated_v2.py',source25_guard_module_sha256=digest('dk4tool/script/format_safety_relocated_v2.py'))",
})
env={**previous.env,**vars(previous),'stage_source':stage_source,'register_source':register_source,
    'SOURCE25_SPEC':SOURCE25_SPEC,'bind_registered_story_percent_guard':bind_registered_story_percent_guard,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-release-contract-original-format-guard-exact-two-route-bindings','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
