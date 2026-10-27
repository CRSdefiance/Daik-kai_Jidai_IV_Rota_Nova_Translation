"""Derive completion tooling without changing the verified pending coverage ledger."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/complete_lil_B157_v3782.py');q=Path('scripts/complete_lil_B158_v3823.py');assert not q.exists();t=p.read_text(encoding='utf-8');changes={
        'B157':'B158','v3782':'v3823','V3782':'V3823','manuscript_v6':'manuscript_v5','release_v3779':'release_v3820','startup_v3781':'startup_v3822',
        'actual_v3773/actual_source_English_all75_panels_seven_actors_two_FE_pause_C281_4885_and_return':'actual_v3814/actual_source_English_all19_panels_four_actors_four_FE_two_pauses_music_picture_and_return','editorial_handoff_verification_v3760':'editorial_handoff_verification_v3801','Lil-B157-Carlo-trade-illness-grief-chosen-family75':'Lil-B158-Cristina-tavern-music-dance-patrons19',
        'all532_manifest':'all533_manifest','equal_V3738':'equal_V3778',"{'revise':31,'retain-wording':44}":"{'revise':14,'retain-wording':5}",
        '(5329,5254,75)':'(5348,5329,19)','5329':'5348','3419':'3433','1910':'1915','3476':'3495','5332':'5351','3730':'3749','v3759':'v3800','V3759':'V3800',
        'revised=31':'revised=14','retained=44':'retained=5','revised_count=31':'revised_count=14','retained_count=44':'retained_count=5','fresh_revisions=31':'fresh_revisions=14','fresh_retentions=44':'fresh_retentions=5','new_revisions=31':'new_revisions=14','justified_retentions=44':'justified_retentions=5','revisions=41':'revisions=14',
        '==75':'==19','records=75':'records=19','credit_added=75':'credit_added=19','completed_targets=75':'completed_targets=19','actual_selected_panels=75':'actual_selected_panels=19','new_completed_records=75':'new_completed_records=19','now_reviewed75':'now_reviewed19','all75':'all19','Complete75':'Complete19',
        'Other82 B158-B160':'Other63 B159-B160','other82_B158_B160':'other63_B159_B160','now_reviewed75_completed_in_V3778':'now_reviewed19_completed_in_V3819','[157]':'[158]','registration_v3777':'registration_v3818',
        'lil_B157_transition_review_v3775/full_screen_transition_and_all13_sheet_review':'lil_B158_transition_review_v3815/full_screen_transition_and_all4_sheet_review',
        'Full V3738 plus75-speech manuscript;532 manifest batches/114 accepted layers.':'Full V3778 plus19-object manuscript;533 manifest batches/114 accepted layers.',
        '64 compiler negatives;release3779/startup3781 pass.':'61 compiler negatives;release3820/startup3822 pass.',
        '## V3782:75 Lil B157 reviews completed in V3778':'## V3823:19 Lil B158 reviews completed in V3819',
        'V3782:75 completed in registered V3778;31 revisions/44 retentions;5329 reread/integrated,5332 source/prose. Other82 and the full wider goal remain active.':'V3823:19 completed in registered V3819;14 revisions/5 retentions;5348 reread/integrated,5351 source/prose. Other63 and the full wider goal remain active.'
    }
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    assert '(5348,5329,19)' in t and 'revisions=14,justified_retentions=5' in t
    compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B158_completion_tools_v3823');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(p),source_sha256=sha(p.read_bytes()),successor=str(q),successor_sha256=sha(q.read_bytes()),current_pending_verifier='work/analysis/editorial_handoff_verification_v3801/verified_handoff.json',no_ledger_or_docs_mutation_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
