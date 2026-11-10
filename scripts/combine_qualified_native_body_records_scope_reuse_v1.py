"""Join exact completed native records while keeping older runtime identity explicit."""
import inspect
from scripts import combine_qualified_native_body_records_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(prior.main),{
    "assert runtime['candidate_sha256']==doc['current_ROM_sha256']":
        "assert runtime==doc['runtime'] and doc['current_ROM_sha256']==doc['exact_existing_native_context_reuse']['target_candidate_sha256']",
    'runtime=runtime,font_sha256=font,records=records,':
        "runtime=runtime,native_context_reuse=doc['exact_existing_native_context_reuse'],font_sha256=font,records=records,",
})
env={**vars(prior),'__file__':__file__}
exec(compile(source,__file__+'::same-every-record-native-guards-explicit-current-scope-provenance','exec'),env)

if __name__=='__main__':env['main']()
