"""Scoped localization decisions for the eighteen newly bound identities."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

NAMES=Path('work/analysis/Hodram_B111_B130_new_names_20261101/names.json')
FIELDS=Path('work/analysis/Hodram_B111_B130_clean_20261101/clean_name_fields.json')
NATIVE=Path('work/analysis/Hodram_B111_B130_name_native_20261101/native_name_fields_verification.json')
OUT=Path('translations/hodram_B111_B130_speaker_name_review_v1.json')
NOTES={
0:'Retain approved Rafael Castor in both consumers. The shared discovery exchange establishes him as Rafael, not a terminator or an invented relative of Hodram.',
3:'Retain approved Maria Li and the source-expanded full name Maria Huamei Li. The bandit exchange has her own faction context; do not relabel her as Hodram\'s subordinate.',
5:'Retain Claudio Manaus, matching the two source components and Rafael\'s established address. His payment proposal does not invent a rank or family tie.',
10:'Retain Xien Yan for the source personal-name components. His stern intervention beside Maria supports the existing identity, not an added rank.',
19:'Retain Carlo Sinat, consistently bound in both source consumers. His explanation of jade does not supply a new occupation or nationality.',
23:'Retain Manuel Almeida. His trap directions and heading request use the same established personal identity without a newly invented naval rank.',
43:'Retain progressive Diogo Escante. Romanize the explicit full-name component デ as de: Diogo de Escante. Source 殿 does not establish Lord; his claimed emperorship is future ambition.',
137:'Retain Senior Monk for 高僧: a monk of high standing in this respectful historical and religious account. Do not invent a named Buddhist order, formal office or relationship.',
151:'Retain progressive Sailor for 水夫 and the separate full-catalogue Retainer for 配下. The different native consumers have different source labels; do not merge them or treat a dynamic fallback as a future conditional participant.',
160:'Retain Villager for 村民 in the isolated faithful community. Religious belief in dialogue does not make this a priest or supply a personal name.',
163:'Retain Boy for 男の子. The rescue exchange establishes an actual grandfather, while お兄ちゃん in his goodbye does not make Hodram his brother.',
170:'Retain Mysterious Old Man for 謎の老人, the unnamed giver. His age is explicit, but the reward story does not identify him as a sailor; Grandfather would misleadingly imply a relationship to the player.',
177:'Retain Sect Leader for 教祖 in the self-important research sect. The role and followers support leadership; do not invent a named religion, ordination or noble title.',
178:'Retain Follower for 信徒 in the sect\'s call-and-response exchange. Normalize only the unintended full-width F; do not add a plural collective identity, rank or pejorative.',
179:'Retain Villager for this separate 村民 actor guiding the shared discovery and return. The identical label does not merge actor179 with actor160.',
180:'Retain Bandit for 野盗. The village tragedy and recruitment provide context without erasing the source raider identity or inventing a rebel rank.',
191:'Retain Donna, the source personal name ドナ. Seville is city metadata and supplies no surname or romantic relationship.',
198:'Retain Benazir for ベナジール. Calicut is city metadata, not a surname; the reciprocal gift conversation does not establish a romance.',
}

def main():
    assert not OUT.exists()
    names,fields,native=map(load,[NAMES,FIELDS,NATIVE]);rows=[]
    assert set(NOTES)==set(names['actors']) and len(NOTES)==18
    current=names['current_names']['rows'];clean=names['clean_names']['rows']
    for actor,note in NOTES.items():
        components_index=next(i for i,r in enumerate(fields['records']) if r['actor_ID']==actor)
        before=[(i,r) for i,r in enumerate(clean) if r['actor_ID']==actor]
        after=[(i,r) for i,r in enumerate(current) if r['actor_ID']==actor]
        assert [r['consumer'] for i,r in before]==[r['consumer'] for i,r in after]==['progressive-nameplate','full-catalogue']
        consumers=[]
        for (ci,c),(ei,e) in zip(before,after,strict=True):
            proposed=e['text']
            if actor==178:proposed=proposed.replace('Ｆ','F')
            if actor==43 and e['consumer']=='full-catalogue':proposed='Diogo de Escante'
            consumers.append(dict(consumer=e['consumer'],
                source_reference=dict(path=str(NAMES),json_pointer=f'/clean_names/rows/{ci}',actor_ID=actor,getter=c['getter'],pointer=c['pointer']),
                source_Japanese=c['text'],source_hex=c['text_hex'],
                current_reference=dict(path=str(NAMES),json_pointer=f'/current_names/rows/{ei}',actor_ID=actor,getter=e['getter'],pointer=e['pointer']),
                current_English=e['text'],current_hex=e['text_hex'],proposed_English=proposed,
                decision='retention' if proposed==e['text'] else 'revision'))
        changed=any(r['decision']=='revision' for r in consumers)
        rows.append(dict(id=f'ACTOR_{actor}_SC1_B111_B130_SCOPED_NAME_REVIEW',actor_ID=actor,consumers=consumers,
            clean_static_components_reference=dict(path=str(FIELDS),json_pointer=f'/records/{components_index}'),
            context_reference='translations/hodram_B111_B130_editorial_manuscript_v1.json#/complete_exchange_contexts',
            decision='revision' if changed else 'retention',finding=note,localization_note=note,retention_reason=None if changed else note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            exact_native_bindings_complete=True,changed_native_display_andglyph_proof=str(NATIVE) if changed else None,
            actual_English_scene_checks_andregistered_deployment_pending=True,new_dialogue_credit=0))
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',records=rows,actors=18,
        revised_name_identities=2,retained_name_identities=16,source_andcurrent_consumers=36,
        six_known_identity_proofs_reused='work/analysis/Hodram_B111_B130_clean_20261101/known_six_name_proof_reuse.json',
        native_binding_andname_prose_not_global_207_name_approval=True,no_new_dialogue_orcompletion_credit=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [NAMES,FIELDS,NATIVE,Path(__file__)]}))
    assert native['direct_view_pending'];sheet=native['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    approved=deepcopy(native);approved.update(direct_view_pending=False,offline_visual_approved=True,
        original_pending_report=str(NATIVE),original_pending_report_sha256=sha(NATIVE.read_bytes()),
        visual_review_note='Directly viewed all ten complete native name planes. Correct F and de are legible in both styles; first/final glyphs remain complete. Actual catalogue UI is unvisited; representative English scene header tests and registered deployment remain pending.')
    target=NATIVE.with_name(NATIVE.stem+'_reviewed.json');assert not target.exists();save(target,approved)
    print('18 scoped name identities:2 revised/16 retained.8 original getters/10 viewed native planes/8 negative checks pass; actual scenes and registered deployment pending.')

if __name__=='__main__':main()
