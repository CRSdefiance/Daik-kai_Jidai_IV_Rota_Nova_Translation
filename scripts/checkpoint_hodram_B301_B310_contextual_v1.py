"""Save all contextual decisions with zero integration credit and protected release identities."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.gloss_hodram_B301_B310_clean_v1 import ROOT,SCOPE
from scripts.refine_hodram_B301_B310_clean_drafts_v2 import MEANINGS,OUT as DRAFTS
from scripts.review_hodram_B301_B310_contextual_v1 import CURRENT,OBJECTS,OUT as PROSE
from scripts.build_registered_hodram_B281_B300_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    scope,meanings,drafts,prose,current,objects,release,package=map(load,(SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,RELEASE,PACKAGE))
    assert scope['total_editorial_objects']==meanings['records_count']==drafts['records_count']==len(prose['records'])==234
    assert scope['source_key_overlap_with_completed_credit']==0 and scope['all_completed_exclusion_keys_checked']==18133
    assert prose['counts']==dict(revision=127,retention=107) and prose['remaining_contextual_comparisons']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert current['runtime']==objects['runtime'] and current['current_ROM_sha256']==release['candidate_sha256']
    assert current['records']==73 and objects['native_style_getter_cases']==184
    roles=ROOT/'role_bindings_v1.json';assert load(roles)['runtime']==current['runtime']
    assert {r['source_selector'] for r in load(roles)['native_roles']['rows']}=={207,208,211,214,215,218}
    assert len(prose['untranslated_current_turns_corrected'])==2 and len(prose['findings_requiring_fresh_display_checks'])==1
    fe=[r for r in prose['records'] if r.get('source_selector')==254]
    assert len(fe)==8 and sum('{MACRO:FI}' in r['english'] for r in fe)==1
    summary=('Hodram B301–B310 has all234 source meanings, logical drafts and contextual decisions saved: '
        '127 proposed revisions and107 justified retentions. The scope has73 ordinary speeches,152 physical voice alternatives andnine captions. '
        'Findings include eight invented water-shortage reports, invented elapsed hours/a collapsed sailor, wrong mosque/vault details, '
        'two untranslated monk turns, a wrong northeastern-China clue and spoken Pant/Wheeze. '
        'Scoped names/terms, fresh display/stored/gameplay checks and integration remain. Integrated coverage stays18,133; main is unchanged.')
    document=f'''# Hodram B301–B310 contextual checkpoint

{summary}

The [clean scope](../{SCOPE.as_posix()}) contains234 unique, disjoint source objects across ten complete blocks:73 ordinary speeches,152 physical alternatives/184 alias slots in23 voice objects andnine captions in four menus. B308 is a voice-object-only reminder, not a control-only block. All source text decodes. The parent clean B301–B324 packet inventories634 objects; the unselected B311–B324 portion contains400. B311’s ordinary Japanese was read only to check the boundary and receives no comparison or completion credit. Numeric adjacency does not prove that the desert trek is the Colosseum journey or establish original event chronology.

All [234 clean meanings](../{MEANINGS.as_posix()}) and [234 logical drafts](../{DRAFTS.as_posix()}) were sealed before eligible current-ROM dialogue was extracted. Clean-source v1 remains preserved. The source-first refinement clarifies one direction gloss to far northeast of China, improves the thank-you/shortcut remarks, removes added profanity and expresses panting as breath sounds. Ten drafts change and one already-correct panting variant is retained; the first refinement attempt stopped at that identical-wording assertion after saving the valid source gloss. Reuse `source_first_refinement_v3.json`; do not restart the failed producer. Existing static name references and item45 supply approved spellings. Relocated pointers require the separately saved fresh-RAM name reference, not guesses from absent ARM9 strings. The provisional source gloss’s Meihua is reconciled to existing Mihwa without rewriting historical evidence. These reference reads are not scoped native getter/name-localization approval or a blanket claim of no historical English exposure.

The [contextual manuscript](../{PROSE.as_posix()}) records every exact source/current reference, source meaning, complete exchange context, finding, revision or justified retention. All four prose gates pass individually; all234 fifth gates remain false. Working greetings, colloquial short replies, formation-context acknowledgments, immediate warnings, pain cries, route-choice captions and considerate injury questions are retained with individual reasons. Long source turns are restored without shortening to imitate old allocations. Ordinary line breaks remain formatter-owned.

The eight B302 C2582 alternatives estimate leaving the desert; they do not report low water. B302 C1786 adds no elapsed hours, and the FE departure notice establishes neither one collapsed sailor nor deaths. Waiting is for the sandstorm to pass, not an invented overexertion rest. Definite versus apparent fatigue and the single elapsed day remain distinct. The mosque honors a king from long ago; he is not said to have built it, and no vault is named. Safia’s help is gratitude for improved dancing, without a newly invented lesson or romance.

Sakura’s temple invitation preserves Hodram’s non-Buddhist objection, looking around and traveling only partway. Kinkaku-ji is restored in the monk reminders; the existing item label is Kublai’s Greatsword. Gerhard’s existing explicit unequip instruction works and is retained. The two Japanese monk turns are translated; the directions remain far northeast of China, near an icy sea, at the base of a vast peninsula by the foot of a high mountain on its eastern coast. No real-world region or ship class is invented. The monk’s warning about evil intentions and corrupt desire is retained in natural grave language, without new doctrine.

The wolf alternatives preserve different source roles for warning, injury and reassurance, not asserted future roster assignments. Japanese supplies no headcount: English uses the primary animal referent without claiming a pack or that only one animal exists. The treatment advice remains prospective and conditional on prompt care, not observed healing. The formation order is made natural, Hodram’s counterfactual regret is restored, and starving becomes a tentative hungry assessment. Pant/Wheeze becomes vocal breath sounds while safety questions stay tentative. Woods’ end is near becomes a natural forest-exit estimate. The choice Drive becomes Drive it off; Hit becomes Fight. Mihwa’s clandestine offer preserves isolation being largely nominal and remains her in-game explanation, not an external historical claim or formal legal exemption. One silence glyph target at B307 R55 still requires fresh native display checks.

Current binding uses registered B281–B300, SHA-256 `{release['candidate_sha256']}`. A fresh own-Hodram4,001-frame startup matches ten prior reviewed RGB captures and exports its own RAM with the staged payload checked. This is not B301–B310 optional-scene gameplay. All73 original current catalogue bindings,184 original style-slot selections andnine caption bindings pass. Native roles207/208/211/214/215/218 are bound from this startup:207 resolves to Hodram and the other unassigned slots fall back to Sailor151. No roster, RNG, money, event flag or assignment override occurs; this is not proof of future conditional participation.

Next review all eight scoped actors and proper/place/item terms through the relevant original consumers. Format225 bodies andnine captions using the validated consumer rules, including eight FE notices and one FI-bearing FE injury notice. Reuse the qualified null-actor FE substitution ABI when dependencies match, but check the changed stored text and every new page freshly. Then inspect readable native sheets, resolve wrap/glyph findings, check reconstructed storage, sample distinct display behavior and integrate through the registered cumulative workflow with exact clean-input patch and candidate-owned startup. Do not activate every conditional line or repeat completed earlier batches.

Integrated totals remain18,133:11,009 revisions and7,124 retentions. Historical source/prose/draft counters remain18,136. No B301–B310 ROM, scene-gameplay coverage or integration credit exists yet. No test/build process remains live. Main, current registered candidate, canonical/clean inputs, all accepted layers/runtime bounds, weekend ZIP and every earlier ROM/translation/retention/evidence remain preserved. Continue the full objective across every route, shared town/shop/random exchange, unfinished earlier contextual pass, names and player-facing prose, with Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit stay separate. No guide photos or main promotion. The full goal remains active.
'''
    paths=(SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,roles,ROOT/'clean_name_fields.json',
        ROOT/'draft_name_reference_v1.json',ROOT/'draft_name_reference_v2.json',ROOT/'source_first_refinement_v3.json',
        ROOT/'own_parent_startup_v1/own_route_context.json',Path(__file__))
    evidence={str(p):digest(p) for p in paths}
    checkpoint(mutation=ROOT/'contextual_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B301–B310: all234 contextual decisions saved; scoped names/terms and display gates pending.',
            next_action='Review scoped names/terms, format225 bodies/nine captions including the FI-bearing FE notice, then native/visual/stored/representative gameplay and integration.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        new_entries={'Hodram_B301_B310_clean_next_20261107':dict(new_credit=0,total_editorial_objects=234,ordinary_speeches=73,
            physical_personality_alternatives=152,typed_caption_records=9,source_meanings_saved=234,localized_drafts_saved=234,
            current_English_comparisons=234,remaining_current_English_comparisons=0,proposed_revisions=127,justified_retentions=107,
            all_four_prose_gate_records=234,scoped_names_pending=True,scoped_terms_pending=True,fresh_native_body_pages_pending=True,
            stored_reconstruction_pending=True,current_story_gameplay_utterances=0,representative_gameplay_pending=True,
            registered_integration_pending=True,all_five_review_gates_pending=True,all_formatting_gates_pending=True,
            clean_meanings_anddrafts_sealed_before_current_ROM_English=True,no_blanket_claim_of_no_historical_English_exposure=True,
            source_key_overlap_with_completed_credit=0,untranslated_turns_corrected=2,punctuation_consistency_targets=1,
            source_only_unselected_tail_objects=400,native_job_live=False,registered_build_live=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence=evidence)},
        summary=summary,document='docs/editorial_Hodram_B301_B310_contextual_20261107.md',document_text=document,completed=18133,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved234 contextual decisions with zero integration credit. Registered18,133 and full goal preserved.')

if __name__=='__main__':main()
