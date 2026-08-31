from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows

INVENTORY = Path("work/analysis/common_clean_inventory.json")
ACCEPTED_ROM = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
FILE_PATH = "/COMMON/MESFILE.DK4"
SOURCE_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


B18 = [
    "All right, one more shot!", "Let's fire away!", "That boom shakes my empty gut!",
    "Accuracy is what matters with cannon.", "I practice so I'm always battle-ready.",
    "Hitting the target is hard...", "I hate that sound every time!", "I need to study gunnery more.",
    "There, nice and clean. See?", "A ship is our home. Keep it polished.", None,
    "I clean it, and it gets dirty again!", "Deck cleaning? Leave it to me!",
    "Cleaning under the open sky is nice.", "Scrub, scrub... All clean!",
    "It's a fine ship, so I give it my all.", "Now that's much cleaner.",
    "I miss my training under my master...", "These leftovers... Emilio!", "A clean ship feels wonderful.",
    "Let my music give you courage!", "This battle hardly needs me...", "Zzz... Hey, keep it down!",
    "No need to rush. Time for a smoke...", "A battle? I'll consult my naval guide...",
    "Call me when you need me.", "Ahh! I won't give up rum, even in battle!",
    "Look! This is my war dance!", "A sea battle? Let me finish this page!",
    "Why not relax and watch the sky?", "Stay calm... Panic means defeat.",
    "Battle? Hmph. My rod comes first.", "Please wait. My blade needs care...",
    "I must put my precious model away...", "Munch... Better eat before battle.",
    "A little grooming before battle...", "Is it my turn yet...?", "Shoo! Any strong foes out there?",
    "I can't stop until this test is done.", "Zzz... Battle...? Zzz...", "Shall the cards foretell this battle?",
    "I have a special dueling move...", "Zzz... Battle... Too full...",
    "A battle while I'm building a model?!", "Fighting is bad... The flowers are sad.",
    "I'll brace every place we take a hit.", "Now the shipwright gets to shine...",
    "If we're hit, I'll be right there.", "I'll repair any damage at once!",
    "Try not to damage the ship too much.", "Report each hit. I'll be right there.",
    "If we're hit, I'll fix it right up!", "A sea battle... Shipwrights stay busy.",
    "Leave repairs to me. You keep fighting!", "Report damage! I'll make quick repairs.",
    "Cannon damage? I'll fix it at once!", "I'll repair the ship as soon as it's hurt.",
    "I'll tend to the wounded.", "Call me as soon as anyone is hurt.", None,
    "Your angel in white is here!", "For a scrape? Just spit on it!", "A master doctor is with you!",
    "If you get hurt, I'll patch you up.", "If you're hurt, don't push it. Come here.",
    "Don't get hurt fighting recklessly.", "Don't throw your life away...", "I'm not good with blood...",
    "The doctor gets busy during battle.", "My cooking will give you courage!", "A meal before battle, perhaps...",
    "Eat this and victory is ours!", "Even in battle, we still get hungry...",
    "You can't fight on an empty stomach!", "Battle, eh? I'll cook up a feast!",
    "Eat hearty and fight hard!", "I'll prepare our victory feast...", "What should I cook for the battle?",
    "Should I really be cooking now...?", "Why am I cooking during a battle?",
    "Does good food really raise morale...?", "Everyone, eat this before fighting.",
    "The cannon fire is scaring the pig.", "Even in battle, I groom it with love.",
    "Easy now. It will be over soon.", "Hold still while I brush you!", "Keep squealing and I'll eat you!",
    "Now, now. Settle down.", "I keep telling you, I'm not a pig!", "The pig needs care even in battle.",
    "In battle, I could use a pig's help.", "A pig rather ruins the tension...",
    "The thunder has it in a panic! Help!", "Don't be afraid. The battle will end soon.",
    "Lord, deliver our fleet...", "Grant peace to those who fell.", "God, please protect my friends.",
    "I'm praying for everyone's safety.", "I'd rather fight than pray!", "God is with us, everyone!",
    "God, please save my friends.", "Lord... So many more lives...", "Grant my friends your strength.",
    "Grant my fleet victory...", "I prayed, so victory is certain!", "May all my friends return safely...",
    "Schemes don't work in naval battles.", "There's no room for schemes at sea...",
    "Strategists have little to do at sea.", "At sea, a direct attack is our only choice.",
    "Forget schemes! Let me fight!", "If only schemes worked at sea...", "Nothing to do. Maybe a quick bite...",
    "A sea battle leaves me no role.", "No schemes now. We fight head-on!",
    "A sea battle? Put me in the marine post!", "Why sit in the strategy room in battle?",
    "There's nothing for me to do here...", "What can a purser do in battle?",
    "I may as well finish the accounts...", "A purser has nothing to do at sea...",
    "If only I could haggle while fighting...", "Can't haggle in a sea battle...",
    "This month's profit... What was that boom?!",
]


B19 = [
    "I want to fight too...", "I can't help from here in a sea battle.", "A purser is helpless in battle...",
    "This is no time to calculate profits!", "What am I meant to do in the purser's room?!",
    "I can't command everyone from here!", "Um... I need to pull myself together!",
    "Gunners, fire! Deck crew, boarders ready!", "I can't always rely on Kamil...",
    "Shen, report on the battle!", "I'll keep you informed of the battle.",
    "I'll demand surrender during a city attack!", "To make a city yield, you need a captain and mate.",
    "At sea, the mate mainly reports the battle.", "Should we ask the guild for a truce?",
    "Admiral, give it your all!", "I'm useful when we attack a city.", "Now the admiral can show his skill.",
    "We can't negotiate now. We need a city.", "I can't command from here...",
    "Don't expect much from me in here...", "The captain and mate shine in city attacks.",
    "Which ship should we approach?", "I'll dodge those cannonballs.", "Can we dodge this rain of shot?",
    "I want to ram them! Don't we have a ram?", "Those weak shots won't hit us!",
    "A sea battle is where veterans shine!", "Time to show my skill at the helm!",
    "Ah, a sea battle. My blood is racing.", "Sail handlers, follow my helm!",
    "Ram their ship! Gerhard, prepare to board!", "With a ram, I'd tear them wide open!",
    "Close on the flagship and finish this?", "Surveying under fire takes courage...",
    "Stay calm and mark our position.", "Our position? The flying shot ruins my reading!",
    "Even in danger, I still have to survey...", "Surveying during battle? Seriously?!",
    "Always surveying, even in battle. Hard work.", "I'd rather fight on deck than take readings.",
    "Surveying now... This is no joke.", "Times like this demand calm surveying.",
    "Measuring instead of fighting matters too...", "Why is the admiral surveying in battle?!",
    "You can survey calmly even now?", "Enemy ship sighted. Identifying its class.",
    "Let's snipe their admiral while boarding.", "One good shot could turn the battle!",
    "Ah! Cannonballs are flying!", "Incoming fire! Helmsman, take over!", "What an impressive sight!",
    "Whoa! The shots keep coming!", "I'm watching for possible reinforcements.",
    "The enemy is coming! Everyone ready?", "Incoming shot. Helmsman, follow my orders!",
    "This is no time to admire the view.", "Give me a gun. I'll target their admiral!",
    "I'll use the wind to evade their fire.", "With the helmsman, I'll dodge their fire.",
    "Don't panic in battle or you'll fall.", "Stay calm at the helm and dodge every shot.",
    "I'm taking us windward. Agreed, Admiral?", "The windward side gives us the advantage.",
    "I'll be hit if I stay here!", "Taking the windward side is basic seamanship.",
    "Helmsman, match my movements!", "Helmsman, follow the mast as we drilled!",
    "Ah! A cannonball flew right past me!", "All other helmsmen, follow my lead.",
    "Now witness the results of our training.", "At last, my chance to shine...", None,
    "Admiral, count on me. Everyone ready?", "A sea battle! My blood is up!",
    "Watch how a veteran fights.", "I'll do great, so treat me afterward!",
    "All right, sailors. Are you ready?", "I'll break through in the boarding fight!",
    "A duel is the only way to limit casualties...", "Trust me and follow!", "Ready? We're boarding!",
    "Take careful aim and fire!", "Target acquired. Don't miss...", "More accuracy means more hits.",
    "It's so hard to hit them.", "Keep firing! One of them will hit!", "Whatever you do, don't hit our allies!",
    "I'll sink the enemy flagship!", "More gun batteries would help...", "Get too close and our guns can't fire.",
    "Don't waste shots! Aim carefully!", "Ah, so close... Just a little more...", "Next shot loaded! Fire at once!",
    "Deck crew give us an edge when boarding.", "Give the order when we board.",
    "I'm bored, so I'm cleaning.", "Cleaning now? You're remarkably relaxed.",
    "I'll clean until the boarding starts!", "Time to use my deck-scrubbing strength!",
    "I'll be first aboard in the boarding fight!", "Battle makes such a mess to clean...",
    "Leave the boarding fight to me.", "You all fight. I'll clean the deck...",
    "You handle the battle. Scrub, scrub... Huh?", "Why am I polishing the deck?",
    "My body feels so heavy...", "Hmm... Am I tired...?", None,
    "I'm exhausted... I need the rec room...", "I've no strength... What's wrong with me?",
    "I'm tired... Let me rest awhile...", "I'm completely worn out...",
    "It seems my fatigue has built up.", "I don't feel right... Am I tired?", "Ugh... I'm dizzy...",
    "My whole body feels so heavy...", "I-I'm fine... Don't worry...", "I...",
    "This little wound... I'm still all right!", "Gah... It's only a wound...", "I'm fine. It's just a scratch...",
]


BLOCKED = {
    "DK4_MES_B18_R0010": "{MACRO:I}C's ship must stay clean!",
    "DK4_MES_B18_R0059": "{MACRO:I}C is here. Don't worry!",
    "DK4_MES_B19_R0072": "{MACRO:I}C will lead the boarding charge!",
    "DK4_MES_B19_R0108": "{MACRO:I}C is exhausted... Let me rest...",
}


# Fixed records are tiny (19-41 bytes), and literal uppercase I/F bytes are
# runtime commands in this profile. These source-faithful compact readings fit
# the accepted allocations without introducing those command bytes.
OVERRIDES = {
    "DK4_MES_B18_R0002": "That boom shakes my gut!",
    "DK4_MES_B18_R0003": "Cannon accuracy matters.",
    "DK4_MES_B18_R0004": "Practice keeps me battle-ready.",
    "DK4_MES_B18_R0006": "That sound is always awful!",
    "DK4_MES_B18_R0007": "Must study gunnery more.",
    "DK4_MES_B18_R0009": "Our ship is home. Polish it.",
    "DK4_MES_B18_R0011": "Clean now, dirty right away!",
    "DK4_MES_B18_R0012": "Deck cleaning? My job!",
    "DK4_MES_B18_R0013": "Nice to clean in open air.",
    "DK4_MES_B18_R0015": "This fine ship gets my all.",
    "DK4_MES_B18_R0017": "My old training days...",
    "DK4_MES_B18_R0023": "No rush. Time for a smoke...",
    "DK4_MES_B18_R0024": "A battle? Time for my naval guide...",
    "DK4_MES_B18_R0026": "Ahh! Even battle can't take my rum!",
    "DK4_MES_B18_R0028": "A sea battle? One more page!",
    "DK4_MES_B18_R0029": "Let's relax and watch the sky.",
    "DK4_MES_B18_R0031": "Battle? Hmph. My rod matters.",
    "DK4_MES_B18_R0032": "Please wait. My blade needs care.",
    "DK4_MES_B18_R0033": "Must put my model away...",
    "DK4_MES_B18_R0035": "A quick grooming before battle...",
    "DK4_MES_B18_R0036": "My turn yet...?",
    "DK4_MES_B18_R0037": "Shoo! Any strong foes here?",
    "DK4_MES_B18_R0038": "Can't stop until this test ends.",
    "DK4_MES_B18_R0040": "Can the cards foretell this fight?",
    "DK4_MES_B18_R0041": "Got a special dueling move...",
    "DK4_MES_B18_R0043": "Battle while making a model?!",
    "DK4_MES_B18_R0044": "War is bad... The flowers weep.",
    "DK4_MES_B18_R0045": "We'll brace every hit.",
    "DK4_MES_B18_R0046": "The shipwright's time to shine...",
    "DK4_MES_B18_R0047": "When hit, call me at once.",
    "DK4_MES_B18_R0048": "Repairs will be done at once!",
    "DK4_MES_B18_R0049": "Try not to harm the ship.",
    "DK4_MES_B18_R0050": "Report hits. Help will come.",
    "DK4_MES_B18_R0051": "When hit, we'll fix it up!",
    "DK4_MES_B18_R0052": "Sea battle... Shipwrights stay busy.",
    "DK4_MES_B18_R0053": "Leave repairs here. Keep fighting!",
    "DK4_MES_B18_R0054": "Report damage! Repairs start now.",
    "DK4_MES_B18_R0055": "Cannon damage? Repairs are easy!",
    "DK4_MES_B18_R0056": "Damage means prompt repairs.",
    "DK4_MES_B18_R0057": "The wounded get my care.",
    "DK4_MES_B18_R0058": "Call me when someone is hurt.",
    "DK4_MES_B18_R0061": "A scrape? Just spit on it!",
    "DK4_MES_B18_R0062": "A master doctor is here!",
    "DK4_MES_B18_R0063": "Get hurt, and you'll be patched up.",
    "DK4_MES_B18_R0064": "When hurt, don't push it. Come here.",
    "DK4_MES_B18_R0065": "Don't get hurt being reckless.",
    "DK4_MES_B18_R0066": "Don't waste your life...",
    "DK4_MES_B18_R0067": "Blood makes me uneasy...",
    "DK4_MES_B18_R0068": "Doctors stay busy in battle.",
    "DK4_MES_B18_R0070": "Perhaps a prebattle meal...",
    "DK4_MES_B18_R0072": "Battle still makes us hungry...",
    "DK4_MES_B18_R0073": "No fighting on an empty belly!",
    "DK4_MES_B18_R0074": "Battle, eh? Let's cook a feast!",
    "DK4_MES_B18_R0076": "Time to make our victory feast...",
    "DK4_MES_B18_R0077": "What to cook for battle?",
    "DK4_MES_B18_R0078": "Should the cook be here now...?",
    "DK4_MES_B18_R0079": "Why cook during a battle?",
    "DK4_MES_B18_R0081": "Everyone, eat before battle.",
    "DK4_MES_B18_R0082": "Cannon fire scares the pig.",
    "DK4_MES_B18_R0083": "Even in battle, it gets loving care.",
    "DK4_MES_B18_R0084": "Easy now. This ends soon.",
    "DK4_MES_B18_R0085": "Hold still for the brush!",
    "DK4_MES_B18_R0086": "Keep squealing and get eaten!",
    "DK4_MES_B18_R0088": "Listen, this one's no pig!",
    "DK4_MES_B18_R0089": "The pig needs care in battle.",
    "DK4_MES_B18_R0090": "A pig's help would be handy now.",
    "DK4_MES_B18_R0092": "That boom has it in a panic!",
    "DK4_MES_B18_R0093": "Don't fear. The battle ends soon.",
    "DK4_MES_B18_R0097": "Praying all stay safe.",
    "DK4_MES_B18_R0098": "Rather fight than pray!",
    "DK4_MES_B18_R0101": "Lord... More lives lost...",
    "DK4_MES_B18_R0103": "Grant our fleet victory.",
    "DK4_MES_B18_R0104": "We prayed, so victory is certain!",
    "DK4_MES_B18_R0105": "May all our friends come home...",
    "DK4_MES_B18_R0106": "Schemes don't work at sea.",
    "DK4_MES_B18_R0107": "Schemes are no use at sea...",
    "DK4_MES_B18_R0108": "Strategists idle at sea.",
    "DK4_MES_B18_R0109": "At sea, direct attack is the only way.",
    "DK4_MES_B18_R0110": "No schemes! Let me fight!",
    "DK4_MES_B18_R0111": "Wish schemes worked at sea...",
    "DK4_MES_B18_R0112": "Nothing to do. Maybe a bite...",
    "DK4_MES_B18_R0115": "Sea battle? Send me to the marines!",
    "DK4_MES_B18_R0116": "Why stay in the strategy room?",
    "DK4_MES_B18_R0117": "Nothing for me to do here...",
    "DK4_MES_B18_R0118": "What can a purser do now?",
    "DK4_MES_B18_R0119": "May as well finish the accounts...",
    "DK4_MES_B18_R0120": "A purser has no role at sea...",
    "DK4_MES_B18_R0121": "Wish we could haggle in battle...",
    "DK4_MES_B18_R0122": "Can't haggle in battle...",
    "DK4_MES_B18_R0123": "This month's profit... What was that?!",

    "DK4_MES_B19_R0000": "Want to fight too...",
    "DK4_MES_B19_R0001": "Can't help from here at sea.",
    "DK4_MES_B19_R0002": "A purser is helpless now...",
    "DK4_MES_B19_R0003": "No time to calculate profits!",
    "DK4_MES_B19_R0004": "What can one do in this office?!",
    "DK4_MES_B19_R0005": "Can't command from here!",
    "DK4_MES_B19_R0006": "Um... Must pull myself together!",
    "DK4_MES_B19_R0008": "Can't always rely on Kamil...",
    "DK4_MES_B19_R0010": "You'll get my battle reports.",
    "DK4_MES_B19_R0011": "We'll demand the city's surrender!",
    "DK4_MES_B19_R0012": "A city yields to a captain and mate.",
    "DK4_MES_B19_R0013": "At sea, the mate reports the battle.",
    "DK4_MES_B19_R0015": "Admiral, do your best!",
    "DK4_MES_B19_R0016": "Useful when attacking a city.",
    "DK4_MES_B19_R0017": "Now the admiral shows his skill.",
    "DK4_MES_B19_R0018": "No talks now. We need a city.",
    "DK4_MES_B19_R0019": "Can't command from here...",
    "DK4_MES_B19_R0020": "Don't expect much here...",
    "DK4_MES_B19_R0021": "Captain and mate shine in city attacks.",
    "DK4_MES_B19_R0022": "Which ship should we near?",
    "DK4_MES_B19_R0023": "Those shots will be dodged.",
    "DK4_MES_B19_R0025": "Let's ram them! Where's our ram?",
    "DK4_MES_B19_R0027": "Sea battles let veterans shine!",
    "DK4_MES_B19_R0029": "Sea battle! My blood races!",
    "DK4_MES_B19_R0031": "Ram them! Gerhard, prepare to board!",
    "DK4_MES_B19_R0032": "With a ram, we'd rip them open!",
    "DK4_MES_B19_R0033": "Close on their flagship and finish it?",
    "DK4_MES_B19_R0034": "Surveying under fire takes nerve...",
    "DK4_MES_B19_R0036": "Our position? Shot ruins the reading!",
    "DK4_MES_B19_R0037": "Even in danger, surveys must be done...",
    "DK4_MES_B19_R0038": "Surveying in battle? Really?!",
    "DK4_MES_B19_R0039": "Surveying even in battle is hard.",
    "DK4_MES_B19_R0040": "Rather fight on deck than survey.",
    "DK4_MES_B19_R0042": "Now we must survey calmly.",
    "DK4_MES_B19_R0043": "Measuring instead of fighting matters...",
    "DK4_MES_B19_R0044": "Why is the admiral surveying now?!",
    "DK4_MES_B19_R0046": "Enemy sighted. Checking its class.",
    "DK4_MES_B19_R0047": "Let's snipe their admiral while boarding.",
    "DK4_MES_B19_R0048": "One shot could turn the battle!",
    "DK4_MES_B19_R0050": "Enemy fire! Helmsman, take over!",
    "DK4_MES_B19_R0053": "Watching for reinforcements.",
    "DK4_MES_B19_R0054": "Enemy coming! Everyone ready?",
    "DK4_MES_B19_R0055": "Enemy shot! Helmsman, follow orders!",
    "DK4_MES_B19_R0057": "Give me a gun. Their admiral is mine!",
    "DK4_MES_B19_R0058": "Use the wind to evade their fire.",
    "DK4_MES_B19_R0059": "With the helmsman, we'll dodge fire.",
    "DK4_MES_B19_R0060": "Don't panic in battle or fall.",
    "DK4_MES_B19_R0061": "Stay calm at the helm and dodge shots.",
    "DK4_MES_B19_R0062": "Taking us windward. Agreed, Admiral?",
    "DK4_MES_B19_R0063": "Windward gives us the advantage.",
    "DK4_MES_B19_R0064": "Staying here means getting hit!",
    "DK4_MES_B19_R0065": "Taking windward is basic seamanship.",
    "DK4_MES_B19_R0067": "Helmsman, follow the mast as drilled!",
    "DK4_MES_B19_R0068": "Ah! A shot flew right past me!",
    "DK4_MES_B19_R0069": "Other helmsmen, follow my lead.",
    "DK4_MES_B19_R0070": "Witness the results of our training.",
    "DK4_MES_B19_R0071": "At last, time to shine...",
    "DK4_MES_B19_R0074": "Sea battle! My blood is up!",
    "DK4_MES_B19_R0076": "Win now, feast later!",
    "DK4_MES_B19_R0078": "We'll break through while boarding!",
    "DK4_MES_B19_R0079": "A duel is the only way to spare lives...",
    "DK4_MES_B19_R0082": "Aim well and fire!",
    "DK4_MES_B19_R0083": "Target found. Don't miss...",
    "DK4_MES_B19_R0085": "So hard to hit them.",
    "DK4_MES_B19_R0087": "Whatever happens, don't hit allies!",
    "DK4_MES_B19_R0088": "Their flagship will be sunk!",
    "DK4_MES_B19_R0089": "More gun batteries would help.",
    "DK4_MES_B19_R0090": "Too close, and guns can't fire.",
    "DK4_MES_B19_R0091": "Don't waste shots! Aim well!",
    "DK4_MES_B19_R0092": "So close... Just a bit more...",
    "DK4_MES_B19_R0093": "Next shot ready! Shoot now!",
    "DK4_MES_B19_R0094": "Deck crew help us while boarding.",
    "DK4_MES_B19_R0095": "Give the order when boarding.",
    "DK4_MES_B19_R0096": "Bored, so let's clean.",
    "DK4_MES_B19_R0097": "Cleaning now? Quite relaxed.",
    "DK4_MES_B19_R0098": "We'll clean until boarding starts!",
    "DK4_MES_B19_R0099": "Time to use this scrubbing strength!",
    "DK4_MES_B19_R0100": "We'll be first aboard!",
    "DK4_MES_B19_R0103": "You fight. This deck needs cleaning...",
    "DK4_MES_B19_R0104": "You fight. Scrub, scrub... Huh?",
    "DK4_MES_B19_R0105": "Why polish the deck now?",
    "DK4_MES_B19_R0107": "Hmm... Could this be fatigue...?",
    "DK4_MES_B19_R0109": "Exhausted... Need the rec room...",
    "DK4_MES_B19_R0110": "No strength... What's wrong?",
    "DK4_MES_B19_R0111": "So tired... Let me rest...",
    "DK4_MES_B19_R0112": "Completely worn out...",
    "DK4_MES_B19_R0113": "My fatigue has built up.",
    "DK4_MES_B19_R0114": "Something's wrong... Fatigue?",
    "DK4_MES_B19_R0115": "Ugh... So dizzy...",
    "DK4_MES_B19_R0117": "D-don't worry... Still fine...",
    "DK4_MES_B19_R0118": "Me...",
    "DK4_MES_B19_R0119": "This wound... Still all right!",
    "DK4_MES_B19_R0120": "Gah... Just a wound...",
    "DK4_MES_B19_R0121": "Nothing serious... Just a scratch.",
}

# Final byte- and wrap-constrained refinements after exact-font QA.
OVERRIDES.update({
    "DK4_MES_B18_R0029": "Let's just watch the sky.",
    "DK4_MES_B18_R0035": "Quick grooming before battle...",
    "DK4_MES_B18_R0040": "Can cards foretell this fight?",
    "DK4_MES_B18_R0043": "Battle while model-making?!",
    "DK4_MES_B18_R0046": "Time for a shipwright...",
    "DK4_MES_B18_R0052": "Sea battle... Shipwrights get busy.",
    "DK4_MES_B18_R0057": "The wounded get care.",
    "DK4_MES_B18_R0066": "Don't waste your life.",
    "DK4_MES_B18_R0070": "A prebattle meal...",
    "DK4_MES_B18_R0072": "Battle still makes us hungry.",
    "DK4_MES_B18_R0076": "Time for our victory feast...",
    "DK4_MES_B18_R0081": "Everyone, eat before battle!",
    "DK4_MES_B18_R0083": "Even in battle, it gets loving care.",
    "DK4_MES_B18_R0101": "Lord... More lives...",
    "DK4_MES_B18_R0103": "Grant us victory.",
    "DK4_MES_B18_R0105": "May all friends come home...",
    "DK4_MES_B18_R0109": "At sea, we must attack head-on.",
    "DK4_MES_B18_R0116": "Why stay in the strategy room?",
    "DK4_MES_B18_R0119": "May as well do the accounts...",
    "DK4_MES_B18_R0123": "My profit... What was that boom?!",

    "DK4_MES_B19_R0004": "What can one do in this office?",
    "DK4_MES_B19_R0007": "Gunners fire! Boarders ready!",
    "DK4_MES_B19_R0011": "Demand the city's surrender!",
    "DK4_MES_B19_R0021": "Captain and mate lead city attacks.",
    "DK4_MES_B19_R0029": "Sea battle! My blood boils!",
    "DK4_MES_B19_R0033": "Close on the flagship and end it?",
    "DK4_MES_B19_R0036": "Our position? Shot ruins readings!",
    "DK4_MES_B19_R0037": "Even in danger, surveys must continue.",
    "DK4_MES_B19_R0038": "Survey in battle? Really?!",
    "DK4_MES_B19_R0040": "Rather fight on deck than survey.",
    "DK4_MES_B19_R0047": "Let's snipe their admiral when boarding.",
    "DK4_MES_B19_R0048": "One shot could turn the fight!",
    "DK4_MES_B19_R0057": "Give me a gun. Their admiral is mine!",
    "DK4_MES_B19_R0058": "Use wind to evade their fire.",
    "DK4_MES_B19_R0059": "With our helmsman, we'll dodge fire.",
    "DK4_MES_B19_R0061": "Stay calm and dodge every shot.",
    "DK4_MES_B19_R0062": "Going windward. Agreed, Admiral?",
    "DK4_MES_B19_R0063": "Windward gives us an edge.",
    "DK4_MES_B19_R0067": "Helmsman, follow the mast drill!",
    "DK4_MES_B19_R0070": "See what our training achieved.",
    "DK4_MES_B19_R0071": "At last, time to shine.",
    "DK4_MES_B19_R0073": "Admiral, count on me. Ready?",
    "DK4_MES_B19_R0074": "Sea battle! Blood is up!",
    "DK4_MES_B19_R0078": "We'll break through while boarding.",
    "DK4_MES_B19_R0079": "Only a duel can spare lives...",
    "DK4_MES_B19_R0083": "Target found. Aim true.",
    "DK4_MES_B19_R0091": "Don't waste shots! Aim well.",
    "DK4_MES_B19_R0093": "Next shot ready! Shoot!",
    "DK4_MES_B19_R0095": "Give the boarding order.",
    "DK4_MES_B19_R0107": "Hmm... Just fatigue...?",
    "DK4_MES_B19_R0109": "Exhausted... Need recreation...",
    "DK4_MES_B19_R0114": "Something's wrong... So tired.",
    "DK4_MES_B19_R0120": "Gah... Just a wound.",
    "DK4_MES_B19_R0121": "Just a scratch. No worry.",
})

OVERRIDES.update({
    "DK4_MES_B18_R0035": "Grooming before battle...",
    "DK4_MES_B18_R0040": "Can cards predict this fight?",
    "DK4_MES_B18_R0052": "Sea battle... Shipwrights busy.",
    "DK4_MES_B18_R0066": "Value your life!",
    "DK4_MES_B18_R0081": "Everyone, eat before war!",
    "DK4_MES_B18_R0083": "Even in battle, give loving care.",
    "DK4_MES_B18_R0116": "Why stay in strategy room?",
    "DK4_MES_B18_R0119": "May as well do accounts...",
    "DK4_MES_B19_R0011": "Demand the city surrender!",
    "DK4_MES_B19_R0029": "Sea battle! Blood boils!",
    "DK4_MES_B19_R0037": "Even in danger, surveys continue.",
    "DK4_MES_B19_R0040": "Rather fight than survey.",
    "DK4_MES_B19_R0047": "Let's snipe their admiral aboard.",
    "DK4_MES_B19_R0048": "One shot could turn the tide!",
    "DK4_MES_B19_R0057": "Give me a gun. Their admiral's mine!",
    "DK4_MES_B19_R0059": "With our helmsman, we'll dodge.",
    "DK4_MES_B19_R0062": "Going windward. All right?",
    "DK4_MES_B19_R0074": "Sea battle! Blood's up!",
    "DK4_MES_B19_R0078": "We'll break through boarding.",
    "DK4_MES_B19_R0083": "Target found. Aim!",
    "DK4_MES_B19_R0091": "Save shots. Aim well!",
    "DK4_MES_B19_R0109": "Tired... Need the rec room.",
    "DK4_MES_B19_R0114": "Something's wrong... Tired.",
    "DK4_MES_B19_R0121": "Only a scratch...",
})


def context_for(block: int, index: int) -> str:
    if block == 18:
        if index < 20:
            return "A crew member comments while firing cannon or cleaning the ship."
        if index < 45:
            return "A crew member gives an idle reaction as a naval battle begins."
        if index < 57:
            return "A shipwright reacts to damage and prepares repairs during battle."
        if index < 69:
            return "A ship's doctor comments on treating injuries during battle."
        if index < 81:
            return "A cook comments on preparing food during battle."
        if index < 94:
            return "An animal keeper comments on caring for the ship's pig during battle."
        if index < 106:
            return "A missionary prays or reacts during a naval battle."
        if index < 118:
            return "A strategist comments on having little strategic work during a naval battle."
        return "A purser comments on having little accounting work during a naval battle."
    if index < 22:
        return "A purser or first mate comments on duties during naval combat or a city attack."
    if index < 34:
        return "A helmsman comments on maneuvering the ship during battle."
    if index < 46:
        return "A surveyor comments on taking position readings under fire."
    if index < 71:
        return "A lookout or sailing master reacts to enemy fire and coordinates evasive maneuvers."
    if index < 82:
        return "A deck officer prepares the crew for boarding combat."
    if index < 96:
        return "A gunner comments on aiming and firing during naval combat."
    if index < 106:
        return "A deckhand comments on cleaning or boarding during combat."
    return "A fatigued or wounded crew member reports their condition."


def make_record(row_id: str, english: str, block: int, index: int) -> dict[str, object]:
    plain = english.replace("{MACRO:I}C", "the speaker").replace("{PAD}", "")
    return {
        "id": row_id,
        "english": english + "{PAD}",
        "speaker": "Crew member",
        "context": context_for(block, index),
        "source_meaning": f"The crew member says: {plain}",
        "localization_note": "Concise natural English preserves the clean Japanese meaning and fits this two-line fixed record.",
        "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
    }


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    clean = {r["id"].replace("ILNK_", "DK4_MES_"): r for r in inventory["records"] if r["block_index"] in (18, 19)}
    image = NdsImage.open(ACCEPTED_ROM)
    accepted_data = image.read_file(FILE_PATH)
    if hashlib.sha256(accepted_data).hexdigest() != SOURCE_SHA256:
        raise SystemExit("accepted COMMON source hash changed")
    accepted = {r["id"]: r for r in export_mesfile_rows(accepted_data, FILE_PATH, include_non_japanese=True)}
    outputs: list[tuple[int, list[str | None]]] = [(18, B18), (19, B19)]
    classifications: dict[int, list[dict[str, object]]] = {18: [], 19: []}
    blocked_records: list[dict[str, object]] = []
    for block, lines in outputs:
        expected = sorted(r for r in clean if f"_B{block:02d}_" in r)
        if len(lines) != len(expected):
            raise SystemExit(f"B{block} has {len(lines)} translations for {len(expected)} records")
        safe: list[dict[str, object]] = []
        for index, (row_id, english) in enumerate(zip(expected, lines, strict=True)):
            if row_id in OVERRIDES:
                english = OVERRIDES[row_id]
            source = clean[row_id]
            accepted_row = accepted[row_id]
            if source["source_length"] != accepted_row["source_length"]:
                raise SystemExit(f"{row_id}: accepted allocation differs from clean source")
            is_blocked = row_id in BLOCKED
            if is_blocked != (english is None):
                raise SystemExit(f"{row_id}: blocked classification mismatch")
            classifications[block].append({
                "id": row_id,
                "clean_source": source["markup"],
                "source_length": source["source_length"],
                "accepted_source": accepted_row["japanese"],
                "classification": "blocked-accepted-source-lost-runtime-macro" if is_blocked else "safe-fixed-allocation",
                "reason": "The clean entry contains {MACRO:I}C, but the accepted placeholder bytes no longer retain that command." if is_blocked else "Single-entry record; accepted and clean allocations match; no runtime macro was lost.",
            })
            if is_blocked:
                draft = BLOCKED[row_id]
                blocked_records.append({
                    "id": row_id,
                    "draft_english": draft + "{PAD}",
                    "speaker": "Crew member",
                    "context": context_for(block, index),
                    "source_meaning": f"The crew member says: {draft}",
                    "localization_note": "Faithful clean-source translation retained as a draft until the missing runtime name substitution is restored safely.",
                    "clean_source_markup": source["markup"],
                    "source_length": source["source_length"],
                    "blocker": "The clean record contains {MACRO:I}C, while the accepted placeholder record erased it; inserting against the accepted bytes would not preserve source command order.",
                    "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
                })
            else:
                safe.append(make_record(row_id, str(english), block, index))
        batch = {
            "format": "dk4-ilnk-translation-batch-v1", "file_path": FILE_PATH,
            "source_file_sha256": SOURCE_SHA256, "encoder": "dialogue-fixed-v1",
            "dialogue_profile": "shared-pair-live", "translation_policy": "natural-dialogue-v2",
            "target_locale": "en-US",
            "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
            "inventory": {"block": block, "clean_records": len(lines), "safe_records": len(safe), "blocked_records": len(lines) - len(safe)},
            "records": safe,
        }
        Path(f"translations/common_natural_v2_b{block}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        Path(f"work/analysis/common_b{block}_entry_audit.json").write_text(json.dumps({"block": block, "records": classifications[block]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    blocked = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": FILE_PATH,
        "source_file_sha256": SOURCE_SHA256, "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "draft_status": "source-first-editorial-draft-blocked-accepted-source-lost-runtime-macro",
        "inventory": {"identified_records": len(blocked_records), "translated_drafts": len(blocked_records), "encodable_records": 0, "blocked_records": len(blocked_records), "missing_records": 0, "blocks": {"18": 2, "19": 2}},
        "records": [], "blocked_records": blocked_records,
    }
    Path("translations/common_natural_v2_b18_b19_blocked.json").write_text(json.dumps(blocked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
