"""Combine306 individual prose decisions; formatting andname-glyph work remain open."""
from copy import deepcopy
from pathlib import Path
import re
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

CURRENT=Path('work/analysis/Hodram_B81_B90_current_20261101/current_effective.json')
CHOICES=Path('work/analysis/Hodram_B81_B90_clean_20261101/B87_two_clean_choice_meanings_before_English.json')
PARTS=[Path('translations/'+name) for name in ['hodram_B81_B85_editorial_prose_v2.json',
    'hodram_B86_editorial_prose_v1.json','hodram_B87_B89_editorial_prose_v1.json']]
OUT=Path('translations/hodram_B81_B89_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not OUT.exists();current=load(CURRENT);sources=load(CHOICES)
    parts=[load(path) for path in PARTS]
    rows=[deepcopy(row) for part in parts for row in part['records']]
    assert len(rows)==len({r['id'] for r in rows})==304
    group=next(g for g in current['groups'] if g['block']==87)
    command=next(c for c in group['all_current_commands'] if c['word']==0x2100)
    raw=bytes.fromhex(command['whole_command_hex']);offsets=struct.unpack_from('<2H',raw,2)
    assert struct.unpack_from('<H',raw)[0]==0x2100 and len(offsets)==2
    for index,source in enumerate(sources['records']):
        at=6+offsets[index];end=raw.index(0,at);body=raw[at:end]
        prior=' '.join(body.decode('cp932').split())
        english=['Agreed.',"I don't have that much money."][index]
        note=[
            'Retain the natural, concise agreement to the requested gift of1000gold. Remove only compiler-owned alignment padding; preserve source option0.',
            'Restore the stated inability to supply that sum, not a claim of having zero money. Preserve source option1 andleave affordability/branch eligibility to the unchanged game logic.'][index]
        row=deepcopy(source)
        row.update(kind='typed-choice-label',source_record_index=None,
            source_reference=dict(file_path=source['file_path'],block=87,command_offset=302,
                source_index=index,offset=source['source_byte_offset'],length=len(bytes.fromhex(source['source_hex']))),
            current_reference=dict(file_path=source['file_path'],block=87,command_offset=command['offset'],
                source_index=index,offset=command['offset']+at,length=len(body)),
            current_hex=body.hex(),current_choice_object_hex=raw.hex(),source_choice_object_hex=sources['choice_command']['source_hex'],
            prior_macro_normalized_comparison=prior,current_raw_storage_English=body.decode('cp932'),
            english=english,logical_English=english,speaker='Player',
            source_meaning=source['source_meaning_gloss'],source_macros=dict(FI=0,FA=0,FO=0),
            context='B87: Janus asks for1000gold;the player agrees ordeclines for lack of that sum. The acceptance andrefusal paths remain distinct.',
            localization_note=note,finding=note,decision='retention' if english==prior else 'revision',
            retention_reason=note if english==prior else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            earlier_English_unconsulted=False,all_five_review_gates_pending=False,
            typed_native_caption_provider_layout_andcontroller_verification_pending=True,new_credit=0)
        rows.append(row)
    contexts={key:value for part in parts for key,value in part['complete_exchange_contexts'].items()}
    for row in rows:
        # Correct joined words in audit notes only; product prose is never
        # automatically rewritten by this metadata cleanup.
        for key in ['context','localization_note','finding','retention_reason']:
            if isinstance(row.get(key),str):row[key]=re.sub(r'\band(?=[A-Za-z])','and ',row[key])
        assert not re.search(r'\band[A-Za-z]',row['english'],re.I),(row['id'],row['english'])
        assert not any(t in row['english'] for t in ['{LB','{PAD','{ALIGN','\n','  '])
        assert {key:row['english'].count('{MACRO:'+key+'}') for key in ['FI','FA','FO']}==row['source_macros']
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    assert len(rows)==306 and len({r['id'] for r in rows})==306
    doc=dict(format='dk4-complete-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],file_path=current['file_path'],
        blocks=list(range(81,90)),unchanged_control_only_reference_block=90,
        records=rows,total_editorial_objects=306,physical_speech_objects=304,typed_choice_objects=2,
        typed_choice_record_IDs=[r['id'] for r in rows if r['kind']=='typed-choice-label'],
        revised=sum(r['decision']=='revision' for r in rows),retained=sum(r['decision']=='retention' for r in rows),
        complete_exchange_contexts=contexts,
        source_macro_counts={key:sum(r['source_macros'][key] for r in rows) for key in ['FI','FA','FO']},
        source_FE_panels=sum(r.get('source_selector')==254 for r in rows),
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),
        first_part_records_reused_with_five_documented_draft_refinements=True,
        original_parts_all_product_English_source_current_refs_anddecisions_preserved=True,
        audit_note_spacing_only_normalized=True,ordinary_wrapping_owned_by_formatter=True,
        all_four_individual_prose_gates_passed=True,all_formatting_gates_false=True,
        scoped_names_review=dict(
            new_native_bindings='work/analysis/Hodram_B81_B90_new_names_20261101/names.json',
            six_known_identities_exact_reuse='work/analysis/Hodram_B81_B90_new_names_20261101/known_six_reuse.json',
            aliases_corrected_in_dialogue=['Christina -> Cristina','Miwoll Gentz -> Mivor Genz','Janus Pasha -> Janus Pasar'],
            retained_full_name='Yukihisa Genjo Shiraki,per glossary andclean/native full getter.',
            actual_kinship='Julio is Cristina\'s grandfather,explicitly confirmed in B85. Hodram andthe rescued child are not their relatives.',
            role_labels='Retain Shopkeeper/Patron/Trader/Port Worker/Guildmaster/Sailor/Boy/Lady within their source occupations orfunctions;Lady is a generic polite label,not an invented noble title.',
            Emilio_name_glyph='Emilio Ferog spelling retained. Progressive/full native name still contains wide F;normal-font metadata correction andnew display checks remain pending.',
            wider_full_catalogue_207_alias_andshared_de_findings_still_open=True),
        named_mentions=dict(Harald='Retain current spelling for sourceヘラルド in Julio\'s remark;do not substitute Gerhard oradd family biography.',
            Meihua='Retain current spelling of美華 as the intended gift recipient;no girlfriend ormarriage is established.',
            item='Golden Crown of Silla is the existing English title supported by新羅の金冠;no historical lore added.',
            proof='Proof of Conquest follows approved B59 usage;restore Indian Ocean,not unspecified eastern ocean.',
            menu='Refit is the registered shipyard heading for改造.'),
        prose_no_ROM_changes_ornew_completion_credit=True,new_credit=0,full_goal_complete=False,
        evidence={str(path):sha(path.read_bytes()) for path in [CURRENT,CHOICES,*PARTS,Path(__file__)]})
    save(OUT,doc)
    print(dict(records=306,speeches=304,choice_labels=2,revisions=doc['revised'],retentions=doc['retained'],
        macros=doc['source_macro_counts'],FE=doc['source_FE_panels'],formatting_approved=0,new_credit=0))
