"""Check the three original B84 training choices with complete dynamically guarded input ownership."""
from scripts import check_editorial_three_choice_single as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
    '    # Same three-index consumer contract as the earlier source-qualified Lil proof.':
        """    adapter=checked_text(adapter,{
        "b'\\\\xA5' * 96":"b'\\\\xA5' * (len(object_bytes)+32)",
        'cpu.mem_read(text - 16, 96)':'cpu.mem_read(text - 16, len(object_bytes)+32)',
    })
    # Same three-index consumer contract as the earlier source-qualified Lil proof.""",
    'assert len(raw)+16<=96 and max(map(len,labels(raw)))<32':
        'assert len(raw)+32<=0x1000 and max(map(len,labels(raw)))<32',
    'compiler_owned_zero_alignment_only_no_speech_encoder=True,':
        'compiler_owned_zero_alignment_only_no_speech_encoder=True,entire_source_object_and16byte_guards_preserved_at_both_ends=True,',
})
exec(compile(source,__file__+'::same-native-three-choice-provider-with-full-input-canary-ownership','exec'),globals())
