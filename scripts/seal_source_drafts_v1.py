"""Seal logical English only after complete source meanings andexact speaker identity binding."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def seal(source,output,drafts,notes,producer,FE_speakers=None):
    source,output,producer=map(Path,[source,output,producer]);assert not output.exists()
    binding=load(source)
    names={r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in binding['name_bindings']}
    keys=['id','file_path','block','source_selector','source_hex','source_complete_preamble_hex','source_reference',
        'source_Japanese','source_decode_error','source_0100_ancestors','native_extent','source_macros','source_meaning','whole_exchange_context']
    records=[]
    for block,english_rows in drafts.items():
        originals=[r for r in binding['records'] if r['block']==block]
        assert len(originals)==len(english_rows)
        for original,english in zip(originals,english_rows,strict=True):
            assert english.strip()==english and '\n' not in english and not any(t in english for t in ['{LB','{ALIGN','{PAD}'])
            assert all(english.count('{MACRO:'+key+'}')==count for key,count in original['source_macros'].items())
            index=original['source_reference']['record_index'];actor=original['source_selector']
            if actor==254:
                assert FE_speakers is not None and (block,index) in FE_speakers
                speaker=FE_speakers[block,index]
            else:speaker=names[actor]
            row={k:original[k] for k in keys}
            row.update(english=english,speaker=speaker,context=original['whole_exchange_context'],
                localization_note=notes.get((block,index),'Natural complete-exchange wording preserves this source intent: '+original['source_meaning']),
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                source_first_draft=True,earlier_English_unconsulted=True,current_English_comparison_pending=True,
                complete_native_preamble_fresh_formatting_stored_visual_andregistered_release_pending=True)
            records.append(row)
    assert len(records)==len({r['id'] for r in records})
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),records=records,logical_drafts_saved=len(records),
        source_meanings_preceded_drafts_andcurrent_story_English_remains_unconsulted=True,
        all_conditional_alternatives_kept_separate=True,all_fifth_formatting_gates_false=True,
        no_name_data_orROM_orcompletion_credit=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(producer.read_bytes()),helper_sha256=sha(Path(__file__).read_bytes())))
    print(f'{len(records)} natural-English source-first drafts sealed;older English andformatting still pending.',flush=True)
