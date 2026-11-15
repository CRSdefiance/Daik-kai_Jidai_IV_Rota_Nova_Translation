"""Publish321 clean-source meanings/drafts with zero completion credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B196_B215_clean_20261110')


def main():
    seal_path=ROOT/'clean_draft_seal_v1.json'
    release_path=Path('work/maria305_B176_B195_release_v1/registered_release_verification.json')
    seal,release=map(load,[seal_path,release_path])
    assert seal['source_objects']==321 and seal['no_current_story_English_read'] and seal['all_five_review_gates_pending']
    for p,h in seal['evidence'].items():assert digest(p)==h
    drafts=load(seal['independent_drafts'])
    assert len(drafts['records'])==321 and all(not any(r['review'].values()) for r in drafts['records'])
    assert all(r['current_English_not_consulted'] for r in drafts['records'])
    evidence={**seal['evidence'],**{str(p):digest(p) for p in [seal_path,release_path,Path(__file__)]}}
    summary=('Maria B196–B215 now has321 saved clean meanings and independent American English drafts across18 complete groups: '
        '296 ordinary bodies,21 physical style alternatives andfour captions. Every draft precedes current-story-English exposure; '
        'source actor components andconditional endings areexplicitly distinguished. Contextual comparison,individual revisions/retentions,'
        'names/terms andallfive gates remain pending. No new ROM orcredit;no worker islive. Integrated22,386,registered d5bc0dc5,'
        'main andfull scope remain unchanged.')
    document='docs/editorial_Maria321_B196_B215_clean_drafts_20261110.md'
    text=f'''# Maria321 clean meanings and independent drafts — November 10, 2026

{summary}

The previous goal turn integrated and credited Maria305 once, then selected the next321 disjoint clean objects. This turn is progress:all321 clean meanings andindependent logical English drafts are authored andsaved before any current story English was read. It doesnot add contextual-completion credit orauthorize aROM. The full goal remains active.

Use `work/Maria_B196_B215_clean_20261110/all321_clean_meanings_v1.json`, `all321_independent_drafts_v1.json` and `clean_draft_seal_v1.json`. All18 source groups and321 source references/bytes remain exact anddisjoint from prior credit. Each authored entry places its source gloss before its independent English;each part's meanings file iswritten before its draft file. Allparts aresealed before first current-story-English exposure. Three immutable authored parts andtheir paired saved meanings/drafts cover B196–201 (87),B202–209 (94) andB210–215 (140). No draft was copied from current translated story text. Every English draft isone logical ASCII paragraph,with original FI counts preserved. Allfive per-record gates arestill false;this isdraft work,not final localization approval.

Full source reading covers Ian's Timur-mail letter andCesare's Russian/Mongol explanation;Julian/Safia's Medusa flirtation;Gerhard's Charles Martel account;Manuel's Attila clue;Yifa's training anduniform story;Samwell's three deliberately repeated shield/phoenix pitches;Carlo's medical-book lead;Manuel's Phidias chisel;Charles's unexplained maritime roar;Jam/Fernando's fortune-telling statue joke;Cesare's angry arrow rumor;Janus's lost-gloves lead;Francisca's stolen rose,its recovery andthe wooden church;andJulio/the priest's figurehead encounter.

The drafts preserve approximate dates,reported hearsay,limited geographical clues,historical claims ascharacter speech,cultural Daqin/Vermilion Bird references,signatures,the stolen gift's explicit father relationship andthe humorous repetitions. They do not turn the rose's barkeep intoFrancisca's father,nor familiar port-worker/barkeep address intobrotherhood orkinship. Clean static actor fields distinguish Cesare13,Carlo19,Samwell22,Yifa25,Ian21,Charles18,Jam11,Fernando20,Julio6 andJulian26. Those fields areidentity references,not native runtime dispatch/getter/nameplate proof. Inparticular,the playacting opponent atselector151 retains its separate crew-role metadata;do not relabel it asaBoy solely from the surrounding children's-game discussion.

New World yes/no replies andthe figurehead's attempt/refusal andsuccess/failure endings arekept asalternatives,not one linear exchange. B215's complete original command inventory isavailable inthe packet;no numeric adjacency,guaranteed success orstat effect execution isclaimed. Source FE panels hand over Frozen Rose andreport FI Spirit+1. Item names,full signatures,role consumers andinstalled UI terms remain provisional until exact source/native bindings. The three crew-message objects have21 physical alternatives;their original alias/voice behavior must still bebound.

**Next:**bind the sealed drafts toexact current effective ordinary/style/menu text,then compare every complete exchange. Retain working English with individual contextual reasons;revise actual meaning,voice,humor orcontinuity failures. Reconcile names/roles/signatures/items/substitutions withnative consumers before sealing the four prose gates. Write logical paragraphs anduse validated full-width consumer-specific formatting;do not copy legacy breaks orshorten good prose tofit. Fresh changed-text native/visual/storage checks,representative display/transition gameplay andregistered integration follow. Reuse the already qualified inventories andprior proofs onlywhen relevant dependencies match.

[The registered Maria305 checkpoint](editorial_Maria305_B176_B195_registered_20261110.md) remains authoritative:720 entries,114 accepted layers,55 passing checks,exact clean-input patch,own startup and24 protected getters. Candidate SHA256:`{release['candidate_sha256']}`. Preserve Market allocation/pointers,six-section ARM9,ASCII right bounds,source25 v2,inherited B164R99 correction,allprior translated archives,names,font andgraphics. No main promotion without acceptance.

Integrated22,386 =13,405 revisions+8,981 justified retentions;historical source/prose/draft22,389. Native story remainder3,512 =Maria1,707+Lil1,805 includes this uncredited321;shared/player-facing inventories remain separate. Preserve allcompleted coverage,earlier unfinished contextual passes,fullstoryline/town/shop/random/player-prose/name/wrap/glyph scope andearly Rafael/tutorial priority. No guide photos. Deferred graphics artwork andlater older-record technical re-audit remain separate. AllgeneratedROMs,translations,drafts andevidence arepreserved. No cleanup,promotion,commit orpush occurred;no worker islive.
'''
    checkpoint(mutation=ROOT/'clean_draft_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria321:all clean meanings/independent drafts saved; current comparison/names/terms/allgates pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,
            next_action='Extract current effective text after the321-draft seal;compare whole exchanges andbind names/roles/terms before first-four-gate approval.'),
        additional_updates={'Maria_SC3_B196_B215_clean_20261110':dict(new_credit=0,
            clean_meanings_andindependent_drafts_pending=False,clean_meanings=321,independent_drafts=321,
            clean_meanings_path=seal['source_meanings'],independent_drafts_path=seal['independent_drafts'],
            clean_source_draft_seal=str(seal_path),current_English_not_read=True,contextual_comparison_pending=True,
            names_terms_consumers_pending=True,all_five_review_gates_pending=True,all_fifth_gates_pending=True,
            registered_integration_pending=True,no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22386,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'clean_draft_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        no_current_story_English_read=True,no_batch_worker_live=True,full_goal_complete=False))
    print('Published321 clean meanings/drafts; currentcomparison/allgates pending;22386 integrated unchanged.')


if __name__=='__main__':main()
