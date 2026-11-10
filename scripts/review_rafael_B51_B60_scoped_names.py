"""Review18 source-defined progressive identities; normalize only Fernan's font artifact."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

SOURCE=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B51_B60_source_identity_checkpoint_v1.json')
RUNTIME=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
OUT=Path('translations/rafael_B51_B60_scoped_progressive_names_v1.json')
REASONS={
    0:'Retain user-approved Rafael Castor and the established progressive ordering. No new royal identity or title is inferred from the restoration dialogue.',
    1:'Retain user-approved Hodram and established Bergstrom. Joakim remains the confirmed middle name in the separate full consumer; the progressive name omits it natively.',
    4:'Retain established Janus Pasar. The source character and cautious advisory voice are unchanged; no military rank is introduced by the name label.',
    5:'Retain established Claudio Manaus and source-specific familiar Clau only inside spoken dialogue. Do not replace the ordinary full nameplate with a nickname.',
    6:'Retain established Julio Erneco. His old-bones joke does not establish a family relationship with Rafael.',
    7:'Retain established Cristina Erneco. The source reaction addresses Silveira, not a newly invented relationship or title.',
    8:'Retain established Arcadius Eudoxios. The bedside and waiting exchange remains understated; the nameplate does not add a gender, romance or family claim.',
    11:'Retain established Jam Ludwyan. Jack belongs to the source-defined full-name consumer and is not newly inserted into the progressive label.',
    14:'Retain established Emilio Ferog. The complete current given name is already ASCII; retain the earlier accepted glyph repair rather than count another correction.',
    20:'Retain established Fernando Dias and the accepted normal-width F. Do not confuse this companion with Fernan Silveira.',
    24:'Retain established Sera Shahrbaraz. Rafael speculates that she might be a princess; the nameplate must not turn that speculation into a rank.',
    35:'Retain the source-defined Fernan Silveira spelling and identity; change only the unintended full-width F to ordinary ASCII in the exclusively owned given-name field.',
    37:'Retain established Abraham Uddin, matching the Uddin Company and spoken Admiral Uddin. Do not introduce Woodin as an alternate spelling during this pass.',
    39:'Retain established Duarte Pereira, matching the explicit governor-of-Indochina references. The source title stays in speech where present; no title is added to the name.',
    84:'Retain natural Shopkeeper for the source plaza-shop owner. The role is accurate and the local context supplies the square; no unrelated occupation, personal name or rank is invented.',
    114:'Retain natural Port Worker for the source familiar older port-office man. Do not render the address as Brother or invent kinship or a formal officer rank.',
    116:'Retain Port Worker for this separately indexed source port-office man. Shared wording does not merge the two native actor objects or invent a family relationship.',
    151:'Retain Sailor for the anonymous subordinate in these ship/crew exchanges. This scoped progressive decision does not approve the separate full-catalogue Retainer label globally.',
}

if __name__=='__main__':
    assert not OUT.exists()
    source,qual=map(load,[SOURCE,RUNTIME/'dependency_qualification.json'])
    field_path=RUNTIME/'Fernan_owned_fields_proposal.json';field=load(field_path)
    assert field['runtime']==qual['runtime'] and len(source['actors'])==18 and set(REASONS)==set(source['actors'])
    rows=[]
    for bound in source['name_bindings']:
        actor=bound['actor_ID'];current=next(c for c in bound['current_consumers'] if c['consumer']=='progressive-nameplate')
        target=current['text'].replace('Ｆ','F') if actor==35 else current['text']
        assert target.isascii() and target.strip()==target
        source_name=' / '.join(f['source_text'] for f in bound['source_andcurrent_fields'] if f['column'] in [0,4] and f['source_text'])
        reason=REASONS[actor]
        rows.append(dict(id=f'ACTOR{actor}_PROGRESSIVE_NAMEPLATE',actor_ID=actor,english=target,speaker=target,
            source_meaning=source_name,context='Scoped progressive nameplate read with the complete B51–B60 exchanges and native actor identity. Full catalogue metadata is outside this decision unless explicitly stated.',
            localization_note=reason,decision='revision' if actor==35 else 'retention',finding=reason,
            retention_reason=None if actor==35 else reason,
            source_reference=dict(binding=str(SOURCE),binding_sha256=sha(SOURCE.read_bytes()),actor_ID=actor,
                source_fields=bound['source_andcurrent_fields'],consumer='progressive-nameplate'),
            current_reference=dict(native_proof=bound['native_proof'],native_proof_sha256=bound['native_proof_sha256'],
                consumer='progressive-nameplate',text_hex=current['text_hex'],qualified_successor_runtime=qual['runtime']),
            context_record_ids=[r['id'] for r in source['records'] if r['source_selector']==actor],
            proposed_owned_field=field['fields'][0] if actor==35 else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            actual_target_headers_unvisited=True))
    save(OUT,dict(format='dk4-scoped-progressive-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        proposed_revisions=1,justified_retentions=17,runtime=qual['runtime'],full_catalogue_metadata_andglobal207_name_review_open=True,
        actor40_full_middle_Fong_von_review_remains_separate=True,no_new_dialogue_credit=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,RUNTIME/'dependency_qualification.json',field_path,Path(__file__)]}))
    print('Reviewed18 progressive names:17 retentions/one Fernan glyph correction;no invented titles orkinship;native display binding pending.')
