"""Join source-first drafts to exact current native records and explicit whole-exchange decisions."""
import argparse
import re
import unicodedata
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def paragraph(text):
    value = ' '.join(unicodedata.normalize('NFKC', text).split())
    return re.sub(r'(?<![A-Za-z])(FI|FA|FO)(?![A-Za-z])', lambda m:'{MACRO:'+m[1]+'}', value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['drafts','current','objects','decisions','out']:
        parser.add_argument('--'+key,type=Path,required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    drafts, current, objects, decisions = [load(p) for p in [args.drafts,args.current,args.objects,args.decisions]]
    assert drafts['all642_drafts_saved_before_current_ROM_dialogue_extraction']
    source = {r['id']:r for r in drafts['records']}
    native_rows = [r for g in current['groups'] for r in g['records']] + objects['choice_records']
    native = {r['id']:r for r in native_rows}
    assert len(source) == len(native) == 642 and set(source) == set(native)
    assert current['current_ROM_sha256'] == objects['current_ROM_sha256']
    selected = {r[0]:r for r in decisions['records']}
    assert len(selected) == len(decisions['records'])
    blocks = {source[ident]['block'] for ident in selected}
    assert set(selected) == {r['id'] for r in drafts['records'] if r['block'] in blocks}
    rows = []
    for draft in drafts['records']:
        row = deepcopy(draft)
        ident = row['id']
        bound = native[ident]
        assert bound['source_hex'] == row['source_hex'] and bound['source_reference'] == row['source_reference']
        for key,value in bound.items():
            if key.startswith('current_') or key in ['selected_native_pointer','earlier_English_unconsulted','native_choice_provider_not_run_as_message_catalogue']:
                row[key] = value
        row['current_reference_pending'] = False
        row['current_English_comparison_pending'] = ident not in selected
        row['source_first_draft_reference'] = dict(path=str(args.drafts),sha256=sha(args.drafts.read_bytes()),id=ident)
        row['current_ROM'] = current['current_ROM']
        row['current_ROM_sha256'] = current['current_ROM_sha256']
        row['prior_macro_normalized_comparison'] = prior = paragraph(bound['current_comparison_paragraph'])
        row['source_meaning_anddraft_preceded_current_ROM_comparison'] = True
        row['kind'] = 'typed-choice-label' if row.get('kind') == 'typed-choice-label' else ('system-panel' if row['source_selector'] == 254 else 'progressive')
        row['prose_comparison_review'] = dict(source=False,context=False,localization=False,naturalness=False)
        if ident in selected:
            decision = selected[ident]
            assert len(decision) in [3,4] and decision[1] in ['revision','retention'] and decision[2].strip()
            row['decision'], row['finding'] = decision[1:3]
            if row['decision'] == 'retention':
                assert prior.encode('cp932').decode('cp932') == prior
                row['english'] = row['logical_English'] = prior
                row['retention_reason'] = decision[2]
            else:
                assert row['english'] != prior
                row['retention_reason'] = None
            row['localization_note'] = decision[2]
            row['whole_clean_exchange_cadence_andemotional_progression_reread'] = True
            row['prose_comparison_review'] = dict(source=True,context=True,localization=True,naturalness=True)
            if len(decision) == 4:
                assert decision[3] == 'place-name-localization-open'
                row['review']['localization'] = row['prose_comparison_review']['localization'] = False
                row['open_localization_question'] = dict(source='アブハーズ',current_dialogue='Abkhaz',current_native_city_UI='Abhaz',
                    source_supported_cross_consumer_decision_andscope_pending=True,not_automatically_choose_legacy_UI_for_compatibility=True)
            if row['decision'] == 'retention':
                assert row['logical_English'] == prior
                row['retained_wording_reformatted_fresh_later'] = True
        else:
            row['decision'] = 'pending-current-comparison'
        row['review']['formatting'] = False
        row['new_credit'] = 0
        rows.append(row)
    compared = [r for r in rows if r['id'] in selected]
    save(args.out,dict(format='dk4-contextual-editorial-prose-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
                       review_gates=['source','context','localization','naturalness','formatting'],
                       file_path=current['file_path'],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
                       current_archive_sha256=current['current_archive_sha256'],blocks=drafts['blocks'],records=rows,
                       complete_comparison_blocks=sorted(blocks),current_comparisons=len(compared),remaining_current_comparisons=len(rows)-len(compared),
                       proposed_revisions=sum(r['decision']=='revision' for r in compared),
                       wording_retentions=sum(r['decision']=='retention' for r in compared),
                       complete_four_gate_comparisons=sum(all(r['prose_comparison_review'].values()) for r in compared),
                       place_name_questions=sum('open_localization_question' in r for r in rows),
                       formatting_andvisual_stored_gameplay_integration_still_pending=True,
                       source_andcurrent_exact_reference_bindings=642,new_credit=0,new_ROMs=0,full_goal_complete=False,
                       evidence={str(p):sha(p.read_bytes()) for p in [args.drafts,args.current,args.objects,args.decisions,Path(__file__)]}))
    print(dict(exact_current_bindings=len(rows),comparisons=len(compared),revisions=sum(r['decision']=='revision' for r in compared),
               retentions=sum(r['decision']=='retention' for r in compared),complete_four_gate_comparisons=sum(all(r['prose_comparison_review'].values()) for r in compared),
               open_place_name_records=sum('open_localization_question' in r for r in rows),new_credit=0))


if __name__ == '__main__':
    main()
