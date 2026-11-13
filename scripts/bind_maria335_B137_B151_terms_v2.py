"""Select exactly referenced commodity names, excluding unreferenced qualified-name suffixes."""
import inspect
import struct
from scripts import bind_maria335_B137_B151_terms_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def referenced_goods_fields(clean,ats):
    pairs=[]
    for text_at in ats:
        needle=struct.pack('<I',previous.BASE+text_at);start=0
        while (field:=clean.find(needle,start))>=0:
            if field%4==0:pairs.append((text_at,field))
            start=field+1
    assert len(pairs)==1,(ats,pairs)
    return [pairs[0][1]]


source=checked_text(inspect.getsource(previous.main),{
    "        assert len(ats)==1,(japanese,ats)\n        pointer=struct.pack('<I',BASE+ats[0]);fields=[];start=0\n        while (at:=clean.find(pointer,start))>=0:\n            if at%4==0:fields.append(at)\n            start=at+1":
        "        fields=referenced_goods_fields(clean,ats)",
    '[currentpath,activepath,helppath,itempath,ruinpath,Path(__file__)]':'[currentpath,activepath,helppath,itempath,ruinpath,Path(previous.__file__),Path(__file__)]',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-exact-source-pointer-current-RAM-Help-andterm-guards','exec'),env)
if __name__=='__main__':env['main']()
