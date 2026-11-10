"""Keep all checked caption states legible when a menu spans the full native width."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
TEMPLATE=Path('scripts/render_native_caption_style_sheet_v1.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    "    args.out.mkdir();sheet=Image.new('RGB',(1100,((len(pictures)+1)//2)*66),'#263238');draw=ImageDraw.Draw(sheet)":
        "    column=max(550,max(pic.width*3+8 for _,pic in pictures))\n    args.out.mkdir();sheet=Image.new('RGB',(2*column,((len(pictures)+1)//2)*66),'#263238');draw=ImageDraw.Draw(sheet)",
    'x,y=i%2*550,i//2*66':'x,y=i%2*column,i//2*66',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-checked-native-pixels-adaptive-readable-columns','exec'),globals())
