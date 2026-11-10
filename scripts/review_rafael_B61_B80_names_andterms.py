"""Record individual name/role retentions andsource-defined aliases without global catalogue approval."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
DECISIONS={
0:('Rafael Castor','Retain user-approved Rafael Castor andthe existing progressive given-name/surname order. FI/FA remain runtime substitutions,not literal default text.'),
3:('Maria Li','Retain approved Maria/Li progressive identity andMaria Huamei Li for the full form when actually used. Her brisk dialogue andexplicit Admiral title do not license an invented birth story ornew rank.'),
4:('Janus Pasar','Retain the established Janus Pasar identity matching sourceジェナス・パサー;no concrete readability defect ornew source fact warrants renaming this recurring tactful companion.'),
5:('Claudio Manaus','Retain Claudio Manaus,matching sourceクラウディオ・マナウス. His familiar Clau address is a separate spoken form;his warm/rough voice does not confer a new rank.'),
6:('Julio Erneco','Retain Julio Erneco,matching sourceフリオ・エルネコ andthe approved earlier crew dialogue. No Grandpa kinship is added to the older companion.'),
8:('Arcadius Eudoxios','Retain the source public Arcadius Eudoxios nameplate. Eirene is explicitly the private female identity discussed in B63/B73;do not globally replace the public alias orrewrite the full-name consumer ordering here.'),
10:('Xien Yan','Retain established Xien Yan for sourceシエン・ヤン. It preserves the supplied sound andconsistent current identity without claiming an official national romanization orsilently inventing different Chinese characters. The source calls him Maria right hand,not General as a formal appointment.'),
11:('Jam Ludwyan','Retain established Jam Ludwyan forジャム・ルドワイヤン. Jack is a separate full-name component;do not automatically expand Jam into an unrelated James orrename him from his exuberant vocal effects.'),
31:('Pedro Valdes','Retain Pedro Valdes progressive identity. The already-corrected full-name de component is preserved separately;do not add Lord oranother unsupported noble title.'),
34:('Barbarossa Hayreddin','Retain established Barbarossa Hayreddin progressive identity andHayreddin in familiar spoken references. The corrected full-name Fazul field is separate;do not invent a pirate-king rank.'),
39:('Duarte Pereira','Retain Duarte Pereira progressive identity. SourceGovernor of Indochina self-boast is intentional speech;keep the ordinary nameplate distinct from that comic self-description.'),
40:('Antony Kuhn','Retain established Antony Kuhn in progressive/spoken uses. The source full-middleフォン/currentＦong component requires its separate source-aware spelling/glyph review;this retention does not approve that unresolved catalogue component.'),
48:('Simon Linares','Retain Simon Linares,matching sourceシモン・リナレス andthe explicit Linares family of Cordoba. His navy pride/family claim does not supply a particular noble rank for the label.'),
80:('Charlotte Miller','Retain Charlotte Miller forシャルロット・ミレール andthe existing native public identity. SourceB64 establishes Romani background butdoes not establish a new British/French nationality from the English surname.'),
83:('Shopkeeper','Retain natural Shopkeeper for広場の店主. The plaza/shop function is preserved without making location metadata an awkward personal name orasserting an unspoken family relationship.'),
104:('Trader','Retain natural Trader for the trading-house man交易所の親父. The familiar older-man term is a role,not Father/Dad orproof of ownership.'),
106:('Trader','Retain Trader for the separate Chinese trading-house actor交易所の親父. Keep the distinct actor/source references even though the English role matches actor104;no kinship ornew proprietor rank is invented.'),
113:('Port Worker','Retain natural Port Worker for出港所の兄貴. Delivering Portugal king summons does not create a new royal official rank;兄貴 is familiar address,not brotherhood.'),
139:('Priest','Retain Priest for神父 andthe priest contact. Religious role is explicit;HighPriest,bishop orfamily Father implications are not supplied by the source.'),
147:('Guildmaster','Retain Guildmaster forギルドの元締め,which explicitly identifies the guild head. Do not reduce the named role to a sailor oradd unspoken political authority.'),
151:('Sailor','Retain Sailor because the actual clean progressive getter returns水夫. The unused full-catalogue配下 metadata is not the public role andmust not become feudal Retainer in these crew/village exchanges.'),
179:('Villager','Retain Villager for村民 in the NewWorld scabbard exchange. The offering/praise does not establish a chief,priest,tribe orspecific ethnic identity.'),
}

if __name__=='__main__':
    output=Path('translations/rafael_B61_B80_scoped_names_andterms_v1.json');assert not output.exists()
    source=ROOT/'source_identity_event_andterm_checkpoint_v1.json';binding=load(source)
    assert set(DECISIONS)==set(binding['actors']) and len(DECISIONS)==22
    sailor_path=Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json');sailor=load(sailor_path)
    clean_sailor=next(r for r in sailor['clean_names']['rows'] if r['actor_ID']==151 and r['consumer']=='progressive-nameplate')
    assert clean_sailor['text']=='水夫'
    records=[]
    for identity in binding['name_bindings']:
        actor=identity['actor_ID'];english,reason=DECISIONS[actor]
        current=next(c for c in identity['current_consumers'] if c['consumer']=='progressive-nameplate')
        assert current['text']==english
        records.append(dict(id=f'ACTOR{actor}_PROGRESSIVE_NAMEPLATE',actor_ID=actor,kind='progressive-nameplate',english=english,speaker=english,
            source_meaning='Source-defined public speaker identity/role from exact clean fields andoriginal progressive getter.',
            context='Reviewed withall complete clean B61–B80 exchanges;only the stated public progressive label is decided here.',
            localization_note=reason,decision='retention',finding=reason,retention_reason=reason,
            source_reference=dict(binding=str(source),binding_sha256=sha(source.read_bytes()),actor_ID=actor,
                clean_fields=[{k:f[k] for k in ['column','source_field','source_pointer','source_hex','source_text']} for f in identity['source_andcurrent_fields']],
                exact_clean_progressive_role='水夫' if actor==151 else None),
            current_reference=dict(binding=str(source),binding_sha256=sha(source.read_bytes()),actor_ID=actor,
                consumer='progressive-nameplate',text_hex=current['text_hex'],native_proof=identity['native_proof'],native_proof_sha256=identity['native_proof_sha256']),
            context_record_ids=[r['id'] for r in binding['records'] if r['source_selector']==actor],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            fresh_orqualified_name_planes_andrepresentative_actual_headers_pending=True,
            global_full_catalogue_or207_names_not_approved=True))
    private_aliases=[dict(actor_ID=8,source='エイレネ',english='Eirene',
        reason='Exact source/private name andcurrent middle component agree;B63/B73 explicitly discuss the concealed female identity. Use Eirene only where spoken,retain Arcadius public controls,anddo not invent a romance.'),
        dict(actor_ID=5,source='クラウ',english='Clau',
        reason='Preserve the deliberate familiar shortening of Claudio in the complete exchanges;do not replace the ordinary full nameplate orimply kinship.')]
    term_rows=binding['source_term_occurrences']
    assert any('交易圏' in r['source_Japanese'] for r in term_rows if r['block'] in [152,166])
    save(output,dict(format='dk4-scoped-name-and-term-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=records,
        all22_progressive_names_individually_retained=True,private_spoken_alias_decisions=private_aliases,
        Estado_source_term=dict(Japanese='エシュタード',definition='Portuguese overseas trading sphere/network;the source explicitly glosses it as交易圏.',
            exact_clean_references=term_rows,English_wording_for_B77_still_to_be_drafted=True,
            not_a_city_orinvented_country_orautomatic_formal_royal_rank=True),
        actor40_full_middle_Fong_von_spelling_andfullwidth_F_review_still_open=True,
        public_private_Arcadius_Eirene_catalogue_ordering_not_rewritten=True,
        global207_name_review_andfull_catalogue_UI_still_open=True,
        all_individual_fifth_gates_pending=True,no_name_data_changes=True,new_dialogue_credit=0,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [source,sailor_path,Path('docs/glossary.md'),Path(__file__)]}))
    print('22 individual progressive name/role retentions;Eirene/Clau aliases andclean-defined Estado trading sphere bound. All display/full-catalogue work remains scoped.',flush=True)
