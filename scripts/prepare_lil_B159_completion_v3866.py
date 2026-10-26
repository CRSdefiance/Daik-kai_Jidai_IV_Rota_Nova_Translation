"""Derive completion of the41 already credited source/prose reviews without duplicate review credit."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/complete_lil_B158_v3823.py');q=Path('scripts/complete_lil_B159_v3866.py');assert not q.exists();t=p.read_text(encoding='utf-8');changes={
        'B158':'B159','v3823':'v3866','V3823':'V3866','release_v3820':'release_v3863','startup_v3822':'startup_v3865','actual_v3814/actual_source_English_all19_panels_four_actors_four_FE_two_pauses_music_picture_and_return':'actual_v3857/actual_source_English_all41_panels_five_actors_elephant_vendor_meal_and_return','editorial_handoff_verification_v3801':'editorial_handoff_verification_v3844','Lil-B158-Cristina-tavern-music-dance-patrons19':'Lil-B159-Samwell-elephant-vendor-cooking-provocations-recruitment41',
        'all533_manifest':'all534_manifest','equal_V3778':'equal_V3819',"{'revise':14,'retain-wording':5}":"{'revise':17,'retain-wording':24}",
        '(5348,5329,19)':'(5389,5348,41)','5348':'5389','3433':'3450','1915':'1939','3495':'3536','5351':'5392','3749':'3790','v3800':'v3843','V3800':'V3843',
        'revised=14':'revised=17','retained=5':'retained=24','revised_count=14':'revised_count=17','retained_count=5':'retained_count=24','fresh_revisions=14':'fresh_revisions=17','fresh_retentions=5':'fresh_retentions=24','new_revisions=14':'new_revisions=17','justified_retentions=5':'justified_retentions=24','revisions=14':'revisions=17',
        '==19':'==41','records=19':'records=41','credit_added=19':'credit_added=41','completed_targets=19':'completed_targets=41','actual_selected_panels=19':'actual_selected_panels=41','new_completed_records=19':'new_completed_records=41','now_reviewed19':'now_reviewed41','all19':'all41','Complete19':'Complete41',
        'Other63 B159-B160':'Other22 B160','other63_B159_B160':'other22_B160','now_reviewed19_completed_in_V3819':'now_reviewed41_completed_in_V3862','[158]':'[159]','registration_v3818':'registration_v3861',
        'lil_B158_transition_review_v3815/full_screen_transition_and_all4_sheet_review':'lil_B159_transition_review_v3858/full_screen_transition_and_all7_sheet_review',
        'Full V3778 plus19-object manuscript;533 manifest batches/114 accepted layers.':'Full V3819 plus41-speech manuscript;534 manifest batches/114 accepted layers.','61 compiler negatives;release3820/startup3822 pass.':'55 compiler negatives;release3863/startup3865 pass.',
        '## V3823:19 Lil B158 reviews completed in V3819':'## V3866:41 Lil B159 reviews completed in V3862',
        'V3823:19 completed in registered V3819;14 revisions/5 retentions;5348 reread/integrated,5351 source/prose. Other63 and the full wider goal remain active.':'V3866:41 completed in registered V3862;17 revisions/24 retentions;5389 reread/integrated,5392 source/prose. Other22 and the full wider goal remain active.'}
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    needle='proofpaths=[';assert t.count(needle)==1;t=t.replace(needle,"proofpaths=[Path(doc['source_nameplate_consumer_proof']),")
    assert '(5389,5348,41)' in t and 'revisions=17,justified_retentions=24' in t
    compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B159_completion_tools_v3866');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(p),source_sha256=sha(p.read_bytes()),successor=str(q),successor_sha256=sha(q.read_bytes()),current_pending_verifier='work/analysis/editorial_handoff_verification_v3844/verified_handoff.json',no_ledger_or_docs_mutation_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
