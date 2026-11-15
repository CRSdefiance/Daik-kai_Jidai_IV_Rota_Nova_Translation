"""Complete the23-article prose review and resolve the same stat's conflicting Help name."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
if __name__=='__main__':
    previous=Path('translations/help_T00_T20_contextual_manuscript_v1.json')
    output=Path('translations/help_early23_contextual_manuscript_v2.json');assert not output.exists()
    binding_path=ROOT/'Power_family_complete_current_bindings_v1.json';bindings=load(binding_path)
    draft_path=ROOT/'T181_T184_clean_meanings_independent_drafts_v1.json';drafts=load(draft_path)
    doc=deepcopy(load(previous));assert bindings['standalone_Influence_topic_IDs']==[181,184,202]
    assert bindings['same_source_metric_native_notice']['current_text'].startswith('Power +%s!')
    reason=('Use Power for勢力値. Existing native COMMON288 says Power +%s!,andthe earlier Help8/9 already call the same bonus power. '
        'Only Help181,184 andRafael continuation202 use standalone Influence. Unify those complete articles withthe native term;'
        'do not change the unrelated verb influenced in skill explanations.')
    for row in doc['records']:
        if row['topic_id'] not in [7,8,9]:continue
        assert row['metric_UI_Influence_versus_COMMON_Power_binding_pending']
        row['english']=row['english'].replace('[[184|Influence]]','[[184|Power]]')
        assert 'Influence' not in row['english']
        row['review']['localization']=True;row['metric_UI_Influence_versus_COMMON_Power_binding_pending']=False
        row['Power_term_decision']=dict(reason=reason,evidence=str(binding_path),sha256=sha(binding_path.read_bytes()))
        if row['topic_id']==7:
            retained=row['retention_reason'];row.update(decision='revision',retention_reason=None,
                finding='Change only the conflicting stat name toPower. '+retained,
                localization_note='Change only the conflicting stat name toPower. '+retained,
                retained_existing_Rafael_description_andcomplete_bonus_reason=retained)
        else:
            row['finding']=row['finding'].replace('Influence follows the existing Help184 label,with cross-consumer Power consistency still pending.',
                'Power follows the existing native gain notice andthe original Help8/9 stat wording.')
            row['localization_note']=row['finding']
    source=load(ROOT/'clean_HELP_source_packet_v2.json');sources={r['topic_id']:r for r in source['records']}
    current={r['topic_id']:r for r in bindings['records']};draft_byid={r['topic_id']:r for r in drafts['records']}
    canonical=IlnkContainer.parse(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file(doc['file_path'])).blocks
    paragraphs={181:('Faction Info',
        'Select a faction on the Route Map to view its information. See [[184|Power]], [[182|Home Port]], [[190|Friendship]] and [[185|Relations]].',
        'Retain the already accurate selected-faction/Route Map instruction andallfour destinations. Change only the conflicting stat label toPower andnormalize visible link spacing/punctuation. Home Port,Friendship andRelations retain their current destination headings.'),
        184:('Power',
        "Power measures a faction's strength in the sea region shown. It increases with greater town [[150|market share]], victories over other factions and discoveries such as ruins.",
        'Retain the natural region-shown definition andallthree correct growth causes. Change Influence toPower,matching native288 andthe protagonist bonuses. Town preservesgeneric街 withoutnarrowing it tothe City settlement class. Do not add a formula,ship count,money orfriendliness as a growth cause.')}
    for index in [181,184]:
        original,cur,draft=sources[index],current[index],draft_byid[index]
        heading,english,note=paragraphs[index]
        doc['records'].append(dict(id=original['id'],topic_id=index,file_path=doc['file_path'],speaker='In-game Help',heading=heading,english=english,
            context='Complete faction-info/stat-definition article reviewed withHelp7/8/9 andthe same-source native Power notice. Selected faction anddisplayed region areexplicit;the player neednot be inthat region.',
            source_meaning=draft['faithful_source_meaning'],localization_note=note,
            source_reference=original['source_reference'],source_hex=original['source_hex'],clean_source_hex=original['source_hex'],canonical_source_hex=canonical[index].hex(),
            current_reference=cur['current_reference'],current_hex=cur['current_hex'],current_source_hex=cur['current_hex'],current_English=cur['current_text'],
            source_Japanese_with_link_IDs=original['source_Japanese_with_link_IDs'],original_links=original['original_links'],original_link_IDs=original['original_link_IDs'],
            current_link_IDs=[r['topic_id'] for r in cur['current_links']],decision='revision',finding=note,retention_reason=None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            independent_draft_reference=dict(path=str(draft_path),sha256=sha(draft_path.read_bytes()),id=original['id']),
            current_reference_packet=dict(path=str(binding_path),sha256=sha(binding_path.read_bytes()),id=original['id']),
            Power_term_decision=dict(reason=reason,evidence=str(binding_path),sha256=sha(binding_path.read_bytes())),
            independent_draft_claim_applies_to_body_not_previously_consulted_UI_heading=True,
            no_authored_wraps_oralignment=True,fresh_native_font_links_rows_bounds_allocation_pagination_andvisual_checks_pending=True,
            actual_gameplay=False,new_credit=0))
    assert len(doc['records'])==23 and len({r['id'] for r in doc['records']})==23
    assert all(all(row['review'][gate] for gate in ['source','context','localization','naturalness']) and not row['review']['formatting'] for row in doc['records'])
    revised=sum(r['decision']=='revision' for r in doc['records']);retained=sum(r['decision']=='retention' for r in doc['records'])
    assert (revised,retained)==(16,7)
    doc.update(proposed_revisions=revised,justified_retentions=retained,first_four_gates_passed=23,
        all23_source_context_localization_naturalness_reviews_passed=True,three_metric_label_bindings_pending=False,
        Power_term_consistency_resolved_for_this_complete_Help_group=True,
        Power_term_evidence=str(binding_path),Power_term_evidence_sha256=sha(binding_path.read_bytes()),
        added_topic202_owned_only_as_Rafael7_continuation=True,
        other_eight_added_current_topics203_to210_unowned_must_remain_byte_exact=True,
        unrelated_skill_explanations_influenced_by_not_rewritten=True,
        previous_manuscript=str(previous),previous_manuscript_sha256=sha(previous.read_bytes()),
        linked_clean_body_drafts=str(draft_path),linked_clean_body_drafts_sha256=sha(draft_path.read_bytes()),
        all_formatting_gates_pending=True,no_Help_ROM_changes_ornew_gameplay_orcompletion_claim=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()))
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [previous,binding_path,draft_path,Path(__file__)]})
    save(output,doc)
    save(ROOT/'Power_term_editorial_decision_v1.json',dict(Japanese='勢力値',English='Power',reason=reason,
        source_current_notice=bindings['same_source_metric_native_notice'],
        current_standalone_Influence_topic_ids=bindings['standalone_Influence_topic_IDs'],
        reviewed_complete_source_topic_ids=[7,8,9,181,184],current_Rafael_continuation202_included=True,
        proposed_manuscript=str(output),proposed_manuscript_sha256=sha(output.read_bytes()),
        no_global_substring_replacement=True,no_new_runtime_orfont_code=True,new_credit=0))
    print('23 complete Help prose reviews:16 proposed revisions/7 retentions;all four prose gates pass. Power resolved contextually;all formatting/native/visual/release gates pending.')
