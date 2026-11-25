"""Verify own cumulative startup,three live surname spans andboth getters for12 protected actors."""
from scripts import verify_rafael5186_startup_v1 as prior
from scripts import verify_hodram_B311_B324_registered_getters_v1 as getters_prior
from scripts.build_registered_hodram_residual_v1 import GETTERS,PARENT,STAGED,STARTUP,NAME_CONFIG,CLEAN
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(prior.source,{
    "release['all_except_owned_middle_fields_exact_to_parent']":"release['all_except_SC1_andthree_owned_surnames_exact_to_parent']",
    "release['middle_fields_config_sha256']":"release['surname_fields_config_sha256']",
    "ownership['changed_bytes']==9":"ownership['changed_bytes']==28",
    'only_nine_owned_middle_field_bytes_differ_in_ARM9=True':'only28_owned_surname_bytes_differ_in_ARM9=True',
})
getters_source=checked_text(getters_prior.source,{
    "203:'Sakura'}":"203:'Sakura',55:'David Flahven',56:'Georg Salzgitter',57:'Nagayoshi Kamuro'}",
    "len(result['rows'])==18":"len(result['rows'])==24",
    'both_name_getters_exact_for_all9_protected_actors':'both_name_getters_exact_for_all12_protected_actors',
    'all nine protected names from Hodram B311-B324 successor own startup':'all12 protected names from the cumulative residual candidate own startup',
})
env={**vars(prior),**getters_prior.env,**globals(),'__file__':__file__}
if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--getters']:
        exec(compile(getters_source,__file__+'::same-original-getters-own-fresh-RAM12-actors','exec'),env);env['verify_getters']()
    else:
        exec(compile(source,__file__+'::same-own-Rafael-smoke-boot-and28-owned-data-byte-inverse','exec'),env)
