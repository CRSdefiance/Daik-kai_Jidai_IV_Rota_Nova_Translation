"""Review the lookout calls, recruitment, resupply, and market tutorials."""

from scripts import review_hodram_B131_B132_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B133_B136_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    133: "Eight different crew voices spot the same creature they have heard about. The alarm, confidence and forms of address differ with the speaker.",
    134: "Hodram finds Gerhard recruiting replacements after injuries. The player can take charge and hear about recruiting and provisioning, or leave it to Gerhard.",
    135: "Manuel is about to take on supplies. Both paths explain what he can handle. The tutorial describes the risk of shortages, the cash limit and changing the mix of provisions.",
    136: "Charles is selling recovered goods. The player can step in and see the trade controls or have Charles leave the cargo aboard.",
}
DECISIONS = {
    133: """
SC1_B133_STYLE_10_0|||The first lookout calls to the admiral and recognizes the fish in two bursts. Keep the short, urgent recognition.
SC1_B133_STYLE_10_38|Admiral! I can see the monster fish!|the monster fish!|This lookout tells the admiral that the fish is in sight. The complete statement distinguishes this slightly steadier voice from the first lookout's abrupt pointing.
SC1_B133_STYLE_10_78|||This lookout first directs attention outward and then asks whether it is the same creature. Keep the question and uncertainty.
SC1_B133_STYLE_10_124|Aah! Th-there it is! The monster fish!|The monster fish!|The speaker screams, stammers while pointing, and identifies the same fish. Keep the extra alarm specific to this variant.
SC1_B133_STYLE_10_176|||The blunt call and skeptical question suit the less formal voice. Keep the distinct lack of an address to the admiral.
SC1_B133_STYLE_10_218|||The stammer on Admiral and emphatic Look preserve this lookout's sudden shock.
SC1_B133_STYLE_10_256|Waaah! There's a monster fish out there!|a monster fish|The alarm comes before the warning, and the creature is described without claiming the lookout recognizes it.
SC1_B133_STYLE_10_296|Admiral! Look out there! It's the monster fish!|Look out there!;the monster fish!|The more emphatic address and full recognition distinguish the final voice from the clipped first call. Preserve its own native slot.
""",
    134: """
5|||Hodram greets Gerhard by his given name and waits for him to explain what he is doing.
9|Good timing, Admiral. Some of our crew were wounded, so I'm recruiting sailors. Would you like to take over?|Some of our crew;recruiting sailors.;like to take over?|Gerhard explains the injuries and ongoing recruitment before inviting Hodram's direction. The invitation leads naturally to the two answers.
SC1_B134_CHOICE_134_0|||The affirmative answer takes responsibility for the recruitment and moves into the tutorial branch.
SC1_B134_CHOICE_134_1|||The original alternative delegates the work to Gerhard. Keep the direct address and the separate branch.
25|Buy the house a round and people looking for work are sure to come over. That makes it easy to recruit sailors.|Buy the house a round;looking for work;recruit sailors.|Gerhard proposes buying drinks for the patrons to draw people looking for work, making it quicker to recruit.
28|||The notice advises bringing more sailors for boarding and warns that a larger crew reduces the distance the fleet can sail. Both parts belong together.
33|||Gerhard acknowledges the decision to delegate. Keep his efficient assent.
""",
    135: """
5|||Hodram checks whether Manuel is ready to depart. The clipped greeting fits a practical order of business.
9|Ah, Admiral. I'm just about to take on supplies. What would you like us to do?|take on supplies.;would you like us to do?|Manuel says he is about to resupply and asks for Hodram's instructions. He has yet to receive them.
SC1_B135_CHOICE_124_0|||The affirmative response lets the admiral direct resupply. Keep the same expression as the linked crew lesson uses for acceptance.
SC1_B135_CHOICE_124_1|||The alternative leaves resupply to Manuel. Keep the same delegation language as in the recruitment lesson.
24|I don't think you need special orders for that.|need special orders|Hodram treats the task as routine. His dry reply gives Manuel a chance to agree.
28|True enough. Just tell the crew to resupply and they'll do the rest.|tell the crew to resupply;they'll do the rest.|Manuel explains that giving the ordinary resupply instruction is enough for the crew to finish the job.
32|||The notice advises resupplying before departure. It warns that loss of food and water can wipe out the fleet rather than claiming that loss is inevitable.
35|||The default is to fill up. Insufficient funds reduce the purchase to what the player can afford.
39|||Declining resupply first is the route to changing the food and water ratio. Keep the condition and sequence.
45|Right, right. I'll get on it.|I'll get on it.|Manuel's easy repeated acknowledgment leads into his promise to start at once.
""",
    136: """
5|||Hodram asks about the recovered goods. Haul fits the crew's informal reply without misleading the player about where the goods came from.
9|We did pretty well. I'm selling the goods now. Want to take over?|selling the goods now.;Want to take over?|Charles thinks the haul was good and has started selling it. His question gives Hodram the choice to step in.
SC1_B136_CHOICE_130_0|||The first caption agrees to direct the sale. Keep its shared affirmative phrasing.
SC1_B136_CHOICE_130_1|||The other caption tells Charles not to sell the haul. The original branch keeps it aboard.
24|||The tutorial names the Trade command and directs the player to choose which goods to buy or sell.
27|||An empty cargo hold is required for a purchase. Selling a cargo first is the stated way to free a hold.
31|||The D-pad selects the goods for sale and A confirms the selection. Preserve both controls and their order.
35|||The player picks a local specialty, presses A, and the game places the chosen goods in the hold. The current wording gives each step.
38|||The notice covers all ships and says X completes the deal after purchases and sales are selected.
44|All right. We'll keep the goods aboard.|keep the goods aboard.|Charles acknowledges the refusal to sell and says the haul will remain aboard.
""",
}
review = checked_text(previous.review, {
    "len(records) == 77": "len(records) == 35",
})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::recruitment-resupply-and-trade", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

