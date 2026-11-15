"""Combine exact, disjoint individual decisions; do not create editorial approval from counts."""
import argparse
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drafts',type=Path,required=True)
    parser.add_argument('--parts',type=Path,nargs='+',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    drafts=load(args.drafts)
    rows=[r for p in args.parts for r in load(p)['records']]
    assert len(rows)==len({r[0] for r in rows})==len(drafts['records'])
    assert {r[0] for r in rows}=={r['id'] for r in drafts['records']}
    assert all(len(r) in [3,4] and r[1] in ['revision','retention'] and r[2].strip() for r in rows)
    order={r['id']:i for i,r in enumerate(drafts['records'])};rows.sort(key=lambda r:order[r[0]])
    save(args.out,dict(format='dk4-whole-exchange-prose-decisions-v1',records=rows,
                      all_individual_decisions_authored_not_inferred_from_counts=True,
                      whole_source_draft_ID_membership_exact=True,new_credit=0,
                      evidence={str(p):sha(p.read_bytes()) for p in [args.drafts,*args.parts,Path(__file__)]}))
    print(dict(decisions=len(rows),revisions=sum(r[1]=='revision' for r in rows),retentions=sum(r[1]=='retention' for r in rows)))
