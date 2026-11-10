"""Review all15 speeches in their six complete source-owned paths;formatting remains pending."""
import struct
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_prose_v7982')
DOC=Path('translations/rafael_B47_editorial_manuscript_v1.json')
NAME_DOC=Path('translations/rafael_B47_speaker_name_review_v1.json')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B47_effective_v7981/all15_effective_English_templates30_original_progressive_dispatches.json')
NAMES=Path('work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json')
FLOW=Path('work/analysis/Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json')
GLOSS=Path('work/analysis/Rafael_B47_branch_gloss_v7979/15_fresh_glosses_six_source_paths_names_bound_before_current_English.json')
CONTROL=Path('work/analysis/Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json')
REVISIONS={
    5:("I still can't tell what Hayreddin's after, but we should be able to get around the Mediterranean now.",
       "Restore the travelers' ability to get around the Mediterranean after the bargain, rather than saying the sea itself has become safer. The conversational uncertainty preserves Julio's caution about Hayreddin's motives."),
    53:("The Ottomans hold roughly the eastern half of the Mediterranean now. That's Pasha's territory. If they target us, we won't stand a chance.",
        "Restore roughly, the eastern-half scope and present situation; identify the Ottoman domain with Pasha's territory. Keep the conditional danger of their targeting the group. The old fleet wording narrowed the source's forces and lost the explicit condition. Pasha is the source surname component, not Janus Pasar."),
    63:("Then we'd better leave the Mediterranean for later, with Pasha's forces so strong there.",
        "Restore Rafael's conclusion about the Mediterranean as a region, rather than only Pasha's waters. Use a natural spoken conclusion after Julio's warning and retain the reason: Pasha's strong influence. This Ottoman-only alternative never accompaniesR70."),
    70:("With Valdes's Spanish forces and Pasha's Ottoman forces so strong there, we'd better leave the Mediterranean for later.",
        "Preserve both separately identified forces, their influence and the explicit Mediterranean region. Pasha is a source name component, so avoid making 'the Pasha' a new rank-based form of reference. This is the alternative toR63, not an additional conclusion spoken after it."),
    77:("There's no need to push for a trading contract. Better not to provoke them.",
        "Replace the stiff 'force a contract' with natural advice not to push for a trading agreement in this dangerous region. The next sentence preserves prudent avoidance of provocation; neither sentence bans all contracts or visits."),
    81:("But we can't ignore the big cities. They may have skilled navigators, so we should at least visit to look for some.",
        "Keep the qualification to the caution: the cities may have skilled navigators. At least visiting to look for them preserves the limited recruiting purpose without promising recruitment or turning prospective crewmates into political allies."),
    102:("Yeah. If we're heading into other waters, we'll need stronger ships. And we'd better toughen ourselves up, too.",
         "Restore the spoken conditional preparation for other waters and make ship improvements and the group's own training distinct. Claudio's casual agreement and energetic 'toughen ourselves up' preserve his rougher voice without adding a rank, objective, or guaranteed result."),
    129:("All right, let's get to work!",
         "Render the openingよし and renewed shared resolve as a natural American response to the work just discussed. This is encouragement to act, not a new destination, conquest, or completed ambition."),
}
RETENTIONS={
    17:"The understated 'we won't last long' naturally carries the Japanese hyperbole about not having enough lives. In context, pirates refers to the dangerous pirates already discussed and 'every time we enter' refers to the Mediterranean. Janus's measured, wry agreement works without a literal extra-lives claim.",
    44:"Julio's brief caution is natural and clear after guarded relief. The following question and explanation supply the risk and territorial context. The semicolon reads as an ordinary spoken pause, not an authored display break; no ban on all Mediterranean entry is asserted.",
    48:"The short, sincere question naturally invites Julio's explanation. It retains Rafael's learning role without inventing kinship, rank, or a more elaborate objection.",
    92:"Janus's concise approval fits directly after the qualified recruiting plan and preserves賢明ですね by intent. It works as a measured reaction without an added promise or overly literal formality.",
    106:"The reminder clearly follows Claudio's preparation advice and preserves visiting large cities and recruiting navigators. 'Remember' works in both source compositions without forcing an earlier on-screen sentence to have been spoken. Recruiting remains the advised goal, not a guaranteed mechanic.",
    110:"Rafael's exclamation naturally conveys his realization of how much remains to do. Read between the practical advice and Janus's dry comment, it carries youthful surprise and mild overwhelm without adding despair or claiming preparation is finished.",
    122:"Janus's understated comment works as a lightly wry response to Rafael's overwhelm before the final resolve. Its simple American phrasing retains the source observation without inventing an occupation, relationship, or rank.",
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAME_DOC.exists()
    current,effective,names,flow,gloss,control=map(read,[CURRENT,EFFECTIVE,NAMES,FLOW,GLOSS,CONTROL])
    assert current['gloss_packet_sha256']==sha(GLOSS.read_bytes()) and current['all15_clean_whole_context_glosses_precede_current_English_exposure']
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes()) and len(effective['source_current_dispatches'])==30
    assert names['candidate_sha256']==current['current_ROM_sha256']==effective['candidate_sha256']
    assert len(flow['representative_text_paths'])==6 and flow['R63_Ottoman_only_andR70_both_powers_mutually_exclusive']
    assert set(REVISIONS).isdisjoint(RETENTIONS) and set(REVISIONS)|set(RETENTIONS)=={r['source_record_index'] for r in current['records']}
    assert control['all48_commands15_complete_preambles_andcomplete_normal_end_preserved']
    image=NdsImage.open(current['current_ROM']);clean=NdsImage.open('work/clean.nds')
    mentions=[]
    for ident,wanted_source,wanted_current in [(31,'バルデス','Valdes'),(33,'パシャ','Pasha'),(34,'ハイレディン','Hayreddin')]:
        versions=[]
        for label,im in [('clean',clean),('current-name-components-only',image)]:
            arm=im.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
            fields=[]
            for column,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
                at=table+32*ident+column
                fields.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,struct.unpack_from('<I',arm,at)[0])))
            versions.append(dict(version=label,ARM9_sha256=sha(arm),fields=fields))
        assert versions[0]['fields'][1]['text']==wanted_source and versions[1]['fields'][1]['text']==wanted_current
        mentions.append(dict(actor_ID=ident,source_component=wanted_source,current_component=wanted_current,component_slot=4,
            exact_fields=versions,decision='retain-component',
            reason='Retain the established surname component used by the clean exchange; no full-name, middle-field, catalogue-UI or new-rank approval is inferred.',
            name_asset_changed=False,full207_name_review_andother_consumers_still_pending=True))
    speakers={0:'Rafael',4:'Janus',5:'Claudio',6:'Julio'}
    rows=[]
    for original in current['records']:
        row=deepcopy(original);index=row['source_record_index']
        eff=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        assert eff['effective_predecessor_paragraph']==row['raw_storage_comparison_paragraph']
        if index in REVISIONS:
            english,note=REVISIONS[index];decision='revision';retention=None
            assert english!=eff['effective_predecessor_paragraph']
        else:
            english=eff['effective_predecessor_paragraph'];note=RETENTIONS[index];decision='retention';retention=note
        assert english.isascii() and all(t not in english for t in ['{','}','\n','\r','%','FI','FA','FO'])
        assert not english.startswith(' ') and not english.endswith(' ')
        row.update(english=english,logical_English=english,speaker=speakers[row['source_selector']],
            source_meaning=row['source_gloss'],context=row['full_clean_exchange_context'],localization_note=note,
            decision=decision,editorial_decision='revise' if decision=='revision' else 'retain-wording',
            retention_reason=retention,editorial_finding=note,effective_predecessor=eff,
            original_voice_class={0:2,4:0,5:4,6:5}[row['source_selector']],
            whole_exchange_situation_voice_andprogression_reviewed=True,exact_source_macros_preserved=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=True,new_credit=0)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':8,'retention':7}
    byid={r['id']:r for r in rows};pathreviews=[]
    for i,path in enumerate(flow['representative_text_paths']):
        sequence=[dict(id=ident,speaker=byid[ident]['speaker'],english=byid[ident]['english']) for ident in path['source_speech_IDs']]
        assert len(sequence) in [5,7,11,14]
        pathreviews.append(dict(path=i,source_speech_IDs=path['source_speech_IDs'],English_exchange=sequence,
            complete_exchange_situation_referents_voice_andemotional_progression_reviewed=True,
            mutually_exclusive_alternatives_not_read_asconsecutive_speech=True,
            no_claim_of_audio_recording_oractual_branch_gameplay=True))
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NAMES,FLOW,GLOSS,CONTROL,Path(__file__)]}
    name_rows=[]
    for retention in names['naming_retentions']:
        actor=retention['actor_ID']
        name_rows.append(dict(actor_ID=actor,name=retention['name'],decision='retain-wording',reason=retention['reason'],
            clean_current_fields=next(r for r in names['complete_clean_andcurrent_name_fields'] if r['actor_ID']==actor),
            original_getters=[r for r in names['native_eight_progressive_andfull_getters']['rows'] if r['actor_ID']==actor],
            source_speech_IDs=[r['id'] for r in rows if r['source_selector']==actor],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            name_asset_changed=False,native_font_bounds_complete_names_actual_B47_headers_andcatalogue_UI_pending=True,new_credit=0))
    save(NAME_DOC,dict(format='dk4-source-context-speaker-name-review-v1',records=name_rows,
        native_proof=str(NAMES),native_proof_sha256=sha(NAMES.read_bytes()),mentioned_components=mentions,
        Janus_Pasar_not_Pasha_andno_inferred_political_association=True,
        four_scoped_retentions_andthree_mentioned_components_not_full207_approval=True,
        full207_name_role_alias_review_active=True,new_credit=0,full_goal_complete=False))
    save(DOC,dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],route=0,route_identity='Rafael',block=47,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        records=rows,revisions=8,retentions=7,source_current_packet=str(CURRENT),effective_packet=str(EFFECTIVE),
        names_packet=str(NAME_DOC),source_controls_packet=str(CONTROL),source_branch_context_packet=str(GLOSS),source_path_packet=str(FLOW),
        six_complete_English_exchange_reviews=pathreviews,complete_clean_glosses_prerequisite_names_andbranch_context_precede_current_comparison=True,
        all15_current_effective_templates_reviewed=True,source_macro_counts=dict(FI=0,FA=0,FO=0),
        all15_formatting_gates_false=True,formatting_review_pending=True,
        body_only_logical_draft_native_prefix_markup_stored_padding_andlayout_owned_by_formatter=True,
        source_selectors=sorted(speakers),FE_panels=0,typed_menu_count=0,
        R63_R70_exclusive_andthree_Janus_lines_conditional=True,
        six_source_path_reviews_not_claimed_as_actual_gameplay=True,
        no_invented_family_rank_alliance_guaranteed_recruitment_orcompleted_ambition=True,
        named_force_components_preserved_without_full_name_orcatalogue_approval=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        native_pages_complete_characters_bounds_pagination_actual_scene_policy_atomic_andrelease_pending=True,
        evidence=evidence|{str(NAME_DOC):sha(NAME_DOC.read_bytes())},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'15_contextual_decisions_six_complete_path_reviews_eight_revisions_seven_retentions.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAME_DOC),names_sha256=sha(NAME_DOC.read_bytes()),
        revisions=8,retentions=7,complete_path_reviews=pathreviews,mentioned_source_components=mentions,
        all15_source_context_localization_naturalness_gates_true_formatting_false=True,
        original_source_provenance_andall48_controls_not_mutated=True,
        no_ROM_registry_ledger_completion_credit_ornew_emulator_run=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    for r in rows:print(r['id'],r['decision'],r['speaker'],repr(r['english']))
    print('15 whole-path decisions:8 revisions/7 justified retentions;four scoped names/three mentioned components retained.Native display andrelease pending;zero credit.')
