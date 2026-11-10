"""Preserve the requested rough planning estimate; do not turn decoder candidates into a completion denominator."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_remaining_estimate_v8264')
SOURCE=Path('work/analysis/editorial_source_universe_v2701c/source_universe_inventory.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();source,ledger=map(read,[SOURCE,LEDGER])
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    counts={f['file_path']:f['counts']['strict-cp932-Japanese-candidate'] for f in source['files']}
    assert sum(counts.values())==27210 and ledger['records_editorially_completed']==7171
    ROOT.mkdir(parents=True);save(ROOT/'rough_candidate_estimate_not_full_goal_denominator.json',dict(
        clean_inventory=str(SOURCE),clean_inventory_sha256=sha(SOURCE.read_bytes()),source_ROM_sha256=source['source_ROM_sha256'],
        source_candidate_counts_by_file=counts,candidate_total=27210,editorially_completed=7171,
        arithmetic_candidate_difference=20039,communicated_approximation='About20,000 text candidates remain to be classified orreviewed across thefour story files andshared text.',
        pending_Hodram_contextual_drafts_not_completed=28,
        exact_player_facing_remaining_count_not_established=True,not_a_verified_fullgoal_denominator_orpercentage=True,
        limitations=['Native NUL/cp932 candidates can include control fragments and repeated text;candidate records are not all confirmed player-facing speech.',
            'Decoder-rejected genuine speech andtyped subobjects need source-consumer classification;completed keys do not all map one-to-one to this lexical inventory.',
            'Help,names,other remaining player-facing files andretrospective contextual/wrapping revisits add separate work;no exhaustive fullgoal denominator isclaimed.'],
        no_completion_credit_orROM_registry_ledger_change=True,new_credit=0,full_goal_complete=False,
        evidence={str(LEDGER):sha(LEDGER.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('Preserved rough20,000-candidate planning estimate;not an exact player-facing count orfullgoal denominator.')
