"""Prepare completion tooling without touching the verified coverage ledger."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    src=Path('scripts/complete_lil_B156_v3742.py');dst=Path('scripts/complete_lil_B157_v3782.py');assert not dst.exists();t=src.read_text(encoding='utf-8')
    replacements={
        'B156':'B157','v3742':'v3782','V3742':'V3782',
        'manuscript_v7':'manuscript_v6','release_v3739':'release_v3779','startup_v3741':'startup_v3781',
        'actual_v3733/actual_source_English_all76_panels_ten_actors_resources_C200_and_return':'actual_v3773/actual_source_English_all75_panels_seven_actors_two_FE_pause_C281_4885_and_return',
        'editorial_handoff_verification_v3720':'editorial_handoff_verification_v3760',
        'Lil-B156-Ian-tavern-harassment-rescue-recruitment76':'Lil-B157-Carlo-trade-illness-grief-chosen-family75',
        'all531_manifest':'all532_manifest','equal_V3692':'equal_V3738',
        "{'revise':41,'retain-wording':35}":"{'revise':31,'retain-wording':44}",
        '(5254,5178,76)':'(5329,5254,75)',
        '5254':'5329','3388':'3419','1866':'1910','3401':'3476','5257':'5332','source/prose5181':'source/prose5332',
        '3655':'3730','v3719':'v3759','V3719':'V3759',
        'revised=41':'revised=31','retained=35':'retained=44','revised_count=41':'revised_count=31','retained_count=35':'retained_count=44',
        'fresh_revisions=41':'fresh_revisions=31','fresh_retentions=35':'fresh_retentions=44','new_revisions=41':'new_revisions=31','justified_retentions=35':'justified_retentions=44',
        '==76':'==75','records=76':'records=75','credit_added=76':'credit_added=75','completed_targets=76':'completed_targets=75','actual_selected_panels=76':'actual_selected_panels=75',
        'new_completed_records=76':'new_completed_records=75','now_reviewed76':'now_reviewed75','all76':'all75','Complete76':'Complete75',
        'Other157 B157-B160':'Other82 B158-B160','other157_B157_B160':'other82_B158_B160',
        'now_reviewed76_completed_in_V3738':'now_reviewed75_completed_in_V3778',
        '[156]':'[157]',"registration_v3737":"registration_v3777",
        'Full V3692 plus76-speech manuscript;531 manifest batches/114 accepted layers.':'Full V3738 plus75-speech manuscript;532 manifest batches/114 accepted layers.',
        '76 compiler negatives;release3739/startup3741 pass.':'64 compiler negatives;release3779/startup3781 pass.',
        '## V3742:76 Lil B156 reviews completed in V3738':'## V3782:75 Lil B157 reviews completed in V3778',
        'V3742:76completed inregisteredV3738;28revisions/22retentions;5178reread/integrated,5181source-prose. Other157andfull widergoalactive.':'V3782:75 completed in registered V3778;31 revisions/44 retentions;5329 reread/integrated,5332 source/prose. Other82 and the full wider goal remain active.'
    }
    for a in replacements:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(replacements,key=len,reverse=True)),lambda m:replacements[m.group()],t)
    # Preserve the former group's inventory; read the latest pending B157 checkpoint.
    t=t.replace("'next_B156_B160_source_scope_v3759'","'next_B157_B160_source_scope_v3759'")
    needle='proofpaths=[DOC,';assert t.count(needle)==1;t=t.replace(needle,"proofpaths=[Path('scripts/lil_B157_completion_text_v3782.py'),Path('work/analysis/lil_B157_transition_review_v3775/full_screen_transition_and_all13_sheet_review.json'),DOC,")
    # Numeric substitutions are simultaneous; check the source accounting gates explicitly.
    assert '(5329,5254,75)' in t and 'source/prose5332' in t
    compile(t,str(dst),'exec');dst.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B157_completion_derivation_v3782');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(src),source_sha256=sha(src.read_bytes()),successor=str(dst),successor_sha256=sha(dst.read_bytes()),no_ledger_or_docs_mutation_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
