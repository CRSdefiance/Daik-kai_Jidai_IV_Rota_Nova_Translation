"""Review40 more SC0 records, preserving message continuity and modal controls."""

from pathlib import Path

from scripts.prepare_name_editorial_v234 import prepare_review

TEXT = {
    "DK4_MES_B159_R0076": ("You come from an old, distinguished family, {MACRO:FI}. That's what worries her.", "Charlotte worries that Rafael's distinguished family background makes them unequal.", "Preserve the established family background without asserting a specific hereditary title."),
    "DK4_MES_B159_R0126": ("... 'Thank you for everything, {MACRO:FI}. My village is safe now.", "Eirene begins Charlotte's message, thanking Rafael and reporting that her village is safe.", "Keep the opening quote and continuation into the next two message records. Natural English places the addressee after the thanks without changing the source meaning."),
    "DK4_MES_B159_R0129": ("I hope {MACRO:FI}'s homeland will be restored too. When your country is back to how it was...", "Charlotte hopes Rafael's country will also recover and begins a condition for her invitation.", "This continues the previous quotation; remove the older draft's extra opening quote. The next record finishes the invitation and closes the quote."),
    "DK4_MES_B159_R0132": ("If you still feel the same as you did then, please come visit me.' ...That's all of her message.", "Charlotte asks Rafael to visit if his feelings remain the same after his country is restored; Eirene then ends the reported message.", "This dependent record closes the quotation opened at R0126 and continued at R0129. Remove its older extra opening quote and preserve the conditional invitation and Eirene's closing narration."),
    "DK4_MES_B159_R0154": ("...You're welcome. Good luck, {MACRO:FI}. What happens with Charlotte is up to you.", "Eirene responds to thanks, encourages Rafael and says the matter of Charlotte depends on him.", "Use a natural response to gratitude and avoid asserting control over Charlotte's entire future."),
    "DK4_MES_B161_R0062": ("Really? If I couldn't stand kids, {MACRO:FI}, I wouldn't have teamed up with you.", "Claudio jokingly says his companionship with Rafael proves he does not dislike children.", "Restore complete conversational sentences and the teasing comparison; Eirene next objects that it is rude to the admiral."),
    "DK4_MES_B164_R0087": ("What a waste! Honestly, {MACRO:FI}, you don't want anything for yourself, do you?", "Claudio laments Rafael's passing up a reward and lack of self-interest.", "Localize 欲がねえ as selfless lack of personal wants rather than the stiff no greed wording. Rafael next explains that work matters more than a reward."),
    "DK4_MES_B164_R0095": ("Fair enough... Let's finish conquering the trade domains! Onward, Admiral {MACRO:FI}!", "Claudio accepts Rafael's explanation and urges completing their domain campaign.", "Retain the established trade-domain terminology and explicit admiral address."),
    "DK4_MES_B165_R0005": ("Welcome, {MACRO:FI}. I'm glad you've come.", "The Portuguese king warmly welcomes Rafael's arrival.", "Restore the warmth of よくぞ来た; no new summons or reward is inserted."),
    "DK4_MES_B166_R0006": ("We're back in Portugal, {MACRO:FI}!", "A companion announces their return to Portugal.", "Use a complete natural arrival announcement."),
    "DK4_MES_B166_R0027": ("...{MACRO:FI}, can I have a word?", "Claudio quietly asks Rafael for a moment to speak before the audience.", "Retain the hesitant conversational request."),
    "DK4_MES_B166_R0073": ("I'm {MACRO:FU}. I have returned to my homeland, Portugal.", "Rafael formally announces his full name and return to his homeland before the king.", "Restore the formal complete self-introduction and report, not a Home at last fragment."),
    "DK4_MES_B166_R0107": ("(That's impressive, {MACRO:FI}!)", "A companion privately admires Rafael being offered the viceroyalty.", "Keep the aside and admiration without inventing a ceremonial action or outfit."),
    "DK4_MES_B166_R0452": ("{MACRO:FI}!! W-what are you all doing?!", "Claudio discovers Rafael and the crew spying and reacts with surprise.", "Restore the source stammer and plural address."),
    "DK4_MES_B166_R0538": ("Hehe, it's all right. Anyway... I heard the news. Congratulations, {MACRO:FI}. Oh, I shouldn't address you so casually now, should I?", "The woman reassures Rafael, congratulates him on the reported honor and corrects her casual address.", "Preserve every part of the courteous teasing response. Keep raw FE and classify its modal transport separately; do not infer the woman's identity from the old letter-caption metadata."),
    "DK4_MES_B166_R0541": ("Th-that's right! Hey, {MACRO:FI}! Should you really be wasting time here?!", "Claudio deflects attention by questioning whether Rafael can afford to linger.", "Retain the stammer and pointed rhetorical question, without inventing a new destination."),
    "DK4_MES_B166_R0770": ("Hehe... Oh, that reminds me! {MACRO:FI}, do you know what this is?", "Eirene remembers the letter and asks whether Rafael recognizes the object.", "Restore the natural recollection/question; the following line identifies it as a letter."),
    "DK4_MES_B166_R0787": ("{MACRO:FI}", "The letter's salutation names Rafael.", "Retain the name-only salutation and raw FE. This is modal letter text, not a spoken NPC line or empty command."),
    "DK4_MES_B166_R0797": ("{MACRO:FI}, thank you very much for everything. I am very well, thank you. Charlotte Miller", "The gloss of Charlotte's beginner Portuguese letter thanks Rafael, reports her well-being and gives her signature.", "Keep the deliberately simple/repetitive thank you wording, which the next speaker calls awkward. Do not polish away that story detail or correct the separate original Portuguese text here. Preserve FE."),
    "DK4_MES_B168_R0051": ("...I'm not a 'kid.' My name is {MACRO:FI} {MACRO:FA}, and I'm this ship's admiral.", "Rafael rejects being called a kid, introduces himself and identifies his actual rank aboard the ship.", "Restore complete natural sentences and the explicit source rank."),
    "DK4_MES_B168_R0067": ("{MACRO:FI}! You don't owe him an apology!", "Claudio insists Rafael need not apologize for the argument.", "The existing natural objection is faithful and retained."),
    "DK4_MES_B168_R0100": ("Heh, then how about it, {MACRO:FI}?", "Claudio cues Rafael to invite Angelo aboard after Angelo acknowledges needing a ship.", "Restore the conversational invitation cue instead of a clipped Then question."),
    "DK4_MES_B176_R0098": ("What a character... {MACRO:FI}, what do we do? Turn him over to the guards?", "Claudio considers handing the returned ship thief to the guards.", "Restore the person being handed over; Call the guard changed the proposed action."),
    "DK4_MES_B176_R0106": ("Hey, {MACRO:FI}, don't tell me his foolishness is catching!", "Claudio jokes that Jam's foolishness has infected Rafael after he proposes recruiting him.", "Localize the contagious-stupidity joke naturally without inventing illness or a real contagion."),
    "DK4_MES_B178_R0064": ("I told you, {MACRO:FI}. To win this game, take coins so you always leave a multiple of four plus one.", "A companion repeats the coin game's winning rule: leave four times an integer plus one coin.", "Preserve the exact strategy and number relation, using complete natural instructions."),
    "DK4_MES_B178_R0089": ("Hey, {MACRO:FI}! I can't stand losing like this! Let's play another round!", "Claudio is frustrated by losing and urges another game.", "Restore the first-person frustration and complete invitation rather than isolated exclamations."),
    "DK4_MES_B178_R0107": ("{MACRO:FI}, listen! I think there may be a way to win this game every time!", "A companion suspects a guaranteed winning strategy exists.", "Preserve the uncertainty in かもしれません; do not prematurely certify the strategy before it is explained."),
    "DK4_MES_B179_R0059": ("{MACRO:FI}... It's rare to meet someone who loves ships this much. Imagine having him aboard...", "A companion admires Manuel's rare devotion to ships and suggests the benefit of recruiting him.", "Keep the unfinished suggestion and enthusiasm; Rafael's next line completes the thought about ship care."),
    "DK4_MES_B181_R0005": ("Hey, {MACRO:FI}, I've had the feeling someone's watching us for a while now.", "Claudio has felt watched for some time.", "Restore the ongoing duration and complete personal observation, retaining uncertainty."),
    "DK4_MES_B181_R0163": ("Come on, {MACRO:FI}! Let's get moving!", "Claudio impatiently pulls Rafael away and urges him to leave.", "Use the natural imperative; the next line objects to Claudio pulling his arm."),
    "DK4_MES_B183_R0019": ("...{MACRO:FI}...", "Sanghyeon respectfully addresses Rafael in the dream.", "Retain the quiet name and surrounding pauses; no unsupported family title is added."),
    "DK4_MES_B184_R0085": ("Well, now I'm curious. Aren't you, {MACRO:FI}?", "Claudio becomes interested in the Golden Crown story and addresses Rafael.", "Restore becoming curious rather than a generic sounds interesting reaction."),
    "DK4_MES_B185_R0054": ("We've fallen behind! Let's hurry too, {MACRO:FI}!", "Claudio recognizes they are behind Julian in searching and urges haste.", "The existing urgency is preserved in natural speech."),
    "DK4_MES_B186_R0012": ("Hello, {MACRO:FI}. Thanks again for your help in Seoul.", "Julian greets Rafael and thanks him for their previous encounter in Seoul.", "Restore 京城ではどうも rather than a bare Hello; the reunion follows the Golden Crown/Mihwa scenes."),
    "DK4_MES_B187_R0019": ("This is bad, {MACRO:FI}! They're all working for her!", "Claudio warns that everyone around them is Aziza's subordinate.", "Preserve the threatening ownership without specifying pirates where this sentence only says subordinates."),
    "DK4_MES_B187_R0092": ("{MACRO:FI} {MACRO:FA}", "Rafael states his full name when Aziza asks who he is.", "Retain the direct name response and both source macros; no speaker selector is invented."),
    "DK4_MES_B206_R0046": ("What?! {MACRO:FI}, did you hear that?!", "Julio excitedly reacts to the news about sake.", "Preserve the surprised question and the reference to the just-heard news."),
    "DK4_MES_B208_R0046": ("{MACRO:FI}: Charm +1!", "Rafael's Charm increases by one.", "Retain the established concise stat feedback, exact quantity, name macro and raw FE selector."),
    "DK4_MES_B20_R0078": ("{MACRO:FI}, the enemy has quite a few ships! Don't forget to send the crew to battle stations!", "A companion warns about the enemy's sizable fleet and reminds Rafael to prepare battle positions.", "Preserve the warning and crew action; old Eirene metadata is not accepted as identity evidence for selector04."),
    "DK4_MES_B213_R0081": ("{MACRO:FI}: Charm +1!", "Rafael's Charm increases by one.", "Retain the established modal stat wording and exact increase."),
    "DK4_MES_B213_R0107": ("{MACRO:FI}: Spirit +1!", "Rafael's Spirit increases by one.", "Retain the established modal stat wording and exact increase; do not substitute a different attribute."),
}

METADATA = {
    "DK4_MES_B159_R0132": {"related_record_template": "DK4_MES_B159_R0129", "speaker": "Eirene reporting Charlotte's message",
                           "context": "Completes the same quoted message across B159 R0126/R0129/R0132; not a new independent quotation. The next line is Rafael's response."},
    "DK4_MES_B166_R0538": {"speaker": "Woman in the courtyard conversation; FE modal presentation",
                           "context": "Rafael apologizes for discovering the courtyard conversation, receives congratulations and a teasing correction of casual address, then Claudio deflects the topic."},
    "DK4_MES_B166_R0787": {"speaker": "Charlotte's letter salutation; FE modal presentation",
                           "context": "Rafael receives Charlotte's beginner Portuguese letter. The following two modal records show her Portuguese thanks and well-being statement before an English gloss/signature."},
    "DK4_MES_B166_R0797": {"speaker": "Gloss of Charlotte's letter; FE modal presentation",
                           "context": "After the beginner Portuguese text, this record glosses its thanks, well-being and signature. The next companion calls the writing awkward, making simplicity/repetition intentional."},
    "DK4_MES_B20_R0078": {"speaker": "Companion using calibrated selector04; identity not inferred from the old Eirene label"},
}


if __name__ == "__main__":
    prepare_review(TEXT, Path("translations/confirmed_name_route_editorial_v236.json"), METADATA)
