"""Save the substantial source/draft/current-binding checkpoint without duplicate credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')
CURRENT = Path('work/analysis/Hodram_B191_B210_current_20261104/current_effective.json')
OBJECTS = Path('work/analysis/Hodram_B191_B210_current_objects_20261104/current_objects.json')
RELEASE = Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')


if __name__ == '__main__':
    draft_path = ROOT / 'complete_clean_English_drafts_v1.json'
    identity_path = ROOT / 'native_identity_checkpoint_v1.json'
    terms_path = ROOT / 'source_current_term_checkpoint_v1.json'
    drafts, identities, current, objects, release = map(load, [draft_path, identity_path, CURRENT, OBJECTS, RELEASE])
    assert len(drafts['records']) == 373 and drafts['speech_drafts'] == 352 and drafts['caption_drafts'] == 21
    assert all(not r['review']['formatting'] for r in drafts['records'])
    assert identities['ordinary_actor_bindings'] == 43 and identities['current_name_consumer_bindings'] == 86
    assert current['records'] == 352 and len(objects['choice_records']) == 21
    assert objects['current_speech_packet_sha256'] == sha(CURRENT.read_bytes())
    assert current['current_ROM_sha256'] == release['candidate_sha256']
    summary = ('B191–B210 now has all 373 clean-source logical English drafts across twenty complete exchanges: '
        '352 speeches and 21 captions in ten menus. All 43 actor identities/86 name consumers are bound: 15 fresh, 28 compatible reuses. '
        'Terms and all 373 current stored/effective references pass binding checks. Individual current-English editorial comparisons, scoped name decisions and fresh display checks remain. '
        '9933 completions and experimental d14c24ba/main are unchanged. No new ROMs, gameplay runs, completion credit or guide photos. Full scope and all evidence preserved.')
    text = '''# Hodram B191–B210: complete source-grounded drafts and current references

All twenty clean Japanese exchanges have been reread as complete conversations, including their conditional endings. All 373 source meanings and then all 373 logical English drafts were sealed before current-ROM English dialogue extraction in this intake. This is not a blanket claim of no historical exposure to related dialogue. The batch comprises 352 speeches and 21 captions across ten typed menus, no style objects and zero completed-record overlaps. B203's offset-78 `0020` is a proven label-free control, not a missing caption.

The 43 ordinary actors have 86 current name-consumer bindings. Fifteen actors received fresh clean/current progressive and full-name checks; 28 actors reuse exact compatible proofs. Complete prior ARM9 images normalize to the current image using only already-registered owned name/static-data repairs; actor models, relevant metadata, component pointers and complete target strings, COMMON and fonts match. Actor154 received two fresh consumers because its available standalone proof predates the runtime-bound repair. One small current selector batch checks all 43 voice classes. No inherited name getter was replayed merely to collect voice information. These are offline native checks, not new gameplay.

Keep distinct Sailor/Retainer consumers. The current Daimyo, Guildmaster, Innkeeper, Alluring Woman, Mysterious Old Man, Stranger and Shady Man bindings preserve source identity without inferring family, nobility beyond the daimyo role, employment, nationality or biography from regional metadata. Binding a native label does not yet credit its contextual editorial retention. Scoped name findings and their individual reasons remain part of the upcoming comparison pass.

Exact clean/current pointer readbacks bind eight goods (including Cordyceps), nine forecast cities, Glassmaking Guide, Shachihoko and the approved Charm/Wits/Spirit terminology. Medicine and dyes are broad source categories, not a particular remedy or pigment. The older global item-name asset still contains Orca Figurehead; the registered correction and current runtime say Shachihoko. Preserve that correction. Source item116 says 鯱の像 while the scene says シャチホコ; these are bound separately. The Rocco Alemkel project spelling is supported by the earlier contextual name proof, without asserting an external historical identity. No wider commodity, category, item or widget-fidelity audit is newly closed.

All 352 speech drafts have individual source, context, localization and naturalness draft gates plus source glosses and specific notes. The 21 menu captions preserve the six repeated price decisions, Ian's three-way decision, the rope purchase/refusal and the earrings' two different questions. No ordinary line breaks, positioning or padding were authored. Exact source keys and runtime macro counts pass, and all parrot call-and-response phrases match their preceding English cues. The first echo omits Angelo's startled interjection, as the Japanese does; this is explicitly checked rather than requiring an incorrect whole-utterance echo.

The town drafts preserve medicine rumors as reports, the daimyo's explicit giyaman/glass explanation, snobbish collectors undercut by the sellers' aside, doubtful dye-buying banter, tobacco peer pressure and the ladies' stated friendship. Later exchanges retain every negotiation price, conditional companion aside and precise attribute recipient. Ian's next time does not invent a next life; the celestial maiden remains speculation. Namahage and the bad-child chant remain named and uncanny; the gift stays unnamed. Carlo explicitly denies being a doctor and has the collapsed stranger brought to an inn, without an invented diagnosis or carrying method. The rope's power is a sales claim, the glass book is explicitly named, the medicinal book stays unnamed and the voluntary 1000 offer drops to 100. Jam's oshiro/castle recognition and the shachihoko/figurehead misunderstanding are preserved. Hodram retains the parrot-catch announcement, even though Angelo boasts afterward. The ceramic-earring legend remains the seller's account and the alternative hostile endings remain separate.

The complete drafts are `work/analysis/Hodram_B191_B210_clean_20261104/complete_clean_English_drafts_v1.json`, with immutable parts and exact dependency hashes in the same folder. Native names: `native_identity_checkpoint_v1.json`; terms: `source_current_term_checkpoint_v1.json`. The clean-only meaning checkpoint remains `complete_clean_meanings_checkpoint_v1.json`.

After those drafts were sealed, the unchanged native catalogue lookup bound all 352 current speech bodies, complete source/current preambles and command-kind sequences. Typed binding separately bound all 21 current captions with exact two/three-choice membership; there are no style objects. Current evidence is `work/analysis/Hodram_B191_B210_current_20261104/current_effective.json` and `work/analysis/Hodram_B191_B210_current_objects_20261104/current_objects.json`. These are source/current references, not finished editorial comparisons or proposed blanket rewrites. Read each existing-English exchange alongside the clean source and logical draft. Retain existing wording that works, explaining why individually; revise only where the source, voice or naturalness warrants it.

Next: finish all 373 individual existing-English comparisons and scoped name/term decisions, then apply fresh consumer-aware formatting, complete glyph/bounds/pagination checks and visual review of every newly generated page. Use the source-supported dramatic layout only where justified. Reuse compatible earlier runtime/storage proofs; add representative gameplay for the batch's distinct menu, paragraph, FE, letter, substitution and transition behaviors or concrete risks. Do not claim natural conditional activation or full playthrough coverage from initialized tests. Integrate the complete reviewed batch only after necessary checks pass through the registered cumulative workflow, exact clean-input patch and candidate-own startup.

All jobs are terminal with exit code zero. There are no new ROMs or emulator runs. Completion remains 9933 (6004 revisions/3929 retentions); historical source/prose/draft counters remain 9936. The current registered experimental candidate is d14c24ba; canonical main is unchanged. This checkpoint adds no completion credit and no finalized retention/revision count. The full editorial objective, every earlier translation and ROM, graphics separation and the later older-record technical re-audit remain intact. No promotion, commit/push, pruning or guide photos.
'''
    checkpoint(mutation=ROOT / 'drafts_current_binding_ledger_mutation_v1',
        batch_key='Hodram_B191_B210_clean_next_20261104',
        batch_updates=dict(source_meanings_saved=373, localized_drafts=373, speech_drafts=352, caption_drafts=21,
            current_English_comparisons=0, remaining_current_English_comparisons=373,
            current_stored_effective_bindings=373, ordinary_actor_bindings=43, current_name_consumer_bindings=86,
            fresh_native_actors=15, exact_reused_native_actors=28, fresh_clean_andcurrent_name_getters_each=30,
            native_identities_bound_contextual_name_andterm_decisions_pending=True,
            native_identity_andterms_still_pending=False, scoped_name_andterm_editorial_decisions_pending=True,
            source_context_andlogical_prose_drafts_complete_not_final_comparison=True,
            all373_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
            all_individual_fifth_formatting_gates_pending=True, actual_new_batch_gameplay=False,
            draft_checkpoint=str(draft_path), draft_checkpoint_sha256=sha(draft_path.read_bytes()),
            identities=str(identity_path), identities_sha256=sha(identity_path.read_bytes()),
            terms=str(terms_path), terms_sha256=sha(terms_path.read_bytes()),
            current_speech_bindings=str(CURRENT), current_speech_bindings_sha256=sha(CURRENT.read_bytes()),
            current_object_bindings=str(OBJECTS), current_object_bindings_sha256=sha(OBJECTS.read_bytes()),
            no_current_ROM_English_extraction_in_this_intake=False,
            prior_source_only_flags_are_historical_current_status_supersedes=True,
            no_live_job=True, new_credit=0, full_goal_complete=False, guide_photos=False),
        summary=summary, document='docs/editorial_hodram_B191_B210_drafts_20261104.md', document_text=text, completed=9933,
        protected={'translations/release_stack.json': release['registry_sha256'], release['candidate']: release['candidate_sha256'],
            'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved 373-draft/current-reference checkpoint; 9933 completions and all earlier work preserved. Full goal active.')
