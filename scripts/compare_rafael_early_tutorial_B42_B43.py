"""Keep sound current wording andrecord individual complete-exchange editorial findings."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104')
CURRENT=Path('work/analysis/Rafael_early_tutorial_B42_B43_current_20261104/current_effective.json')
OUTPUT=Path('translations/rafael_B42_B43_contextual_editorial_manuscript_v1.json')
DECISIONS={
    42:[
        ('R','Replace the compressed supplies fragment with Julio’s natural explanation andrestore his invitation to come to the port.'),
        ('K','Dock staff is a natural collective description ofthe attendant;the complete short explanation preserves automatic resupply andJulio’s easygoing teaching voice without inventing kinship.'),
        ('R','Use a natural if-condition andstate that resupply is limited by available funds;With little money,they buy is awkward andless clear to a beginner.'),
        ('K','The existing instruction clearly preserves declining resupply first,the adjustable water/food ratio andthe qualification that this is rarely needed. Reflow its legacy breaks without changing words.'),
        ('R','Clarify reduced sailor performance andwasted ship potential;Even fine ships fail risks implying mechanical failure not stated by the source.'),
        ('K','Ready? is natural,brief andexactly functions asJulio’s preparation check.'),
        ('R','Restore Rafael’s excited first-person question;What after departure? is a compressed fragment rather than natural dialogue.'),
        ('R','Replace the literal Your spirit ran ahead with Claudio’s natural teasing about enthusiasm without planning.'),
        ('K','Ha,never thought Clau would say that is natural teasing inthe complete exchange. Clau is source-explicit andalready used inthe approved opening;keep the familiar form.'),
        ('K','What?! You make me sound thoughtless! naturally protests the implication inthe planning exchange;the context makes unthinking behavior clear rather than adding a moral accusation.'),
        ('R','Restore a conversational mock-apology andthe source’s sarcastic brilliant-plan challenge rather than the terse Surprised you had an idea.'),
        ('K','Huh? Well... That’s it!! preserves Claudio’s hesitation andsudden idea;the source’s emphatic outburst supports the doubled exclamation.'),
        ('R','Restore Claudio’s explicit first-person boarding fantasy. The current imperative Board them can misread asa tutorial instruction to attack.'),
        ('K','...Good grief. is a natural weary Janus reaction that preserves the comic beat;retain it over the alternative Oh,dear.'),
        ('R','Replace think properly andthe literal many-lives phrasing with Rafael’s natural warning about their current lack ofskill andthe danger.'),
        ('K','The current port-visiting recommendation is clear,natural andkeeps both named regions;the surrounding lesson supplies its wider exploratory purpose.'),
        ('R','Explain learning through visits rather than Navigation andtrade skills come naturally,which is stiff andcan imply automatic stat growth instead ofpractical knowledge.'),
        ('K','Yes! Let’s recruit more companions too! is natural excited agreement andretains Rafael’s recruiting suggestion.'),
        ('K','Our current roster is too thin forthe voyage ahead is idiomatic andretains Julio’s concern,setting up Claudio’s response.'),
        ('K','Old man! Why look at me?! naturally preserves Claudio’s familiar complaint;the preceding glance/context supplies when you say that without an invented family relationship.'),
        ('K','Come now. More companions would help. is natural mediation andretains Janus’s agreement with recruiting.'),
        ('K','FI,you’ll surely be blessed with good companions is natural warm reassurance fromthe older mentor;blessed with is idiomatic anddoes not assert a religious event. Preserve FI.'),
        ('K','Julio... already preserves Rafael’s soft personal response;no replacement is needed.'),
        ('R','Restore expanding the fleet’s ship count. Expand andmaintain ships can imply enlarging individual vessels rather than acquiring more.'),
        ('R','Use port-to-port trading andaccumulating money;around the world unnecessarily suggests global travel asa beginner prerequisite.'),
        ('R','Give the warning natural spoken rhythm instead offunds only fall,while preserving Julio’s original ownership andthe setup forthe joke.'),
        ('R','Restore Rafael’s explicit personal repayment promise;the current We’ll earn it back omits returning the loan to Julio.'),
        ('R','Replace Hahaha,a joke with a natural reassurance that Julio is teasing,thenretain the departure invitation.'),
    ],
    43:[
        ('K','Still with me? Now let me explain the navigators--people like us is natural introductory teaching speech andpreserves the group identification.'),
        ('R','Restore assigning duties asone important responsibility rather than the overcompressed An admiral assigns the crew.'),
        ('R','Restore the smooth-sailing purpose andnatural instruction toassign duties while looking atthe deck screen.'),
        ('K','The existing captain explanation andship-direction joke are natural andfaithful. The current First begins with ASCII F;retain the registered repair andremove premature wrapping through formatting only.'),
        ('R','Restore adjustment relative tothe wind,an omitted instructional fact,andmatch the visible Sail Handler role term. Keep one per mast.'),
        ('K','Helmsmen make the ship turn fast is natural,concise andaccurate inthe role-explanation sequence.'),
        ('K','The existing skilled-helmsman sentence naturally explains quick tactical positioning andneeds no prose rewrite.'),
        ('R','Replace adjutant with the visible First Mate label. Clarify that the role enables negotiation with other powers rather than implying diplomacy is automatically handled;preserve optionality,voyage fatigue andthe unsung-helper image.'),
        ('R','Spell out latitude andlongitude fornew players instead ofthe compressed coordinates label;preserve automatic movement andthe job’s importance.'),
        ('K','Reports who ships serve andhow nearby towns fare is natural andretains both affiliation andtown-condition reports while atsea.'),
        ('K','The existing closing naturally says the basic assignments suffice andencourages experimenting with the other roles;retain it andreflow ordinary breaks.'),
        ('K','The existing system instruction exactly preserves X,Deck View andchanging navigator assignments. Keep the clear wording;the four premature short rows belong tothe formatter.'),
    ],
}

if __name__=='__main__':
    assert not OUTPUT.exists()
    drafts_path=ROOT/'all40_logical_English_drafts_v1.json';drafts=load(drafts_path);current=load(CURRENT)
    assert drafts['current_ROM_English_dialogue_unconsulted_in_this_intake'] and len(drafts['records'])==current['records']==40
    by={r['id']:r for r in drafts['records']};rows=[]
    for group in current['groups']:
        choices=DECISIONS[group['block']];assert len(choices)==len(group['records'])
        for prior,(decision,note) in zip(group['records'],choices,strict=True):
            original=by[prior['id']];assert all(original[k]==prior[k] for k in ['source_hex','source_reference','source_complete_preamble_hex'])
            english=original['english'] if decision=='R' else prior['current_comparison_paragraph']
            if decision=='K':
                for m in ['FI','FA','FO']:english=english.replace(m,'{MACRO:'+m+'}')
            assert english==english.strip() and not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}','  ']);english.encode('cp932')
            raw=bytes.fromhex(prior['source_hex'])[1:]
            assert all(english.count('{MACRO:'+m+'}')==raw.count(m.encode()) for m in ['FI','FA','FO'])
            row=deepcopy(prior);row.update(english=english,logical_English=english,speaker=original['speaker'],context=original['context'],
                kind='system-FE' if prior['source_selector']==254 else 'progressive',
                planned_English_markup='{SPEAKER:'+format(prior['source_selector'],'02X')+'}'+english,
                source_record_index=prior['source_reference']['record_index'],source_native_extent=prior['native_extent'],
                decision='revision' if decision=='R' else 'retention',finding=note,retention_reason=note if decision=='K' else None,
                localization_note=note,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                source_meanings_anddrafts_preceded_current_ROM_English_extraction=True,
                whole_exchange_cadence_relationships_situation_andemotional_progression_reviewed=True,
                current_English_comparison_pending=False,current_English_now_exposed=True,
                no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
                original_logical_draft_reference=dict(path=str(drafts_path),sha256=sha(drafts_path.read_bytes()),id=prior['id']),
                fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=True,new_credit=0)
            rows.append(row)
    revised=sum(r['decision']=='revision' for r in rows);retained=len(rows)-revised;assert (revised,retained)==(19,21)
    assert next(r for r in rows if r['id']=='DK4_MES_B43_R0017')['english'].startswith('First,')
    doc=dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        file_path='/data/SC0.DK4',blocks=[42,43],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,proposed_revisions=revised,wording_retentions=retained,
        all_four_individual_prose_gates_passed=True,all_formatting_gates_false=True,all40_source_current_exact_references_andindividual_findings=True,
        source00_complete_preamble_andRafael_macro_fresh_display_binding_pending=True,registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [drafts_path,CURRENT,ROOT/'native_identity_and_UI_terms_v1.json',Path(__file__)]})
    # The strict release validator correctly rejects pending formatting gates.
    # Persist a prose packet with those gates false; validate the final batch
    # only after its native,visual,stored andrepresentative checks are complete.
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in rows)
    save(OUTPUT,doc)
    print('40 whole-exchange contextual comparisons saved:19 revisions/21 justified retentions;fresh formatting remains.')
