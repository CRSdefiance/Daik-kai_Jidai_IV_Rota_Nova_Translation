"""Record42 scoped name decisions and approve the three new offline name-plane sets."""
from copy import deepcopy
from pathlib import Path

from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT
from scripts.review_hodram_B0_B41_contextual_v1 import OUT as PROSE

OUT=Path('translations/hodram_B0_B41_scoped_names_review_v1.json')
REASONS={
0:'Retain approved Rafael Castor as a reference identity. This extra table reference does not make Rafael an observed speaker in this SC1 scope.',
1:'Retain approved Hodram and Joakim, with Bergstrom. The two native consumers intentionally distinguish Hodram Bergstrom from Hodram Joakim Bergstrom; royal service and admiral address add no new nameplate title.',
2:'Retain Lil Argot. Her accusation in the disguised-fleet scene is a mistaken belief, not proof that Maria attacked her, and no new relationship is added.',
3:'Retain approved Maria Li and full Maria Huamei Li. The source full spoken name is preserved while this table reference does not invent Maria’s on-scene presence or a religious biography.',
7:'Retain Cristina Erneco for source actor7. Her optional rescue intervention is not Lil’s line. The wider Cristina/Christina consumer distinction stays separately open; this is not a global alias rewrite.',
9:'Retain approved Camille, with Overijssel and explicit Marinus in the full-name consumer. His personal familiarity with Kuhn and Maria’s warning do not add kinship, an occupation or a new rank.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. Formal swordsman speech does not create a lord title or a family relationship with Al.',
16:'Retain Gerhard Adernkatz. His formal counsel, tactical concerns and human observations remain his voice; no age or family label is appended.',
17:'Retain Al Shin and full Al Ferid Shin. His rescue and concern for Aziza establish no romance, marriage or new title.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort. Tactical gunnery and excited assistance add no scientist title or military rank to the name.',
20:'Retain Fernando Dias and the earlier repaired ASCII initial. His wager against Espinosa is dialogue, not a new gambler occupation label.',
23:'Retain Manuel Almeida. His poem, prayers and practical calls do not justify a priest, poet or navigator title in the nameplate.',
24:'Retain Sera Shahrbaraz and full Sera Altos Shahrbaraz. B15’s embedded anonymous Foreign Girl label must remain unrevealing; B40’s named native actor and opaque cry do not justify translating her language.',
27:'Retain Aziza Nurennahar. Her explicitly pirate father and later renunciation are story facts; her grateful joining does not add a romance, ransom-debt contract or new family label.',
29:'Retain Martin Speyer. The Hanseatic cog identification and attack are scene context, not an invented shipowner title or historical identity.',
33:'Retain Hardum Pasha and full Hardum Ahmet Pasha as the source-bound components. Pasha is used as the source’s address; do not invent Lord or a new biographical claim.',
34:'Retain Barbarossa Hayreddin and full Barbarossa Fazul Hayreddin. The carried-on Barbarossa name is explicit, but biological descent or a separate formal title is not.',
36:'Retain Geronimo Espinosa and full Geronimo de Espinosa. Keep the already qualified de component; the challenge does not prove a new rank or nationality.',
37:'Retain Abraham Uddin and full Abraham Ibn Uddin. His explicit Muslim claim is his antagonistic speech, not a newly invented religious office in his label.',
40:'Retain Antony Kuhn and full Antony von Kuhn. Correct Kuen in this dialogue to the registered identity. Do not silently identify the fictional character with an external historical Coen or infer nationality from a particle.',
41:'Retain Sojin Kurushima. The Ming/foreigner insult does not create a new employer title or a real-world identity in the name.',
42:'Retain Vasquez Maldonado and full Vasquez de Maldonado. Keep the explicit existing de component; fleet numbers and contempt add no rank.',
43:'Retain Diogo Escante and full Diogo de Escante. His source pact and help identify a conditional ally, not a permanent merged faction or newly titled sovereign.',
52:'Retain Mushari Sidra and full Mushari Es Sidra. The withdrawal orders refer to his fleet; the source component Es is not expanded into an invented title or ancestry.',
53:'Retain Arnajud Jaume. Use the same Arnajud in the two-fleet order rather than the dialogue’s Al Najuud variant; do not invent a title or split one source component into unproved names.',
55:'Retain the existing David Flahven spelling and normalize only its mismatched full-width surname initial F. Both native consumers currently display the defect.',
56:'Render the explicit ザルツギッター surname as Salzgitter, retaining Georg and its source pronunciation. The surname supplies no birthplace, historical identity or title.',
57:'Render the explicit カムロ surname as Kamuro, retaining Nagayoshi. Do not infer kanji, a military office or a real-world warrior identity.',
60:'Retain Juan Blanco. His friendly reinforcement offer remains a distinct conditional speaker, not another name for Escante.',
63:'Retain Julian Vermeer. His drinking and alleged betrayal supply no new occupation title, nationality or moral label in his nameplate.',
65:'Retain registered Plett Perrault and correct Prett in the story. The murder accusation and claimed remorse do not create a new title or certify innocence.',
66:'Retain Jean Ramusio. His smuggling defense remains a self-serving claim, not a biographical nameplate description.',
68:'Retain Jacob Portunto. The stolen-cargo complaint and Calicut escort do not add an official pirate rank or a new spelling.',
71:'Retain William Clive. Screeches and repeated threats do not become a psychiatric label, an animal identity or a magical title.',
72:'Retain Hernan Berio. His fighting boasts and Athens custody supply no invented Lord title, historical identity or alternate Berrio surname.',
73:'Retain Iscal Yasar. The royal target and defeat sequence add no new rank, title or narrator-certified death to the name.',
78:'Retain Sirwood Eme. The symbol-based foreign cry remains semantically opaque; Sirwood is a name component, not the English title Sir.',
151:'Retain Sailor in the progressive consumer and Retainer in the full-name consumer for 配下. European metadata is not a surname or an actor-specific biography; dynamic role assignments remain to bind separately.',
153:'Retain Sailor and Retainer in the two actual name consumers for 配下. The Islamic-region slot does not establish a distinct personal name or ethnicity; unused region metadata is not approved as player prose here.',
183:'Retain Angel as the source’s one-component pirate name. Rough speech supplies no invented gender, surname, religious identity or rank.',
184:'Retain Snake as the source’s one-component pirate name. The mutiny and command assignment do not add a serpent identity or an official rank to the label.',
185:'Retain Dandy as the source’s one-component pirate name. The formal readiness reply and ransom demand do not create a noble title or new surname.',
}


def main():
    assert not OUT.exists()
    bound_path=ROOT/'scoped_names_current_v1.json'
    proof_path=ROOT/'name_field_checks_v1/native_name_fields_verification.json'
    proposal_path=ROOT/'name_field_inputs_v1/owned_fields_proposal.json'
    bound,proof,proposal,prose=map(load,(bound_path,proof_path,proposal_path,PROSE))
    assert bound['original_native_name_getters']==84 and bound['scoped_actors']==42
    assert set(REASONS)=={r['actor_ID'] for r in bound['records']}
    assert proof['proposal_sha256']==digest(proposal_path)
    assert len(proof['planes'])==12 and len(proof['consumer_plane_bindings'])==24
    assert len(proof['negative_cases_rejected'])==8
    assert proof['name_data_plan']['complete_parent_inverse_exact'] and proof['no_ROM_created']
    sheet=Path(proof['review_sheet']['path'])
    assert digest(sheet)==proof['review_sheet']['sha256']
    assert all(digest(p['preview'])==p['preview_sha256'] and p['complete_glyphs_bounds_andindependent_pixels_pass'] for p in proof['planes'])
    amended=next(v for v in proof['versions'] if v['version']=='proposed')['names']['rows']
    fields={r['actor']:r for r in proposal['fields']}
    rows=[]
    for old in bound['records']:
        actor=old['actor_ID'];row=deepcopy(old)
        forms=[deepcopy(r) for r in amended if r['actor_ID']==actor] if actor in fields else deepcopy(old['current_consumers'])
        assert len(forms)==2
        row.update(decision='revision' if actor in fields else 'retention',finding=REASONS[actor],
            localization_note=REASONS[actor],proposed_consumers=forms,
            source_reference=dict(actor_ID=actor,fields=[f for f in old['source_andcurrent_fields']]),
            current_reference=dict(candidate=bound['target_candidate'],candidate_sha256=bound['target_candidate_sha256'],
                actor_ID=actor,original_consumers=old['current_consumers']),
            context_record_ids=[r['id'] for r in prose['records'] if r.get('source_selector')==actor],
            source_fields_are_not_automatic_biography_orunused_metadata_approval=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_plane_status='fresh-proposed-and-current-planes-directly-viewed' if actor in fields else 'exact-compatible-plane-reuse-orfresh-check-pending',
            representative_gameplay_andregistered_name_layer_pending=actor in fields,
            full_catalogue_UI_unvisited=True,new_credit=0)
        if actor in fields:row['owned_field_proposal']=fields[actor]
        rows.append(row)
    approval=ROOT/'name_field_visual_approval_v1.json';assert not approval.exists()
    save(approval,dict(native_verification=str(proof_path),native_verification_sha256=digest(proof_path),
        review_sheet=str(sheet),review_sheet_sha256=digest(sheet),all12_current_andproposed_planes_directly_viewed=True,
        proposed_names=['David Flahven','Georg Salzgitter','Nagayoshi Kamuro'],
        normal_ASCII_F_andcomplete_leading_trailing_characters_visible=True,
        independent_native_pixel_bounds_character_codes_and8_rejections_pass=True,
        only28_owned_data_bytes_change_with_exact_whole_ARM9_inverse=True,
        offline_styles11_and1_not_actual_catalogue_UI_ornew_gameplay=True,
        actual_headers_registered_layer_andown_candidate_startup_pending=True,new_credit=0))
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',records=rows,scoped_actors=42,
        justified_retentions=39,name_revisions=3,original_current_getters=84,
        corrected_name_fixture_getters=12,corrected_name_unique_planes=12,corrected_name_consumer_style_bindings=24,
        three_corrected_name_plane_sets_visually_approved=True,
        retained_name_plane_dependency_reuse_orfresh_check_pending=True,
        full_catalogue_UI_unvisited=True,no_global207_name_approval=True,
        dynamic_roles_andremaining_terms_pending=True,registered_integration_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (bound_path,proof_path,proposal_path,approval,PROSE,Path(__file__))}))
    print('Saved42 name decisions:39 retentions/3 revisions. All12 changed-name planes viewed; actual/registered checks remain.')


if __name__=='__main__':main()
