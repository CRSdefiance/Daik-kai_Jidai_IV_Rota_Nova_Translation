"""Bind the polder term and distinct source/native monetary amounts."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_terms_v3541')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
HISTORY=Path('translations/lil_B139_B140_contextual_final_review_v1.json')
FUNDS=Path('work/analysis/lil_B141_funds_v3537b/source_million_threshold_and900000_payment_seven_boundary_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();source,history,funds=map(read,[SOURCE,HISTORY,FUNDS]);image=NdsImage.open(source['current_ROM']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[140];rows=[]
    for r in history['records']:
        if r['block']!=140 or 'ポルダー' not in r['source_Japanese']:continue
        at=r['integrated_reference']['offset'];raw=bytes.fromhex(r['integrated_hex']);assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert 'polder' in r['english'].casefold();rows.append(dict(id=r['id'],source_Japanese=r['source_Japanese'],approved_English=r['english'],current_reference=r['integrated_reference'],current_hex=r['integrated_hex']))
    assert rows and funds['source_threshold_gold']==1000000 and funds['source_payment_gold']==900000
    selected=[dict(id=r['id'],source_Japanese=r['source_Japanese'],source_hex=r['source_hex']) for r in source['records'] if r['source_record_index'] in [26,69,73,80]];assert len(selected)==4
    ROOT.mkdir(parents=True);save(ROOT/'source_current_polder_and_distinct_monetary_amounts.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),approved_context_review=str(HISTORY),approved_context_review_sha256=sha(HISTORY.read_bytes()),current_complete_B140_sha256=sha(block),approved_polder_entries=rows,source_B141_term_amount_entries=selected,native_finance_proof=str(FUNDS),native_finance_proof_sha256=sha(FUNDS.read_bytes()),million_total_and_predicate_threshold=1000000,student_borrowed_fraction='one tenth',remaining_amount_and_actual_payment=900000,currency_gold_not_cargo_gold=True,polder_is_land_reclamation_concept_not_new_town_name_or_completed_outcome=True,source_171_remains_unnamed_research_student_without_invented_degree_nationality_or_rank=True,no_new_source_or_completion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Approved polder entries and one-million total/900000 payment bound;currency and future construction remain distinct.')
