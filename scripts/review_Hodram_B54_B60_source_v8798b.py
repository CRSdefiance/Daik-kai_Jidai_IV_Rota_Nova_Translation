"""Record direct source review, source-linked context, scoped names and the open de-name lead."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_source_review_v8798b')
NAMES_OUT=Path('translations/hodram_B54_B60_speaker_name_review_v1.json')
PROOFS={
    'gloss':'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json',
    'controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
    'names':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json',
    'clean_names':'work/analysis/Hodram_B54_B60_clean_names_v8793/twenty_clean_full_andprogressive_compositions_current_binding.json',
    'display':'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json',
    'context':'work/analysis/Hodram_B54_B60_clean_context_v8795/complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json',
    'paths':'work/analysis/Hodram_B58_source_paths_v8796/all64_structural_paths_49utterance_memberships_unforced_opening_reference.json',
    'macros':'work/analysis/Hodram_B54_B60_source_macros_v8797b/FI_given_FA_surname_original_virtual_getter_trace.json',
}
REASONS={
    1:'Retain approved Hodram and Joakim, with Bergstrom, in the source given-middle-surname structure. Both original source getters and actual current captain-object getters bind the components. This supplies no custom-name or full-catalogue UI approval.',
    20:'Fernando Dias naturally preserves フェルナンド・ディアス and the current given/surname identity in the optional companion comment. Retain the existing full-width F storage and its complete native rendering; do not invent a middle particle, nationality or rank.',
    23:'Manuel Almeida preserves マヌエル・アルメイダ in the optional comments and personal recollection. Its complete source full getter has no middle field; do not add a historically plausible de or other biography. The first-person memory and Christian reference remain source character speech.',
    24:'Sera Shahrbaraz and full Sera Altos Shahrbaraz preserve all source components. Linked clean B142 R243/R250/R253 explicitly supplies the name and the captain settling on Sera; retain that distinction rather than inventing a shorter family name or a relationship. Her language learning does not change her identity.',
    36:'Geronimo Espinosa preserves the original progressive ジェロニモ・エスピノサ and the person identified by surname in B58/B60 and full name in linked B142. Geronimo is natural established English spelling for the source sound. Progressive retention does not approve the untranslated デ in the current full getter; that distinct full-name finding remains open.',
    84:'Shopkeeper is natural English for 広場の店主 in these formal local-witness and quest-giver exchanges. The role is still a shopkeeper even when speaking about abuses or offering a map. Do not turn this person into a guildmaster, official or ruler, or append the unused regional Africa field as a surname.',
    113:'Port Worker preserves 出港所の兄貴 as an informal port-service role in the identity check and guild message. The familiar 兄貴 does not establish a brother relationship or rank. Keep the role distinct from the guild person being mentioned.',
    114:'Port Worker preserves the same source role during the accusation against Espinosa. The actual father and missing-family relationship comes from the spoken 俺の親父, not from the speaker label. Do not attach Africa as a surname or infer an official rank.',
    119:'Port Worker is supported by the actual source label in the newcomer exchange. The low laugh may be unsettling, but does not establish a pirate, thug or villain identity. The unused regional インディオ table field must not become a racialized player-facing surname or invented biography.',
    141:'Innkeeper naturally localizes 宿屋のおばさん as the business role. The familiar female address does not establish aunt kinship or a precise age; the accusation about villagers does not add a governmental title. The regional Africa field is unused by the actual source/current generic-role getters.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES_OUT.exists();data={k:read(p) for k,p in PROOFS.items()};display,names,clean_names=data['display'],data['names'],data['clean_names']
    assert len(display['records'])==82 and display['complete_native_source_page_count']==82 and len(display['review_sheets'])==11
    viewed=[*display['review_sheets'],names['review_sheet']]
    for p in viewed:assert sha(Path(p['path']).read_bytes())==p['sha256']
    assert [data['controls'][k] for k in ['complete_source_commands','complete_speech_preambles','relative_sites','native_relative_cases','raw_unforced_query_cases','opaque_structural_decode_pairs','normal_seeded_end_cases']]==[152,82,24,120,6,33,175]
    assert data['paths']['unconditional_utterances']==31 and data['paths']['conditional_utterances']==18 and len(data['paths']['models'])==64
    assert data['macros']['FI_andFA_source_referents_proved_by_original_captain_virtual_slots_not_coincidentally_equal_strings']
    source_groups=data['context']['groups'];assert [g['block'] for g in source_groups]==[15,37,65,128,142]
    assert sum(len(g['records']) for g in source_groups)==160
    choices=[]
    for group in source_groups:
        block=bytes.fromhex(group['clean_block_hex'])
        for c in group['commands']:
            if c['word']!=0x2100:continue
            at=c['offset'];base=at+6
            for index in range(2):
                label_at=base+struct.unpack_from('<H',block,at+2+index*2)[0];raw=block[label_at:block.index(0,label_at)]
                choices.append(dict(block=group['block'],option_index=index,source_command_offset=at,source_label_offset=label_at,source_record_index=block[:label_at].count(b'\0'),source_hex=raw.hex(),source_Japanese=raw.decode('cp932')))
    assert [c['source_Japanese'] for c in choices]==['攻撃準備だ','それは越権行為だろう…']
    context_note='Read all160 surrounding spoken source records and both original B37 choices as context only. B37 identifies a slave ship and offers an imperative to prepare to attack versus concern about exceeding authority; the crew also treats it as an admissible target. B15 follows a fight, releases captives, and introduces a frightened girl with whom the captain cannot communicate; ancestry/religion remarks are the captain\'s tentative perceptions, not new narrator facts. B56 proposes temporary local shelter because she differs ethnically from other captives. B142 shows her following, the debate about taking a civilian woman aboard, the invitation conveyed by gestures, her full-name introduction, and the captain\'s awkward warmth. Source event links37->15->56->142->128->57 provide dependencies only, not exact location, elapsed time, earned chronology or native eligibility. B128 has no spoken text. B57 excludes event65; B65 is the later departure/reunion source context, with an unspecified statement in another language. Preserve that statement as unspecified and do not invent its translation or a confirmed romance. These context records and choices are not added to the82-unit batch or credited as completed localization.'
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(names['candidate']);ja,arm=[i.read_file('/__arm9__.bin') for i in [clean,current]]
    identity=next(r for r in names['complete_clean_current_static_fields'] if r['actor_ID']==36);middle=next(f for f in identity['current'] if f['kind']=='middle')
    assert middle['text']=='デ' and middle['hex']=='8366' and middle['pointer']!=0
    base=names['complete_clean_current_static_fields'][0]['clean'][0]['table_field']-32*names['complete_clean_current_static_fields'][0]['actor_ID']
    uses=[]
    for ident in range(207):
        for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
            at=base+32*ident+col;pointer=struct.unpack_from('<I',arm,at)[0]
            if pointer==middle['pointer']:
                uses.append(dict(actor_ID=ident,field=kind,table_field=at,source_table_field_hex=ja[at:at+4].hex(),current_table_field_hex=arm[at:at+4].hex(),
                    source_given=string(ja,struct.unpack_from('<I',ja,base+32*ident)[0]),current_given=string(arm,struct.unpack_from('<I',arm,base+32*ident)[0])))
    needle=struct.pack('<I',middle['pointer']);refs=[];at=0
    while True:
        at=arm.find(needle,at)
        if at<0:break
        refs.append(dict(offset=at,aligned_to4=at%4==0,is_known_name_table_field=any(r['table_field']==at for r in uses)));at+=1
    fullname=next(r for r in clean_names['clean_current_consumer_bindings'] if r['actor_ID']==36 and r['consumer']=='full-catalogue')
    lead=dict(actor_ID=36,current_full_name=fullname['current_text'],source_full_name=fullname['clean_text'],proposed_full_name='Geronimo de Espinosa',
        source_full_getter=next(r for r in clean_names['source_native_getters']['rows'] if r['actor_ID']==36 and r['consumer']=='full-catalogue'),
        current_full_getter=next(r for r in names['fresh_twenty_progressive_andfull_current_getters']['rows'] if r['actor_ID']==36 and r['consumer']=='full-catalogue'),
        exact_current_middle_field=middle,all207_name_table_fields_pointing_to_same_string=uses,raw_ARM9_pointer_occurrences=refs,
        proposed_de_is_transliteration_of_actual_source_component_not_rank_ornew_relationship=True,
        source_spoken_fullname_in_clean_B142_R0027_confirms_component=True,
        no_global_two_byte_replacement_orname_asset_edit_authorized_by_this_inventory=True,
        all_affected_fields_native_consumers_deployment_ownership_andscoped_release_checks_still_required=True,
        raw_pointer_occurrences_are_static_evidence_not_complete_runtime_call_coverage=True,formatting_andregistered_integration_pending=True)
    reviews=[]
    for ident in REASONS:
        binding=next(r for r in clean_names['clean_current_consumer_bindings'] if r['actor_ID']==ident and r['consumer']=='progressive-nameplate')
        reviews.append(dict(actor_ID=ident,consumer_scope='progressive-nameplate-in-clean-B54-B60-exchanges',source_display=binding['clean_text'],current_display=binding['current_text'],decision='retention',
            source_andcurrent_native_references=deepcopy(binding),context=REASONS[ident],retention_reason=REASONS[ident],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            formatting_actual_representative_andbatch_release_scope_pending=True,
            actual_B54_B60_headers_fullcatalogue_UI_all207_andcustomnames_not_approved=True))
    ROOT.mkdir(parents=True);save(ROOT/'Geronimo_de_particle_field_andshared_pointer_inventory.json',lead)
    save(NAMES_OUT,dict(format='dk4-scoped-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=reviews,full_name_open_findings=[lead],source_given_middle_surname_components_androle_metadata_kept_separate=True,
        all10_progressive_wordings_editorially_retained_withindividual_context_reasons=True,formatting_actual_andregistered_gates_still_pending=True,
        no_dialogue_retention_source_prose_orcompletion_credit_added=True,new_credit=0,full_goal_complete=False))
    save(ROOT/'source_context_names_display_review_before_current_English.json',dict(candidate=names['candidate'],candidate_sha256=names['candidate_sha256'],
        all82_source_native_pages_and11_sheets_directly_viewed=True,source_andcurrent_names_sheet_directly_viewed=True,viewed_sheets=viewed,
        source_context_records_read=160,source_context_typed_choice_labels=choices,context_note=context_note,
        source_names_current_getters_default_FI_FA_semantics_FE_null_consumer_andbranch_memberships_bound=True,
        source_macro_counts=display['source_macro_counts'],original_FI_given_andFA_surname_from_readonly_native_virtual_calls=True,
        retained_names_packet=str(NAMES_OUT),retained_names_packet_sha256=sha(NAMES_OUT.read_bytes()),
        Geronimo_fullname_untranslated_de_open_ownership_consumer_andrelease_lead=str(ROOT/'Geronimo_de_particle_field_andshared_pointer_inventory.json'),
        all_actual_vs_offline_customnames_fullcatalogue_andnatural_activation_limits_preserved=True,
        source_ready_for_current_English_comparison_not_final_localization_orformatting_approval=True,
        existing_B54_B60_English_dialogue_bodies_still_unconsulted=True,
        no_new_ROM_emulator_capture_orledger_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [*PROOFS.values(),NAMES_OUT,Path(__file__)]}))
    print('Source review:all82native pages/11sheets+names viewed;160linked source utterances/2context choices read;10scoped name retentions/proven FIgiven FAsurname. Geronimo デ lead shares '+str(len(uses))+'namefields;no asset edit. Ready forcurrent-English comparison;zero credit.',flush=True)
