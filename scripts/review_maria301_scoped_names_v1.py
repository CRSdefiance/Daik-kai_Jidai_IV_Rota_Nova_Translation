"""Document36 contextual name/role retentions; font/display gates remain pending."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
REASONS = {
1: 'Retain approved Hodram and Joakim with Bergstrom. The two native forms intentionally differ by the middle component. Assistance against a common foe and tactical blame add no new rank or permanent alliance.',
2: 'Retain established Lil Argot. Her pride, rescue debt, mistaken accusation and apology belong to the same character; familiar calls do not establish kinship or a new title.',
3: 'Retain approved Maria Li and full Maria Huamei Li. The existing components agree with the settled naming policy. Her command and compassion do not add a noble, religious or family biography.',
7: 'Retain Cristina Erneco for the optional rescue speaker. Her contempt for ganging up belongs to this actor, not Lil. The separate Cristina/Christina consumer audit is not globally resolved here.',
9: 'Retain approved Camille, with Overijssel and explicit Marinus in the full-name form. His familiarity with Lil and the received warning add neither a family relationship nor a new occupation.',
10: 'Retain Xien Yan as the established source-bound rendering. Formal counsel, mentor-like praise and sea reflections do not make Grandpa or another family/age label appropriate.',
11: 'Retain Jam Ludwyan and full Jam Jack Ludwyan. Boisterous victory and rescue cries remain his voice; Jack is a native name component, not an additional speaker or invented nickname.',
12: 'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. Samurai diction is supported, but Al-dono must not confer Lord rank or a family relationship.',
16: 'Retain Gerhard Adernkatz. Recognition of an unnamed previously relinquished object supplies no reason for its loss, former-owner biography or additional title.',
17: 'Retain Al Shin and full Al Ferid Shin. His forceful rescue and concern for Aziza establish no romance, marriage or noble rank; address Maria as Admiral rather than Sir.',
21: 'Retain Ian Dukov. The alternative authenticity argument and ghost-ship question belong to Ian; do not assume that every alternative speaker is simultaneously present.',
23: 'Retain Manuel Almeida. His sea/mother poem does not prove his mother died or supply a priest/poet title for the nameplate.',
25: 'Retain Yifa Sol as the established readable rendering of the source components. Her objection to self-serving fabrication adds no new rank, origin or relationship.',
26: 'Retain Julian Lopes for actor26. His chivalric intervention and dismay are not actor63 Julian Vermeer’s lines; a shared given name does not merge their identities.',
27: 'Retain Aziza Nurennahar. Her pirate father and request to be called simply Aziza are explicit; the keepsake and grateful recruitment add no marriage, romance or ransom-service contract.',
28: 'Retain James Clifford. His manipulation, insults and fire metaphor do not establish an actual fire injury or a new title.',
31: 'Retain Pedro Valdes and full Pedro de Valdes as the reference identity mentioned by Maria and Escante. He is not a newly observed speaker; the explicit de component adds no invented nobility.',
40: 'Retain Antony Kuhn and full Antony von Kuhn. Reconcile Kuen in the dialogue to this registered identity. Sama does not support Lord, and the particle does not prove a real-world historical identity.',
41: 'Retain Sojin Kurushima. Rough ane-san address is not a sister relationship; the samurai quarrel and coercion add no new formal rank or real-world biography.',
42: 'Retain Vasquez Maldonado and full Vasquez de Maldonado as the mentioned reference identity. His reported words are not a new on-scene utterance or proof of a new relationship.',
43: 'Retain Diogo Escante and full Diogo de Escante. Conqueror is the source’s contextual address; independence rhetoric does not establish a lawful new crown or benevolent motive.',
44: 'Retain Robert Stork for actor44 in the ambush. Preserve the separate source reference to Richard in B30 instead of silently renaming either actor to reconcile different passages.',
57: 'Retain the registered Nagayoshi Kamuro surname correction. The source カムロ supports Kamuro; the iron-armored ships do not establish a historical warrior identity or a new office.',
64: 'Retain Yuris Huygens. His boast about elite noble birth remains a claim in dialogue, not a new titled nameplate or a narrator-certified biography.',
67: 'Retain Gabriel Cardocci as the existing source-bound rendering of ガブリエル/カルドッチ. Agreement violations and repeated encounters add no alternate person or historical identity.',
68: 'Retain Jacob Portunto. An illicit trader’s piracy and cargo complaint do not justify a more specific smuggling conviction or new captain rank in the nameplate.',
71: 'Retain William Clive. His unusual cackles, shrieks and curses do not make him an animal, establish a mental-health label or prove a magical power.',
72: 'Retain Hernan Berio in both native consumers. Correct Berrio in Maria’s spoken identification; fighting boasts and Athens custody do not support an alternate surname or Lord title.',
74: 'Retain Richard Townsend. The shocked ship question and separate explicit Richard reference do not make him Robert Stork or reveal a new employer beyond the source exchange.',
151: 'Retain Sailor on the progressive nameplate and Retainer in the separate catalogue for 配下. European-region metadata is not a surname or an approved ethnicity label.',
153: 'Retain Sailor/Retainer in the two actual consumers. Islamic-region metadata supplies neither a personal name nor a newly approved religious biography.',
155: 'Retain Sailor/Retainer for the subordinate warning Kuhn. Southeast-Asian metadata is not a surname or a newly established nationality.',
156: 'Retain Sailor/Retainer for the current startup’s dynamic fallback actor. The strict role slot is unassigned; this does not make actor156 an actually assigned or observed B32 lookout. East-Asian metadata is not a surname.',
183: 'Retain the one-component pirate name Angel. Enthusiastic maneuvering and mutiny do not create a surname, gender claim, religious identity or rank.',
184: 'Retain the one-component pirate name Snake. Command assignment and taunts do not make him a literal serpent or add an official rank to the name.',
185: 'Retain Dandy as the source’s one-component pirate name. A formal readiness reply and a ransom question do not establish nobility or a new surname.',
}


def main():
    out = ROOT/'scoped36_name_editorial_review_v1.json'
    assert not out.exists()
    names_path = ROOT/'scoped36_name_bindings_v1.json'
    proposals_path = ROOT/'all301_contextual_proposals_v1.json'
    roles_path = ROOT/'dynamic_roles_current_v1.json'
    names,proposals,roles = map(load,[names_path,proposals_path,roles_path])
    assert names['runtime']==roles['runtime'] and proposals['records_count']==301
    assert len(names['records'])==len(REASONS)==36 and {r['actor_ID'] for r in names['records']}==REASONS.keys()
    records=[]
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID']
        row.update(decision='retention',finding=REASONS[actor],retention_reason=REASONS[actor],
            localization_note=REASONS[actor],
            source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=names['runtime']['candidate'],candidate_sha256=names['runtime']['candidate_sha256'],
                actor_ID=actor,original_consumers=row['current_consumers']),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            final_font_complete_glyph_bounds_andrepresentative_display_checks_pending=True,
            source_components_not_automatic_biography_orunused_metadata_approval=True,
            no_global207_name_approval_ornew_dialogue_credit=True,new_credit=0)
        records.append(row)
    save(out,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',records=records,
        scoped_actors=36,justified_name_retentions=36,name_field_revisions=0,
        original_native_getters_bound=72,fresh_supplementary_getters=2,exact_reused_getters=70,
        all_four_name_prose_gates_pass=True,all_name_formatting_gates_pending=True,
        spoken_Berio_andKuhn_fixes_in_dialogue_proposals_not_name_table_patches=True,
        dynamic_startup_role_not_new_scene_assignment=True,no_global_name_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [names_path,proposals_path,roles_path,Path('docs/glossary.md'),Path(__file__)]}))
    print('Saved36 contextual name/role retentions;72 current getter bindings;name formatting remains pending;zero credit.')


if __name__=='__main__':
    main()
