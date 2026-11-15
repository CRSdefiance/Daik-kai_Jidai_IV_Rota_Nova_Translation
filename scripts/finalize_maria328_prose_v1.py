"""Seal complete-exchange prose andscoped names after exact current-consumer reconciliation."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT = Path('translations/maria_B73_B95_contextual_review_v1.json')
GATES = ['source','context','localization','naturalness','formatting']
NAME_REASONS = {
3: 'Retain approved Maria Li and full Maria Huamei Li. Her skepticism, compassion, anti-domination stance and uncertainty about the Proof do not add a religious affiliation, crown or family biography.',
4: 'Retain Janus Pasar in both consumers. His telescope story is reported and doubted, not a new name or confirmed historical identity.',
6: 'Retain Julio Erneco. Cristina is explicitly his granddaughter in this exchange, so grandfather is supported here; his concern does not imply she is incapable.',
7: 'Retain Cristina Erneco in both native consumers and Cristina in Julio/Maria body references. This is a spoken reference, not a newly observed speaker or global resolution of every older Christina occurrence.',
10: 'Retain Xien Yan. His mentor-like familiarity, guesses and tactical bluff give him neither family ties to Maria nor a church or army office.',
11: 'Retain Jam Ludwyan and full Jam Jack Ludwyan. The festival exclamation is his exuberant optional setup, not evidence all setup alternatives happen together.',
12: 'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His formal blade appreciation supports courteous diction, not an invented samurai rank or literal third-person this one.',
14: 'Retain Emilio Ferog. His personal food search remains his comic motivation, not a new crew mission or surname/occupation change.',
18: 'Retain Charles Rochefort and full Charles Jean Rochefort. His scientific curiosity and tentative amber hypothesis add no independently certified academic or medical credential.',
22: 'Retain Samwell Khan and full Samwell da Khan as the source-bound established forms. Da is a native component, not a newly inferred title, ancestry or real historical identity; the armor rumors establish no biography.',
114: 'Retain Port Worker for the source port-office worker. Familiar brother-like address is not kinship; regional metadata is not a name or nationality claim.',
137: 'Retain Senior Monk for 高僧. The religious stature is explicit in the source role; do not add a sect, personal name or government office.',
139: 'Retain Priest for 神父. The blessing and Trinitarian prayer support this generic religious role, not a specific denomination or new personal identity.',
148: 'Retain Guildmaster for the guild leader. The round-trip challenge, reward and ruins guidance supply no noble rank or personal name.',
151: 'Retain Sailor in the progressive consumer and Retainer in the separate catalogue for 配下. A source injury is not a death; regional metadata does not establish a surname.',
153: 'Retain Sailor/Retainer for the two actual consumers. The discovery complaint does not establish the nature of a deception, religion or a named military rank.',
156: 'Retain Sailor/Retainer for the explicit subordinate and current-startup fallback. Strict role getters return208 while speech dispatch resolves156 for selectors208/214/215; this is not an actual future lookout/rescuer assignment or roster claim.',
160: 'Retain Villager for 村民. His belief that visitors share his religion remains his assumption; neither regional metadata nor his plea establishes Maria\'s faith.',
163: 'Retain Boy for 男の子. His grandfather relationship is explicit, while his familiar older-sister farewell does not make Maria his sister.',
170: 'Retain Mysterious Old Man for 謎の老人. It is a natural source-supported role label for an initially unknown elder; the local grandson relationship does not justify globally renaming this shared actor Grandfather.',
177: 'Retain Sect Leader for 教祖 as a natural neutral role label. The fictional group\'s revelations and world-rule claims are his own; cult leader in Xien\'s teasing body line is descriptive, not another personal identity or a named real religion.',
178: 'Retain Follower for 信徒. Participation in this fictional sect is explicit; no real denomination, personal name or soldier rank follows.',
188: 'Retain Margrete in both current consumers for マルグレーテ. The readable established spelling is preferable to introducing a provisional Margarete variant from the clean gloss; Hamburg metadata is not a surname or biography.',
191: 'Retain Donna in both consumers for ドナ. The pilgrimage suggestion supplies no title, family relationship or nationality to append to her name.',
}
REFINEMENTS = {
'DK4_MES_B73_R0026': ('Through science! We use human reason to shed a little light on the wonders of this world that lie beyond our understanding.',
    'Read-aloud refinement removes an ambiguous it that could refer to the world rather than human understanding, preserving science\'s limited explanatory ambition.'),
'DK4_MES_B74_R0063': ("Now that you've compared Cristina to Minerva, I'd love to find that shield. If it really exists, I'd like her to have it...",
    'Give Julio a natural heartfelt wish instead of makes me want that shield very much, preserving the comparison, conditional existence and protective gift intention.'),
'DK4_MES_B78_R0022': ("The best food in the world... But how could you know there's nothing more delicious?",
    'Use natural food/taste comparison rather than the finest taste collocation; preserve Maria\'s skeptical question.'),
'DK4_MES_B85_R0019': ('Hm? Yes, of course.',
    'Express the priest\'s puzzled beat as a natural interjection instead of an isolated leading question mark before his permission.'),
'DK4_MES_B88_R0025': ("We are the chosen! We'll unearth the treasures recorded here and rule over those godless fools!",
    'Replace inventory-like listed treasure with natural villain dialogue and the source\'s pointing reference to treasures recorded here; these remain the leader\'s claims.'),
}


def main():
    names_out = ROOT/'scoped24_names_editorial_review_v1.json'
    proof_out = ROOT/'contextual_prose_qualification_v1.json'
    assert not any(p.exists() for p in [OUT,names_out,proof_out])
    proposals_path = ROOT/'all328_contextual_proposals_v1.json'
    name_path, term_path, role_path = [ROOT/n for n in ['scoped_names_macros_reference_v1.json','scoped_terms_reference_v1.json','dynamic_roles_current_v1.json']]
    objects_path = ROOT/'current_objects_v1/current_objects.json'
    proposals,names,terms,roles,objects = map(load,[proposals_path,name_path,term_path,role_path,objects_path])
    runtime = proposals['runtime']
    assert runtime == names['runtime'] == terms['runtime'] == roles['runtime'] == objects['runtime']
    assert len(proposals['records']) == 328 and {r['actor_ID'] for r in names['records']} == set(NAME_REASONS)
    assert terms['full_Proof_term']['singular'] == 'Proof of Conquest'
    assert roles['source_selectors'] == [207,208,214,215]
    role_forms = {r['source_selector']:r for r in roles['native_roles']['rows']}
    scoped, forms = [], {}
    for original in names['records']:
        row = deepcopy(original)
        actor = row['actor_ID']
        approved = {c['consumer']:c['text'] for c in row['current_consumers']}
        assert set(approved) == {'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor] = approved['progressive-nameplate']
        reason = NAME_REASONS[actor]
        row.update(id=f'SC3_B73_B95_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,
            english=forms[actor],speaker=forms[actor],context='Complete Maria B73–B95 source exchanges andexact short/full native consumers;scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            decision='retention',finding=reason,localization_note=reason,retention_reason=reason,
            review={g:g!='formatting' for g in GATES},name_localization_andfresh_display_approval_pending=False,
            fresh_native_display_orcompatible_proof_binding_pending=True,unused_metadata_not_globally_approved=True,
            no_global207_name_approval=True,new_credit=0)
        scoped.append(row)
    save(names_out,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=scoped,scoped_actors=24,runtime=runtime,individual_name_retentions=24,first_four_gates_pass=True,
        formatting_gates_pending=True,no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [name_path,term_path,role_path,Path(__file__)]}))
    rows, amendments = deepcopy(proposals['records']), []
    for row in rows:
        before = text = row['english']
        notes = []
        if "Conqueror's Proof" in text:
            assert row['id'] in ['DK4_MES_B83_R0004','DK4_MES_B89_R0015','DK4_MES_B94_R0017']
            text = text.replace("Conqueror's Proof",'Proof of Conquest')
            notes.append('Reconcile the legacy full term to Proof of Conquest, the singular of the exact registered Proofs of Conquest story anchor; native short UI forms remain Proof/Conq Proof.')
        if row['id'] in REFINEMENTS:
            text, note = REFINEMENTS[row['id']]
            notes.append(note)
        if text != before:
            amendments.append(dict(id=row['id'],before=before,after=text,reason=' '.join(notes)))
            row['finding'] += ' '+' '.join(notes)
            row['localization_note'] = row['finding']
            if row['decision'] == 'retention':
                row.update(decision='revision',retention_reason='')
        assert not any(row['review'].values())
        assert row['source_meaning'] and row['finding'] and row['whole_exchange_context']
        assert text.isascii() and text.strip() == text and not any(t in text for t in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert {t:text.count(t) for t in row['source_macros']} == row['source_macros']
        assert not re.findall(r'\bF(?!I\b|A\b|O\b|U\b)[A-Z]\b',text)
        assert (text == row['current_comparison_paragraph']) == (row['decision'] == 'retention')
        if row['decision'] == 'retention':
            assert row['retention_reason']
        source_kind, selector = row['kind'], row.get('source_selector')
        if source_kind == 'typed-menu-caption':
            kind, speaker = 'typed-choice-label', 'Player choice in source puzzle'
        elif source_kind == 'physical-style-alternative':
            assert selector in [208,214,215]
            kind, speaker = 'progressive', f'Dynamic style selector{selector};original voice slots{row["source_style_indices"]};conditional assignment unvisited'
            obj = next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
            row.update(native_object_kind='4100-style-alternative',source_object_hex=obj['source_object_hex'],
                source_choice_object_hex=obj['source_object_hex'],virtual_formatter_prefix_not_in_stored_body=True,
                current_record_index=row['current_reference']['physical_record_index'])
        else:
            assert source_kind == 'ordinary-speech'
            if selector == 254:
                kind = 'system-FE'
                speaker = 'FE unpictured riddle voice' if row['block'] in [87,92] else 'FE system message' if row['block']==91 or row['id']=='DK4_MES_B93_R0099' else 'FE unpictured voice/narration'
                assert row['source_complete_preamble_hex'] == '0040ffff00fe' and row['source_hex'].startswith('fe')
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            elif selector in role_forms:
                kind = 'progressive'
                speaker = 'Maria (native captain selector207)' if selector==207 else f'Dynamic role selector{selector};startup fallback {forms[role_forms[selector]["resolved_actor_ID"]]};conditional assignment unvisited'
            else:
                assert selector in forms
                kind, speaker = 'progressive', forms[selector]
        row.update(english=text,logical_English=text,proposed_English=text,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},current_English_not_consulted=False,current_English_now_exposed=True,
            names_terms_consumers_andfresh_display_approval_pending=False,approved_names_terms_titles_andruntime_substitutions_pending=False,
            scoped_prose_name_term_references=[str(names_out),str(term_path),str(role_path)],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,
            registered_release_and_completion_credit_pending=True)
    counts, kinds = Counter(r['decision'] for r in rows), Counter(r['kind'] for r in rows)
    assert counts == {'revision':143,'retention':185} and kinds == {'progressive':286,'system-FE':27,'typed-choice-label':15}
    assert len(amendments) == 8 and len(rows) == 328
    doc = dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=sorted({r['block'] for r in rows}),
        records=rows,source_objects=328,complete_exchanges=21,proposed_revisions=143,justified_retentions=185,runtime=runtime,
        current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],scoped_name_term_andreadaloud_amendments=amendments,
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        all328_paragraphs_read_in21_complete_exchanges=True,native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [proposals_path,name_path,names_out,term_path,role_path,objects_path,Path(__file__)]})
    structural = deepcopy(doc)
    structural['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(structural)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as exc:
        assert 'v2 requires per-record' in str(exc)
        blocked = str(exc)
    else:
        raise AssertionError('Unformatted prose passed release gate')
    save(OUT,doc)
    save(proof_out,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=328,complete_exchanges=21,
        revisions=143,retentions=185,scoped_name_retentions=24,first_four_individual_gates_pass=True,all_fifth_gates_false=True,
        exact_macro_counts=dict(FI=2,FA=0,FO=0,FU=0),structural_projection_pass=True,
        unformatted_manuscript_rejected_by_release_gate=blocked,amendments=amendments,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed328 four-gate prose decisions:143 revisions/185 retentions;24 scoped names;formatting andintegration remain pending.')


if __name__ == '__main__':
    main()
