"""Seal 277 clean-source drafts, retaining all 114 earlier ordinary drafts exactly."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/analysis/Hodram_B211_B230_clean_20261104')
OUT=ROOT/'complete_clean_English_drafts_v1.json'
STYLES=ROOT/'all29_clean_style_drafts_v1.json'
CAPTIONS=ROOT/'all7_clean_caption_drafts_v1.json'

def main():
    assert not any(p.exists() for p in (OUT,STYLES,CAPTIONS))
    means_path=ROOT/'complete_clean_meanings_before_English.json';means=load(means_path)
    parts=[ROOT/(name+'_clean_English_drafts_v1.json') for name in
        ['B211_B215_64','B216_B220_50','B221_B225_60','B226_B230_67']]
    ordinary=[row for path in parts for row in load(path)['records']]
    assert len(ordinary)==len({r['id'] for r in ordinary})==241
    arrivals={
        0:('Admiral, a letter from {name} has arrived.','Conversational report of arrival, with the source author retained.'),
        1:('Admiral, we have received correspondence from {name}.','Formal correspondence preserves the more formal source register.'),
        2:("Admiral, you've got a letter from {name}.",'Slightly casual report; the shared physical alternative preserves both personality aliases.'),
        3:("There's a letter for you from {name}, Admiral.",'Gentle, polite delivery without translating an honorific into a relationship.'),
        4:('Got a letter from {name} for you, Admiral.','A clipped familiar report reflects the rougher source ending without inventing rudeness.'),
        5:("Admiral, there's a letter here from {name}.",'An older voice remains straightforward and familiar, without forced archaic English.'),
        6:('Admiral! A letter from {name}!','Simple excited address preserves the youthful register without baby talk.'),
    }
    reactions=[
        ("That's some complicated wording. Just like Yukihisa.",'Conversational reaction to difficult wording, not illegible handwriting.'),
        ('Quite difficult prose. Typical of Yukihisa.','The formal, restrained appraisal preserves characteristic authorial style.'),
        ("That's complicated, isn't it? Just like Yukihisa.",'A casual shared observation preserves the familiar register.'),
        ("It's rather complicated, isn't it? So like Yukihisa.",'A gentle observation preserves the source voice without inventing intimacy.'),
        ("That's some awfully fancy writing. Just like Yukihisa.",'Rougher skepticism reflects the affected complexity implied by the source.'),
        ('Difficult prose, that. Just like Yukihisa.','An older familiar voice comments on the prose without a new factual judgment.'),
        ("It's too hard. I can't understand what it says.",'This alternative cannot understand the content and does not identify Yukihisa; preserve that distinct reaction.'),
        ('Such difficult prose. Ah, so very like Yukihisa.','Expansive adult delivery retains the stronger source emphasis.'),
    ]
    styles=[];captions=[]
    for original in means['records']:
        if 'source_style_indices' in original:
            indices=original['source_style_indices']
            if original['block']==213 and original['source_command_offset']==702:
                assert len(indices)==1
                english,note=reactions[indices[0]]
            else:
                assert original['source_command_offset']==8 and indices in [[0],[1],[2,7],[3],[4],[5],[6]]
                name={213:'Yukihisa',218:'Janus',226:'Ian'}[original['block']]
                template,note=arrivals[indices[0]];english=template.format(name=name)
                if name=='Janus':note+=' Use the existing Janus Pasar name consistently with the bound getter and signed letter.'
            row=dict(original);row.update(english=english,logical_English=english,
                speaker='Runtime-selected companion',context=original['exchange_context'],localization_note=note,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                complete_clean_exchange_andemotional_progression_reviewed=True,current_reference_pending=True,
                current_ROM_English_conversation_comparison_pending=True,
                no_authored_ordinary_breaks_alignment_orpadding=True,new_credit=0)
            styles.append(row)
        elif 'source_index' in original:
            b,at,index=original['block'],original['source_command_offset'],original['source_index']
            if b==216 and at==64:
                english=['Yes','No'][index];note='Answer whether Romance of the Three Kingdoms is familiar; preserve the separate knowledge branches.'
            elif b==216:
                assert at==230
                english=['Zhao Yun','Guan Yu','Zhuge Liang'][index]
                note='Choose the named commander; retain the source menu identity and the matching Zhao Yun branch. Kongming in the following prose is the same Zhuge Liang, not another option.'
            else:
                assert (b,at)==(224,138)
                english=['I have','I haven\'t'][index];note='Answer whether the Crusades are familiar; both distinct opening replies converge on the same debate.'
            row=dict(original);row.update(english=english,logical_English=english,kind='typed-choice-label',
                speaker='Player menu',context=original['exchange_context'],localization_note=note,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                complete_clean_exchange_andemotional_progression_reviewed=True,current_reference_pending=True,
                current_ROM_English_conversation_comparison_pending=True,
                no_authored_ordinary_breaks_alignment_orpadding=True,new_credit=0)
            captions.append(row)
    assert len(styles)==29 and sum(len(r['source_style_indices']) for r in styles)==32
    assert len(captions)==7 and len({(r['block'],r['source_command_offset']) for r in captions})==3
    rows=ordinary+styles+captions;source={r['id']:r for r in means['records']}
    assert len(rows)==len(source)==277 and {r['id'] for r in rows}==set(source)
    ledger=load('translations/editorial_review_current_v1.json')
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not keys & {(r['file_path'],r['id']) for r in rows}
    for row in rows:
        assert all(row[k]==source[row['id']][k] for k in ['source_reference','source_hex','source_Japanese','source_meaning'])
        assert row['english']==row['english'].strip() and not any(t in row['english'] for t in ['\n','{LB','{ALIGN','{PAD}','  '])
        row['english'].encode('cp932')
        raw=bytes.fromhex(row['source_hex'])
        assert all(row['english'].count('{MACRO:'+m+'}')==raw.count(m.encode('ascii')) for m in ['FI','FA','FO'])
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
    assert ordinary[:114]==[row for p in parts[:2] for row in load(p)['records']]
    save(STYLES,dict(records=styles,physical_alternatives=29,selector_slots=32,physical_objects=4,all_fifth_gates_pending=True,new_credit=0))
    save(CAPTIONS,dict(records=captions,complete_menus=3,all_fifth_gates_pending=True,new_credit=0))
    save(OUT,dict(format='dk4-source-first-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC1.DK4',blocks=list(range(211,231)),records=rows,
        ordinary_speeches=241,physical_style_alternatives=29,style_alias_slots=32,typed_captions=7,menu_objects=3,
        previous114_drafts_exactly_preserved=True,new_drafts=163,
        no_completed_source_key_overlap=True,complete_source_references_andmacro_counts_pass=True,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        no_blanket_before_any_historical_English_exposure_claim=True,
        individual_draft_prose_gates_not_final_existing_English_comparison=True,
        all_current_comparisons_andfresh_formatting_native_visual_storage_gameplay_release_pending=True,
        new_credit=0,new_ROMs=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [means_path,*parts,STYLES,CAPTIONS,Path(__file__)]}))
    print('Sealed 277 source-bound drafts: 241 speeches, 29 physical styles and seven captions; all earlier 114 drafts exact.')

if __name__=='__main__':main()
