"""Localize eleven complete town exchanges and their tentative trade forecasts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_hodram_B171_B190_drafts import save_part, ROOT

DRAFTS = {
    180: [
        "Bananas! Bananas are the future!", "Bananas?", "Yes! With that flavor, they're bound to be a hit!",
        "You think so?", "I do! If I say they're good, they're good!", "All right. What would you like me to do?",
        "Buy as many bananas as you can.", "Sure, sure.", "It's the age of the banana! Ohohoho!",
        "Bananas may soon be all the rage in Seville.",
    ],
    181: [
        "Tomatoes! Tomatoes are the future!", "Really? Something that bright red?",
        "That red is what makes them so wonderful! The color of passion! Ah, it reminds me of the love that set my young heart on fire.",
        "...I see. How nice for you.", "Start making and selling tomato dishes at once!", "All right.",
        "Now, don't let this tomato craze pass us by!", "Sure, sure.", "Then do your best! Ohohoho!",
        "Tomatoes may soon be all the rage in Genoa.",
    ],
    182: [
        "Nothing beats bread you've baked yourself.", "Quite right. My husband was absolutely delighted.",
        "Is homemade bread really that good?", "Oh, it's wonderful. Isn't it?",
        "Absolutely. That bakery on the corner doesn't even come close.", "Really? Maybe I should try making it myself.",
        "You certainly should.", "I'll show you how.", "Oh, would you? I'd love that!",
        "Then let's go and buy the ingredients right away.", "What will we need?", "Wheat, for starters.",
        "Wheat may soon be all the rage in Amsterdam.",
    ],
    183: [
        "Huh? You're still drinking that stuff?", "Got a problem with that?", "No, but wine's the thing now. Wine!",
        "Wine? Is it any good?", "It's the best!", "It's that good?", "With wine, who needs anything else?",
        "I'll give it a try. Barkeep! A glass of wine!", "Coming right up!", "Glug, glug, glug...",
        "Well?", "Now that's good! Barkeep! Another!", "One for me, too!",
        "Wine may soon be all the rage in Sao Jorge.",
    ],
    184: [
        "Did you notice that lovely scent they were wearing?", "So you noticed it too!", "I wonder what fragrance it was.",
        "I couldn't say. But I'm sure it's going to catch on.", "Oh, dear! We must get some before everyone else!",
        "Indeed we must.", "Next time we meet them, shall we be bold and ask?", "What a splendid idea. Let's!",
        "Goodbye, then.", "Goodbye.", "Fragrances may soon be all the rage in Lisbon.",
    ],
    185: [
        "Did you see that brilliant red ruby?", "Oh, yes. It was magnificent.", "Oh? What are you two talking about?",
        "The necklace that lady was wearing.", "Oh, that one! What a beautiful stone. And so large!",
        "I'd love a man to give me a gift like that. Just once in my life.", "Quite so... (Sigh...)",
        "(Sigh...)", "(Sigh...)", "Rubies may soon be all the rage in Athens.",
    ],
    186: [
        "Have you heard? The princess is getting engaged!", "To the duke's son, isn't it?",
        "I hear the ring costs enough to buy a mountain.",
        "Just what you'd expect from a duke... When will we get to see her wearing it?",
        "It won't be long. And once she wears it, imagine how many ladies will want the same stone!",
        "Oh! We can't wait until it's fashionable! What stone is it? Do you know?",
        "I don't. We must find out at once!", "Gemstones may soon be all the rage in London.",
    ],
    187: [
        "Hm?", "It's truly magnificent!", "You think so?", "He'll go down in history as a great artist.", "Huh.",
        "You ought to buy one of his works now.", "I think this one's better!",
        "It's not bad, but it's no match for his work.", "What nonsense, you two. That one is clearly the better work.",
        "I don't care what you say. I'm buying his painting!", "I'll take something by this painter!", "I'll take this one!",
        "Thank you very much!", "Slam!", "Finally! I wish they'd stop arguing in my shop every time they come in.",
        "What was all that racket about?", "A pastime for the rich.", "A pastime for the rich?",
        "Yes. Collecting paintings has become all the rage lately.", "Sounds like a refined hobby.",
        "Though few of them can actually tell a good painting from a bad one.", "Hahaha! You don't mince words, do you?",
        "Oh! Keep that between us, will you?", "Don't worry.", "Paintings may soon be all the rage in Basra.",
    ],
    188: [
        "Oh, this is delicious! Just wonderful.", "It really is. Tea is wonderful.",
        "It's strange that something this good didn't catch on sooner.", "It is. People just don't know a good thing when they taste it.",
        "Oh, we're almost out of tea. Would you pick some up tomorrow?", "Of course. I'll get some.",
        "Tea really is delicious. It's so soothing.", "We couldn't live without our tea.",
        "Tea may soon be all the rage in Sofala.",
    ],
    189: [
        "Brr... It's freezing!", "It hasn't been this cold in a long time.",
        "I wish I had a fur coat. I'm going to freeze at this rate!",
        "Apparently, furs are selling well in this cold. Prices are rising, too.", "So they say... Brr.",
        "I hope it warms up soon.", "So do I. But while it's this cold, I still want a fur coat.",
        "Furs may soon be all the rage in Stockholm.",
    ],
    190: [
        "Hmm... Something's missing. Of course! Sweetness! It needs to be sweeter.", "Sweeter?",
        "Yes! The customers won't be satisfied with something so light. It has to be sweet! Sweeet!",
        "Right... You think so?", "Of course! If I say so, that's that!", "Right. How should I make it sweeter?",
        "That's your job to figure out, isn't it?", "...Sure, sure.", "Sweet things are bound to catch on.", "Sure, sure.",
        "Sweetness! That's what matters. Do your best! Ohohoho!", "Sweet foods may soon be all the rage in Alexandria.",
    ],
}

CONTEXTS = {
    180: 'The imperious Owner predicts a banana craze and orders the Cook to buy stock. His doubtful, resigned responses contrast with her certainty; the system forecast remains tentative.',
    181: 'The same Owner romanticizes the red of tomatoes and demands dishes for sale. The Cook remains dry and resigned. No husband or particular former lover is invented.',
    182: 'Three Ladies praise bread baked at home, offer instruction and decide to buy ingredients. The second Lady explicitly mentions her husband. Wheat connects the exchange to the precise trade-good forecast.',
    183: 'A Sailor persuades a skeptical Patron to try wine. The audible gulping and immediate order for more complete the small conversion before the forecast.',
    184: 'Two genteel Ladies conspire to identify and obtain an admired fragrance ahead of the fashion. The wearer is not gendered or named in Japanese.',
    185: 'Three Ladies admire a ruby necklace, wish for a gift from a man and sigh in sequence. Do not invent husbands, noble ranks or the wearer\'s identity.',
    186: 'Two Ladies gossip about a princess, a duke\'s son and an extravagant ring. Their desire to anticipate the fashion precedes a generic gemstone forecast; the particular gem and royal names are unknown.',
    187: 'Three customers compete over paintings, buy their choices and leave. The Shopkeeper privately questions their taste to a Sailor, who promises discretion. Preserve the argument, door sound and change to candid conversation.',
    188: 'A close pair enjoy tea, disparage others\' taste and discuss buying more tomorrow. Shared household wording supports familiarity without establishing marriage. The earlier user screenshot is disclosed for the tea-shopping line.',
    189: 'The same pair complain of exceptional cold. A fur-coat wish leads to reported sales and prices, then a hope for warmer weather and renewed desire for furs.',
    190: 'The Owner insists on sweetness but makes the Cook devise the method. Preserve her repeated emphatic sweet and affected laugh against his resigned replies; no sugar or recipe is named.',
}

NOTES = {
    180: [
        'Keep the exaggerated future prediction and repeated commodity.', 'Preserve the skeptical echo.',
        'Retain flavor as her reason for expecting success.', 'Keep the Cook\'s doubt.', 'Preserve her imperious self-certainty.',
        'Keep acceptance followed by the practical question.', 'Preserve buying as many as possible.',
        'Use a resigned recurring reply rather than enthusiastic agreement.', 'Keep the triumphant repetition and distinctive laugh.',
        'Preserve bananas, Seville and the system\'s tentative forecast.',
    ],
    181: [
        'Repeat the Owner\'s established introductory pattern with tomatoes.', 'Keep the doubt specifically about the intense red.',
        'Preserve passionate red and one remembered youthful love; no spouse or multiple romances are added.',
        'Retain the Cook\'s dry politeness.', 'Keep making and selling dishes, without inventing a recipe.',
        'Preserve the brief assent.', 'Keep her urgency about missing the trend.', 'Repeat his resigned reply.',
        'Preserve the encouragement and affected laugh.', 'Preserve tomatoes, Genoa and uncertainty.',
    ],
    182: [
        'Make the activity unmistakably baking one\'s own bread, not buying it or comparing unrelated bread types.',
        'Husband is explicit in this record; do not extend that relationship to other speakers.',
        'Keep the third woman\'s question about homemade bread.', 'Preserve the first woman\'s enthusiasm and appeal for agreement.',
        'Localize the corner bakery comparison without a literal visual idiom.', 'Keep tentative interest in trying it herself.',
        'Preserve encouragement.', 'Use a natural offer of instruction.', 'Keep the pleased response to the offer.',
        'Preserve immediately buying ingredients, not buying finished bread.', 'Retain the ingredient question.',
        'Keep source wheat and the exact trade commodity; do not invent a flour commodity or milling process.',
        'Preserve wheat, Amsterdam and the tentative market forecast.',
    ],
    183: [
        'Leave the unnamed old drink unspecified.', 'Keep the Patron\'s defensive challenge.',
        'Preserve the admission that it is not bad and the shift to wine\'s popularity.', 'Retain the taste question.',
        'Keep the enthusiastic praise.', 'Preserve the repeated skeptical question.', 'Keep the comic hyperbole without literal deprivation.',
        'Use Barkeep as an occupational address, not Master as a rank.', 'Use a natural acknowledgment of the drink order.',
        'Render the three audible gulps in familiar English.', 'Keep the request for a verdict.',
        'Preserve the enthusiastic conversion and immediate second order.', 'Keep the first man\'s added order.',
        'Use the bound Sao Jorge spelling and preserve the wine forecast.',
    ],
    184: [
        'Keep the fragrance as worn by a person; singular they avoids an unsupported gender.',
        'Preserve their shared noticing.', 'Keep the unknown scent identity.', 'Retain ignorance alongside confidence about fashion.',
        'Preserve the desire to get ahead of others.', 'Keep their agreement in a genteel voice.',
        'Keep a future meeting and the plan to ask, without inventing a named occasion.', 'Preserve approval of the plan.',
        'Use a natural farewell without fixing a time of day.', 'Return the farewell.',
        'Fragrances preserves the scent-focused source category without inventing a named perfume.',
    ],
    185: [
        'Preserve ruby and its striking red.', 'Keep the second woman\'s admiration.', 'Retain the newcomer\'s question.',
        'Identify the necklace and unnamed lady, not an invented social event.', 'Keep size and beauty.',
        'The desired giver is a man, not a stated husband; preserve the once-in-a-lifetime wish.',
        'Keep agreement and the first audible sigh; parenthetical notation only localizes the vocal cue.',
        'Preserve the second sigh in the three-speaker comic sequence.', 'Preserve the third sigh rather than collapsing the exchange.',
        'Keep rubies, Athens and uncertainty.',
    ],
    186: [
        'Princess and impending engagement are explicit source facts.', 'The duke and his son are also explicit; do not supply names.',
        'Preserve the mountain-buying comparison as reported gossip, not a price.',
        'Keep admiration for the duke and the question about seeing the princess wear the jewel.',
        'Preserve anticipation and expected demand without naming a gem.', 'Keep urgency and both questions about the unidentified stone.',
        'Retain ignorance and the decision to inquire.', 'Use a generic gemstone forecast; no ruby or diamond is invented.',
    ],
    187: [
        'Keep the listener\'s attention-catching beat.', 'Preserve enthusiastic judgment.', 'Retain the questioning response.',
        'Keep the prediction of the unnamed artist\'s lasting fame.', 'Preserve the unimpressed response.',
        'Keep the recommendation to buy now without inventing resale profit.', 'Retain the competing preference.',
        'Preserve the qualified concession followed by comparison.', 'Keep the third customer\'s competing certainty.',
        'Retain the first man\'s defiant buying decision.', 'Keep buying a work by the preferred painter rather than inventing an artist name.',
        'Preserve the third selection.', 'Keep the Shopkeeper\'s business thanks.',
        'Localize the explicit slamming sound; preserve its FE consumer.',
        'Keep relief and the complaint about their repeated arguments.', 'Use a natural question about the commotion.',
        'Preserve rich people\'s pastime as the explanation.', 'Keep the questioning echo.',
        'Retain the specific new fashion for collecting paintings.', 'Keep the listener\'s comment on refinement.',
        'Express lack of a discerning eye in plain English, limited to the collectors discussed.',
        'Preserve laughter and recognition of the blunt remark.', 'Keep the request for discretion.',
        'Retain assurance of secrecy.', 'Preserve paintings, Basra and the tentative forecast.',
    ],
    188: [
        'Preserve pleasure and emphatic praise.', 'Keep the man\'s shared appreciation of tea.',
        'Retain surprise that tea did not become popular earlier.', 'Adapt a discerning-eye idiom to taste without changing the judgment.',
        'The earlier user screenshot wording already fits the clean meaning naturally: retain the tea shortage and tomorrow request, with incidental exposure disclosed.',
        'Preserve the ready promise to buy some.', 'Keep deliciousness and the calming effect.',
        'Preserve affectionate hyperbole without inventing marriage or a health dependency.', 'Keep tea, Sofala and uncertainty.',
    ],
    189: [
        'Use a familiar cold reaction; freezing is conversational exaggeration.', 'Preserve how unusual this degree of cold is.',
        'Keep the fur-coat wish and fear of freezing.', 'Preserve weather-driven sales and prices as reported information.',
        'Keep agreement with the report and continuing discomfort.', 'Retain the hope for warmer weather.',
        'Preserve the contrast between that hope and wanting a coat meanwhile.', 'Keep furs, Stockholm and uncertainty.',
    ],
    190: [
        'Keep the missing flavor as sweetness rather than an invented ingredient.', 'Preserve the Cook\'s questioning echo.',
        'Keep light flavor, customer dissatisfaction and exaggerated emphasis on sweet.', 'Retain doubt rather than enthusiastic agreement.',
        'Preserve her insistence on being right.', 'Keep the question about method.',
        'The Cook must devise the solution; do not add a sugar order or recipe.', 'Repeat the resigned response after her refusal to explain.',
        'Keep the Owner\'s confident prediction distinct from the tentative system message.', 'Preserve the repeated acquiescence.',
        'Retain sweetness, the demand for effort and her recurring affected laugh.',
        'Sweet foods preserves the broad source category and Alexandria without specifying sugar.',
    ],
}

if __name__ == '__main__':
    labels = load(ROOT / 'town_forecast_city_terms_v1.json')
    assert len(labels['records']) == 11
    assert {r['current_label'] for r in labels['records']} == {
        'Seville', 'Genoa', 'Amsterdam', 'Sao Jorge', 'Lisbon', 'Athens', 'London', 'Basra', 'Sofala', 'Stockholm', 'Alexandria'}
    save_part('B180_B190_130', DRAFTS, CONTEXTS, NOTES, __file__)
