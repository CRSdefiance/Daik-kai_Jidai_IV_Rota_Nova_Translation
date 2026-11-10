"""Save individual whole-exchange decisions against exact sealed/current inputs."""
import argparse
import inspect
from pathlib import Path
from scripts import maria328_contextual_writer_v1 as previous
from scripts.seal_clean_editorial_prose_stage_v1 import row_key
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['root','drafts','decisions','out']:ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--expected-records',type=int,required=True)
    args=ap.parse_args();assert args.out.parent==args.root
    decisions={};number=None
    for line in args.decisions.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        if line.startswith('@'):
            number=int(line[1:]);assert number not in decisions;decisions[number]={};continue
        parts=line.split('|',3);key,mode,reason=parts[:3]
        assert number is not None and key not in decisions[number] and mode in ['R','D','T'] and reason.strip()
        assert len(parts)==(4 if mode=='T' else 3)
        decisions[number][key]=(None if mode=='R' else 'D' if mode=='D' else parts[3],reason)
    source=checked_text(inspect.getsource(previous.write),{
        "draft_path = ROOT/'all328_independent_drafts_v1.json'":"draft_path = DRAFT_PATH",
        "len(drafts['records']) == 328":"len(drafts['records']) == EXPECTED_RECORDS",
        "original['independent_English_draft']":"original['english']",
    })
    env={**previous.write.__globals__,'ROOT':args.root,'DRAFT_PATH':args.drafts,'EXPECTED_RECORDS':args.expected_records,
        'key':row_key,'__file__':__file__}
    exec(compile(source,__file__+'::same-individual-source-current-macro-andzero-gate-guards','exec'),env)
    assert sum(len(v) for v in decisions.values())==args.expected_records
    env['write'](decisions,args.out.name,args.decisions)


if __name__=='__main__':main()
