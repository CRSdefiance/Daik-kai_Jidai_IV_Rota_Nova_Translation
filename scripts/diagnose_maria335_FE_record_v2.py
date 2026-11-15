"""Observe one exact failed FE layout with the unchanged guarded native painter."""
import argparse
import inspect
from pathlib import Path
from scripts import diagnose_maria335_B139_R199_FE_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--id',required=True)
    ap.add_argument('--plan',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    source=checked_text(inspect.getsource(previous.main),{
        "out=ROOT/'FE_B139_R199_diagnostic_v1'":"out=args.out",
        "planpath=ROOT/'plan_continuity_v2/automatic_plans.json'":"planpath=args.plan",
        "r['id']=='DK4_MES_B139_R0199'":"r['id']==args.id",
    })
    env={**previous.main.__globals__,'args':args,'__file__':__file__}
    exec(compile(source,__file__+'::same-guarded-observation-exact-record','exec'),env)
    env['main']()


if __name__=='__main__':main()
