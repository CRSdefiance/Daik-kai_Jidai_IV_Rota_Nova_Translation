"""Exact reviewed Hodram-B49 labels in original order; native provider owns sizing."""
import struct
from dk4tool.dialogue.hodram_B49_profile_v1 import contract

def compile_choices(rows):
    d=contract();bindings=d["choice_bindings"]
    if not isinstance(rows,list) or len(rows)!=2 or any(not isinstance(r,dict) for r in rows) or [r.get("id") for r in rows]!=list(bindings):
        raise ValueError("Exact Hodram-B49 two-choice source order required")
    chunks=[];offsets=[];cursor=0
    for row in rows:
        b=bindings[row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact Hodram-B49 choice source/prose/context required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual Hodram-B49 choice gates required")
        offsets.append(cursor);chunk=row["english"].encode("ascii")+b"\0"
        chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    result=struct.pack("<3H",0x2100,*offsets)+b"".join(chunks)
    if offsets!=[0,12] or result.hex()!=d["choice_object_hex"]:
        raise ValueError("Exact Hodram-B49 original-count/source-index native choice object required")
    return result
