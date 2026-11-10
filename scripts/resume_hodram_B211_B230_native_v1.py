"""Keep completed per-block native proofs and use the zero-authored-break runner."""
from scripts import resume_editorial_native_blocks_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'scripts/check_editorial_compiled_pages_v5.py':'scripts/check_editorial_compiled_pages_v8.py',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-block-reuse-with-zero-authored-break-checks','exec'),{**vars(previous),'__file__':__file__,'__name__':'__main__'})
