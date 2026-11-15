"""Whole B51 clean-source exchange: four revisions and one justified retention."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_prose_v8560')
CURRENT = Path('work/analysis/Hodram_B51_current_v8559/current_effective.json')
GLOSS = Path('work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json')
DISPLAY = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
VIEW = Path('work/analysis/Hodram_B51_source_view_v8557/source_view.json')
FLOW = Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')
TERM = Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v5.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v1.json')
NAMES = Path('translations/hodram_B51_speaker_name_review_v1.json')

CONTEXT = ('A gruff port worker warns Hodram to leave the southern Mediterranean. Hodram asks what the warning means. '
    'The worker explains that someone alarming is around and gives well-meant advice to head for another sea for self-preservation. '
    'The source event30-completed structural branch omits both later reactions. On the incomplete branch, a separate raw predicate '
    'includes Charles\'s questioning echo only for value1; Gerhard\'s private, unconfirmed suspicion follows, with or without that echo. '
    'The original query/branch result channel and extents are proven offline; these are not observed naturally reached paths. '
    'The source does not identify the person or establish a rank, gender, rulership, biography or relationship. '
    'Event51 has no listed prerequisite or exclusion, which does not prove outer eligibility, original location or chronology. '
    'Block numbering does not link this warning to the preceding gift exchange.')

DECISIONS = {
    6: dict(decision='revision', english="I don't know what you've got planned here in the southern Mediterranean, but take my advice: you'd be better off leaving.",
        finding='The existing Whatever your plans here loses the explicit southern Mediterranean setting and compresses the speaker\'s stated lack of knowledge. Leave while you can adds a narrowing opportunity that the Japanese does not state.',
        rationale='Restore the named sea area using the already reviewed southern Mediterranean term. I don\'t know what you\'ve got planned expresses the speaker\'s lack of knowledge in a gruff, conversational voice. Take my advice and you\'d be better off leaving preserve a warning and recommendation, without turning the worker into an authority expelling the party from a town or building. The contractions sound natural aloud; the length is chosen for meaning and voice, with relocation and automatic wrapping responsible for fit.'),
    10: dict(decision='revision', english='...What do you mean?',
        finding='...Why? asks for a reason but does not fully convey the source request to explain the warning\'s meaning.',
        rationale='Use the complete, idiomatic question What do you mean? for どういうことだ. Keep the initial hesitation. Read after the worker\'s warning, it asks for clarification in Hodram\'s restrained voice; it adds no accusation, recognized enemy or unsupported hostility.'),
    14: dict(decision='revision', english="There's someone around here who's bad news. I'm telling you for your own good: you'd better head for another sea.",
        finding='A monster rules here adds rulership and makes the description a categorical monster label. Neither is stated in the clean Japanese. The short sail elsewhere also leaves the explicit self-preservation advice largely implicit.',
        rationale='Someone around here who\'s bad news naturally conveys the alarming, unspecified ヤツ in this gruff warning. It does not name the person, assign a gender, crime, rank or political control, or assert supernatural identity. I\'m telling you for your own good localizes the well-meant idiom 悪いことは言わねえ together with the stated 身のため motive, without claiming the worker never lies or guarantees safety. Head for another sea preserves the direction to a different sea area. The worker is still blunt and colloquial rather than formally polite.'),
    32: dict(decision='revision', english='...Bad news?',
        finding='A terrifying man? asserts a male referent and an explicit fear description. It also drops the source\'s hesitant lead-in.',
        rationale='Echo the worker\'s new bad news description as a short, hesitant question. This preserves the source questioning repetition of とんでもないヤツ without confirming identity, strength or gender. The fragment is an intentional conversational echo, not allocation-driven telegraphy. It belongs only to Charles\'s nested conditional speech and must not be presented as part of every actual path.'),
    39: dict(decision='retention', english='(Could it be?)',
        finding='The existing parenthesized question already works as a sudden, private and unresolved suspicion after the warning.',
        rationale='Retain the complete parenthesized question because Could it be? is natural American English for the startled possibility in まさか. The short question can carry the source\'s incredulity in this exchange without mechanically copying Japanese punctuation or asserting that Gerhard recognizes a named person. Parentheses preserve the private thought; the unfinished referent preserves uncertainty. Do not add an identity, a remembered relationship or an explicit confirmation. Retain these words for their contextual effect, not because an older translation or technical gate approved them.'),
}

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    current, gloss, display, view, flow, term = map(read, [CURRENT, GLOSS, DISPLAY, VIEW, FLOW, TERM])
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed'] == 7224 and not ledger['full_goal_complete']
    assert current['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert gloss['all5_clean_utterances_glossed_before_current_English'] and view['all5_complete_source_pages_andfour_qualified_reused_nameplanes_directly_viewed']
    assert current['source_gloss_sha256'] == sha(GLOSS.read_bytes()) and current['source_native_display_sha256'] == sha(DISPLAY.read_bytes())
    assert flow['original_parser_r3_receives_carried_value_word'] and len(flow['caller_fragment_cases']) == 50 and len(flow['source_structural_paths']) == 10
    termrow = next(r for r in term['records'] if r['id'] == 'DK4_MES_B31_R0006')
    assert 'southern Mediterranean' in termrow['english'] and '南地中海' in termrow['source_Japanese'] and all(termrow['review'].values())
    completed = {historical_key(r) for family in ledger['completed_editorial_families'] for r in family['records']}
    assert len(completed) == 7224 and not completed & {historical_key(r) for r in current['records']}
    rows = []
    speaker_names = {1: 'Hodram Bergstrom', 16: 'Gerhard Adernkatz', 18: 'Charles Rochefort', 113: 'Port Worker'}
    for original in current['records']:
        row = deepcopy(original)
        choice = DECISIONS[row['source_record_index']]
        text = choice['english']
        assert (text == row['effective_predecessor_paragraph']) == (choice['decision'] == 'retention')
        assert text == text.strip() and not any(v in text for v in ['\n', '\r', '{LB', '{ALIGN', '{PAD', '  '])
        row.update(english=text, logical_English=text, planned_English_markup=f'{{SPEAKER:{row["source_selector"]:02X}}}' + text,
            speaker=speaker_names[row['source_selector']], context=CONTEXT, source_meaning=row['first_clean_source_gloss'],
            localization_note=choice['rationale'], finding=choice['finding'], decision=choice['decision'],
            retention_reason=choice['rationale'] if choice['decision'] == 'retention' else None,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            native_body_consumer='progressive', authored_ordinary_breaks=0, authored_alignment_spaces=0, manual_break_reason='',
            prior_raw_storage_preserved=row['current_raw_storage_English'], prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],
            whole_exchange_read_aloud_cadence_andemotional_progression_reviewed=True,
            previous_translation_andall_source_current_references_preserved=True, source_prose_orcompletion_credit_added=False,
            formatting_native_stored_actual_policy_atomic_andregistered_integration_pending=True)
        rows.append(row)
    assert len(rows) == 5 and Counter(r['decision'] for r in rows) == {'revision': 4, 'retention': 1}
    reasons = {
        1: 'Retain the approved Hodram and Joakim, with the established Bergstrom. The clean given, middle and surname fields and distinct progressive/full getters preserve Hodram Bergstrom and Hodram Joakim Bergstrom. No rank, biography or relationship is added.',
        16: 'Retain Gerhard Adernkatz. The clean ゲルハルト/アーデルンカッツ identity and prior registered surname correction are explicitly bound to the actual current field. Both current getters and the complete style11 header use Adernkatz; historical Ardelknatts fields remain as historical evidence, not a second current spelling.',
        18: 'Retain Charles Rochefort and the full-catalogue Charles Jean Rochefort. These are the established natural English spellings of シャルル/ロシュフォール with middle ジャン. The source selector12 resolves this actor, not another crew member. No nobility, rank, nationality or relationship is inferred from the name.',
        113: 'Retain Port Worker for this exchange. 出港所の兄貴 supplies a familiar male port/departure-office role, not proof of literal brotherhood. Port Worker is a natural occupational label for the gruff adviser here and avoids inventing a family relationship or official rank. The Europe surname-table metadata is not spoken and is not part of either current getter. This scoped retention does not complete the wider seven-context role review or the full207-name review.',
    }
    names = []
    for binding in display['scoped_clean_current_four_names_andreused_native_consumers']:
        actor = binding['actor_ID']
        names.append(dict(actor_ID=actor, speaker=speaker_names[actor], decision='retention', context=CONTEXT,
            localization_note=reasons[actor], retention_reason=reasons[actor], exact_source_current_native_binding=binding,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
            complete_native_nameplanes_directly_viewed=True, no_new_name_asset_orall207_credit=True,
            native_consumers_reused_only_through_exact_complete_current_code_COMMON_font_andwholeactors=True,
            not_actual_B51_header_capture_orcustom_player_name_coverage=True))
    save(NAMES, dict(format='dk4-speaker-name-review-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=names, scoped_actor_IDs=[1, 16, 18, 113], source_display=str(DISPLAY), source_display_sha256=sha(DISPLAY.read_bytes()),
        no_new_name_asset_orall207_name_review_credit=True, wider_Port_Worker_contexts_remain_open=True, new_credit=0, full_goal_complete=False))
    doc = dict(format='dk4-script-batch-v1', translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], file_path='/data/SC1.DK4', route=1, route_identity='Hodram', blocks=[51],
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'], current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'], current_archive_sha256=current['current_archive_sha256'],
        records=rows, revised=4, retained=1, total_editorial_objects=5, physical_speech_objects=5, typed_choice_objects=0,
        names_packet=str(NAMES), names_packet_sha256=sha(NAMES.read_bytes()), source_context=str(GLOSS), source_context_sha256=sha(GLOSS.read_bytes()),
        current_packet=str(CURRENT), current_packet_sha256=sha(CURRENT.read_bytes()), source_result_flow=str(FLOW), source_result_flow_sha256=sha(FLOW.read_bytes()),
        approved_region_term=dict(path=str(TERM), sha256=sha(TERM.read_bytes()), record_ID=termrow['id'], source_reference=termrow['source_reference'],
            source_Japanese=termrow['source_Japanese'], reviewed_English=termrow['english'], term='southern Mediterranean'),
        source_macro_counts=dict(FI=0, FA=0, FO=0), source_FE_panels=0, all_five_clean_first_glosses_precede_current_English=True,
        whole_exchange_conditional_context_andemotional_progression_reviewed=True, all_five_four_prose_gates_true_formatting_false=True,
        ordinary_wrapping_owned_by_formatter=True, no_new_ROM_orregistered_stage_orcompletion_credit=True, new_credit=0, full_goal_complete=False)
    save(DOC, doc)
    ROOT.mkdir(parents=True)
    save(ROOT / 'contextual_review.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), names=str(NAMES), names_sha256=sha(NAMES.read_bytes()),
        records=[dict(id=r['id'], source_reference=r['source_reference'], current_reference=r['current_reference'], source_hex=r['source_hex'],
            current_hex=r['current_hex'], prior=r['effective_predecessor_paragraph'], english=r['english'], decision=r['decision'], finding=r['finding'],
            reason=r['localization_note']) for r in rows], revised=4, retained=1, scoped_name_retentions=4,
        source_first_whole_exchange_prose_review_only=True, all_formatting_gates_false_until_native_fullwidth_completeglyph_bounds_pagination_stored_andactual_checks=True,
        formal_profile_policy_atomic_andregistered_work_pending=True, no_credit=True, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [CURRENT, GLOSS, DISPLAY, VIEW, FLOW, TERM, DOC, NAMES, Path(__file__)]}))
    for row in rows:
        print(row['id'], row['decision'], repr(row['english']))
    print('B51 whole exchange: four revisions, one individually justified retention and four scoped name retentions. Formatting, actual, policy and registered integration remain pending; zero completion credit.')
