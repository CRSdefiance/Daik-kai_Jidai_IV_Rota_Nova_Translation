"""Preserve the two-choice native contracts while resolving optional span paths from the exact owning route."""
from scripts import check_editorial_two_choice_explicit_captain_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    source,current=bytes.fromhex(rows[0]['source_choice_object_hex']),bytes.fromhex(rows[0]['current_choice_object_hex'])":
        "    assert doc['file_path'] in ['/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4']\n    assert all(r['file_path']==doc['file_path'] and all(r[k].get('file_path',doc['file_path'])==doc['file_path'] for k in ['source_reference','current_reference']) for r in rows)\n    source,current=bytes.fromhex(rows[0]['source_choice_object_hex']),bytes.fromhex(rows[0]['current_choice_object_hex'])",
    "image.read_file(ref['file_path'])":"image.read_file(ref.get('file_path',doc['file_path']))",
})
scope={**previous.main.__globals__,'__file__':__file__};exec(compile(source,__file__+'::same-two-choice-ABI-pixels-bounds-rejections-exact-owning-route-path','exec'),scope)
main=scope['main']
if __name__=='__main__':main()
