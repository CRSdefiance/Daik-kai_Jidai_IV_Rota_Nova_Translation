"""Draft complete early tutorials as logical paragraphs using the visible UI terms."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104')
DRAFTS={
    42:[
        "Once you've hired a crew, you'll need supplies. Food and water, that is. You can get them at the port. Come along.",
        'The young fellow at the port takes care of resupply for you. Nice and easy.',
        "If you're short on money, he'll resupply as much as you can afford.",
        "If you turn down resupply, you can change the balance of water and food. Though you probably won't need to do that very often.",
        "Without enough supplies, your sailors can't do their best. Even a fine ship won't help you then. Keep an eye on how much you have left.",
        'All set?',
        "We're finally setting sail! But... what should we do once we're out there?",
        "What? You got all worked up without thinking that far ahead?",
        "Ha! I didn't expect to hear that from you, Claudio.",
        "What's that supposed to mean?! You make it sound like I never think about anything!",
        "Oh, forgive me. I hadn't realized you had a plan. Let's hear this brilliant idea, then.",
        "Huh? Well, I... Hmm... I've got it!",
        "How about taking out pirates? I'll board their ships and knock those thugs down one after another!",
        '...Oh, dear.',
        "Let's think this through... We aren't nearly good enough for that yet. We'd just get ourselves killed.",
        "Quite right. I'd start by visiting ports in the Mediterranean, the North Sea, and other regions.",
        "Visit enough ports, and you'll pick up the basics of sailing and trading along the way.",
        "Right! And let's find some more people to join us!",
        "Yes. If we're to keep sailing, I would feel better with more than our present company.",
        'Hey, old man! Why are you looking at me when you say that?!',
        "Now, now. We certainly would be better off with more companions.",
        "{MACRO:FI}, I'm sure you'll find good people to sail with you.",
        'Julio...',
        "And we'll need more money to buy more ships and keep them running.",
        "Keep trading from port to port, and the money will add up.",
        "Neglect trade, though, and your funds will only dwindle. That was my money, you know. Mind how you use it.",
        "I'm grateful, Julio. I'll earn it back and repay you properly...",
        "Ho ho ho! I'm only joking. Don't worry about it. Now, shall we be on our way?",
    ],
    43:[
        "Everything clear so far? Now I'll tell you about navigators. That's us.",
        "Assigning duties is one of an admiral's important jobs.",
        "To keep things running smoothly, you'll assign each navigator a duty. Let's do that while looking at the deck screen.",
        "First, you're the captain, {MACRO:FI}. A ship can't sail without a captain. It can't decide where to go on its own.",
        "Next is the Sail Handler. They adjust the angle of the sails to the wind. You'll need one for each mast.",
        'Then the Helmsman. Important if you want your ship to turn quickly.',
        'A skilled Helmsman can also get your ship into a good position quickly during a naval battle.',
        "Then there's the First Mate. You can sail without one, but having one lets you negotiate with other powers and helps everyone tire less quickly at sea. An unsung hero.",
        "A Surveyor lets you use automatic movement and tells you the fleet's latitude and longitude. An important job, that.",
        "The Lookout reports who other ships belong to and what's happening in towns while you're at sea.",
        "That should cover the basics of getting a ship out to sea. Try different things and see what else you can learn.",
        'Press X and select Deck View from the menu. You can change navigator assignments on the deck screen.',
    ],
}
NOTES={
    42:[
        'Keep hiring,supplies,food/water andthe port trip;no free supplies ornew purchase made.',
        'The young port worker is not a brother orrelative;automatic service stays explicit.',
        'Preserve the available-funds limit rather than promising full-capacity resupply.',
        'Keep the decline-first control sequence,the adjustable ratio andJulio’s practical qualification.',
        'Preserve sailor performance,the wasted ship andthe reminder to watch remaining supplies.',
        'A short conversational readiness question.',
        'Rafael’s excitement turns to an honest request for a plan.',
        'Claudio’s teasing reaction sets up Janus’s dry comeback.',
        'Use the approved Claudio name in natural teasing rather than a false relationship orrank.',
        'Claudio protests the implication that he never thinks.',
        'Polite mock-apology andthe brilliant-plan challenge preserve Janus’s humor.',
        'Keep Claudio’s hesitation followed by sudden confidence.',
        'The boarding proposal is Claudio’s fantasy;no instruction that the player must attack now.',
        'A restrained weary reaction;do not invent an insult.',
        'Localize the many-lives idiom naturally,preserving their present lack of skill andthe danger.',
        'Preserve the Mediterranean,North Sea andbroader port-visiting recommendation.',
        'Learning comes from visiting ports;no tutorial reward orstatistic invented.',
        'Rafael adds recruiting to their plan.',
        'Julio’s concern about the present group sets up Claudio’s pointed complaint.',
        'Familiar old man address is supported;no grandfather relationship.',
        'Janus mediates while agreeing that they need more people.',
        'Preserve FI exactly andJulio’s personal confidence in Rafael.',
        'A soft personal response without adding a title orkinship.',
        'More money supports both fleet growth andmaintenance.',
        'Preserve repeated trading as the way to accumulate funds.',
        'The warning andJulio’s original ownership set up the following reassurance.',
        'Rafael remains grateful andsincerely intends to repay the loan.',
        'The gentle laugh resolves the money reminder as a joke before departure.',
    ],
    43:[
        'The transition checks understanding andintroduces navigators as the companions themselves.',
        'Natural personnel language without changing the admiral’s responsibility.',
        'The assignment explanation stays tied to looking at the actual deck screen.',
        'Retain captain,FI andthe ship-direction joke;First is ordinary ASCII,with fresh glyph/layout checks still required.',
        'Match Sail Handler to the visible duty label andretain one per mast pluswind adjustment.',
        'Match Helmsman andpreserve fast turning as the function.',
        'Combat positioning is a separate benefit,not a bonus speed statistic.',
        'Use the native First Mate label rather than the inconsistent adjutant tooltip term;keep optionality,negotiation,fatigue andthe unsung-helper image.',
        'Use the native Surveyor label;both automatic movement andcoordinates remain. Do not invent a button name.',
        'Use the native Lookout label andretain ship affiliation andtown reports at sea.',
        'The listed jobs suffice for ordinary sailing;encourage experimenting with the remaining assignments.',
        'Keep X andthe exact Deck View menu wording;the screen heading itself is Deck. No implementation detail in the instruction.',
    ],
}

if __name__=='__main__':
    output=ROOT/'all40_logical_English_drafts_v1.json';assert not output.exists()
    meanings_path=ROOT/'complete_clean_meanings_before_English.json';binding_path=ROOT/'native_identity_and_UI_terms_v1.json'
    meanings,binding=map(load,[meanings_path,binding_path]);assert binding['no_current_story_English_extracted']
    names=load(binding['source_actor_bindings']);speakers={r['actor_ID']:r['text'] for r in names['current_names']['rows'] if r['consumer']=='progressive-nameplate'}
    rows=[]
    for block,texts in DRAFTS.items():
        source=[r for r in meanings['records'] if r['block']==block]
        assert len(source)==len(texts)==len(NOTES[block])
        for original,english,note in zip(source,texts,NOTES[block],strict=True):
            assert english==english.strip() and not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}','  '])
            english.encode('cp932');raw=bytes.fromhex(original['source_hex'])[1:]
            assert all(english.count('{MACRO:'+m+'}')==raw.count(m.encode()) for m in ['FI','FA','FO'])
            row=dict(original);row.update(english=english,logical_English=english,speaker=speakers.get(original['source_selector'],'System panel'),
                context=original['exchange_context'],localization_note=note,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                current_ROM_English_conversation_comparison_pending=True,current_reference_pending=True,
                fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=True,
                source_selector00_complete_preamble_andRafael_macro_display_binding_still_pending=True,
                no_authored_ordinary_breaks_alignment_orpadding=True,individual_draft_prose_gates_not_final_comparison_approval=True)
            rows.append(row)
    assert len(rows)==40
    save(output,dict(format='dk4-source-first-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',blocks=[42,43],review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        current_ROM_English_dialogue_unconsulted_in_this_intake=True,all_individual_fifth_gates_pending=True,
        source_meanings_andlogical_drafts_saved_before_current_dialogue=True,no_blanket_before_any_historical_English_exposure_claim=True,
        new_credit=0,new_ROMs=0,guide_photos=False,evidence={str(p):sha(p.read_bytes()) for p in [meanings_path,binding_path,Path(__file__)]}))
    print('40 logical Rafael tutorial drafts saved,usingFirst Mate andDeck View;comparison/display still pending;no credit.')
