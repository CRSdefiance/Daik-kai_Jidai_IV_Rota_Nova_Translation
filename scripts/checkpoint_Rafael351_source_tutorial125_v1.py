"""Checkpoint complete351 clean drafts and125 contextual tutorial comparisons without credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
SEALED = ROOT/'sealed351_v1/all_source_meanings_andindependent_drafts.json'
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
OBJECTS = Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
REVIEW = Path('translations/rafael_B121_B140_priority_tutorial_comparison_v1.json')
BUILD = Path('work/analysis/Rafael516_registered_build_v1_20261105')
LIVE = BUILD/'OS_live_source351_checkpoint.json'

if __name__ == '__main__':
    sealed, current, objects, review, live = map(load,[SEALED,CURRENT,OBJECTS,REVIEW,LIVE])
    assert (sealed['source_objects'],sealed['ordinary_speech_drafts'],sealed['physical_style_drafts'],sealed['source_caption_drafts']) == (351,307,34,10)
    assert sealed['remaining_source_speech_style_orcaption_drafts'] == 0 and len(sealed['records']) == 351
    assert current['records'] == 307 and (len(objects['style_records']),len(objects['choice_records']),objects['native_style_getter_cases']) == (34,10,48)
    assert (review['contextual_comparisons'],review['proposed_revisions'],review['justified_retentions'],review['four_gate_passes']) == (125,68,57,105)
    assert len(review['pending_UI_name_term_IDs']) == 20 and review['remaining_source_comparisons'] == 226
    assert all(not r['review']['formatting'] for r in review['records'])
    assert live['confirmed_live_by_OS'] and live['PID'] == 56664 and live['session'] == 20868
    assert not (BUILD/'completion.json').exists()
    receipts = [Path('work/analysis')/name/'completion.json' for name in
        ['Rafael_B121_B140_current_binding_gc_v1_20261105','Rafael351_current_objects_gc_v1_20261105']]
    for receipt in receipts:
        result = load(receipt)
        assert result['terminal'] and result['completed_without_exception'] and result['all_locked_sources_unchanged']
        assert not result['garbage_collection']['errors'] and result['garbage_collection']['peak_private_bytes'] < 200*1024*1024
    summary = ('Rafael early story/all tutorials remain first. All351 B121–B140 clean meanings/independent drafts aresealed '
        '(307 speeches,34 personality variants,10 captions);no existing drafts lost. Current stored/effective text and48 style getters arebound toverified678. '
        'Seven complete early tutorials nowhave125 contextual comparisons:68 proposed revisions/57 justified retentions,105 four-prose-gate passes, '
        '20 exact UI/item-label holds;226 comparisons andall fresh display gates remain. Found3 full-width I letters,two full-width question glyphs, '
        'a missing FO substitution,unclear unclaimed-share condition,andlost Deck-role/map/investment context. These fixes arenotin the running516 build. '
        'That680-entry build20868/PID56664 isfreshly OS-confirmed live,collector errors empty,registry9bc4dd5e/core27ce unchanged. '
        '11845 integrated;verifiedcc71/main unchanged. No guidephotos,pruning orpromotion;full scope/ROMs/evidence preserved.')
    document = f'''# Rafael351 source complete and tutorial125 comparisons — November 5, 2026

Rafael’s early story and all tutorials remain first. Preserve the full editorial objective, all routes andunfinished earlier passes, shared town/shop/random dialogue, names, glyphs andremaining prose. All ROMs, translations, justified retentions andevidence remain. No guide photos, pruning ormain promotion.

## Source and current binding

`{SEALED}` seals **all351 source meanings andindependent logical drafts**, before current-ROM English extraction inthis intake:307 ordinary speeches,34 physical personality variants and10 captions. It joins the preserved115 drafts with139 B127–B135 drafts and97 B136–B140 drafts. Six complete eight-slot personality objects andall five two-choice menus areincluded fromthe beginning; B130/B131 remain control-only. No source gate isautomatically approved bysealing, andno blanket historical unexposure isclaimed.

`{CURRENT}` binds all307 ordinary stored/effective bodies tothe own verified678/captain0 snapshot. `{OBJECTS}` binds all34 style bodies,10 captions and48 original style-slot getter cases. Existing source-control/alias/catalogue readers arereused withoutnew renderer investigation orstory reachability claims. Both fixed read-only binding jobs completed under200MB peak private memory; no emulator capture orlarge rendering run overlapped the ongoing build. These arecomparison inputs,notnew gameplay orformat approval.

The full clean conversations include sailing/trade/crew/route tutorials, Julian/Claudio treasure banter, the rescue/reward exchange, jade/tablet observations, gender/identity-sensitive Cristina recruitment andthe colonial/slave-trade confrontation. Source notes preserve uncertainty,actualkinship versus familiar address,andpersonality variants thatmake different claims about afigurehead. Inparticular, the late treasure exchange distinguishes alegend fromproof ofexistence anduses drinking-joke idioms ratherthan literallyturning Rafael intofood. Do notflatten those shifts during comparison.

## Early tutorials reviewed first

`{REVIEW}` contains **125 individual contextual comparisons:68 proposed revisions and57 justified retentions** acrosscomplete B127–B129 andB137–B140 exchanges,including eight captions. All125 have source/context/naturalness review;105 pass allfour prose gates and20 retain localization holds forprecise UI/role/item labels. Every formatting gate isfalse. The remaining226 objects have clean drafts andexact current bindings,buttheir contextual comparisons arenotcomplete.

Concrete findings,withindividual exact source/current references inthe manuscript:

- B128 R189 hasone full-width`Ｉ`;B139 R5 hastwo. Preserve the already-natural wording ofthese two speeches anduse ASCII`I`. B128 R114 andB139 R59 also use full-widthquestion glyphs;their questioning intent isretained withASCII punctuation. No global normalization ofnative controls orfixed-width consumers isauthorized.
- B139 R23 drops the source`FO` company substitution andchanges having agreements withLisbon/Ceuta intosimply trading there. The proposal restores the substitution andthe actual route prerequisite. All125 proposed logical texts pass exact source FI/FA/FO counts.
- B129 R27 requires **unclaimed** market share tobe available,notmerely thatMadeira hasmarket share. B129 R24 also loses local goods besides sugar andturns the expected future base role intoa certainty.
- B139 R30 loses the Deck-screen assignment context forCaptain/Surveyor. R42 omits destination selection onthe map. R71 reduces going toLisbon,buying a sextant,andJulio managing withit toan impersonal promise. Retain R74’s correctlyexplicit instruction toequip Julio himself.
- B128 R93 appears totell the player tocontrol the wind. The proposal clearlyinstructs adjusting the sails whilewatching wind direction. The A/B opening andL/R turning mappings remain exactlythose inthe clean source;their final labels/formatting andrequired focused display checks stillremain.
- B140 restores the Indian Ocean trading-route context,construction expertise,military-investment category andqualified expected saving,ratherthan an unconditional vague fortification advantage. No historical date,numericaldiscount ornewcombatbonus isadded.

Natural dialogue revisions restore Julio’s reassuring mentor voice,Rafael’s hesitant questions,andClaudio’s playful goal-hunting remark where the current prose isclipped orstilted. Existing clear controls,brief responses andgood explanations areindividually retained. For example,the existing Madeira sentence keeps the small-island detail morefullythanthe independent draft;source-first drafting doesnotforce replacement ofbetter current wording.

Twenty held records explicitly list unresolved mode/map/auto-travel/flagship-allocation/place/item labels. A prior bound ARM9 label identifies 航路図 as`Map`,whilecurrent prose varies between`Route Map` and`Auto Travel` andsome independent drafts use`Route Chart`/`Auto Sail`. Resolve the applicable visible consumer usingexact existing native/runtime proofs; donotapprove a label justbecause a stored string looks plausible. Captain/Surveyor,trade-house,Arms,Full/Half/Anchor,Cape Verde andsextant bindings remain scoped tothese held records. No user question isneeded where repository evidence canresolve them.

## Build and continuation

The running **516-object cumulative build doesnotcontain these125 new proposals**. It remains the previously qualified261+255 integration described inthe [preceding checkpoint](editorial_Rafael516_build_next351_20261105.md). Session20868/PID56664 isfreshly confirmed live by`{LIVE}`;collector errors remain empty. Preserve originalcore27ce0796,registry9bc4dd5e,all114 accepted layers andall eight final stages. Quiet output isnotterminal;poll thissame handle/PID orits authoritativecompletion. Do notrestart itorlaunch duplicate full builds.

Continue the remaining226 complete-exchange comparisons,thenresolve scoped names/dynamic roles andthe20 tutorial-label holds. Reuse all351 drafts andthe current bindings. Afternecessary prose checks,format substantial completed batches andrun fresh changed-text/native/stored/visual checks;the current source bindings donotgive display coverage. Use representative gameplay fordistinct risks andidentify unvisited content. Do notshorten good prose justtofit earlier line breaks.

On680 buildterminal0,run the preparedfinal516 verifier,exact clean patch reconstruction,own planned-startup identity/RAM binding andboth Fernan getters beforeonce-only credit. Reuse the completed4001-frame planned capture ifthe final hash isa51c79e4. Onfailure preserveitanddiagnose the concrete cause. Original679’s MemoryError remains historical,notan active wait. All remaining final-build instructions areinthe preceding checkpoint.

Integrated totals remain11845=6836 revisions+5009 retentions;historicalsource/prose11848 unchanged. Verified experimentalcc71ec06 andmain3cb827e4 remainunchanged. Graphics artwork andthe later older-record technical re-audit remain separate. Full goal active.
'''
    # Keep the name in this documentation consistent with the actual source/prose identity.
    document = document.replace('Julian/Claudio','Julio/Claudio')
    evidence = {str(p):sha(p.read_bytes()) for p in [SEALED,CURRENT,OBJECTS,REVIEW,LIVE,*receipts]}
    checkpoint(mutation='work/analysis/Rafael351_source_tutorial125_checkpoint_20261105',
        batch_key='Rafael_SC0_B121_B140_clean_20261105',
        batch_updates=dict(all_source_drafts_sealed=str(SEALED),all_source_drafts_sealed_sha256=sha(SEALED.read_bytes()),
            clean_meanings_andindependent_drafts=351,remaining_clean_drafts=0,current_speech_binding=str(CURRENT),
            current_speech_binding_sha256=sha(CURRENT.read_bytes()),current_style_choice_binding=str(OBJECTS),current_style_choice_binding_sha256=sha(OBJECTS.read_bytes()),
            contextual_comparisons=125,proposed_revisions=68,justified_retentions=57,four_prose_gate_passes=105,
            pending_UI_name_term_IDs=review['pending_UI_name_term_IDs'],remaining_comparisons=226,
            tutorial_comparison=str(REVIEW),tutorial_comparison_sha256=sha(REVIEW.read_bytes()),
            all_current_comparisons_name_term_controls_andfive_gates_pending=False,
            remaining_comparisons_UI_holds_andall_fifth_gates_pending=True,all_fifth_formatting_gates_pending=True,evidence=evidence,new_credit=0),
        additional_updates={
            'Rafael516_registered_cumulative_20261105':dict(new_credit=0,build_live_receipt=str(LIVE),
                build_live_receipt_sha256=sha(LIVE.read_bytes()),build_live_at_OS_checkpoint=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='125 earlytutorial comparisons saved;remaining226/20 labelholds,680 buildactive',
                registered_build_live=True,registered_build_session=20868,registered_build_PID=56664,
                next_action='Poll20868/PID56664;continue remaining226 contextual comparisons andresolve20 UI/item holds usingexisting exact native proofs. All351 source drafts/current bindings saved.')},
        summary=summary,document='docs/editorial_Rafael351_source_tutorial125_20261105.md',document_text=document,completed=11845,
        protected={'translations/release_stack.json':'9bc4dd5e408f4e474844d25b1602d2cc4560db371d7c5ee4a92af8b3753cc6c9',
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            'out/all_routes_combined_help97_rafael330_20261105_candidate.nds':'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'})
    print('Checkpoint saved:351 clean drafts/current bindings;125 tutorial comparisons,68 revisions/57 retentions,20 holds.680 build20868/PID56664 live;11845 integrated,no newcredit ormain change.')
