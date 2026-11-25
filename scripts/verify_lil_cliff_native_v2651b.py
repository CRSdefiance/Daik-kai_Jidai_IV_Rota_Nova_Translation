"""Preserve2651 refusal;retain the font helper's keyword-only defaults."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_lil_cliff_native_v2651.py').read_text();old="argdefs=old_raster.__defaults__);pixels,events,font=raster(ctx.arm,wrapped)";new="argdefs=old_raster.__defaults__);raster.__kwdefaults__=old_raster.__kwdefaults__;pixels,events,font=raster(ctx.arm,wrapped)";assert source.count(old)==1;source=source.replace(old,new).replace('lil_cliff_native_v2651','lil_cliff_native_v2651b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
