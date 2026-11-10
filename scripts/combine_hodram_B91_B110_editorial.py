"""Combine209 speech decisions andtwo typed belief answers; no formatting approval."""
from copy import deepcopy
from pathlib import Path
import re
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_two_choice_object_v1 import labels
from scripts.audit_story_glyph_consistency import load,save

CURRENT=Path('work/analysis/Hodram_B91_B110_current_20261101/current_effective.json')
PARTS=[Path('translations/hodram_B91_B97_editorial_prose_v1.json'),Path('translations/hodram_B100_B110_editorial_prose_v1.json')]
SOURCE_CHOICES=Path('work/analysis/Hodram_B91_B110_clean_20261101/B91_two_clean_choice_meanings_before_English.json')
OUT=Path('translations/hodram_B91_B110_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not OUT.exists();current=load(CURRENT);parts=[load(p) for p in PARTS]
    rows=[deepcopy(r) for part in parts for r in part['records']];assert len(rows)==209
    refinements=[]
    for row in rows:
        proposed=None
        if row['id']=='DK4_MES_B95_R0005':
            assert row['english']=='! This place...';proposed='Ah! This place...'
            reason='Use a natural English interjection for the sudden recognition instead of an isolated Japanese-style exclamation mark.'
        elif row['id']=='DK4_MES_B97_R0027':
            assert row['english']=='Never. A shinobi whose true identity is discovered must die. Such is their code...'
            proposed='Never. A ninja whose true identity is discovered must die. Such is their code...'
            reason='Use the already explained ninja term instead of adding the unnecessary synonym shinobi;the corrected subject of the death rule is unchanged.'
        if proposed is not None:
            refinements.append(dict(id=row['id'],before=row['english'],after=proposed,reason=reason))
            row.update(english=proposed,logical_English=proposed,planned_English_markup=row['planned_English_markup'].split('}',1)[0]+'}'+proposed)
            row['localization_note']+=' '+reason;row['finding']+=' '+reason
    original=load(SOURCE_CHOICES);group=current['groups'][0]
    command=next(c for c in group['all_current_commands'] if c['word']==0x2100)
    raw=bytes.fromhex(command['whole_command_hex']);offsets=struct.unpack_from('<2H',raw,2)
    assert group['block']==91 and command['offset']==112 and len(raw)==24 and offsets==(0,8)
    for i,source in enumerate(original['records']):
        at=6+offsets[i];body=labels(raw)[i];prior=' '.join(body.decode('cp932').split())
        english=['I do.',"I don't."][i]
        note=['Answer the question about believing in miracles,not a generic instruction to trust the stranger. Preserve option0.',
            'Decline belief in miracles,not a claim that the man is untrustworthy. Preserve option1 andthe separate refusal/stat branch.'][i]
        row=deepcopy(source);row.update(kind='typed-choice-label',source_record_index=None,
            source_reference=dict(file_path=source['file_path'],block=91,command_offset=112,source_index=i,offset=source['source_byte_offset'],length=len(bytes.fromhex(source['source_hex']))),
            current_reference=dict(file_path=source['file_path'],block=91,command_offset=112,source_index=i,offset=112+at,length=len(body)),
            current_hex=body.hex(),current_choice_object_hex=raw.hex(),source_choice_object_hex=original['choice_command']['source_hex'],
            prior_macro_normalized_comparison=prior,current_raw_storage_English=body.decode('cp932'),english=english,logical_English=english,
            speaker='Player',source_meaning=source['source_meaning_gloss'],source_macros=dict(FI=0,FA=0,FO=0),
            context='B91: the Sailor asks whether the captain believes in miracles;the two answers preserve their original source indices anddistinct branches.',
            localization_note=note,finding=note,decision='revision',retention_reason=None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),earlier_English_unconsulted=False,
            typed_native_caption_provider_layout_andcontroller_verification_pending=True,new_credit=0)
        rows.append(row)
    assert len(rows)==len({r['id'] for r in rows})==211
    for row in rows:
        assert all(32<=ord(c)<127 for c in row['english']),row['id']
        assert not any(s in row['english'] for s in ['{LB','{PAD','{ALIGN','\n','  '])
        assert not re.search(r'\band[A-Za-z]',row['english']),row['id']
        assert {key:row['english'].count('{MACRO:'+key+'}') for key in ['FI','FA','FO']}==row['source_macros']
    contexts={key:value for part in parts for key,value in part['complete_exchange_contexts'].items()}
    doc=dict(format='dk4-complete-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],file_path=current['file_path'],blocks=[g['block'] for g in current['groups'] if g['records']],
        unchanged_control_only_reference_blocks=[94,96,98,99,106,107],records=rows,total_editorial_objects=211,physical_speech_objects=209,typed_choice_objects=2,
        typed_choice_record_IDs=[r['id'] for r in rows if r['kind']=='typed-choice-label'],revised=sum(r['decision']=='revision' for r in rows),
        retained=sum(r['decision']=='retention' for r in rows),complete_exchange_contexts=contexts,source_macro_counts=dict(FI=2,FA=0,FO=0),source_FE_panels=7,
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),post_prose_refinements=refinements,
        all_four_individual_prose_gates_passed=True,all_formatting_gates_false=True,ordinary_wrapping_owned_by_formatter=True,
        new_name_bindings='work/analysis/Hodram_B91_B110_new_names_20261101/names.json',
        known_name_reuse='work/analysis/Hodram_B91_B110_clean_20261101/known_name_proof_reuse.json',
        dynamic_CF='work/analysis/Hodram_B91_B110_clean_20261101/current_CF_role0_binding.json',
        Spirit_label_precedent='translations/confirmed_name_editorial_v289.json:DK4_MES_B91_R0109',
        pending_name_display_findings=['Fernando wide-F native name.','Samwell full-name Japanese middle componentダ.'],
        source_current_references_findings_andjustified_retentions_individual=True,no_ROM_ornew_completion_credit=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE_CHOICES,*PARTS,Path(__file__)]})
    assert doc['revised']==129 and doc['retained']==82;save(OUT,doc)
    print(dict(objects=211,speeches=209,typed_labels=2,revisions=129,retentions=82,formatting_approved=0,new_credit=0))
