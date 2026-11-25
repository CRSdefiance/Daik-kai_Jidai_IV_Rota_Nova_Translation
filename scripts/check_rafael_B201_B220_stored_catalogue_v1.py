"""Verify every reconstructed speech survives the original pre-macro catalogue lookup."""
from scripts.prepare_rafael_B181_B200_focus_v1 import catalogue as prior, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(prior,{
    'Rafael_B181_B200_current2165_20261106':'Rafael_B201_B220_current2549_20261106',
    'len(rows)==384':'len(rows)==382',
    'all384_stored_effective_body_bindings.json':'all382_stored_effective_body_bindings.json',
    '384 stored story and town bodies pass':'382 stored story and town bodies pass',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-original-lookup-all-382-speeches','exec'),globals())

