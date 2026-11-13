"""Apply the qualified original-role binder to an explicit complete batch scope."""
import argparse
import inspect
from pathlib import Path
from scripts import bind_maria328_roles_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    ap.add_argument('--expected-records',type=int,required=True)
    ap.add_argument('--selectors',type=int,nargs='+',required=True)
    args=ap.parse_args();assert args.selectors==sorted(set(args.selectors))
    source=checked_text(inspect.getsource(previous.main),{
        'assert len(records) == 38 and selectors == [207,208,214,215]':
            'assert len(records) == EXPECTED_RECORDS and selectors == SELECTORS',
        'captain==3':'captain=='+str(args.captain),
        'captain=3':'captain=CAPTAIN',
        'all14_ordinary_and24_physical_style_references_bound=True':
            'all_scoped_ordinary_andphysical_style_references_bound=True,scoped_reference_count=len(records)',
    })
    env={**vars(previous),'ROOT':args.root,'CAPTAIN':args.captain,'EXPECTED_RECORDS':args.expected_records,
        'SELECTORS':args.selectors,'__file__':__file__}
    exec(compile(source,__file__+'::same-original-dynamic-role-ABI-source-headers-and-snapshot-contract','exec'),env)
    env['main']()


if __name__=='__main__':main()
