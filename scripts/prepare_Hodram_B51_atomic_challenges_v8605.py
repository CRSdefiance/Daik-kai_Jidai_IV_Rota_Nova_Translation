"""Derive semantic rejection and genuinely wrong-memory tests for the B51 atomic stage."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_atomic_challenge_tools_v8605');assert not root.exists()
    source=Path('scripts/challenge_Hodram_B50_atomic_v8540.py').read_text(encoding='utf-8')
    a=source.index('    terminal=read(');b=source.index('    ROOT.mkdir',a)
    specs="""    specs=[
        ('config-format',CONFIG,['format'],'unapproved-release','exact complete source-qualified configuration'),
        ('config-parent',CONFIG,['parent_ROM_sha256'],'0'*64,'whole in-memory predecessor/reference identities'),
        ('config-prior-profile',CONFIG,['required_registered_stack_dependency','predecessor_profile'],'incomplete-route','explicit registered V8543/Adernkatz/B49/B50 dependency'),
        ('doc-context',DOC,['records',0,'context'],read(DOC)['records'][0]['context']+' Invented relationship.','Exact Hodram-B51 approved prose/source/context'),
        ('doc-English',DOC,['records',0,'english'],read(DOC)['records'][0]['english']+' Unapproved words.','Exact Hodram-B51 approved prose/source/context'),
        ('doc-source-bytes',DOC,['records',0,'source_hex'],'01'+read(DOC)['records'][0]['source_hex'][2:],'Exact Hodram-B51 approved prose/source/context'),
        ('doc-final-reference',DOC,['records',0,'final_reference','offset'],19,'Exact Hodram-B51 approved prose/source/context'),
        ('sealed-record-order',SEAL,['records'],list(reversed(read(SEAL)['records'])),'five sealed exact source/current/final references'),
        ('current-block-bytes',Path(paths['current']),['groups',0,'current_block_hex'],'00'+read(paths['current'])['groups'][0]['current_block_hex'][2:],'complete literal source/current blocks'),
        ('relocation-source-hash',Path(paths['relocation']),['groups',0,'source_block_sha256'],'0'*64,'complete source/current block'),
        ('wrong-query-value',Path(paths['stored']),['stored_queries',0,'native_result',1],1,'both unforced queries and all six return words'),
        ('discarded-sixth-query-word',Path(paths['stored']),['stored_queries',1,'native_result',5],1,'both unforced queries and all six return words'),
        ('wrong-normal-value-carry',Path(paths['stored']),['normal_seeded_ends',1,'native_result',1],0,'twenty-five complete normal result/value carries and all six return fields'),
        ('lost-complete-body-name-hold',Path(paths['actual']),['groups',0,'speeches',0,'complete_holds'],read(paths['actual'])['groups'][0]['speeches'][0]['complete_holds'][:-1],'every independently reconstructed actual trace/hold/header/return/following-command field'),
        ('false-Charles-visit',Path(paths['actual']),['groups',1,'unvisited_conditional_text_IDs'],[],'exact observed andexplicitly unvisited source memberships'),
        ('comparison-final-RNG',Path(paths['comparison']),['groups',0,'final_PRNG_seeds'],[0,0],'exact raw RNG/calendar scope'),
        ('sealed-scope',SEAL,['observed_scope','all_measured_timing_PRNG_RGB_andcalendar_limits_retained'],False,'all measured actual fixture/timing/RNG/component/calendar/RGB limits'),
    ]
"""
    semantic=derive('scripts/challenge_Hodram_B50_atomic_v8540.py','scripts/challenge_Hodram_B51_atomic_v8605.py',{
        source[a:b]:specs,'hodram_B50_editorial_v1':'hodram_B51_editorial_v1',
        'scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'Hodram_B50_atomic_challenges_v8540':'Hodram_B51_atomic_challenges_v8605',
        'Frozen Hodram-B50':'Frozen Hodram-B51','All16 changing':'All17 changing'})
    memory=derive('scripts/validate_Hodram_B50_wrong_memory_v8550.py','scripts/validate_Hodram_B51_wrong_memory_v8605.py',{
        'hodram_B50_editorial_v1':'hodram_B51_editorial_v1',
        'scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'Hodram_B50_wrong_memory_v8550':'Hodram_B51_wrong_memory_v8605'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(semantic=semantic,wrong_memory=memory,semantic_only_outer_dependency_digest_bypass_all_frozen_native_guards_active=True,wrong_memory_all_guards_active=True,zero_commits_andwhole_input_unchanged_required=True,new_credit=0,full_goal_complete=False))
