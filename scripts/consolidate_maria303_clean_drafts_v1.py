"""Bind303 source-first meanings/drafts andnative source controls without current-English intake."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.meaning_maria_B58_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

SPEAKERS={3:'Maria Huamei Li',4:'Janus Pasar',7:'Cristina Erneco',10:'Xien Yan',12:'Yukihisa Shiraki',
    14:'Emilio Ferog',15:'Angelo Puccini',16:'Gerhard Adernkatz',18:'Charles Jean Rochefort',
    20:'Fernando Dias',26:'Julian Lopez',74:'Richard Townsend',79:'Mivor Genz',82:'Shopkeeper',
    108:'Trade house trader',109:'Shipyard man',152:'Unnamed former sailor',162:'Boy',167:"Boy's mother"}

def main():
    out=ROOT/'all303_clean_meanings_andindependent_drafts_v1.json';assert not out.exists()
    source_path=ROOT/'clean_source_packet.json';packet=load(source_path)
    paths=[ROOT/'B58_independent_drafts_v2.json',ROOT/'B59_B61_independent_drafts_v1.json',ROOT/'B62_B70_independent_drafts_v1.json']
    drafts=[load(p) for p in paths];byid={r['id']:r for d in drafts for r in d['records']}
    assert len(byid)==sum(d['source_objects'] for d in drafts)==packet['records']==303
    assert all(d['current_English_not_consulted'] and d['all_five_review_gates_pending'] for d in drafts)
    image=NdsImage.open(packet['source_ROM']);assert digest(packet['source_ROM'])==packet['source_ROM_sha256']
    bank=IlnkContainer.parse(image.read_file(packet['file_path'])).blocks
    rows=[];counts={k:0 for k in ['FI','FA','FO','FU']};ordinary=FE=choices=0
    for group in packet['groups']:
        block=bank[group['block']];assert block.hex()==group['clean_block_hex']
        commands={c['offset']:c for c in group['all_source_commands']}
        for source in group['records']:
            row=deepcopy(byid[source['id']]);raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
            assert all(row[k]==source[k] for k in ['source_reference','source_hex','source_Japanese'])
            assert block[at:at+len(raw)]==raw and not row['covered'] and not row['exact_credited_source_bindings']
            assert row['source_meaning'] and row['independent_clean_first_draft'] and row['source_meaning_reviewed_from_complete_clean_exchange']
            assert row['review']==dict(source=False,context=False,localization=False,naturalness=False,formatting=False)
            row.update(source_object_kind=source['kind'],context=row['whole_exchange_context'],
                source_current_comparison_pending=True,names_terms_consumers_andfresh_display_approval_pending=True,
                independent_draft_precedes_current_English_intake=True,no_new_completion_credit=True,new_credit=0)
            if source['kind']=='ordinary-speech':
                ordinary+=1;prefix=raw[0];command=commands[row['source_reference']['command_offset']]
                assert command['word']==0x4000 and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
                assert raw[1:].decode('cp932')==row['source_Japanese']
                row.update(source_word=command['word'],source_command_offset=command['offset'],
                    source_0100_ancestors=command['ancestor_0100_offsets'],source_native_extent=command['native_extent'],
                    kind='system-FE' if prefix==254 else 'progressive')
                if prefix==254:
                    FE+=1
                    row['speaker']=('Boy, explicit unseen voice' if row['block']==58 else
                        'Knocking sound' if row['block']==59 else 'System instruction' if row['block']==60 else
                        'System result message' if row['block']==64 else 'Animal cry')
                    row['FE_not_resolved_as_actor254_oran_invented_portrait']=True
                else:
                    assert prefix in SPEAKERS;row['speaker']=SPEAKERS[prefix]
                row['source_macros']={k:raw[1:].count(k.encode()) for k in counts}
            else:
                choices+=1;row.update(kind='typed-choice-label',speaker='Player choice (Maria)',source_macros={k:0 for k in counts})
            for token,number in row['source_macros'].items():
                assert row['english'].count(token)==number,(row['id'],token)
                counts[token]+=number
            row['english'].encode('ascii')
            rows.append(row)
    assert len(rows)==303 and ordinary==299 and choices==4 and {r['id'] for r in rows}==set(byid)
    save(out,dict(format='dk4-clean-first-editorial-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,source_objects=303,physical_speech_objects=299,typed_choice_objects=4,source_FE_panels=FE,
        complete_exchanges=10,blocks=[g['block'] for g in packet['groups']],source_macro_counts=counts,
        source_packet=str(source_path),source_packet_sha256=digest(source_path),source_draft_files=[str(p) for p in paths],
        all_meanings_saved_before_independent_drafts=True,all_drafts_saved_before_current_story_English_intake=True,
        current_English_not_consulted_for_these303_objects=True,
        current_source_binding_contextual_comparison_names_terms_andfresh_formatting_pending=True,
        speaker_metadata_not_native_nameplate_orfull_name_approval=True,
        all_individual_five_review_gates_pending=True,source_controls_andruntime_macros_preserved=True,
        no_manual_wrap_alignment_orpadding_authored=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [source_path,*paths,Path(__file__)]}))
    print('Sealed303 clean meanings/independent drafts:299 speeches/',FE,'FE panels/four captions;macro counts',counts,';all comparisons andgates pending.')
if __name__=='__main__':main()
