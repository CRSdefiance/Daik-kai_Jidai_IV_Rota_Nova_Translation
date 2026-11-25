"""Review Hans and Rafael's encounter with the medicinal-book seller."""

from inspect import getsource

from scripts import review_rafael_B211_B213_20261122 as prior_review
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = prior_review.paired.ROOT / "contextual_decisions_B215.json"
WRAPS = {}
DECISIONS = {
    215: """
5|||Hans notices the object first and wonders what it is. The short question gets Rafael's attention.
9|||Rafael asks whether Hans found something before he has looked closely himself.
14|Here, take a look.||Hans points out what caught his eye. His wording is conversational and direct.
18|||Rafael tentatively identifies the object as some kind of insect. Keep his uncertainty.
23|But look at that odd growth. It looks like grass.|It looks like grass.|Hans points out what seems to be grass growing from the object. Preserve the strange appearance as an observation.
27|I see what you mean.||Rafael acknowledges the observation without claiming to know what it is.
32|That's called cordyceps.||The stranger supplies its name. Use the same term as the registered trade-good label.
35|||Rafael reacts without words as an unfamiliar voice identifies the object.
40|In China, it's prized as medicine.||The stranger describes how it is valued in China. Keep the attribution as part of his account.
43|||Rafael is surprised that what he took for an insect is used as medicine.
48|||Hans's musing echoes Rafael's surprise and leaves room for the stranger to make his offer.
52|That's right. Here, you can have this.||The stranger confirms what he said and offers something new. The next two lines identify it.
56|||Rafael asks about the offered object without assuming what it is.
61|It's a book about all sorts of ingredients used in medicine.|ingredients used in medicine.|The stranger identifies the book and describes its scope broadly. His answer gives no particular recipe.
64|||Rafael politely declines because he considers the book valuable.
68|||The stranger says he no longer needs the book and repeats his offer without naming a price.
71|||Rafael starts to object and trails off. Keep the interruption before the older man replies.
76|||The older man chuckles and points out that Rafael's companion looks interested. He claims no family or formal relationship.
79|Huh? Oh, I just thought I'd like to read it.|I'd like to read it.|Hans is caught out and admits his interest, with a small hesitation before he answers.
83|All right. Would you take 1,000 gold for it?|1,000 gold for it?|Rafael acknowledges Hans's interest and offers 1,000 gold instead of accepting the book without payment.
87|Ho ho ho. Make it 100 gold.|100 gold.|The older man keeps his chuckle and asks for one tenth of what Rafael offered.
92|FI's Charm rose by 1!||The notice specifies one point of Charm and keeps the name token. Match the earlier revised stat notice at maximum name width.
""",
}

source = checked_text(getsource(prior_review.main), {
    'len(records) == 81 and len({r["id"] for r in records}) == 81':
        'len(records) == 22 and len({r["id"] for r in records}) == 22',
    'for r in records) == 2': 'for r in records) == 0',
    'for r in records) == 6': 'for r in records) == 1',
})
scope = vars(prior_review) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
