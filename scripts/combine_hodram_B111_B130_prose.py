"""Bind all 323 decisions without granting formatting or completion credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

INPUTS=[Path('translations')/name for name in [
    'hodram_B111_B119_editorial_prose_v1.json',
    'hodram_B120_B130_editorial_prose_v1.json',
    'hodram_B111_B130_alternatives_prose_v1.json']]
OUT=Path('translations/hodram_B111_B130_editorial_manuscript_v1.json')

def main():
    assert not OUT.exists()
    docs=[load(p) for p in INPUTS]
    rows=[deepcopy(r) for d in docs for r in d['records']]
    assert len(rows)==len({r['id'] for r in rows})==323
    assert len({d['current_ROM_sha256'] for d in docs})==1
    source_scoped_revisions={
        (120,32):('Long ago, this country was invaded by the Yuan, said to be the largest empire in history.',
            'Use largest for 最大 rather than an ambiguous judgment of greatness; retain the monk\'s reported account.'),
        (126,10):('You found it, so you have the right to keep this knife.',
            'Preserve the source small-knife object without upgrading it to a different weapon class or importing a widget title.'),
        (126,26):('Then how about this? You take the knife, and we take all the pay for this job.',
            'Use the same knife term across the proposed exchange; the two parties and entire job payment remain explicit.'),
    }
    for row in rows:
        row['prose_decision_input']=next(str(p) for p,d in zip(INPUTS,docs) if any(r['id']==row['id'] for r in d['records']))
        key=(row['block'],row.get('source_record_index'))
        if key in source_scoped_revisions:
            english,note=source_scoped_revisions[key]
            row['previous_prose_preserved']=row['english']
            row['english']=row['logical_English']=english
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+english
            row['localization_note']+=' '+note
            row['finding']=row['localization_note']
            row['decision']='revision';row['retention_reason']=None
        if 'source_style_indices' in row:
            row['native_object_kind']='4100-style-alternative';row['kind']='progressive'
            row['source_record_index']=row['source_reference']['physical_record_index']
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']=True
        elif 'source_index' in row:
            row['native_object_kind']=row['kind'];row['kind']='typed-choice-label'
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    rows.sort(key=lambda r:(r['block'],r['source_reference']['offset'] if 'source_reference' in r else r['source_byte_offset']))
    assert sum(r['kind']=='typed-choice-label' for r in rows)==15
    assert sum(r.get('native_object_kind')=='4100-style-alternative' for r in rows)==48
    save(OUT,dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],
        current_ROM=docs[0]['current_ROM'],current_ROM_sha256=docs[0]['current_ROM_sha256'],
        current_archive_sha256=docs[0]['current_archive_sha256'],file_path='/data/SC1.DK4',
        blocks=list(range(111,131)),complete_exchange_contexts={k:v for d in docs for k,v in d['complete_exchange_contexts'].items()},
        records=rows,total_editorial_objects=323,ordinary_speech_objects=260,physical_speech_objects=308,
        personality_alternatives=48,personality_alias_slots=64,typed_choice_objects=15,typed_choice_commands=5,
        revised=sum(r['decision']=='revision' for r in rows),retained=sum(r['decision']=='retention' for r in rows),
        all_clean_meanings_precede_current_English=True,all_current_English_now_compared=True,
        all_four_individual_prose_gates_passed=True,all_formatting_gates_false=True,
        ordinary_wrapping_owned_by_formatter=True,native_style_aliases_andmenu_indices_preserved=True,
        names='work/analysis/Hodram_B111_B130_new_names_20261101/names.json',
        known_names='work/analysis/Hodram_B111_B130_clean_20261101/known_six_name_proof_reuse.json',
        dynamic_roles='work/analysis/Hodram_B111_B130_clean_20261101/current_all_six_dynamic_roles.json',
        pending_name_display_findings=['Follower178 wide F','Diogo43 full-name デ'],
        new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,Path(__file__)]}))
    print(OUT,323,'prose decisions',sum(r['decision']=='revision' for r in rows),'revisions',sum(r['decision']=='retention' for r in rows),'retentions; formatting pending.')

if __name__=='__main__':main()
