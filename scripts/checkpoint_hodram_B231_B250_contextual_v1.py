"""Save complete source-first and contextual work without claiming display or release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_hodram_B211_B230_v1 import RELEASE,REGISTRY
from scripts.draft_hodram_B231_B250_clean_v1 import OUT as DRAFTS,MEANINGS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B231_B250_scope_v1 import ROOT,SCOPE
from scripts.review_hodram_B231_B250_contextual_v1 import OUT as PROSE,CURRENT,OBJECTS
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

def main():
    release,ledger,package,scope,means,drafts,prose,current,objects=map(load,(RELEASE,LEDGER,PACKAGE,SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS))
    assert ledger['records_editorially_completed']==17308 and not ledger['full_goal_complete']
    assert means['source_meanings']==drafts['records_count']==prose['records_count']==225
    assert prose['counts']=={'retention':109,'revision':116} and prose['remaining_contextual_comparisons']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert current['runtime']==objects['runtime'] and current['records']==209 and objects['native_style_getter_cases']==16
    assert current['current_ROM_sha256']==release['candidate_sha256']
    assert scope['all18_excluded_clean_source_positions_andbytes_exact'] and len(scope['excluded_credited_records'])==18
    summary=('Hodram B231–B250 now has all 225 clean meanings, independent drafts and contextual comparisons saved: '
        '116 proposed revisions and 109 justified retentions. The 18 completed B237 records remain excluded. '
        'Findings include an untranslated transport instruction, wrong Indian Ocean clue, inconsistent names and a full-width F. '
        'Scoped names/terms and fresh formatting, visual, stored, gameplay and release checks remain. Integrated credit stays 17,308.')
    doc=f'''# Hodram B231–B250: complete contextual comparison

{summary}

The [225 individual source meanings](../{MEANINGS.as_posix()}) and [225 independent English drafts](../{DRAFTS.as_posix()}) were sealed before the eligible current story English was extracted. All complete exchanges were read together. Only previously reviewed name forms and scoped item/stat terminology were consulted as references; no claim is made that the entire project had never been exposed to historical English. The [contextual manuscript](../{PROSE.as_posix()}) binds every record to exact clean/current references, with a specific revision finding or justified retention. All four prose gates pass individually. Every formatting gate remains false.

Scope is 209 ordinary speeches, 14 physical voice alternatives in two eight-slot objects, and two captions in one menu. There are 19 complete eligible blocks; B235 is control-only. B237’s 18 papal-trade records match their credited clean bytes and positions exactly and remain excluded. The raw intake and previous review remain intact. The [scope receipt](../{SCOPE.as_posix()}) records these boundaries.

The review keeps Samwell’s three linked treasure pitches as a running joke, with Hodram’s increasing recognition and eventual praise for useful research. It preserves personal intentions, hearsay and broad geographic leads; neither interest nor luck becomes an item already earned. Carlo’s uncertain old recollection stays tentative. Manuel’s reported Roman tool metaphor keeps its humor without a new political explanation. Charles’s measured letter remains distinct from Jam’s intentionally spoken register. Cesare’s rant remains comic and skeptical rather than a narrator’s disproof. Francisca’s birthday gift, actual father and gratitude remain explicit. The figurehead trial’s refusal, failure, success and one-point Spirit reward remain separate source branches. The survey job retains transportation, extra sailors, money, exact reward and market-share wording.

Concrete corrections include B232 R48’s Indian Ocean (not eastern ocean); the corresponding Africa/India callback in B233 R38; B233’s heard helmet rumor and iron material; B234’s old tentative recollection rather than a known report or a hopeless search; B238’s far-west clue and the navy’s chance arrival; B241’s Janus (not Gennas); B239’s full Jam Jack Ludwyan signature (not Ludwayer); personal I/my forms replacing this man, this woman and this elder; B242’s idiom about overlooking nearby things without inventing a hidden church; and B248 R16’s wholly Japanese instruction to carry the survey party as sailors and hire extra crew at the tavern. The gold award remains exactly 42,000 coins. Sofala’s market-share increase remains slight and unquantified.

Two text-rendering leads have revised ASCII targets pending fresh native checks: B239 R39 contains full-width Ｆ in Fernando, and B244 R14 uses an isolated full-width question mark. No global normalization is applied to controls, fixed-width consumers or deliberate native punctuation. The scoped Armadillo Hide title retains the established item label while preserving its iron-hard quality explicitly around it; review the shorter catalogue label and all other named terms in the upcoming scoped term pass. Do not add Magic Leather Gloves or Demon Figurehead as spoken item names where the clean dialogue only says gloves or figurehead. Spirit is the permanent attribute; Mood is a separate condition. Regional metadata remains metadata, not new surnames or biographies.

Current bindings use the registered Hodram B211–B230 cumulative candidate, SHA-256 `{release['candidate_sha256']}`. A new own-Hodram 4,001-frame startup verifies captain/route 1, exact staged payload, fresh read-only RAM and ten byte-identical previously reviewed opening captures. The [209 current effective-text lookups](../{CURRENT.as_posix()}) and [16 voice-slot/current caption bindings](../{OBJECTS.as_posix()}) preserve complete preambles, source command kinds and all aliases. This startup and these lookups are not gameplay or visual approval of B231–B250. No new render pages, scene gameplay or ROM have been produced for this batch.

Next review the 18 ordinary source actors plus the dynamic-role fallback as applicable, bind the scoped names and item/city/stat terms to this exact runtime, resolve any real localization findings, then format the 223 logical speech bodies and two captions. Reuse qualified unchanged consumer/font/control proofs. Run fresh checks for all changed text, inspect every generated page, refine concrete wrapping problems, reconstruct complete stored blocks and use representative gameplay for distinct behaviors. Integrate only after necessary checks pass. Keep any uncertainty or unvisited catalogue/scene conditions explicit.

Integrated coverage remains 17,308, with 10,584 revisions and 6,724 retentions. The registered test candidate, patch, main and weekend ZIP are unchanged. Preserve all earlier translations, generated ROMs and failed proofs. Every remaining route, shared/shop/town/random exchange, unfinished earlier contextual pass, name/role label and player-facing resource remains in scope. Deferred graphics artwork and the later older-record technical re-audit stay separate. No guide photos are collected. The full goal remains active.
'''
    checkpoint(mutation=ROOT/'contextual_checkpoint_v1',batch_key='Hodram_B231_B250_clean_next_20261107',
        batch_updates=dict(new_credit=0,source_meanings_saved=225,localized_drafts_saved=225,
            current_English_comparisons=225,remaining_current_English_comparisons=0,proposed_revisions=116,justified_retentions=109,
            all_four_prose_gate_records=225,all_five_review_gates_pending=True,all_formatting_gates_pending=True,
            scoped_names_andterms_pending=True,fresh_native_body_pages_pending=True,stored_reconstruction_pending=True,
            current_story_gameplay_utterances=0,representative_gameplay_pending=True,registered_integration_pending=True,
            no_current_English_dialogue_consulted=False,clean_meanings_anddrafts_sealed_before_current_English=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),
            evidence={str(p):digest(p) for p in (SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,ROOT/'own_parent_startup_v1/own_route_context.json',Path(__file__))}),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B231–B250: all 225 contextual decisions saved; names/terms and display checks pending.',
            next_action='Review scoped names and terms, then format 223 bodies/two captions and perform fresh native/visual checks.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B231_B250_contextual_20261107.md',document_text=doc,
        completed=17308,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved all 225 contextual decisions. Integrated credit 17,308, current release and full scope preserved.')

if __name__=='__main__':main()
