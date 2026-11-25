"""Publish completed349-source research without release credit or promotion."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    rp=Path('work/maria359_B253_B274_release_v1/registered_release_verification.json');release=load(rp)
    ready=ROOT/'research_completion_v1/research_completion.json';proof=load(ready)
    assert proof['all_individual_five_gates_pass'] and (proof['records'],proof['revisions'],proof['retentions'])==(349,184,165)
    paths=[rp,ready,ROOT/'source_selection_v1.json',ROOT/'clean_draft_seal_v1.json',ROOT/'offline_display_approval_v1.json',ROOT/'gameplay_review_v1.json',Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B275–B285 passes all five individual gates:349 contextual reviews,184 revisions,165 justified retentions and19 scoped names. '
        'All347 body pages,eight captions and21 name strings pass native anddirect visual review. Ten layouts improve andthree pages are reclaimed. '
        'Storage passes341 lookups,330 branch cases,303 loads and606 handoffs. Three initialized emulator samples observe191 bodies/193 pages,allthree menus,two page turns,seven FE returns andthree sailing returns. '
        'Registered integration/once-only credit remain. Integrated23,429,registered138381bd,main andfull scope remain unchanged;no worker islive.')
    document='docs/editorial_Maria349_B275_B285_research_ready_20261110.md'
    text=f'''# Maria B275–B285 research ready — November 10, 2026

{summary}

The previous goal turn registered Maria359 and prepared/pushed the cumulative candidate as6191f07abd3b3c8fd9f3784fef7ee75471fcac3e. This turn is progress:349 exact disjoint source objects in11 complete exchanges received clean meanings and independent drafts before current-English extraction,complete contextual comparisons andallfive individual gates. Source/current references,findings andretention reasons arein `{proof['manuscript']}`;19 scoped name reviews arein `{proof['names']}`. All27 personality objects/162 physical alternatives/216 slots/243 compiler negatives,three menus/eight captions/18 alignments/66 returns/32 planes/23 negatives and21 name strings pass. Names retain source-bound staged Magistrate/Priest roles;actor25 isYifaSol,not Emilio. Mihwa's existing reading isretained inthis scope without inventing nationality orsurname;the broader name-reading inventory remains open.

Concrete corrections preserve weapons andarmor,wokou pirates,a genuine Nagasaki priest distinct fromimpostors,fetching the doctor,the1000-coin informant,tomorrow inMacao,the alternative lies nextweek OR Hangzhou,Jacob's working acquaintance,the uncertain future scheme,more than100 claimed Jesuits,the former actor impersonating a magistrate,the governor completely fooled andnearly losing his head,Westerners andJapanese,the village far northeast OF China,the Forbidden City,an ancient illustrated-map rumor,distinct injury/treatment roles215/218 andone-day treatment. Retain good short replies andcharacter-specific crisis speech. No invented rank,kinship,arrest outcome,poison ordeath.

Fresh final plans are`plan_v6/automatic_plans.json`:341 bodies/347 pages plus8 captions,no errors,warnings orfailures. All34 baseline sheets andtwo final changed-layout sheets aredirectly viewed;allfinal347 pages match complete native glyphs,canaries,bounds,consumption andpagination. Ten final layouts differ frominitial350-page plans,which become347 without shortening prose. Three additional final closing-phrase repairs avoid small trailing fragments whilekeeping reasonably full first pages. The exact as/soon ordinary soft wrap keepsone source paragraph onone page;its original warning andexactsource/current/English bindings arepreserved. No native guard iswaived. Prior failed/superseded plans,allgenerated pages andROMs remain.

Complete clean/current/command/block/archive/serialized-ROM inverses pass. Stored proof has104 fresh parity pages and243 exact compatible pages,330 native branch cases,all341 effective catalogue lookups,303 loads and606 handoffs. Three bounded initialized emulator QA hosts run77043 frames andshow191 distinct bodies/193 pages,12 effective voice4 alternatives,all8 captions/two- andthree-choice menus,two page turns,all7 FE returns,7 FI substitutions and3 sailing returns. All21 actual body/menu/transition sheets aredirectly viewed.150 bodies and150 other physical style alternatives remain offline-only. These hosts preserve original setup/cleanup butconcatenate conditional alternatives;natural activation,original outcomes/rewards/geography/chronology,fullroutes andhardware remain unvisited. The reused observer's inherited Maria359 unlock scope label identifies the runner version;the exact fixture ROMs/manifests andall observed records belong toMaria349. No guide photos.

Next use`research_completion_v1/research_completion.json`,the pure`dk4tool/patch/maria349_release_v1.py`transaction andregistered driver`build_registered_maria349_v1.py`. Preserve the complete723-entry predecessor,114 accepted layers,Market16-byte format/both pointers,six-section ARM9,ASCII rightbounds,source25v2 andB164R99 padding repair. Require eight semantic mutations,exact clean-input patch,candidate-owned startup and24 protected getters before registration orcredit. Main requires user acceptance. Integrated23,429=13,997 revisions+9,432 retentions;historicalsource/prose23,432. Native story remainder2,469=Maria664+Lil1,805 includes this349 uncredited scope. Allstorylines,earlier unfinished contextual reviews,shared/shop/town/random/player-facing prose,names,wraps/glyphs andearly Rafael/tutorial priority remain in scope. Deferred graphics artwork andlater older-record technical re-audit remain separate. The fullgoal staysactive.
'''
    checkpoint(mutation=ROOT/'research_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria349 B275–B285 research ready;registration andonce-only credit pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=184,justified_retentions=165,qualified_scoped_names=19,current_batch_actual_gameplay_observations=191,current_batch_actual_gameplay_pages=193,
            current_batch_evidence=evidence,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,no_batch_worker_live=True,guide_photos=False,previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Qualify/stage cumulative349 successor;own startup/protected getters,register andcredit once,package andpush.'),
        new_entries={'Maria_SC3_B275_B285_clean_20261110':dict(new_credit=0,source_objects=349,complete_exchanges=11,source_speech_objects=179,
            physical_style_alternatives=162,typed_choice_labels=8,clean_meanings=349,independent_drafts=349,current_English_not_read=False,
            contextual_comparison_pending=False,names_terms_consumers_pending=False,all_five_review_gates_pending=False,all_fifth_gates_pending=False,
            registered_integration_pending=True,no_batch_worker_live=True,revisions=184,retentions=165,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=23429,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Published349 research-ready reviews;23429 integrated andregistered parent unchanged.')

if __name__=='__main__':main()
