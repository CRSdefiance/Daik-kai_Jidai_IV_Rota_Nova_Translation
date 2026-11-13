"""Original546B8 no-argument notice and full native/independent literal font."""
import inspect,textwrap
from pathlib import Path
from scripts import probe_inspection_status_fonts_v1574 as previous
from scripts.hot_spring_notice_plan_v1632 import compiled
if __name__=='__main__':
    source=textwrap.dedent(inspect.getsource(previous).split("if __name__=='__main__':\n",1)[1])
    source=source.replace('E:/Rota Nova translations/Generated/work/emulation_v193/sea_inspection_final_v1567d_1563/frame_006100_arm9_ram.bin',
        'E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_live_v1626_1622/frame_009830_arm9_ram.bin')
    source=source.replace('both_native_status_panels_2x.png','Experience_notice_native_panel_2x.png').replace(
        'Both original546B8 pipelines and full native/independent glyph planes pass;12 invalid inputs rejected;literal modal origin x0 preserved.',
        'Original notice310 pipeline/full native-independent font passes;12 invalid inputs rejected;literal x0 and complete T/period preserved.')
    env={**previous.__dict__,'__file__':__file__,'compiled':compiled,'ROOT':Path('work/analysis/hot_spring_notice_fonts_v1633'),
        'PLAN':Path('work/analysis/hot_spring_notice_payload_v1632/native_payload_plan.json'),'DOC':Path('translations/hot_spring_notice_editorial_manuscript_v1.json')}
    exec(compile(source,__file__,'exec'),env)
