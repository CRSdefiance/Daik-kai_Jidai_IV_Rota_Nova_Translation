"""Prepare reversible reference sealing; production mutation remains gated on completed policy."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/seal_Rafael_B47_references_v8006.py','scripts/seal_Rafael_B48_references_v8060.py',{
        'B47':'B48','R53':'R347','Rafael15':'Rafael91',
        'Rafael_B47_release_paths_v8006':'Rafael_B48_release_paths_v8060',
        'Rafael_B47_reference_tools_v8006':'Rafael_B48_reference_tools_v8060',
        "{'B45':'B47'}":"{'B45':'B48'}",
        "policy['positive_count']==15 and policy['negative_count']==302":"policy['positive_count']==91 and policy['negative_count']==1454",
        "group['block']==47":"group['block']==48",'[47]':'[48]','block=47':'block=48','==1344':'==4948',
        'all15':'all91','all48_commands24_relative_sites120_cases':'all163_commands28_relative_sites140_cases',
        'four_native_only_speeches_andJanus_header_explicit':'thirteen_native_only_speeches_andthree_headers_explicit',
        'fifteen exact':'ninety-one exact','15 exact records/48 commands/24 fixups':'91 exact records/163 commands/28 fixups',
    }))
