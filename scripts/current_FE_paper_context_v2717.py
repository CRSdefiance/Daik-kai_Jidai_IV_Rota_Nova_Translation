"""Reuse the frozen current typed FE painter without installing captured RAM."""
import ast
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.verify_lil_FE_display_v1737 import OBS,snapshots
from scripts.verify_village_wrap_v608 import read
from scripts import verify_lil_seville_FE_v2713 as prior

SOURCE=Path('scripts/verify_lil_seville_FE_v2713.py')
SOURCE_SHA='fcfb8487e12bc44574cf74265191f93c781a9117c61d9c18ea81329edce53d4a'
BASE=0x02000000

class CurrentFEPaper:
    def __init__(self,image):
        if sha(SOURCE.read_bytes())!=SOURCE_SHA:
            raise ValueError('Frozen typed-paper constructor/painter differs')
        arm=image.read_file('/__arm9__.bin')
        observed=read(OBS);captured=next(r for r in observed['rows'] if r.get('complete_readonly_snapshots'));data=snapshots(captured)
        actual_ctx=list(struct.unpack('<19I',bytes.fromhex(captured['context_76_hex'])))
        actual_view=list(struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex'])))
        actual_font=list(struct.unpack('<6I',bytes.fromhex(captured['font_object_24_hex'])))
        actual_header=list(struct.unpack_from('<5I',data['WRAM'],actual_view[4]-BASE));palette=(actual_view[4]+actual_header[3])&0xffffffff
        if not(actual_ctx[1:6]==[0,0,228,48,1] and actual_view[10:16]==[228,48,0,0,228,48] and actual_view[18:20]==[0,0] and actual_font[1:3]==[6,12] and actual_header[:3]==[4,72,48]):
            raise ValueError('Actual source FE mode1 geometry differs')
        assert data['WRAM'][palette-BASE:palette-BASE+32]==arm[palette-BASE:palette-BASE+32]
        for vt in [actual_ctx[0],actual_view[0],actual_view[20],actual_font[0],actual_font[5]]:
            assert BASE<=vt<BASE+len(arm)-32 and arm[vt-BASE:vt-BASE+32]==data['WRAM'][vt-BASE:vt-BASE+32]
        nodes=[n for n in ast.walk(ast.parse(SOURCE.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='paint']
        assert len(nodes)==1
        env={**prior.__dict__,**locals(),'ascii_font':GameAsciiFont.from_arm9(arm)}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE),'exec'),env)
        self.paint=env['paint'];self.captured=captured
        self.scope='Current cold machine plus captured typed graphics descriptors/font parameters with explicit pointer rebasing. No initialized historical RAM/ITCM/DTCM overlay. Frozen2713paint function andcanary/full-independent-plane checks execute unchanged.'
