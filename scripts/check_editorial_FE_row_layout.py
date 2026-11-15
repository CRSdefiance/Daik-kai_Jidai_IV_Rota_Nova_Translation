"""Compare planned FE rows with observed original-painter glyph positions."""
import argparse
from collections import defaultdict
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['plan','native','out']:parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--record-findings',action='store_true')
    args=parser.parse_args();assert not args.out.exists()
    plan,native=map(load,[args.plan,args.native]);assert native['plan_sha256']==sha(args.plan.read_bytes())
    expected={r['id']:r for r in plan['records']};rows=[];failures=[]
    for row in native['records']:
        if row['kind']!='system-FE':continue
        target=[]
        for line in expected[row['id']]['lines']:
            for macro,name in [('FI','Hodram'),('FA','Bergstrom'),('FO','Bergstrom Fleet')]:line=line.replace('{MACRO:'+macro+'}',name)
            target.append(line)
        observed=defaultdict(str)
        for event in row['complete_native_English_display']['events']:
            if event['kind']=='ascii':observed[event['y']]+=chr(event['code'])
            else:raise ValueError('Additional native glyph kind needs explicit layout mapping')
        visible=[dict(y=y,text=text.strip()) for y,text in sorted(observed.items()) if text.strip()]
        wanted=[dict(y=i*12,text=t) for i,t in enumerate(target)]
        passed=visible==wanted and len(wanted)<=4
        result=dict(id=row['id'],planned_rows=wanted,observed_rows=visible,pass_exact_logical_row_placement=passed)
        rows.append(result)
        if not passed:failures.append(result)
    save(args.out,dict(plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),native=str(args.native),native_sha256=sha(args.native.read_bytes()),
        records=rows,FE_records=len(rows),findings=failures,unexpected_blank_rows_orwraps_absent=not failures,
        original_painter_coordinates_not_an_illustrative_font_preview=True,new_credit=0,actual_gameplay=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('FE layout:',len(rows),'records;',len(failures),'findings')
    assert not failures or args.record_findings

if __name__=='__main__':main()
