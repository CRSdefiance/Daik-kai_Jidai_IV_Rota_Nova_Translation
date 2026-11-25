"""Prepare representative early/middle/late zero-commit semantic failures and stable wrapper."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_atomic_challenge_tools_v8772');assert not root.exists()
    source=Path('scripts/challenge_Hodram_B52_atomic_v8692.py').read_text('utf-8')
    a=source.index('    specs=[');z=source.index('    ROOT.mkdir',a)
    specs="""    specs=[
        ('doc-English',DOC,['records',0,'english'],read(DOC)['records'][0]['english']+' Unapproved words.','Exact Hodram-B31-B53 approved prose/source/context'),
        ('relocation-source-hash',Path(paths['relocation']),['groups',0,'source_block_sha256'],'0'*64,'complete source/current block'),
        ('lost-body-name-hold',Path(paths['B31_actual']),['groups',0,'speeches',0,'complete_holds'],read(paths['B31_actual'])['groups'][0]['speeches'][0]['complete_holds'][:-1],'every independently reconstructed actual trace/hold/header/return/following-command field'),
        ('false-sealed-scope',SEAL,['observed_scope','initialized_whole_script_fixtures_not_original_optional_activation_location_or_earned_progress'],False,'every measured actual/offline/unforced alternate-path limit'),
    ]
"""
    challenge=derive('scripts/challenge_Hodram_B52_atomic_v8692.py','scripts/challenge_Hodram_B31_B53_atomic_v8772.py',{
        source[a:z]:specs,'B52':'B31_B53',
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_atomic_challenges_v8692':'Hodram_B31_B53_atomic_challenges_v8772',
        'Frozen Hodram-B52 contract changed':'Frozen Hodram-B31-B53 contract changed',
        '16 genuinely changed semantic defects':'4 genuinely changed semantic defects',
    })
    wrapper=derive('dk4tool/patch/hodram_b52_extension_v2.py','dk4tool/patch/hodram_b31_b53_extension_v2.py',{'B52':'B31/B53','hodram_B52_editorial_v2':'hodram_B31_B53_editorial_v2'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(challenge=challenge,wrapper=wrapper,
        original_full_object_identity_files_components_andserialized_bytes_zero_commit_guards_preserved=True,
        representative_early_editorial_middle_reference_late_actual_andfinal_scope_failures=True,
        all_native_frozen_editorial_semantic_guards_active_only_outer_digest_gate_bypassed_for_inmemory_evidence_injection=True,
        production_no_bypass_andno_disk_evidence_edit=True,new_credit=0,full_goal_complete=False))
