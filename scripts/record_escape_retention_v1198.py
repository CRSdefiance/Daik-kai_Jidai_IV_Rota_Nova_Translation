"""Retain a preview-only ROM inventory receipt; never apply deletions."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    plan=Path('work/rom_retention/20261021T1910351630555Z.json');doc=read(plan)
    assert len(doc['roms'])==227 and sum(r['action']=='keep' for r in doc['roms'])==199
    assert not plan.with_suffix('.result.json').exists() and not plan.with_suffix('.journal.jsonl').exists()
    assert all(Path(r['path']).is_file() and Path(r['path']).stat().st_size==r['bytes'] for r in doc['roms'])
    row=next(r for r in doc['roms'] if r['path'].lower().endswith('out\\all_routes_combined_v1189_candidate.nds'))
    assert row['action']=='keep' and row['reason'].startswith('pinned:')
    archive=Path('E:/Rota Nova translations/Editorial review/V1197 Direct escape correction and completion')
    dest=archive/'retention_preview.json';receipt=archive/'retention_preview_receipt.json'
    assert not dest.exists() and not receipt.exists();copy2(plan,dest)
    assert dest.read_bytes()==plan.read_bytes()
    save(receipt,{'plan':str(plan),'plan_sha256':sha(plan.read_bytes()),'archived_plan':str(dest),
        'all227_inventory_ROMs_still_present_at_original_lengths':True,'keep_count':199,'proposed_delete_count':28,
        'no_ApplyPlan_result_or_deletion_journal':True,'no_deletions_performed':True,
        'current_V1189_physically_pinned':True,'automatic_preview_review_initially_required_branch_inspection_then_approved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    copy2(Path(__file__),archive/'scripts'/Path(__file__).name)
    print('Retention preview archived:227 ROMs still present;199 kept,28 proposed only; no deletion.',flush=True)


if __name__=='__main__':main()
