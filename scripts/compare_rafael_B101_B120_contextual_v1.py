"""Seal241 individual contextual decisions, leaving concrete identity/term andfresh display holds."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from translations.rafael_B101_B120_contextual_decisions_v1 import RETAIN, OVERRIDES, FINDINGS, CHOICE_RETAIN, PUNCTUATION_RETENTIONS

ROOT = Path('work/analysis/Rafael_B101_B120_current678_20261105')
SEALED = Path('work/analysis/Rafael_B101_B120_clean_20261105/sealed241_v1/all_source_meanings_andindependent_drafts.json')
OUT = Path('translations/rafael_B101_B120_contextual_prose_review_v1.json')
SPEAKERS = {0:'Rafael',4:'Janus',5:'Claudio',6:'Julio',8:'Arcadius (current native binding pending)',12:'Yukihisa',14:'Emilio',
    22:'Samwell (current native binding pending)',75:'Hans (current native binding pending)',135:'Temple guardian (public label pending)',
    137:'Monk (public label pending)',139:'Priest (current native binding pending)',151:'Sailor',160:'Villager (public label pending)',
    177:'Sect leader (public label pending)',178:'Followers (public label pending)',188:'Margrete (current native binding pending)',
    191:'Donna (current native binding pending)',207:'Dynamically selected speaker; native context binding pending',254:'FE presenter/system panel'}
TERMS = {'ミネルヴァの盾':'Minerva shield item title', '孔雀かたびら':'Peacock Mail item title',
    'ジャガー神の宿る胴着':'jaguar-god garment item title', 'アリスタルコスの望遠鏡':'Aristarchus telescope item title',
    'ヘスティア':'Hestia cauldron item title', '村正':'Muramasa item title', '古代巨石文明研究会':'research society title',
    'スールヤバルマン':'Suryavarman name', 'ヴィシュヌ':'Vishnu name', 'ヴェーダ':'Vedas term'}
UNBOUND_ACTORS = {8,22,75,135,137,139,160,177,178,188,191,207}


def main():
    assert not OUT.exists()
    current, findings, sealed = map(load, [ROOT/'current_effective.json', ROOT/'current_choice_andglyph_findings_v1.json', SEALED])
    assert sealed['source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake']
    assert (sealed['source_speech_drafts'], sealed['source_caption_drafts']) == (229,12)
    rows, holds, glyph_changes = [], [], []
    for group in current['groups']:
        for original in group['records']:
            row = deepcopy(original)
            key = row['block'],row['source_reference']['record_index']
            old = row['current_comparison_paragraph']
            retained = key[1] in RETAIN.get(key[0],{})
            normalizations = PUNCTUATION_RETENTIONS.get(key,{})
            logical = old
            for before,after in normalizations.items():
                assert before in logical
                logical = logical.replace(before,after)
            english = logical if retained else OVERRIDES.get(key,row['independent_English_draft'])
            assert key in FINDINGS if not retained else key not in FINDINGS
            reason = RETAIN[key[0]][key[1]] if retained else FINDINGS[key]
            pending = []
            if row['source_selector'] in UNBOUND_ACTORS:
                pending.append('Bind/review source andcurrent public identity/consumer for selector'+str(row['source_selector'])+'.')
            pending.extend('Bind established '+label+'.' for source,label in TERMS.items() if source in row['source_Japanese'])
            if row['source_selector'] == 207:
                pending.append('Preserve runtime-selected identity; do not index207 as a static actor-table row.')
            assert english.isascii() and english.strip() == english and not any(c in english for c in '\r\n\t')
            assert not any(t in english for t in ['{LB','{ALIGN','{PAD}'])
            assert all(english.count('{MACRO:'+m+'}') == n for m,n in row['source_macros'].items())
            row.update(english=english, decision='retention' if retained else 'revision', finding=reason,
                retention_reason=reason if retained else None, localization_note=reason, speaker=SPEAKERS[row['source_selector']],
                current_English=row['current_effective_text'], current_normalized_logical_English=logical,
                documented_punctuation_normalizations=normalizations,
                wording_retention_doesnot_approve_old_encoded_bytes=retained,
                current_English_comparison_pending=False, current_name_andterm_bindings_pending=pending,
                native_name_controls_andfresh_formatting_pending=True,
                review=dict(source=True,context=True,localization=not pending,naturalness=True,formatting=False), new_credit=0)
            if normalizations:
                glyph_changes.append(dict(id=row['id'],changes=normalizations,wording_retained=True,consumer_andpixels_still_pending=True))
            if pending:
                holds.append(dict(id=row['id'],reasons=pending))
            rows.append(row)
    assert len(rows) == 229 and sum(r['decision']=='retention' for r in rows)==108
    for original in findings['choices']:
        row = deepcopy(original)
        key = row['block'],row['source_command_offset'],row['source_index']
        old = ' '.join(row['current_English'].split())
        retained = key in CHOICE_RETAIN
        reason = CHOICE_RETAIN[key] if retained else {
            (114,296,0):'Make the knowledge answer a natural first-person response to the riddle, not clipped Know it.',
            (114,296,1):'Use a natural complete negative knowledge answer, consistent with the neighboring first-person answer.',
            (114,296,2):'Restore the complete denial that such an animal exists; No beast reads like a truncated label.',
            (114,534,1):'Keep the addressee and explicit Sphinx identification in natural English; preserve choice index1.',
            (114,534,2):'Something else is a natural alternative answer rather than the bare category Other.',
            (118,370,0):'Spell out second for a readable riddle answer; preserve the exact one-second value.',
            (118,370,1):'Spell out seconds while preserving the exact thirty-second wrong-answer alternative.',
            (118,370,2):'Spell out seconds while preserving the exact fifty-nine-second correct-answer alternative.',
            (119,336,1):'Specify the action of turning right so the caption does not look like a direction-only prompt.',
            (119,336,2):'Specify the action of turning left and preserve its distinct menu index.'
        }[key]
        english = old if retained else row['independent_English_draft']
        row.update(english=english, decision='retention' if retained else 'revision', finding=reason, localization_note=reason,
            retention_reason=reason if retained else None, current_normalized_logical_English=old,
            speaker='Player choice', current_English_comparison_pending=False,
            current_name_andterm_bindings_pending=[], native_complete_choice_object_binding_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False), new_credit=0)
        rows.append(row)
    assert len(rows)==241 and {r['id'] for r in rows}=={r['id'] for r in sealed['records']}
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(131,110)
    evidence=[SEALED,ROOT/'current_effective.json',ROOT/'current_choice_andglyph_findings_v1.json',
        Path('translations/rafael_B101_B120_contextual_decisions_v1.py'),Path(__file__)]
    save(OUT,dict(format='dk4-editorial-contextual-prose-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',file_path=current['file_path'],blocks=list(range(101,121)),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        source_speeches=229,source_choice_labels=12,contextual_comparisons=241,proposed_revisions=131,justified_retentions=110,
        four_gate_passes=sum(all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in rows),
        pending_name_term_IDs=holds,wording_retentions_with_scoped_punctuation_changes=glyph_changes,
        current_non_ASCII_findings=findings['current_non_ASCII_findings'],
        whole_exchange_reviewed_before_choosing_retention_orrevision=True,
        source_drafts_preceded_current_story_English_extraction_in_this_intake=True,no_blanket_historical_exposure_claim=True,
        all_fifth_formatting_gates_pending=True,all_native_visual_stored_gameplay_andregistered_integration_pending=True,
        no_static_actor207_identity_inferred=True,no_global_name_approval=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in evidence}))
    print(dict(compared=241,revisions=131,retentions=110,name_term_holds=len(holds),
        four_gate_passes=sum(all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in rows),formatting_approved=0,new_credit=0))


if __name__ == '__main__':
    main()
