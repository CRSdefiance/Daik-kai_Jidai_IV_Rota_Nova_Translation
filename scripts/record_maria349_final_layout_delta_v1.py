"""Record exact final layout changes and page savings without recounting credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')
def main():
    out=ROOT/'final_layout_delta_v1.json';assert not out.exists()
    before,after=[ROOT/p for p in ['plan_v1/automatic_plans.json','plan_v6/automatic_plans.json']]
    a,b=map(load,[before,after]);byid={r['id']:r for r in a['records']}
    changes=[dict(id=r['id'],before_hex=byid[r['id']]['encoded_hex'],final_hex=r['encoded_hex'],
        before_pages=byid[r['id']]['expected_native_pages'],final_pages=r['expected_native_pages'])
        for r in b['records'] if r['encoded_hex']!=byid[r['id']]['encoded_hex']]
    assert len(changes)==10 and sum(r['expected_native_pages'] for r in a['records'])==350
    assert sum(r['expected_native_pages'] for r in b['records'])==347
    save(out,dict(final_changed_record_count=10,pages_reclaimed=3,changes=changes,unchanged_logical_English_andnative_controls=True,
        evidence={str(p):digest(p) for p in [before,after,ROOT/'offline_display_approval_v1.json',Path(__file__)]},new_credit=0))
if __name__=='__main__':main()
