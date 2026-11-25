"""Read the actual saved preview and native_font_plane_sha256 receipt keys."""
from pathlib import Path
SOURCE=Path('scripts/audit_hodram_opening_actual_v2027.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    old="path=Path(proof['native_plane']);pixels=path.read_bytes();assert sha(pixels)==proof['native_plane_sha256'];width=216"
    new="path=Path(proof['preview']);assert sha(path.read_bytes())==proof['preview_sha256'];im=Image.open(path).convert('RGB');pixels=bytes(int(im.getpixel((x,y))==(0,8,0))for y in range(64)for x in range(216));assert sha(pixels)==proof['native_font_plane_sha256'];width=216"
    assert text.count(old)==1;text=text.replace(old,new).replace('hodram_opening_actual_v2027','hodram_opening_actual_v2027d')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
