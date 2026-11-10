"""Keep the clean negative concern and Rafael's reassuring answer coherent in English."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
ID='DK4_MES_B69_R0069'
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subset',action='store_true');args=parser.parse_args()
    if args.subset:
        full=ROOT/'formatting_input_v4.json';plan=ROOT/'automatic_v11/automatic_plans.json'
        doc,plans=map(load,[full,plan]);target=ROOT/'reassurance_native_subset_v11'
        assert not target.exists();target.mkdir()
        subset=deepcopy(doc);subset.update(records=[r for r in doc['records'] if r['id']==ID],
            subset_of=str(full),subset_of_sha256=sha(full.read_bytes()))
        manuscript=target/'manuscript.json';save(manuscript,subset)
        subplan=deepcopy(plans);subplan.update(records=[r for r in plans['records'] if r['id']==ID],
            manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
            subset_of=str(plan),subset_of_sha256=sha(plan.read_bytes()))
        assert len(subset['records'])==len(subplan['records'])==1 and not subplan['failures']
        save(target/'plans.json',subplan)
        print('Prepared one exact changed FE page;538 unchanged records retain their existing native evidence.')
    else:
        source=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v3.json')
        output=source.with_name('rafael_B61_B80_contextual_editorial_manuscript_v4.json')
        prior=ROOT/'formatting_input_v3.json';formatted=ROOT/'formatting_input_v4.json'
        assert not output.exists() and not formatted.exists()
        reason=('Clean 似合わない？ and そんなことないよ！ express outfit insecurity and reassurance. '
            'Doesn\'t it suit me? followed by Not at all! can sound like an insult in English. '
            'Does it look bad on me? preserves her concern and makes the retained Not at all! clearly reassuring; '
            'her Really?/first-time outfit explanation and his Looks wonderful! remain coherent.')
        for before,after in [(source,output),(prior,formatted)]:
            doc=deepcopy(load(before));row=next(r for r in doc['records'] if r['id']==ID)
            assert row['english']=="Doesn't it suit me?" and bytes.fromhex(row['source_hex'])[1:].decode('cp932')=='似合わない？'
            row.update(english='Does it look bad on me?',finding=reason,
                contextual_followup=dict(previous_English=row['english'],source_question='似合わない？',
                    source_answer='そんなことないよ！',answer_id='DK4_MES_B69_R0073',
                    preceding_id='DK4_MES_B69_R0065',following_ids=['DK4_MES_B69_R0078','DK4_MES_B69_R0082'],
                    no_new_relationship_rank_story_fact_or_completion_credit=True))
            answer=next(r for r in doc['records'] if r['id']=='DK4_MES_B69_R0073')
            assert answer['english']=='Not at all!' and bytes.fromhex(answer['source_hex'])[1:].decode('cp932')=='そんなことないよ！'
            answer['finding']='Retain the emphatic reassurance Not at all! in reply to the corrected negative appearance concern. It now clearly denies that the outfit looks bad.'
            assert row['decision']=='revision' and answer['decision']=='retention'
            doc.update(previous_manuscript=str(before),previous_manuscript_sha256=sha(before.read_bytes()),
                additional_contextual_reassurance_finding=reason,one_changed_English_ID=ID,
                proposed_revisions=210,wording_retentions=329,new_credit=0,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(after,doc)
        assert ID not in load(ROOT/'visual_preferences_v9.json')['records']
        print('Corrected one negative-question exchange;210 proposed revisions/329 retentions unchanged. Fresh one-page formatting pending.')
