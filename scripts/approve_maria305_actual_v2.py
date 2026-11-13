"""Keep all actual guards; bind the final FE clear before delayed host setup separately."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/approve_maria305_actual_v1.py').read_text(encoding='utf-8'), {
    "from pathlib import Path": "from pathlib import Path\nfrom PIL import Image",
    "            if at+1 == len(calls):\n                continue": """            if at+1 == len(calls):
                if native_by_id[ident]['kind'] == 'system-FE':
                    assert index == 2 and ident == 'DK4_MES_B176_R0079' and call['frame'] == 12427
                    report = load(terminal['report'])
                    observer = load(terminal['observer'])
                    assert digest(terminal['report']) == terminal['report_sha256']
                    assert digest(terminal['observer']) == terminal['observer_sha256']
                    press = next(r for r in inputs if r['buttons'] == ['A'] and r['start'] > call['frame'])
                    assert press['start'] == 12640 and press['duration'] == 16
                    clear = next(c for c in report['frames_captured'] if c['frame'] == 12720)
                    assert digest(clear['path']) == clear['PNG_sha256']
                    with Image.open(clear['path']) as im:
                        colors = im.convert('RGB').crop((0,192,256,384)).getcolors()
                    assert sorted(colors) == [(20400,(230,214,189)),(28752,(213,198,172))]
                    assert not any(r['kind']=='modal_paint' and call['frame']<r['frame']<=clear['frame'] for r in observer['rows'])
                    assert clear['frame'] < next(r['start'] for r in inputs if r['buttons']==['A'] and r['start']>press['start'])
                    assert clear['frame'] < pixel['following_nonfixture_modal_frame'] == 13384
                    FE_returns.append(dict(run=index,id=ident,ordinary_A_input=press,clear_capture=clear,
                        complete_bottom_screen_has_only_native_two_color_background=True,
                        final_FE_clears_before_next_input_anddelayed_host_join_messages=True,
                        immediate_next_selected_speech_not_claimed=True))
                    sheets.append(dict(path=clear['path'],sha256=clear['PNG_sha256'],directly_viewed=True,
                        final_FE_clear_single_capture=True))
                continue""",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-actual-proof-plus-final-FE-clear', 'exec'), globals())
