"""Preserve2646b boundary refusal;separate loaded template from post-printf input."""
from pathlib import Path
import re
if __name__=='__main__':
 source=Path('scripts/verify_support_fonts_v2646.py').read_text();source=re.sub(r'\belse(?=\d)','else ',source)
 old="assert native['input_hex']==ctx.entries[n].text.hex()and native['formatted_hex']==sample['formatted_hex']"
 new="loader_owner=int.from_bytes(ctx.arm[0x552A0:0x552A4],'little');native['loaded_template_hex']=bytes(ctx.machines[-1][0].mem_read(loader_owner+0x2030,512)).split(b'\\0')[0].hex();assert native['loaded_template_hex']==ctx.entries[n].text.hex()and native['input_hex']==ctx.entries[n].text.replace(b'%s',bytes.fromhex(sample['argument_case']['hex']),1).hex()and native['formatted_hex']==sample['formatted_hex']"
 assert source.count(old)==1;source=source.replace(old,new).replace('support_fonts_v2646','support_fonts_v2646c');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
