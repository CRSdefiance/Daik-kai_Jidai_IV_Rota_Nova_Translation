"""Apply the qualified complete-buffer native lookup to an explicit stored scope."""
import argparse
from pathlib import Path
from scripts import check_maria301_stored_catalogue_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['stored','current','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True);ap.add_argument('--expected-records',type=int,required=True)
    args=ap.parse_args()
    source=checked_text(previous.source,{
        "Path('work/Maria_B0_B32_clean_20261109/stored_catalogue_all_v1')":f'Path({str(args.out)!r})',
        "Path('work/Maria_B0_B32_clean_20261109/stored_v1/stored_native_verification.json')":f'Path({str(args.stored)!r})',
        "Path('work/Maria_B0_B32_clean_20261109/current_v1/current_effective.json')":f'Path({str(args.current)!r})',
        'captain=3':f'captain={args.captain}','==299':f'=={args.expected_records}',
        'all299_stored_effective_body_bindings.json':'all_stored_effective_body_bindings.json',
        'all299_ordinary_and_style_bodies_checked=True':f'all_scoped_ordinary_and_style_bodies_checked=True,body_count={args.expected_records}',
        '299 stored ordinary and alternate-voice bodies pass':f'{args.expected_records} stored ordinary and alternate-voice bodies pass',
    })
    exec(compile(source,__file__+'::same-full-buffer-SP-input-andunowned-memory-original-native-lookup','exec'),
        {'__file__':__file__,'__name__':'__main__','TEMPLATE':previous.TEMPLATE})


if __name__=='__main__':main()
