"""Save complete clean-first comparison and scoped names without granting display or release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B231_B250_v1 import RELEASE,REGISTRY
from scripts.draft_hodram_B251_B280_clean_v1 import OUT as DRAFTS
from scripts.gloss_hodram_B251_B280_clean_v1 import ROOT,SCOPE,OUT as MEANINGS
from scripts.review_hodram_B251_B280_contextual_v1 import OUT as PROSE,CURRENT,OBJECTS
from scripts.review_hodram_B251_B280_names_v1 import NATIVE as NAMES,REVIEW as NAME_REVIEW
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

def main():
    paths=(SCOPE,MEANINGS,DRAFTS,PROSE,CURRENT,OBJECTS,NAMES,NAME_REVIEW,ROOT/'name_planes_v1/native_name_planes.json')
    scope,meanings,drafts,prose,current,objects,names,review,planes=map(load,paths)
    release,ledger,package=map(load,(RELEASE,LEDGER,PACKAGE))
    assert scope['total_editorial_objects']==meanings['records_count']==drafts['records_count']==prose['records_count']==216
    assert not scope['source_key_overlap_with_completed_credit'] and prose['counts']=={'retention':88,'revision':128}
    assert prose['remaining_contextual_comparisons']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert current['runtime']==objects['runtime']==names['runtime']==review['runtime']==planes['runtime']
    assert current['current_ROM_sha256']==release['candidate_sha256'] and names['current_native_getters']==42
    assert review['scoped_actors']==review['justified_retentions']==21 and review['name_revisions']==0
    assert (planes['scoped_actors'],planes['distinct_strings'],planes['fresh_name_planes'],planes['exact_reused_name_planes'])==(21,18,12,6)
    assert planes['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert ledger['records_editorially_completed']==17533 and not ledger['full_goal_complete']
    visual=ROOT/'scoped_names_visual_approval_v1.json';assert not visual.exists()
    sheets=[ROOT/'name_planes_v1/names_part1.png',ROOT/'name_planes_v1/names_part2.png']
    save(visual,dict(native=str(paths[-1]),native_sha256=digest(paths[-1]),all18_name_strings_directly_viewed=True,
        sheets=[dict(path=str(p),sha256=digest(p)) for p in sheets],leading_internal_trailing_glyphs_fit_andfont_consistent=True,
        offline_only=True,actual_new_batch_headers_unvisited=True,full_catalogue_UI_unvisited=True,new_credit=0))
    summary=('Hodram B251–B280 has all 216 clean meanings, drafts and contextual decisions saved: '
        '128 proposed revisions and 88 justified retentions. All 21 scoped names are retained with reasons; '
        '42 fresh getters and all 18 directly viewed name strings pass. Two untranslated instructions, India/location errors, '
        'inconsistent names, an invented Lord and two glyph targets are identified. Scoped terms and fresh body/menu, stored, gameplay '
        'and release checks remain. Integrated coverage stays 17,533; main is unchanged.')
    doc=f'''# Hodram B251–B280: complete contextual comparison and scoped names

{summary}

The original clean B251–B270 intake is preserved. Its 135 ordinary speeches, 16 voice alternatives and seven captions made a 158-object batch. Ten additional complete blocks supply 58 speeches; their disjoint source inventories are joined without re-extracting the first twenty. The [scope receipt](../{SCOPE.as_posix()}) has 216 unique, nonoverlapping source keys: 193 ordinary speeches, 16 physical alternatives in two eight-slot voice objects, and seven captions in three menus, across 30 complete blocks. All 17,533 credited keys are checked; no already-credited source record is reopened or counted again. No block is control-only.

All [216 clean meanings](../{MEANINGS.as_posix()}) and [216 independent logical drafts](../{DRAFTS.as_posix()}) were sealed before eligible current story English was extracted. Exact clean Japanese references, complete preambles, branch membership, aliases and substitutions remain on every record. Only existing name/stat references were consulted for drafting. Provisional Romanized Carducci/Berrio glosses do not silently rename accepted Gabriel Cardocci/Hernan Berio; the original gloss remains preserved. Do not claim that no historical English had ever been seen.

The [contextual review](../{PROSE.as_posix()}) gives every record its exact current binding, faithful meaning, whole-exchange context, individual revision or retention finding and four passing prose gates. All fifth gates remain false. The two figurehead exchanges preserve the separate taking/leaving rewards, a compassionate unidentified voice, an imperious voice, and Fernando’s unconfirmed fear of a curse. Parenthetical private thoughts stay private. The floating-ice riddle retains full-water, front/rises, left/falls and right/unchanged conditions and original choice indices. The shrine’s identity, treasure titles, doctrine and unspoken item names are not supplied.

The linked guild scenes retain distinct requests, reminders, capture returns, advances, rewards and optional ruins clues. The Yuris encounter keeps dreamy aesthetic distraction followed by realization of neglected duties; London comes before the estate. Gabriel’s unpaid-tab joke and repeated excuse remain linked to the Stockholm return, without paying his tab or assigning ownership of suspected stolen property. Julian’s Portuguese/Spain accusation and reported courier work remain the speaker’s claims. The father/daughter revenge facts are explicit, but no age, name, kinship with the guildmaster or execution is invented. Jean’s self-serving smuggling defense and anticipated excuse retain their deadpan payoff. Jacob’s possessive cargo complaint receives its original correction. Hernan’s self-aggrandizement supplies no Lord title.

Concrete revisions include two wholly Japanese instructions, B256 R9 and B260 R17; Yulis to native Yuris; Prett Perot/Prett to accepted Plett Perrault; the actual Forbidden City instead of Purple Palace; India instead of the broader South Asia in B273 R9/B275 R12/R17; the guildmaster instead of Barkeep in B265 R17; first-person speech instead of this man/this one; and FA as surname address rather than faction membership. All ten currency results retain exact quantities and restore gold coins, and all seven market-share results stay slight and unquantified. The physical riddle answers and item-possession conditions are unchanged.

Two glyph targets await fresh body renders: B252 R116’s full-width question/exclamation pair becomes ASCII `?!`, and B274 R15’s mistaken lowercase `l` in `am l` becomes the English pronoun `I`. No global punctuation conversion or font-artwork change is applied. The 88 retentions have individual reasons, including working short replies, conventional formal voices, natural panic cries, the tavern proprietor’s interrupted bill appeal, concise job reminders, voice alternatives and menu responses. Retained prose still needs fresh formatting where the new cumulative batch is reconstructed.

The [21 scoped name/role decisions](../{NAME_REVIEW.as_posix()}) preserve approved public forms with individual source/context reasons. Both original current getters pass for all 21, using this registered build’s fresh own-Hodram startup RAM. Exact clean fields and pointers are rechecked; the unchanged source constructor ABI is reused without new clean getter permutations. Staged current fields are read from the owned runtime mapping, not assumed to be static file pointers. Regional metadata stays opaque and supplies no surname, religion, rank or biography. Source selector207 resolves to Hodram and 208 to the ordinary unassigned Sailor fallback; this proves a display context, not future conditional participation.

Native name planes use 12 fresh and six exact cached strings, qualified by identical complete ARM9/font/COMMON inputs. Duplicate Port Worker and Guildmaster labels account for 21 actors but only 18 distinct nameplate strings. Both sheets were directly viewed; every complete leading/trailing glyph and all name widths pass. The [direct-view receipt](../{visual.as_posix()}) does not claim actual B251–B280 headers or full catalogue UI. The global 207-name review remains open.

Bindings use registered Hodram B231–B250, SHA-256 `{release['candidate_sha256']}`. A fresh own-Hodram 4,001-frame startup matches ten previously viewed opening captures, validates complete staged payload and exports fresh read-only RAM. It is not gameplay coverage for these scenes. All 193 current catalogue lookups, 16 original current style-slot selections and seven caption bindings pass. None is a new source-control or whole-route characterization claim.

Next finish scoped geographic/stat terms, preserving the established San Jorge term and the Luck/Charm distinction. The current body scope is 209 renderable speeches: 178 progressive bodies including the 16 physical alternatives, plus 31 FE bodies. The eight substitution-bearing speeches comprise two FI system notices, three FI greetings and three FA surname addresses. Preserve the FE distinctions between inscriptions, sounds, entity voices and result notices. Use the validated native consumer rules; run new checks on changed text and review every new page, including riddle and voice panels, complete leading/trailing characters and page transitions. Resolve concrete early wraps without shortening good prose. Then reconstruct complete blocks, check stored text, sample representative distinct display behaviors and integrate through the registered cumulative release/clean-input patch workflow. Do not require activating every conditional line or repeat compatible technical proofs wholesale.

Integrated coverage stays 17,533 (10,699 revisions, 6,834 retentions). Historical source/prose counters remain 17,536. There is no new ROM or integrated credit for B251–B280 yet. Current registered candidate, clean input, canonical base, accepted runtime including ASCII right bounds, main and weekend ZIP remain unchanged. All remaining storylines, earlier unfinished contextual passes, shared shop/town/random exchanges, names and player-facing resources remain in scope with Rafael/tutorial priority. Deferred graphics artwork and the later older-record re-audit remain separate. No guide photos are collected. No job remains live; the full goal remains active.
'''
    evidence={str(p):digest(p) for p in (*paths,visual,ROOT/'own_parent_startup_v1/own_route_context.json',ROOT/'role_bindings_v1.json',Path(__file__))}
    checkpoint(mutation=ROOT/'contextual_names_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B251–B280: 216 contextual decisions and 21 scoped names saved; body/menu checks pending.',
            next_action='Bind scoped terms, format 209 bodies/seven captions, review fresh native pages and refine concrete wraps before storage/gameplay/integration.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        additional_updates={'Hodram_B251_B270_clean_next_20261107':dict(new_credit=0,expanded_into='Hodram_B251_B280_clean_next_20261107',
            original_clean_intake_preserved=True,clean_intake_inventory_pending=False,overlap_reconciliation_pending=False,
            expansion_reason='158 objects in the first twenty blocks; ten complete additional blocks make a practical 216-object batch.',
            no_separate_completion_credit=True)},
        new_entries={'Hodram_B251_B280_clean_next_20261107':dict(new_credit=0,total_editorial_objects=216,ordinary_speeches=193,
            physical_personality_alternatives=16,typed_caption_records=7,source_meanings_saved=216,localized_drafts_saved=216,
            current_English_comparisons=216,remaining_current_English_comparisons=0,proposed_revisions=128,justified_retentions=88,
            all_four_prose_gate_records=216,scoped_names_reviewed=21,scoped_name_revisions=0,scoped_name_retentions=21,
            scoped_name_strings_visually_reviewed=18,scoped_current_getters_passed=42,scoped_name_sheets_viewed=2,
            scoped_terms_pending=True,fresh_native_body_pages_pending=True,stored_reconstruction_pending=True,
            current_story_gameplay_utterances=0,representative_gameplay_pending=True,registered_integration_pending=True,
            all_five_review_gates_pending=True,all_formatting_gates_pending=True,no_current_English_dialogue_consulted=False,
            clean_meanings_anddrafts_sealed_before_current_English=True,native_job_live=False,registered_build_live=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence=evidence)},
        summary=summary,document='docs/editorial_Hodram_B251_B280_contextual_20261107.md',document_text=doc,
        completed=17533,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved 216 complete contextual decisions and 21 scoped name reviews. Integrated credit 17,533 and full objective preserved.')

if __name__=='__main__':main()
