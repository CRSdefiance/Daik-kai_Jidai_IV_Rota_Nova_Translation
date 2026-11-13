"""Restore active skill labels; preserve the valid contextual prose and reopen five fresh display checks."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')
BIND=Path('work/analysis/HELP_active_skill_labels_20261105/active_terms_binding_v2.json')

def plain(text):return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]',r'\1',text).split())

if __name__=='__main__':
    old=ROOT/'whole_article_comparisons_v4.json';out=ROOT/'whole_article_comparisons_v5.json';assert not out.exists()
    prior=load(old);binding=load(BIND);doc=deepcopy(prior)
    assert binding['Help30_topics_requiring_correction']==[116,117,118,121,126]
    assert binding['inactive_original_Health_Social_Tactics_strings_are_not_active_skill_names']
    changes={116:('Health','Vigor'),117:('Social','Speech'),118:('Tactics 120','Guile 120'),121:('Social','Speech'),126:('Health','Vigor')}
    for row in doc['records']:
        n=row['topic_id']
        if n in changes:
            before,after=changes[n];assert before in row['english'];row['english']=row['english'].replace(before,after)
            if n in [116,117,126]:
                assert plain(row['english'])==plain(row['current_English'].split('\n',1)[1])
                row.update(decision='retention',retention_reason={116:'Retain the accurate Animal Keeper/Vigor130 explanation and food-only production effect.',
                    117:'Retain the accurate Missionary/Speech160 explanation, fatigue benefit, goods-to-trend link and belief-based refusal.',
                    126:'Retain the accurate Deckhand/Vigor30 explanation, boarding benefit, easier leveling and rapid-fatigue warning.'}[n])
                row['finding']=row['retention_reason']+' Active names confirmed from current own-RAM skill pointers and complete actual character-screen masks; earlier static-string correction is superseded.'
            else:
                row['finding']=('Use active Guile120; preserve source inspiration, reviewed Plot caption, possible scheme prevention and inn intelligence.'if n==118 else
                    'Use active Speech100; preserve First Mate duties, fatigue and surrender effects, and the reviewed Send Letter caption.')
            row['localization_note']=row['finding'];row['review']['localization']=True;row['review']['formatting']=False
            row['fresh_active_term_correction_needs_display']=True
        row['active_term_binding']=str(BIND);row['active_term_binding_sha256']=sha(BIND.read_bytes())
        row['previous_static_skill_inference_superseded']=True
        if row['decision']=='retention':assert plain(row['english'])==plain(row['current_English'].split('\n',1)[1])
    assert sum(r['decision']=='revision'for r in doc['records'])==10
    doc.update(proposed_revisions=10,justified_retentions=20,first_four_gates_passed=30,all_fifth_gates_pending=True,
        active_term_binding=str(BIND),active_term_binding_sha256=sha(BIND.read_bytes()),
        superseded_static_term_inference=['Health as active生命力','Social as active説得力','Tactics as active謀略術'],
        changed_article_IDs=[116,117,118,121,126],all20_retained_bodies_word_exact=True,
        previous_comparisons=str(old),previous_comparisons_sha256=sha(old.read_bytes()),
        all_unchanged_prose_gates_andcontrol_proofs_preserved=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    save(out,doc);print('Help30 corrected to active names:10 revisions/20 exact-body retentions. Five changed pages need fresh formatting;all other proofs retained.')
