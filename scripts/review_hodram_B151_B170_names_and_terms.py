"""Record scoped source-based names and fixed-slot proposals; native display/release remain open."""
import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B151_B170_clean_20261102')
MANUSCRIPT=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v2.json')
NAMES={
 0:'Retain approved Rafael Castor; B168 actor0 is Rafael, not the active captain or an invented rank.',
 1:'Retain approved Hodram and Joakim with established Bergstrom; the full-name middle component stays distinct from the progressive name.',
 5:'Retain Claudio Manaus; Clau in B168 is the explicit familiar source nickname, not a new family relationship.',
 6:'Retain Julio Erneco and the earlier glyph repair; older-man address and veteran language do not supply kinship or military service.',
 7:'Retain Cristina Erneco in these bound consumers; a shared surname with Julio does not establish kinship. Other Cristina/Christina consumers remain separate scope.',
 8:'Retain Arcadius Eudoxios and full Arcadius Eirene Eudoxios; B168 uses this original actor, not Fernando.',
 11:'Retain Jam Ludwyan and full Jam Jack Ludwyan, preserving the source name sounds and explicit J-A-M without imposing a national biography.',
 13:'Retain source-reviewed Cesare Tony; the legacy Tohni body spelling is inconsistent with the existing individual decision.',
 15:'Retain Angelo Puccini, including the explicit full self-introduction; his Italian exclamation supplies voice without a new rank.',
 16:'Retain source-reviewed Gerhard Adernkatz; do not regress to Adelknauts or turn his personal loyalty into kinship.',
 17:'Retain Al Shin and full Al Ferid Shin, preserving all three source components without dropping Shin or adding a title.',
 18:'Retain Charles Rochefort and full Charles Jean Rochefort; his new institute directorship comes from B156 dialogue, not name metadata.',
 19:'Retain individually reviewed Carlo Sinat rather than legacy Sinato; his actual family loss is explicit, unlike the innkeeper relationship.',
 20:'Retain Fernando Dias with the earlier normal-F repair; preserve the full name rather than introducing him only as Dias.',
 21:'Retain Ian Dukov in his full introduction and both native consumers; appearance and harassment do not establish another gender identity.',
 22:'Retain Samwell Khan and full Samwell da Khan, preserving the registered middle-field repair; Samuel is not this source name.',
 23:'Retain Manuel Almeida; the committee chairmanship is an explicit later appointment, not part of the name.',
 24:'Retain Sera Shahrbaraz and full Sera Altos Shahrbaraz; B156 explicitly states princess, but neither marriage nor engagement follows.',
 25:'Retain Yifa Sol for イファ・ソル, consistently with her alternate lamp suggestion and named praise.',
 78:'Retain source-reviewed Sirwood Eme; Sirwood is one proper name, not a Sir title, and companionship supplies no family relationship.',
 92:'Retain natural Barkeep for 酒場の親父; proprietor address does not make him a father.',
 96:'Retain Patron for 酒場の客; the role does not supply a personal name, nationality or new relationship.',
 105:'Retain Trader for the trading-post proprietor; Adil is the personal name in this exchange, not a global replacement for every actor105 use.',
 113:'Retain Port Worker for 出港所の兄貴; the familiar address does not establish brotherhood or military rank.',
 115:'Retain Port Worker without adding the regional metadata as religion, nationality or surname.',
 116:'Retain Port Worker for the eyewitness; the regional table field is not a personal biography.',
 120:'Retain Guard for 衛兵, with no invented officer rank or country in the global label.',
 121:'Retain Guard for 衛兵; the regional metadata does not create a religious title or nationality.',
 125:'Retain King for explicit 国王; do not globally add a country from this one royal audience.',
 132:'Retain generic Priest for the religious officiant 祭主; do not infer Islam or a named denomination from regional metadata.',
 142:'Retain Innkeeper for 宿屋のおばさん; neither the label nor concern for Adil proves she is his wife.',
 148:'Retain Guildmaster for the explicit guild head; it is an occupational role, not a noble title.',
 151:'Retain source-native progressive Sailor and distinct catalogue Retainer; static 配下 alone does not determine the progressive getter.',
 152:'Retain source-native Sailor and distinct Retainer consumers; the hostile scene does not authorize rewriting the shared actor range globally.',
 164:'Retain the earlier reviewed Man label; the couple relationship does not establish husband, marriage or an age.',
 165:'Retain the earlier reviewed Woman label; the couple relationship does not establish wife, marriage or an age.',
}


if __name__=='__main__':
    target=Path('translations/hodram_B151_B170_scoped_names_andterms_v1.json')
    updated=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v3.json')
    proposal=ROOT/'two_static_text_slots_proposal_v1.json'
    assert not any(p.exists() for p in [target,updated,proposal])
    bindings_path=ROOT/'native_identity_and_item_checkpoint_v1.json'
    bindings=load(bindings_path);doc=load(MANUSCRIPT)
    assert set(NAMES)=={r['actor_ID'] for r in bindings['records']}
    rows=[]
    for i,bound in enumerate(bindings['records']):
        actor=bound['actor_ID'];names={r['consumer']:r['text'] for r in bound['current_consumers']}
        rows.append(dict(id=f'SC1_B151_B170_ACTOR_{actor}_SCOPED_NAME',actor_ID=actor,english=names['progressive-nameplate'],
            speaker=names['progressive-nameplate'],context='Complete B151–B170 exchanges and original source identity; this is scoped consumer approval only.',
            source_meaning=' / '.join(f['text'] for f in bound['clean_fields'] if f['text'] is not None),
            localization_note=NAMES[actor],decision='retention',retention_reason=NAMES[actor],
            context_record_ids=bound['context_record_ids'],current_consumers=bound['current_consumers'],
            exact_binding_reference=dict(path=str(bindings_path),sha256=sha(bindings_path.read_bytes()),key='records',index=i),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_display_proof_reuse_orfresh_plane_binding_pending=True,actual_full_catalogue_UI_unvisited=True,new_credit=0))
    rows.append(dict(id='SC1_B161_MENTIONED_MIVOR',actor_ID=79,english='Mivor',speaker='Mentioned name',
        context='B161 dance response; admiration does not establish a romance or shared-surname relationship.',
        source_meaning='ミヴォール',localization_note='Retain Mivor, preserving source ヴォ vowel/consonant and current native given name rather than legacy Mivall.',
        decision='retention',retention_reason='The established given name matches the source sound; no new full-name or biography claim.',
        context_record_ids=['DK4_MES_B161_R0056'],exact_binding_reference=dict(path=str(bindings_path),sha256=sha(bindings_path.read_bytes()),key='mentioned_name'),
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    city_reason=('Retain Abkhaz for アブハーズ in the complete Black Sea rebuilding exchange. '
                 'It preserves the established dialogue identity and a readable English kh rendering, without renaming the town to Abkhazia or asserting new political facts. '
                 'Propose correcting the shorter Abhaz city label to this chosen spelling; do not select a weaker name solely for legacy UI compatibility.')
    ship_reason=('Use Elysion for エリュシオン and spoken エリュシオン号, preserving the original ship identity. '
                 '号 is a ship-designating suffix, not part of a new English name. Good Luck remains the evidentiary carving. '
                 'The separate Japanese code literal needs its consumer qualified before any ROM change.')
    runtime=bindings['runtime'];parent=Path(runtime['candidate']);assert sha(parent.read_bytes())==runtime['candidate_sha256']
    arm=NdsImage.open(parent).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    fields=[];proposed=bytearray(arm)
    for ident,field,ja,en,reason in [('ABKHAZ_CITY',1199308,'アブハーズ','Abkhaz',city_reason),('ELYSION_CODE_LITERAL',178732,'エリュシオン','Elysion',ship_reason)]:
        source_pointer=struct.unpack_from('<I',clean,field)[0];pointer=struct.unpack_from('<I',arm,field)[0]
        assert pointer==source_pointer
        at=pointer-0x02000000;source_end=clean.index(0,at);current_end=arm.index(0,at)
        assert clean[at:source_end].decode('cp932')==ja
        encoded=en.encode('cp932')+b'\0';capacity=source_end-at+1
        assert len(encoded)<=capacity
        refs=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4)
              if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+capacity]
        source_refs=[dict(offset=i,pointer=struct.unpack_from('<I',clean,i)[0]) for i in range(0,len(clean)-3,4)
              if pointer<=struct.unpack_from('<I',clean,i)[0]<pointer+capacity]
        assert refs==source_refs==[dict(offset=field,pointer=pointer)]
        old=arm[at:at+len(encoded)];proposed[at:at+len(encoded)]=encoded
        entry=dict(id=ident,pointer_field_offset=field,pointer=pointer,physical_offset=at,
            clean_slot_hex=clean[at:source_end+1].hex(),current_full_slot_hex=arm[at:at+capacity].hex(),source_text=ja,
            current_text=arm[at:current_end].decode('cp932'),english=en,source_slot_capacity=capacity,
            owned_span_bytes=len(encoded),old_span_hex=old.hex(),target_span_hex=encoded.hex(),aligned_pointer_references=refs,
            source_aligned_pointer_references=source_refs,all_pointers_andallocation_unchanged=True,
            native_consumer_bounds_andrelease_approval_pending=True)
        fields.append(entry)
        rows.append(dict(id=ident,english=en,speaker='Scoped proper-name term',context='B155 town report' if ident=='ABKHAZ_CITY' else 'B167–B168 missing-ship exchange',
            source_meaning=ja,localization_note=reason,decision='revision',owned_field=entry,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    inverse=bytearray(proposed)
    for f in fields:inverse[f['physical_offset']:f['physical_offset']+f['owned_span_bytes']]=bytes.fromhex(f['old_span_hex'])
    assert bytes(inverse)==arm and len(proposed)==len(arm)
    assert sum(f['owned_span_bytes'] for f in fields)==15
    save(proposal,dict(format='dk4-source-qualified-static-text-slots-proposal-v1',parent_ROM=str(parent),parent_ROM_sha256=sha(parent.read_bytes()),
        parent_ARM9_sha256=sha(arm),proposed_ARM9_sha256=sha(proposed),fields=fields,owned_span_bytes=15,
        changed_bytes=sum(a!=b for a,b in zip(arm,proposed,strict=True)),complete_parent_ARM9_inverse_exact=True,
        no_ROM_mutation_ornew_allocation=True,native_consumer_ownership_bounds_actual_andregistered_release_pending=True,
        source_qualified_aligned_pointer_scan_not_all_possible_computed_alias_proof=True,new_credit=0))
    save(target,dict(format='dk4-scoped-name-andterm-localization-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,ordinary_actors=36,mentioned_actor=1,static_terms=2,
        dialogue_prose_credit_not_added=True,no_new_global207_name_approval=True,proposal=str(proposal),proposal_sha256=sha(proposal.read_bytes()),
        runtime=runtime,evidence={str(p):sha(p.read_bytes()) for p in [bindings_path,MANUSCRIPT,Path(__file__)]}))
    updated_doc=deepcopy(doc)
    for row in updated_doc['records']:
        if row['id'] in ['DK4_MES_B155_R0015','DK4_MES_B155_R0019']:
            assert row['open_localization_question']['source']=='アブハーズ' and not row['review']['localization']
            row['resolved_localization_question']=dict(**row.pop('open_localization_question'),decision='Abkhaz',
                reason=city_reason,name_review=str(target),name_review_sha256=sha(target.read_bytes()),city_UI_native_andrelease_pending=True)
            row['review']['localization']=row['prose_comparison_review']['localization']=True
            row['localization_note']=row['finding']=city_reason
            row['retention_reason']=city_reason
    assert all(all(r['prose_comparison_review'].values()) for r in updated_doc['records'])
    updated_doc.update(complete_four_gate_comparisons=642,place_name_questions=0,scoped_name_review=str(target),
        scoped_name_review_sha256=sha(target.read_bytes()),static_term_native_fields_pending=str(proposal),
        earlier_pending_manuscript=str(MANUSCRIPT),earlier_pending_manuscript_sha256=sha(MANUSCRIPT.read_bytes()))
    save(updated,updated_doc)
    print('39 scoped name/term decisions;all642 four-prose-gate passes. Two fixed-slot proposals/15 owned bytes;native consumer/display/release pending. No ROM orcredit.')
