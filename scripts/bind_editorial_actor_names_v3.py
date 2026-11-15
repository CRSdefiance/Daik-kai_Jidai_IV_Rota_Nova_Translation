"""Use the requested captain in the legacy selector proof as well as the runtime guard."""
from scripts.bind_editorial_actor_names_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "    voice_env=dict(original_names.__globals__)\n    exec(compile(prior['source_owned_voice_function'],__file__+'::current-voices','exec'),voice_env)":
        """    voice_env=dict(original_names.__globals__)
    voice_source=checked_text(prior['source_owned_voice_function'],{'assert captain==1':'assert captain=='+str(args.captain)})
    exec(compile(voice_source,__file__+'::current-voices-explicit-captain','exec'),voice_env)""",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-name-andvoice-ABI-whole-RAM-guards-explicit-captain','exec'),globals())
