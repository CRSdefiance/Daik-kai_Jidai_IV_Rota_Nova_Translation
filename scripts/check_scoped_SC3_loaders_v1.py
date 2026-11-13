"""Run the qualified complete SC3 archive/cache/parent proof on an explicit rebuild."""
import argparse
import inspect
from pathlib import Path
from scripts import check_maria301_loaders_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['reconstruction','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--expected-changed-blocks',type=int,required=True)
    args=ap.parse_args()
    source=checked_text(inspect.getsource(previous.main),{
        "len(rebuilt['changed_blocks']) == 32":f"len(rebuilt['changed_blocks']) == {args.expected_changed_blocks}",
        'Maria301-stored-research':'SC3-scoped-stored-research',
    })
    env={**vars(previous),'REBUILT':args.reconstruction,'OUT':args.out,'__file__':__file__}
    exec(compile(source,__file__+'::same303-native-loader-cache-and606-parent-handoff-contract','exec'),env)
    env['main']()


if __name__=='__main__':main()
