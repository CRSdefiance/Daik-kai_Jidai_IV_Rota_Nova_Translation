"""Approve Adernkatz consistently from clean identity/full exchanges andcurrent effective consumers."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_surname_review_v8202')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
EFFECTIVE=Path('work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json')
NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')
OLD_HODRAM_NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v1.json')
HODRAM_NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')
OUT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
REASONS={
('DK4_MES_B27_R0091'):('Gerhard politely recognizes Hodram by reputation andintroduces his full name after Lil/Camille leave.','Retain the clear,courteous self-introduction andheard-of-you acknowledgment;the only lexical correction is the family spelling. Do not add a current rank,retirement,mentorship orrelationship to this sentence.'),
('DK4_MES_B27_R0094'):('Hodram recognizes the named admiral for his pirate-hunting reputation;Gerhard immediately replies that this is in the past.','Retain the surprised recognition andpirate-hunter question. Admiral is explicit in this source line;the following reply preserves the past distinction without inserting new biography into the nameplate.'),
('DK4_MES_B74_R0060'):('Camille warmly greets an admiral he knew briefly before,after leading Lil to his home.','Retain the respectful,enthusiastic long-time-no-see greeting asnatural spoken English. Recompile asone paragraph so the old break between It\'s andbeen is not inherited.'),
('DK4_MES_B74_R0185'):('Camille introduces the admiral by full name to Lil before explaining his former fleet andpirate-hunting background.','Retain the direct introduction,source FI substitution andexplicit Admiral title. Preserve source wording without adding the next historical explanation early orfixing FI to a literal player name.'),
('DK4_MES_B74_R0260'):('After Lil andGerhard conditionally agree to sail together,Camille rejoices,thanks the admiral andasks forfuture guidance;Gerhard then asks to be called Gerhard underLil\'s captaincy.','Retain the enthusiastic thanks andrequest forcontinued guidance. Source 今後も andthe previously acknowledged brief acquaintance support this respectful continuity;it doesnot establish a formal apprenticeship orspecific earlier training. Preserve the following address-correction joke anddo not claim the player hasfinished a battle lesson.'),
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not HODRAM_NAMES.exists()
    current,effective,names,oldnames=map(read,[CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES])
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes()) and len(effective['effective_current_records'])==5
    assert effective['native_names_packet_sha256']==sha(NAMES.read_bytes()) and names['measured_default_macro_lengths']==dict(FI=3,FA=5,FO=9)
    rows=[]
    for original in current['records']:
        row=deepcopy(original);before=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        assert before['registered_catalogue_match'] is None and before['effective_predecessor_template_hex']==row['current_hex'][2:]
        text=before['effective_predecessor_paragraph'];assert text.count('Ardelknatts')==1
        english=text.replace('Ardelknatts','Adernkatz')
        for token in ['FI','FA','FO']:
            english=english.replace(token,'{MACRO:'+token+'}')
        assert not any(v in english for v in ['\n','\r','{LB','{ALIGN','{PAD'])
        for token in ['FI','FA','FO']:assert english.count('{MACRO:'+token+'}')==bytes.fromhex(row['source_hex'])[1:].count(token.encode())
        context,retention=REASONS[row['id']]
        row.update(english=english,logical_English=english,speaker={1:'Hodram',9:'Camille',16:'Gerhard'}[row['source_selector']],
            source_meaning=context,context=row['source_context']+' '+context,localization_note='Standardize the established family form Adernkatz forアーデルンカッツ;retain allother working words andintent. '+retention,
            editorial_finding='Current family spelling conflicts with14existing Adernkatz consumers. The complete clean exchange confirms one identity. Newordinary wrapping must be generated;do notcopy existingline breaks orallocationpadding.',
            decision='revision',editorial_decision='surname-consistency-revision-existing-prose-justifiably-retained',retention_reason=retention,
            effective_predecessor_template_hex=before['effective_predecessor_template_hex'],effective_predecessor_paragraph=text,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            already_completed_record_revisit_no_duplicate_source_prose_orcompletion_credit=True,body_words_except_surname_retained_exactly=True)
        rows.append(row)
    assert len(rows)==5 and sum('{MACRO:FI}' in r['english'] for r in rows)==1
    image=NdsImage.open(current['current_ROM']);arm=image.read_file('/__arm9__.bin');slot=1435252;size=20
    before=arm[slot:slot+size];assert before==b'Ardelknatts\0'+bytes(size-len(b'Ardelknatts\0'))
    target=b'Adernkatz\0'+bytes(size-len(b'Adernkatz\0'))
    updated=deepcopy(oldnames);gerhard=next(r for r in updated['records'] if r['actor_ID']==16)
    gerhard.update(name='Gerhard Adernkatz',current_name='Gerhard Ardelknatts',current_surname='Ardelknatts',target_surname='Adernkatz',decision='revision',
        finding='Resolved by complete clean context andcurrent consumer census:standardize the existing Adernkatz form,which follows the source sound order andalready occurs14times. Six inconsistent consumers require a registered correction. The provisional Ardelnkatts alternative is superseded without being shipped.',
        localization_note='Retain Gerhard forゲルハルト;use the already established Adernkatz forアーデルンカッツ consistently across progressive/full names andspoken references. This is a project localization decision;no definitive official Latin spelling orGerman historical identity is claimed.',
        required_registered_dependency='Gerhard_Adernkatz_consistency_correction',name_asset_andfive_SC2_mentions_still_pending=True,
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
    updated.update(prior_review=str(OLD_HODRAM_NAMES),prior_review_sha256=sha(OLD_HODRAM_NAMES.read_bytes()),
        surname_source_localization_decision_resolved_assets_andformatting_pending=True,
        five_individual_localization_retentions_one_surname_concern_not_auto_approved=False,
        five_individual_retentions_one_source_based_surname_revision_allformatting_pending=True,
        consistency_current_packet=str(CURRENT),consistency_current_packet_sha256=sha(CURRENT.read_bytes()),
        no_name_asset_ROM_registry_orcompletion_credit_change=True)
    ROOT.mkdir(parents=True);save(HODRAM_NAMES,updated)
    save(OUT,dict(format='dk4-surname-consistency-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',route=2,route_identity='Lil',blocks=[27,74],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        current_archive_sha256=current['current_archive_sha256'],records=rows,revised=5,retained=0,typed_choice_records=[],
        name_records=[dict(id='DK4_NAME_ADERNKATZ_15E674',actor_ID=16,file_path='/__arm9__.bin',offset=slot,bytes=size,current_hex=before.hex(),target_hex=target.hex(),
            source_Japanese='アーデルンカッツ',current_English='Ardelknatts',english='Adernkatz',reason='Use the same source-faithful established surname already used by14other current consumers;one fixed name slot updates progressive/full native consumers consistently.',
            pointer_fields_ownership_unowned_bytes_native_getters_andglyphs_still_require_checks=True)],
        selected_spelling='Adernkatz',all14_existing_Adernkatz_occurrences_protected=True,all6_inconsistent_consumers_explicitly_planned=True,
        all_other_prose_words_andsource_runtime_macros_retained=True,new_wraps_owned_by_formatter=True,
        current_andfive_whole_clean_exchanges=str(CURRENT),current_andfive_whole_clean_exchanges_sha256=sha(CURRENT.read_bytes()),
        effective_proof=str(EFFECTIVE),effective_proof_sha256=sha(EFFECTIVE.read_bytes()),native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),
        required_for_Hodram_name_review=str(HODRAM_NAMES),required_for_Hodram_name_review_sha256=sha(HODRAM_NAMES.read_bytes()),
        no_official_Latin_orhistorical_biography_claim=True,no_new_source_prose_orcompleted_record_credit=True,
        allfive_previous_credit_classifications_revisions_so_unique_revised_retained_totals_unchanged=True,
        native_logical_layout_glyph_name_slot_alias_pointer_inverse_actual_atomic_registered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES,HODRAM_NAMES,Path(__file__)]}))
    print('Adernkatz decision saved:one sharedname slot/five prior-revised paragraphs;allotherwords andFI retained.Hodram namelexical concern resolved;assets/layout/actual/release pending.Zero duplicate credit.')
    for row in rows:print(row['id'],row['english'])
