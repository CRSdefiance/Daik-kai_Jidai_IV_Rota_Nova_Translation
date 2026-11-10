"""Bind one inherited alignment-pad use, retaining complete native-command inverses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.script import reviewed_scene_rebuild_v3 as qualified
from scripts.rebuild_maria335_B137_B151_reviewed_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


def rebuild_block(arm,clean,current,records,compiled,inventory,compound):
    special=[r for r in records if len(bytes.fromhex(r['source_hex']))!=len(bytes.fromhex(r['current_hex']))]
    if not special:return qualified.rebuild_block(arm,clean,current,records,compiled,inventory,compound)
    assert len(special)==1
    row=special[0]
    assert row['id']=='DK4_MES_B139_R0177'
    assert row['source_hex']=='0a82b582a982b5814182b182cc946a97f592708ed282cd8163'
    assert row['current_hex']=='0a4275742074686973207368616d656c657373206d616e2e2e2e'
    at=row['source_reference']['offset']
    assert at==row['current_reference']['offset']==2059
    raw=bytes.fromhex(row['source_hex']);prior=bytes.fromhex(row['current_hex'])
    assert len(raw)==25 and len(prior)==26
    source_commands=inventory(arm,clean)[0];current_commands=inventory(arm,current)[0]
    a=next(c for c in source_commands if c['offset']==at-5)
    b=next(c for c in current_commands if c['offset']==at-5)
    assert a['word']==b['word']==0x4000 and a['native_extent']==b['native_extent']==32
    assert clean[at:at+27]==raw+b'\0\0' and current[at:at+27]==prior+b'\0'
    assert clean[at-5:at]==current[at-5:at]
    assert a['offset']+a['native_extent']==b['offset']+b['native_extent']==2086
    # Normalize only the inverse span: clean raw25 + its original NUL padding.
    # The actual source string/reference remains25 bytes in the returned proof.
    normalized=deepcopy(records)
    bound=next(r for r in normalized if r['id']==row['id'])
    bound['source_hex']=(raw+b'\0').hex()
    target,proof=qualified.rebuild_block(arm,clean,current,normalized,compiled,inventory,compound)
    item=next(r for r in proof['text_records'] if r['id']==row['id'])
    assert item['source_hex']==bound['source_hex']
    item.update(source_hex=row['source_hex'],clean_inverse_span_hex=bound['source_hex'],
        source_raw_string_length=25,current_raw_string_length=26,source_alignment_NUL_bytes_in_inverse_span=1,
        exact_native_command_extent_unchanged_before_rebuild=True)
    proof['inherited_source_alignment_pad_binding']=dict(id=row['id'],source_command=a,current_command=b,
        source_raw_hex=row['source_hex'],current_raw_hex=row['current_hex'],
        source_inverse_span_hex=bound['source_hex'],original_NUL_alignment_not_prose=True,
        source_current_native_command_boundaries_identical=True,full_clean_andparent_inverses_still_exact=True)
    return target,proof


source=checked_text(previous,{
    "from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block":
        "from scripts.rebuild_maria335_B137_B151_reviewed_v2 import rebuild_block",
    "ROOT/'reconstruction_v1'":"ROOT/'reconstruction_v2'",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-guards-one-exact-inherited-NUL-alignment-span','exec'),globals())
