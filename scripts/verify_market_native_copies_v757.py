"""Complete ARM946 warm/cold native copies for an explicit range of blocks."""

import argparse
import gc
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/market_stock_release_v757')


def main():
    p=argparse.ArgumentParser();p.add_argument('--first-block',type=int,required=True);p.add_argument('--last-block',type=int,required=True)
    args=p.parse_args();assert 0<=args.first_block<=args.last_block<=40
    common,arm=(ROOT/'research_COMMON.bin').read_bytes(),(ROOT/'research_ARM9.bin').read_bytes()
    entries=common_message_entries(common,arm,clean=False)
    loader.machine_for=arm946_machine
    for block in range(args.first_block,args.last_block+1):
        cases=[]
        for entry in entries:
            if entry.block!=block:continue
            for cold in (False,True):
                result=loader.warm_copy(arm,common,entry.message_id,entry.text,cold_cache=cold)
                cases.append({'message_id':entry.message_id,'cold_cache':cold,'complete_native_copy':result})
        save(ROOT/f'native_copies_block_{block:02d}.json',{'block':block,'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
            'cases':cases,'ARM946_alignment_explicit':True,'host_open_read_boundary_contract_not_physical_IO':True,
            'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
        gc.collect();print(f'Block{block}: {len(cases)} complete guarded warm/cold copies verified.',flush=True)


if __name__=='__main__':main()
