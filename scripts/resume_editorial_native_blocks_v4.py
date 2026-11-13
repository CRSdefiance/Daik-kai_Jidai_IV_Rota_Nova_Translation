"""Reuse exact checked blocks with distinct ordinary and virtual-style role preambles."""
from scripts.resume_hodram_B211_B230_native_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "            assert original['source_header_hex']==source_role['source_header_hex']\n            assert original['source_style_indices']==source_role['source_style_indices']":
        """            if original.get('native_object_kind')=='4100-style-alternative':
                assert source_role['kind']=='4100-style-alternative'
                assert original['source_header_hex']==source_role['source_header_hex']
                assert original['source_style_indices']==source_role['source_style_indices']
            else:
                assert source_role['kind']=='ordinary-speech'
                assert original['source_complete_preamble_hex']==source_role['source_complete_preamble_hex']""",
})
if __name__=='__main__':
    from scripts import resume_editorial_native_blocks_v3 as base
    exec(compile(source,__file__+'::same-exact-block-reuse-and-complete-ordinary-orstyle-role-contract','exec'),
        {**vars(base),'__file__':__file__,'__name__':'__main__'})
