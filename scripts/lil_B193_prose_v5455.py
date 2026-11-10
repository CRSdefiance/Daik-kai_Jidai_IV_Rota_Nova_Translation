"""Cooking,reported ingredient knowledge,relative cost and explicit friendship."""
REVISIONS={
    6:("Oh, that was delicious. I've never had such a wonderful meal.",
        'Restore the relaxed satisfied reaction and complete first-person first-time praise. Best meal ever is an abrupt slogan that flattens the genteel delighted voice. The natural American sentence preserves the speaker’s judgment without naming a dish,restaurant,host or cuisine.'),
    17:('Hee hee. This is the secret.',
        'Keep the soft playful laugh and restore the explicit secret reveal. See this? changes the declaration into a question and drops 秘密. This retains the source deictic without inventing a gesture,item-display command or transfer.'),
    21:('?',
        'Retain the lone questioning reaction semantically and use the ordinary ASCII question mark for the English paragraph. This is a punctuation normalization from the legacy full-width mark,not added dialogue,an inferred identity or a changed emotional response.'),
    25:("They're called chili peppers. I'm told they're a kind of spice. They go beautifully with the local ingredients.",
        'Restore the reported classification in なんですって and the local-ingredient compatibility judgment. The plural names the ingredient class,not a counted quantity. Drop unsupported our ownership. The genteel explanation distinguishes chili peppers from chili stew,powder,a recipe,a national origin or a health effect. It remains a character’s knowledge and taste judgment.'),
    37:("Oh, that's a relief. Perhaps I'll try cooking with it tonight.",
        'Restore the explicit relief and personal tentative wish to use the ingredient in tonight’s cooking. The old we will try changes the speaker’s first-person intention into joint action and omits the cooking referent. Perhaps preserves かしら;no purchase or completed preparation is added.'),
    40:("I'd like to cook with it, too.",
        'Make the second Lady’s desire to cook intelligible in response to the first Lady’s tentative household plan. Me too! loses the explicit 作りたい after the old ambiguous we line. This is a personal wish,not a trade request or completed dish.'),
    44:('Then would you like me to show you how to cook with it now?',
        'Preserve the polite offer/question,explicit cooking instruction and immediate 今から. Come invents movement and the old imperative loses the offer and timing. The natural friendly American invitation keeps the teaching intention without supplying recipe steps or a completed lesson.'),
    47:('Oh, really?!',
        'Restore the delighted reaction and source emphasis in まあ、本当に！？ after the unexpected teaching offer. A plain Really? can sound neutral or skeptical;the small exclamation keeps the warm emotional progression without adding a factual claim.'),
}
RETAIN_NOTES={
    10:'Retain Quite. Such a lively flavor. The refined clipped agreement naturally follows the first Lady’s satisfied praise,and lively flavor conveys the stimulating taste in 刺激的なお味. It supports a distinct genteel voice without a literal exciting-taste construction,an exact heat level or health claim.',
    14:'Retain How did you make this so tasty? The immediate meal context makes this a natural preparation question addressed to the cook. Its past-tense English refers to the meal just enjoyed and preserves the source’s how-to intent;it does not introduce trade or a recipe.',
    29:'Retain My,is it not expensive? with its existing contraction and spacing. My carries the polite surprised まあ and the question preserves concern about cost. It neither asserts an amount nor makes a shortage,profit or narrator-market claim.',
    33:'Retain Not really. It is an idiomatic gentle relative reassurance in direct answer to the expense question. The conversational ellipsis preserves the modest source answer without making the ingredient free or universally cheap.',
    51:'Retain How kind! This is natural warm appreciation of the offered instruction. It expresses ご親切ですこと without an invented fee,obligation or repayment,and fits the gently formal social exchange.',
    55:'Retain Of course. We are friends. with its existing contraction. It naturally grounds the willingness in the source-explicit friendship and 当然. The relationship is supported here;no additional kinship,marriage,romance,rank or prior history is implied.',
    59:'Retain Chilies may catch on in Seoul. Chilies is a natural American plural for the chili-pepper ingredient just explained,consistent with the unchanged compact commodity label Chili. May catch on preserves the prospective forecast,and Seoul is bound to both source 京城 aliases. No earned fashion,earlier location,shortage,price rise,profit or chili-stew claim is added.',
}
