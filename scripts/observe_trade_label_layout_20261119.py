"""Observe Trade label arguments and clip rectangles during an ordinary replay."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_market_context_v2112 as observer_base
from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_trade_labels_20261119 as replay
from scripts.source_locked_derivation_v5118 import checked_text

base = replay.base
TARGETS = (0x020D5404,)
TRADE_TEXT = (0x020C1384,0x020C13A8,0x020C13CC,0x020C1888,0x020C18AC,0x020C18D0,
              0x020C18F4,0x020C1918,0x020C1BC4,0x020C1BE8,0x020C20A0,0x020C22AC)


def observer(rom,folder):
    scope = vars(observer_base)|dict(ROOT=folder,ROM=rom,TARGETS=TARGETS,TRADE_TEXT=TRADE_TEXT)
    code = checked_text(getsource(observer_base.prepare_contract),{'for pc in(REQUEST,FONT):':'for pc in TARGETS:'})
    exec(compile(code,__file__+"::trade_contract","exec"),scope)
    scope['prepare_contract']()
    source = getsource(observer_base.Observer)
    first = source.index('    if frame<31000:return')
    last = source.index('   except BaseException as exc:',first)
    replacement = '''    if v[18] not in TRADE_TEXT:return
    ctx,pointer = v[4:6]
    if 0x02000000<=ctx<=0x023FFFC0:
     context=ct.string_at(self.wram+ctx-0x02000000,64)
    else:
     origin=struct.unpack('<I',self.image.read(self.dtcm_base,4))[0]
     assert origin<=ctx<=origin+0x4000-64,(ctx,origin)
     context=self.image.read(self.dtcm+ctx-origin,64)
    assert 0x02000000<=pointer<=0x023FFFC0
    text=ct.string_at(self.wram+pointer-0x02000000,64).split(b'\0')[0]
    words=struct.unpack('<16I',context)
    key=v[18],pointer,text,words[1:5],words[9:11]
    if key in self.seen:return
    self.seen.add(key)
    self.rows.append(dict(frame=frame,caller_LR=v[18],context=ctx,pointer=pointer,text=text.decode('cp932'),
                          text_hex=text.hex(),clip_rect=words[1:5],cursor=words[9:11],view_words=words))
'''.replace('\0','\\0')
    exec(compile(source[:first]+replacement+source[last:],__file__+"::trade_observer","exec"),scope)
    return scope['Observer']


def input_schedule(case):
    assert case=='baseline_trace'
    plan = base.load(replay.PLAN)
    inputs = Path(plan['unchanged_inputs'])
    assert base.digest(inputs)==plan['unchanged_inputs_sha256']
    return base.load(inputs),list(replay.FRAMES),11600,inputs,plan['source_save']


def main():
    scope = vars(playback)|dict(ROOT=replay.ROOT,parent=SimpleNamespace(ROM=replay.parent.ROM,RELEASE=replay.parent.RELEASE),
        observer=observer,get_schedule=input_schedule,FOCUS=set(),__file__=__file__)
    exec(compile(getsource(playback.main),__file__+"::ordinary_trade_observation","exec"),scope)
    scope['main']('baseline_trace')


if __name__=='__main__':
    main()
