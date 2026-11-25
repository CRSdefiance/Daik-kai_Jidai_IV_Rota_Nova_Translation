"""Observe the packed Town Summary headings in the original screen flow."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_market_context_v2112 as native
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_trade_categories_20261119 as current
from scripts import replay_lisbon_shopkeeper_20261119 as lisbon
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/town_summary_20261119')
RETURN = 0x020B6118


def observer(rom, folder):
    scope = vars(native) | dict(ROOT=folder, ROM=rom, RETURN=RETURN)
    code = checked_text(getsource(native.prepare_contract), {
        'for pc in(REQUEST,FONT):': 'for pc in (FONT,):',
    })
    exec(compile(code, __file__ + '::contract', 'exec'), scope)
    scope['prepare_contract']()
    source = getsource(native.Observer)
    first = source.index('    if frame<31000:return')
    last = source.index('   except BaseException as exc:', first)
    replacement = r'''    if v[18]!=RETURN or self.rows:return
    ctx, pointer = v[4:6]
    def word_address(address, size):
     if 0x02000000 <= address <= 0x02400000-size:
      return ct.string_at(self.wram+address-0x02000000, size)
     origin=struct.unpack('<I',self.image.read(self.dtcm_base,4))[0]
     assert origin<=address<=origin+0x4000-size,(address,origin)
     return self.image.read(self.dtcm+address-origin,size)
    layout = v[13]
    text=word_address(pointer,24)
    words=struct.unpack('<16I',word_address(ctx,64))
    self.rows.append(dict(frame=frame, caller_LR=RETURN, pointer=pointer, text_hex=text.hex(),
        clip_rect=words[1:5], cursor=words[9:11], layout_pointer=layout,
        layout_hex=word_address(layout,0x200).hex(), registers=v[4:20]))
'''
    exec(compile(source[:first] + replacement + source[last:], __file__ + '::summary', 'exec'), scope)
    return scope['Observer']


def schedule(_case):
    events, _, _, source, donor = lisbon.schedule('lisbon')
    return [r for r in events if r['start'] <= 5001], [3200, 3720, 4750, 5150], 5200, source, donor


def capture(case):
    parent = current
    if case == 'corrected':
        from scripts import stage_town_summary_20261119 as parent
    scope = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=observer, get_schedule=schedule,
                                 FOCUS=set(), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::lisbon', 'exec'), scope)
    scope['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('baseline_v2', 'corrected'))
    capture(parser.parse_args().case)
