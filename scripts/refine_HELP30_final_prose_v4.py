"""Close the assignment-hub link and strategist-inspiration findings before final formatting."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')
if __name__=='__main__':
    prior=ROOT/'whole_article_comparisons_v3.json';out=ROOT/'whole_article_comparisons_v4.json';assert not out.exists()
    doc=deepcopy(load(prior))
    row=next(r for r in doc['records']if r['topic_id']==105)
    assert '[[106| Personnel,]]'in row['english']
    row['english']=row['english'].replace('[[106| Personnel,]]','[[106| Crew Setup,]]')
    row.update(decision='revision',retention_reason=None,finding='Retain the clear assignment, prerequisite and ability explanation; change the assignment-hub link to the actually observed Crew Setup caption so it matches article106 and the current menu.')
    row['localization_note']=row['finding']
    row=next(r for r in doc['records']if r['topic_id']==118)
    row['english']='Officers assigned here become Strategists and need Tactics 120 or higher. When your Strategist has an idea, you can choose [[16|Plot]] at the Tavern. They may also stop enemy schemes before they happen. When you stay at an Inn, they gather information about other factions.'
    row['finding']='Use native Tactics for 謀略術120. ひらめく is getting an idea, rather than having already devised the scheme you are about to plan. Use the reviewed Plot command caption; preserve possible prevention of enemy schemes and inn-triggered information gathering.'
    row['localization_note']=row['finding']
    assert all(all(r['review'][g]for g in ['source','context','localization','naturalness'])and not r['review']['formatting']for r in doc['records'])
    assert sum(r['decision']=='revision'for r in doc['records'])==13
    doc.update(proposed_revisions=13,justified_retentions=17,all18_retained_bodies_word_exact_with_titles_reviewed_separately=False,
        all17_retained_bodies_word_exact_with_titles_reviewed_separately=True,previous_comparisons=str(prior),previous_comparisons_sha256=sha(prior.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(out,doc);print('Final30 prose:13 revisions/17 exact-body retentions;all four prose gates pass, display pending.')
