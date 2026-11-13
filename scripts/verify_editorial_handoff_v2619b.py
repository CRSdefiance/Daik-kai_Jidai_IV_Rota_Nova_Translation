"""Keep the pre-execution draft;fix syntax and normalize Windows receipt paths."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2619.py').read_text()
 changes={"assert struct_unpack:=__import__('struct').unpack_from":"struct_unpack=__import__('struct').unpack_from",'else208':'else 208','else18':'else 18','editorial_handoff_verification_v2619':'editorial_handoff_verification_v2619b','V2619-audit':'V2619b-audit',"if p.startswith('docs/')or p=='translations/editorial_review_current_v1.json':":"if p.replace(chr(92),'/').startswith('docs/')or p.replace(chr(92),'/')=='translations/editorial_review_current_v1.json':"}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
