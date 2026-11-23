"""Review the remaining original letter variants and menus in Rafael B241–260."""

from inspect import getsource

from scripts import pair_rafael_B241_B260_20261122 as paired
from scripts import review_rafael_B221_B224_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B241_B260.json"
CARRY = paired.ROOT / "earlier_contextual_decisions_B241_B260.json"
DECISIONS = {
    247: """
STYLE_8_0|||The crew member tells the admiral a letter has arrived from Charles. The brief neutral delivery suits the first voice.
STYLE_8_42|||Keep the formal announcement that they have received a letter, with Charles as the sender.
STYLE_8_84|||The conversational announcement serves both original voice slots in this alias.
STYLE_8_122|||This voice politely says the admiral has a letter from Charles. Preserve the recipient and sender.
STYLE_8_164|||You've got a letter is the natural rougher voice here and keeps the opening address.
STYLE_8_202|||The older voice puts the letter first and calls the admiral by title at the end.
STYLE_8_240|||The excited summons and short notice introduce Charles's letter in the livelier voice.
""",
    248: """
STYLE_8_0|||The crew voice succinctly announces the letter and identifies Jam before his informal opening.
STYLE_8_40|||Keep the more formal received-letter construction as a distinct delivery from the others.
STYLE_8_80|||The casual announcement is shared by both original alias slots. Preserve the sender and the slots.
STYLE_8_116|||The polite voice has a letter for the admiral and identifies Jam without inferring a relationship.
STYLE_8_156|||The familiar You've got a letter captures the rougher original diction.
STYLE_8_192|||The older voice offers the letter first and addresses the admiral at the end.
STYLE_8_228|||Keep the lively call and the short exclamation announcing mail from Jam.
""",
    251: """
494_0|||The first caption affirms travel to the New World and leads to Rafael's direct question about why Francisca asks.
494_1|||The second caption denies having been there and leads to Rafael explaining he has yet to travel that far.
""",
    254: """
698_0|||This accepts the priest's invitation to try moving the figurehead. Keep the inclusive first-person invitation.
698_1|||This declines and leaves the figurehead in the wooden church. The shorter label remains clear after the priest's question.
""",
    260: """
450_0|||The first caption confirms to Cesare that Rafael means to take the figurehead. Keep the direct acknowledgment.
450_1|||The second emphatically denies that he means to take it and sets up Cesare's private disappointment.
""",
}

source = checked_text(getsource(prior.main), {
    '    records = []': '''    carry = base.load(CARRY)
    assert carry["candidate_sha256"] == packet["candidate_sha256"]
    pending = {row["id"] for row in carry["pending_records"]}
    records = []''',
    'zip(group["records"], decisions, strict=True)': 'zip((row for row in group["records"] if row["id"] in pending), decisions, strict=True)',
    'len(records) == 56 and len({row["id"] for row in records}) == 56': 'len(records) == 20 and {row["id"] for row in records} == pending',
    'for row in records) == 15': 'for row in records) == 14',
    'for row in records) == 5': 'for row in records) == 6',
    '    assert not OUTPUT.exists()': '    assert all(row["decision"] == "retention" for row in records)\n    assert not OUTPUT.exists()',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
