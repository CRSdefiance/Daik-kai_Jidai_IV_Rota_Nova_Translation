"""Record individual contextual name decisions and bind their exact existing evidence."""
from pathlib import Path
from copy import deepcopy

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

MANUSCRIPT = Path('translations/hodram_B131_B150_editorial_manuscript_v2.json')
ROOT = Path('work/analysis/Hodram_B131_B150_editorial_20261102')
IDENTITIES = Path('work/analysis/Hodram_B131_B150_clean_20261102/native_identity_reuse_checkpoint.json')
FRESH = Path('work/analysis/Hodram_B131_B150_new_names_20261102/names.json')
KNOWN = Path('work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json')
MENTIONED = Path('work/analysis/Hodram_B131_B150_clean_20261102/mentioned_name_components.json')
THREE = Path('work/analysis/Hodram_B131_B150_two_name_sources_20261102/complete_three_owner_names.json')
PROPOSAL = Path('work/analysis/Hodram_B131_B150_name_fields_20261102/owned_fields_proposal_v2.json')

DECISIONS = {
    0: ('Rafael Castor', 'Retain the approved Rafael spelling and source Castor surname. B143 actor0 is this original character, not the active captain or an invented rank.'),
    1: ('Hodram Bergstrom', 'Retain approved Hodram and Joakim and the established Bergstrom surname; keep Joakim in the full-name consumer rather than adding it to the ordinary nameplate.'),
    4: ('Janus Pasar', 'Retain the established rendering of ジェナス・パサー consistently with earlier crew exchanges; the name supplies no new rank or family relationship.'),
    13: ('Cesare Tony', 'Retain the established Cesare Tony spelling for チェザーレ・トーニ in these trade and item exchanges; preserve his identity across consumers without an unsupported new spelling.'),
    16: ('Gerhard Adernkatz', 'Retain established Gerhard Adernkatz for ゲルハルト・アーデルンカッツ, consistent with his counsel throughout the complete exchanges.'),
    18: ('Charles Rochefort', 'Retain Charles Rochefort and full-name Charles Jean Rochefort, matching シャルル・ジャン・ロシュフォール. His private motive remains undisclosed; the name adds no biography.'),
    23: ('Manuel Almeida', 'Retain Manuel Almeida for マヌエル・アルメイダ, keeping the established identity and spelling across his advice and item explanations.'),
    24: ('Sera Shahrbaraz', 'Retain Sera Shahrbaraz and full Sera Altos Shahrbaraz. The B142 naming exchange explicitly supplies the name; do not rename her, invent an adoption or marriage, or treat the language barrier as already resolved.'),
    26: ('Julian Lopes', 'Retain the established Julian Lopes for ユリアン・ロペス, consistent with the complete bamboo-assembly exchange and earlier crew dialogue.'),
    36: ('Geronimo Espinosa', 'Keep the established progressive name and render the explicit full-name デ as de. The full name is Geronimo de Espinosa; the particle adds no noble title or biography.'),
    38: ('Zamorin Nagarpur', 'Retain source ザモリン・ナガルプル and full ザモリン・アフマド・ナガルプル as Zamorin Nagarpur / Zamorin Ahmad Nagarpur; preserve the source-supported title/name form without inventing another office or relationship.'),
    42: ('Vasquez Maldonado', 'Keep the established progressive name and render the explicit full-name デ as de. Retain Vasquez de Maldonado without adding a new title or family fact.'),
    43: ('Diogo Escante', 'Retain progressive Diogo Escante and already corrected full-name Diogo de Escante. The earlier registered de repair remains intact; do not regress or re-credit it.'),
    49: ('Alonso Rosa', 'The shared component also belongs to clean アロンソ・デ・ローサ. Retain progressive Alonso Rosa and localize only the explicit full-name デ as de; this ownership extension is not evidence that Alonso appears in B131–B150.'),
    58: ('Jorge Albacete', 'Retain Jorge Albacete for ホルヘ・アルバセテ, consistently identifying the source speaker without expanding his role or biography.'),
    92: ('Barkeep', 'Retain natural Barkeep for 酒場の親父. The label identifies the tavern proprietor; translating 親父 as a family relationship would invent one.'),
    113: ('Port Worker', 'Retain natural Port Worker for 出港所の兄貴. The familiar 兄貴 does not establish brotherhood or an officer rank; the workplace supplies the supported role.'),
    147: ('Guildmaster', 'Retain Guildmaster for ギルドの元締め: the source identifies the guild head, so this occupational label is supported and does not invent a nobiliary or military rank.'),
    151: ('Sailor', 'Retain nameplate Sailor for 水夫 and the separate catalogue label Retainer for 配下, following the existing individual review of these distinct native consumers. These are generic roles; a fallback actor does not establish a future conditional participant.'),
    203: ('Sakura', 'Retain Sakura for さくら in the complete B131 gift exchange. Osaka is the source-supported place in that exchange; do not turn 大坂 metadata into an asserted personal surname or a new full-name-consumer approval.'),
}


def ref(path, key, index=None):
    result = dict(path=str(path), sha256=sha(path.read_bytes()), key=key)
    if index is not None:
        result['index'] = index
    return result


def main():
    output = Path('translations/hodram_B131_B150_speaker_name_review_v1.json')
    assert not output.exists()
    doc, identities, fresh, known, mentioned, three = map(load, [MANUSCRIPT, IDENTITIES, FRESH, KNOWN, MENTIONED, THREE])
    proofs = {x['actor_ID']: Path(x['prior_proof']) for x in identities['ten_known_actor_reuses']}
    proofs.update({a: FRESH for a in fresh['actors']})
    rows = []
    for actor, (english, reason) in DECISIONS.items():
        references, consumers = [], []
        if actor in [36, 42, 49]:
            for version in ['clean_names', 'current_names']:
                for i, row in enumerate(three[version]['rows']):
                    if row['actor_ID'] == actor:
                        references.append(ref(THREE, version + '.rows', i))
                        consumers.append(dict(version=version, consumer=row['consumer'], text=row['text'], text_hex=row['text_hex']))
        elif actor == 203:
            i = next(i for i, r in enumerate(mentioned['records']) if r['actor_ID'] == actor)
            references.append(ref(MENTIONED, 'records', i))
        elif actor in [1, 16, 18]:
            i = next(i for i, r in enumerate(known['complete_clean_current_static_fields']) if r['actor_ID'] == actor)
            references.append(ref(KNOWN, 'complete_clean_current_static_fields', i))
            for i, row in enumerate(known['fresh_thirtytwo_progressive_andfull_current_getters']['rows']):
                if row['actor_ID'] == actor:
                    references.append(ref(KNOWN, 'fresh_thirtytwo_progressive_andfull_current_getters.rows', i))
                    consumers.append(dict(version='current_names', consumer=row['consumer'], text=row['text'], text_hex=row['text_hex']))
        elif actor == 43:
            pass  # The separately corrected registered consumer is bound below.
        else:
            path = proofs[actor]
            native = load(path)
            for version in ['clean_names', 'current_names']:
                for i, row in enumerate(native.get(version, {}).get('rows', [])):
                    if row['actor_ID'] == actor:
                        references.append(ref(path, version + '.rows', i))
                        consumers.append(dict(version=version, consumer=row['consumer'], text=row['text'], text_hex=row['text_hex']))
        if actor == 43:
            prior = Path('translations/hodram_B111_B130_speaker_name_review_final_v1.json')
            reviews = load(prior)['records']
            references.append(ref(prior, 'records', next(i for i, r in enumerate(reviews) if r['actor_ID'] == actor)))
        assert references, actor
        contexts = [r['id'] for r in doc['records'] if r.get('source_selector') == actor]
        if actor == 151:
            contexts += [r['id'] for r in doc['records'] if r.get('source_selector') == 214]
        if actor in [36, 42, 203]:
            token = {36: 'Espinosa', 42: 'Maldonado', 203: 'Sakura'}[actor]
            contexts += [r['id'] for r in doc['records'] if token in r['english']]
        revised = actor in [36, 42, 49]
        rows.append(dict(id=f'ACTOR_{actor}_SC1_B131_B150_SCOPED_NAME_REVIEW', actor_ID=actor,
                         english=english, context_reference=str(MANUSCRIPT), context_record_ids=sorted(set(contexts)),
                         exact_source_current_references=references, consumers=consumers,
                         decision='revision' if revised else 'retention', finding=reason,
                         localization_note=reason, retention_reason=None if revised else reason,
                         review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
                         alias_ownership_only_no_new_scene_appearance=actor == 49,
                         mention_only_no_full_catalogue_identity_approval=actor == 203,
                         actual_full_catalogue_UI_unvisited=True, new_dialogue_credit=0))
    native_paths = [Path('work/analysis/Hodram_B131_B150_name_native_20261102/native_name_fields_verification.json'),
                    Path('work/analysis/Hodram_B131_B150_retained_name_native_20261102/native_name_fields_verification.json')]
    reviewed_paths = []
    for path in native_paths:
        proof = load(path)
        assert len(proof['negative_cases_rejected']) == 13
        assert proof['name_data_plan']['owned_span_bytes'] == 4
        assert proof['name_data_plan']['complete_parent_inverse_exact']
        assert all(p['complete_glyphs_bounds_andindependent_pixels_pass'] for p in proof['planes'])
        reviewed = deepcopy(proof)
        reviewed.update(original_pending_report=str(path), original_pending_report_sha256=sha(path.read_bytes()),
                        offline_visual_approved=True, direct_view_pending=False,
                        visual_review_note='Every newly generated name/style plane directly viewed at readable scale; complete initial/final letters, spaces and de components fit the proven native bounds. Actual catalogue UI remains unvisited.')
        target = path.with_name('native_name_fields_verification_reviewed.json')
        assert not target.exists()
        save(target, reviewed)
        reviewed_paths.append(target)
    assert len(rows) == 20 and sum(r['decision'] == 'revision' for r in rows) == 3
    save(output, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', records=rows,
                      actors=list(DECISIONS), revised_name_identities=3, retained_name_identities=17,
                      dynamic_role_review=dict(source_selector=214, role_index=7,
                          source_bound_personality_object='SC1 block133 offset10',
                          current_original_fallback='Sailor; actor151, voice4',
                          source_proof=str(IDENTITIES), source_proof_sha256=sha(IDENTITIES.read_bytes()),
                          review='Preserve the original role resolver and eight personality alternatives. The initialized fallback is not an assigned participant in every future conditional scene.'),
                      source_and_current_native_bindings_exact=True, scoped_context_not_global207_name_approval=True,
                      native_planes_directly_viewed=32, native_getters_current_and_proposed=32,
                      owned_name_span_bytes=4, reviewed_physical_name_fields=2, reviewed_field_owners=3,
                      all_five_gates_pass_in_scoped_context=True, registered_deployment_pending=True,
                      no_new_dialogue_orcompletion_credit=True, new_credit=0,
                      evidence={str(p): sha(p.read_bytes()) for p in [MANUSCRIPT, IDENTITIES, FRESH, KNOWN, MENTIONED, THREE, PROPOSAL, *reviewed_paths, Path(__file__)]}))
    print('PASS20 scoped name decisions:3 corrections/17 justified retentions;32 viewed native planes;4 owned bytes;deployment pending.')


if __name__ == '__main__':
    main()
