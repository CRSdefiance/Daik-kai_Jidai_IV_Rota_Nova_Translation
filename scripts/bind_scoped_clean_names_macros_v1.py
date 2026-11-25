"""Run the qualified scoped name and default-macro binder for a sealed clean batch."""
import argparse
import inspect
from pathlib import Path
from scripts import bind_maria286_names_macros_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['root','drafts','current','out']:ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    ap.add_argument('--spoken',nargs='*',default=[])
    args=ap.parse_args();assert len(args.spoken)==len(set(args.spoken))
    source=checked_text(inspect.getsource(previous.main),{
        "ROOT/'scoped_names_macros_reference_v1.json'":"OUTPUT",
        "ROOT/'all286_clean_meanings_andindependent_drafts_v2.json'":"DRAFTS",
        "ROOT/'current_v1/current_effective.json'":"CURRENT",
        'captain=3':'captain=CAPTAIN',
        "expected={'ハイレディン','バルデス','パシャ','クーン','エスカンテ'}":"expected=EXPECTED",
        'assert len(spoken)==5 and expected==':'assert len(spoken)==len(EXPECTED) and expected==',
        'assert get(0x7F244)==3':'assert get(0x7F244)==CAPTAIN',
        "scope='one aligned default-name call on captain3; not arbitrary custom names or complete formatting approval'":
            "scope=f'one aligned default-name call on captain{CAPTAIN}; not arbitrary custom names or complete formatting approval'",
    })
    env={**vars(previous),'ROOT':args.root,'OUTPUT':args.out,'DRAFTS':args.drafts,'CURRENT':args.current,
        'EXPECTED':set(args.spoken),'CAPTAIN':args.captain,'__file__':__file__}
    exec(compile(source,__file__+'::same-source-fields-original-name-getters-and-macro-ABI','exec'),env)
    env['main']()


if __name__=='__main__':main()
