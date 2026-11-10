"""Save the full contextual batch with zero integration credit and protected releases."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.gloss_hodram_B281_B300_clean_v1 import ROOT,SCOPE,OUT as MEANINGS
from scripts.draft_hodram_B281_B300_clean_v2 import OUT as DRAFTS
from scripts.review_hodram_B281_B300_contextual_v1 import OUT as PROSE,CURRENT,OBJECTS
from scripts.build_registered_hodram_B251_B280_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE


def main():
    scope,meanings,drafts,prose,current,objects,release,package=map(load,(SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,RELEASE,PACKAGE))
    assert scope['total_editorial_objects']==meanings['records_count']==drafts['records_count']==len(prose['records'])==384
    assert scope['source_key_overlap_with_completed_credit']==0 and scope['all_completed_exclusion_keys_checked']==17749
    assert prose['counts']==dict(revision=181,retention=203) and prose['remaining_contextual_comparisons']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert current['runtime']==objects['runtime'] and current['current_ROM_sha256']==release['candidate_sha256']
    assert current['records']==242 and objects['native_style_getter_cases']==144
    roles=ROOT/'role_bindings_v1.json';assert load(roles)['runtime']==current['runtime']
    assert {r['source_selector'] for r in load(roles)['native_roles']['rows']}=={207,208,211,215,216}
    summary=('Hodram B281–B300 has all 384 clean-source meanings, logical drafts and contextual decisions saved: '
        '181 proposed revisions and 203 justified retentions. The scope has 242 ordinary speeches, 131 physical voice alternatives and 11 captions. '
        'Findings include incorrect Indian Ocean clues, invented bounty-hunter deaths, reversed Charles-absence reminders, '
        'a countdown changing zero to go and five punctuation consistency targets. Scoped names/terms and all fresh display/gameplay/release gates remain. '
        'Integrated coverage stays 17,749; main is unchanged.')
    doc=f'''# Hodram B281–B300 contextual checkpoint

{summary}

The [clean intake](../{SCOPE.as_posix()}) reconciles all 17,749 credited source keys. All 384 objects are unique and disjoint: 242 speeches, 131 physical alternatives in 18 voice objects/144 alias slots, and 11 captions in five menus, across 20 complete blocks. No block is control-only. Every clean source string decodes. Source B301–B303 was read briefly as neighboring context; B301 is a separate Colosseum clue, so B300 is not a truncated continuation. Those neighboring records gain no review credit.

All [384 clean meanings](../{MEANINGS.as_posix()}) were sealed before current-ROM story English was extracted. The [384 logical drafts](../{DRAFTS.as_posix()}) likewise precede current extraction and preserve complete preambles, substitutions, source alternatives and aliases. Names and nonstory terminology references supply current Iscal, Proof of Conquest and Ancient City Map; these are not new term-consumer approvals. Historical name references could include other old prose; no blanket absence of prior English exposure is claimed. The original source gloss’s provisional Iskal spelling remains preserved. Fifteen draft refinements remove unnecessary male-only-party/friendship assumptions; all other 369 drafts and all other fields remain exact. The v2 producer’s final count assertion expected14 instead of15 after writing the valid draft; the separate `clean_draft_source_refinement_v3.json` verifies the actual15 without rewriting either draft.

The [contextual comparison](../{PROSE.as_posix()}) supplies exact source/current references, faithful meanings, complete exchange contexts, individual findings, revisions and justified retentions. All four prose gates pass on every record; all 384 fifth gates remain false. Existing natural royal statements, short reactions, guild replies, route reminders, conventional menu captions and working voice variants are explicitly retained. No prose is shortened to fit, manually wrapped or padded.

The royal task restores operating beyond the Indian Ocean and the complete Iscal Yasar target. The following argument preserves universal recognition, qualification to acquire a sea-region Proof, all seven Proofs, domestic as well as foreign recognition, and uncertainty about the objects’ intrinsic worth. The dry private conclusion remains distinct from the respectful court exchange.

William’s linked job restores tribute, the Mexico/England references, the band’s undeclared status and the tactic of provoking its hidden leader. B286 R35 does not establish a bounty-hunter death toll. B287 R12 does not imprison Hodram; it expresses relief at being rid of the captive. The villager’s grand praise is deliberately undercut by his candid admission that he asks many strong-looking people, with little expectation and no refund if the search fails. He personally joins the search and waits at the city gate; no extra companions are invented. All five currency notices keep their exact quantities and explicit gold coins; both market-share increases remain slight and unquantified.

The bear/tiger/snake expeditions preserve all voice alternatives, map gates, separate menus, source aliases, injuries/fatigue/time, and optional character lines. The bear may eat people; it is not confirmed as a man-eater. Members are attacked, not necessarily mauled; the tiger is defeated, not explicitly declared dead. Friendly-fire warnings need not assume a male-only party or personal friendships. Emilio genuinely falls asleep while playing dead. Animal sounds and panting remain nonlexical cries, not the spoken stage direction Pant. The snake remains a giant snake and the trap a bog/swamp, without an unspoken species or quicksand hazard.

The fish is not newly identified as a demon. Malacca’s intact ancient-kingdom ruins remain rumor. The Christian settlement’s rock-hewn houses remain rumor; Byzantine ancestry remains Gerhard’s question, not external historical endorsement. The smoke warning does not prematurely diagnose poison or add a substance, death or doctrine.

The gunpowder sequence preserves Charles’s research, sulfur at the trade house, timber for charcoal from elsewhere, saltpeter in an Indian Ocean town and unquantified material thresholds. B297/B298/B299 R11 are wishes for absent Charles, not assertions that he is present. Charles sets the explosive and sends others back to town; he does not order them to set it. The exact countdown ends in zero. No real-world proportions, extra manufacturing instructions or added casualties appear.

Five scoped punctuation targets await fresh native/glyph checks: B283 R100, B290 R179 and B296 R33 use ASCII periods for the same silence; B287 R65 uses an ASCII question mark; B290 R92 uses ASCII exclamation marks. These text-display checks are separate from font artwork. Do not globally normalize consumer-specific full-width text.

Binding uses registered B251–B280, SHA-256 `{release['candidate_sha256']}`. Its fresh own-Hodram 4,001-frame startup matches ten prior reviewed RGB captures, verifies staged payload and exports its own read-only RAM. The startup is not B281–B300 gameplay coverage. All 242 original current catalogue bindings, 144 original voice-slot selections and 11 caption bindings pass. Native dynamic-role dispatch covers207/208/211/215/216:207 resolves to Hodram; the other unassigned roles fall back to Sailor in this startup. This is not future conditional participation or a roster/state override.

Next review scoped names/role labels and spoken terms from their clean fields and current consumers. Fourteen source actors and four additional spoken-name references are available; do not turn regional metadata into surnames, religion or biography. Then format all373 renderable bodies and11 captions using validated consumer rules, inspect every generated page, resolve premature wraps/glyph targets, check stored scripts, sample distinct display behavior and integrate through the registered cumulative workflow with exact clean-input patch and own startup. Reuse compatible proofs; do not visit every conditional speech or replay completed earlier batches.

Integrated totals remain17,749:10,828 revisions and6,921 retentions. Historical source/prose counters remain17,752. There is no B281–B300 ROM, gameplay coverage or integrated credit yet. Main, current registered candidate, canonical base, clean input, accepted layers/runtime bounds, weekend ZIP and all earlier ROMs/translations/retentions/evidence remain preserved. No live process remains. Continue every storyline, shared shop/town/random exchange, unfinished earlier contextual pass, names and player-facing prose, with Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos. Full goal remains active.
'''
    paths=(SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,roles,ROOT/'clean_name_fields.json',ROOT/'draft_name_reference_v1.json',ROOT/'clean_draft_source_refinement_v3.json',ROOT/'own_parent_startup_v1/own_route_context.json',Path(__file__))
    evidence={str(p):digest(p) for p in paths}
    checkpoint(mutation=ROOT/'contextual_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B281–B300: all384 contextual decisions saved; names/terms and display gates pending.',
            next_action='Review scoped names/terms, format373 bodies/11 captions, inspect pages and resolve wrap/glyph findings before stored/gameplay/integration checks.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        new_entries={'Hodram_B281_B300_clean_next_20261107':dict(new_credit=0,total_editorial_objects=384,ordinary_speeches=242,
            physical_personality_alternatives=131,typed_caption_records=11,source_meanings_saved=384,localized_drafts_saved=384,
            current_English_comparisons=384,remaining_current_English_comparisons=0,proposed_revisions=181,justified_retentions=203,
            all_four_prose_gate_records=384,scoped_names_pending=True,scoped_terms_pending=True,fresh_native_body_pages_pending=True,
            stored_reconstruction_pending=True,current_story_gameplay_utterances=0,representative_gameplay_pending=True,
            registered_integration_pending=True,all_five_review_gates_pending=True,all_formatting_gates_pending=True,
            clean_meanings_anddrafts_sealed_before_current_ROM_English=True,no_blanket_claim_of_no_historical_English_exposure=True,
            source_key_overlap_with_completed_credit=0,punctuation_consistency_targets=5,native_job_live=False,
            registered_build_live=False,contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence=evidence)},
        summary=summary,document='docs/editorial_Hodram_B281_B300_contextual_20261107.md',document_text=doc,completed=17749,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved384 contextual decisions with zero integration credit. Registered17,749 and full objective preserved.')


if __name__=='__main__':main()
