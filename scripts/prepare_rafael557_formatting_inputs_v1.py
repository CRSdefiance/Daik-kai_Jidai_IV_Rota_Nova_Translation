"""Keep complete exchanges and mark all61 substitutions without authoring line breaks."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('translations/rafael_B141_B160_contextual_review_v1.json')
PROSE=Path('translations/rafael_B141_B160_contextual_review_v2.json')
OUT=Path('translations/rafael_B141_B160_formatting_manuscript_v1.json')
PREFERENCES=Path('translations/rafael_B141_B160_visual_preferences_v1.json')

if __name__=='__main__':
    assert all(not p.exists() for p in [PROSE,OUT,PREFERENCES])
    original=load(SOURCE);prose=deepcopy(original)
    refinements={
        'DK4_MES_B143_R0082':("Ahem. We should let them speak. Let's keep quiet.",
            'Keep Arcadius\'s discreet, inclusive request to let the principals speak; replace the dangling Quietly phrase with a natural request for silence.'),
        'DK4_MES_B145_R0177':('When I decided to sail with Hans, I thought it best to dress as a man.',
            'Retain the timing and Eirene\'s personal judgment while avoiding repeated decided in the same sentence; Hans still supplies the following safety rationale.'),
    }
    for row in prose['records']:
        if row['id'] not in refinements:continue
        assert row['decision']=='revision' and not row['review']['formatting']
        english,note=refinements[row['id']]
        row['previous_contextually_reviewed_English']=row['english']
        row['english']=english;row['finding']=row['localization_note']=note
    prose.update(previous_manuscript=str(SOURCE),previous_manuscript_sha256=sha(SOURCE.read_bytes()),
        final_exchange_readaloud_refinements=refinements,revision_retention_counts_unchanged=True)
    prose['evidence'].update({str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]})
    save(PROSE,prose)
    doc=deepcopy(prose);tokens=0
    for row in doc['records']:
        assert row['review']['formatting'] is False
        row['editorial_logical_English']=row['english']
        if row['kind']=='typed-choice-label':continue
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for macro in ['FI','FA','FO','FU']:
            count=row['english'].count('{MACRO:'+macro+'}')
            assert count==row['native_literal_token_counts'].get(macro,0)
            tokens+=count
        assert isinstance(row['source_record_index'],int)
        row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
        row['prior_macro_normalized_comparison']=None
    assert tokens==61 and len(doc['records'])==557
    doc.update(previous_manuscript=str(PROSE),previous_manuscript_sha256=sha(PROSE.read_bytes()),
        physical_speech_objects=549,ordinary_speech_objects=549,style_physical_speech_objects=0,
        style_command_objects=0,typed_choice_objects=8,typed_choice_commands=4,
        pending_name_term_IDs=[],all557_individual_four_prose_gates_pass=True,
        native_macro_tokens_explicitly_marked_no_other_prose_changes=True,
        current_FU_expansion_parity_width_anddisplay_proof_pending=True,
        historical_Raphael_lengths_not_assumed_for_current_Rafael=True)
    save(OUT,doc)
    save(PREFERENCES,dict(records={},all_paragraphs_use_qualified_default_formatter_first=True,
        progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,
        source_default_available_width_to_be_validated_against_actual_compiled_pages=True,
        author_inserted_ordinary_breaks=0,new_credit=0))
    release=load('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
    summary=('Rafael/all tutorials remain first. The557 complete comparisons remain235 revisions/322 retentions; '
        'two final read-aloud refinements improve Arcadius\'s quiet request and Eirene\'s repeated decided phrasing. '
        'Latest prose v2 and formatting-input v1 preserve exact bindings and explicitly mark all61 FI/FA/FO/FU substitutions. '
        'No authored wraps or inherited per-record guard budgets. All557 fifth gates stillfalse; FU2 actual expansion/parity/width '
        'and allfresh native pages/previews/stored checks/focused tests remain next. Integrated12712/cumulative3bf3/main3cb8/registry/core '
        'unchanged; no new gameplay,ROM orcredit. Full scope/evidence preserved; no guide photos orpromotion.')
    text=f'''# Rafael557 formatting-input checkpoint — November 5, 2026

Continue the full goal with **Rafael and all tutorials first**. The completed contextual work is documented in [the557 comparison checkpoint](editorial_Rafael557_contextual_checkpoint_20261105.md); do not repeat its source extraction, current comparison or name getters.

Latest logical prose: `{PROSE}`. It preserves all557 individual findings,235 proposed revisions and322 justified retentions. A final read through the exchanges improves two lines:Arcadius's dangling request for quiet becomes an inclusive complete sentence; Eirene's explanation avoids repeating decided. Earlier versions are preserved. Four prose gates pass per record; all fifth gates remainfalse.

Formatter input: `{OUT}`. All61 native substitutions are explicitly marked, including FU2, without authored line breaks or further wording changes. `{PREFERENCES}` starts with empty record preferences and the established216px progressive/228px physical FE defaults. Do not inherit another source record's narrower guard budget or layout choices. Typed captions remain separate. The two FU occurrences still need actual current expansion, ASCII parity and width qualification; do not assume historic Raphael lengths. Existing FU codec/profile/rebuild support is already known.

Next run fresh native formatting and complete glyph/bounds/pagination checks for all549 speeches and separate eight typed captions. Review every generated page on readable contact sheets and refine formatting for concrete findings. Use representative actual transitions, page behavior and FU tests, then complete stored/catalogue/loader/allocation checks and registered cumulative integration with an exact clean-input patch. Newly changed text has no display approval from older wording. No new gameplay, font planes or page previews have been generated at this checkpoint.

Integrated totals remain12712; cumulative3bf3/main3cb8, registry/core, allROMs and114 accepted layers unchanged. Allroutes/shared/town/random/earlier unfinished prose remainin scope. Global names and two catalogue de pointer corrections remain open under proper ownership. Deferred artwork and later older-record re-audit remain separate. No guide photos, promotion orcommit/push. Full goal active.
'''
    checkpoint(mutation='work/analysis/Rafael557_formatting_input_checkpoint_20261105',
        batch_key='Rafael_SC0_B141_B160_clean_20261105',
        batch_updates=dict(new_credit=0,manuscript=str(PROSE),manuscript_sha256=sha(PROSE.read_bytes()),
            formatting_manuscript=str(OUT),formatting_manuscript_sha256=sha(OUT.read_bytes()),
            visual_preferences=str(PREFERENCES),visual_preferences_sha256=sha(PREFERENCES.read_bytes()),
            final_readaloud_refinement_IDs=sorted(refinements),all61_literal_substitutions_explicitly_marked=True,
            all_fifth_formatting_gates_pending=True,current_FU_expansion_parity_width_anddisplay_pending=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557 prose v2/formatting input v1 ready;fresh native formatting andFU2 proof next',
            next_action='Qualify actual current FU2 expansion/parity/width;fresh all557 consumer-specific formatting/pages/visual andfocused tests;then registered integration.')},
        summary=summary,document='docs/editorial_Rafael557_formatting_input_checkpoint_20261105.md',document_text=text,
        completed=12712,protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256']})
    print('Saved557 formatting inputs withall61 explicit macros andno authored wraps;235 revisions/322 retentions. Allfifth gates pending;12712 integrated unchanged.')
