"""Use the same source-bound catalogue lookup with the current actual Rafael context."""
from scripts import extract_editorial_current_v6 as previous
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx = RegisteredRuntime(args.release,args.startup)':'ctx = RegisteredRuntime(args.release,args.startup,captain=0)',
})
env={**previous.__dict__,'RegisteredRuntime':RegisteredRuntime,'__file__':__file__}
# v6 owns the assembled function in its globals; retain the original modules and
# source guards while changing only the explicit own-context constructor.
exec(compile(source,__file__+'::same-native-catalogue-lookup-own-Rafael-context','exec'),env)
main=env['main']
if __name__=='__main__':main()
