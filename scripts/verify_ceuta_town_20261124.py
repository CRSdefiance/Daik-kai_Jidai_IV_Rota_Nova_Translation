"""Review the observed Ceuta exchanges and bind their original roles and arguments."""

import json
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_ceuta_town_20261124 as play
from scripts import preflight_ceuta_contract_refusal_20261124 as draft
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = evidence.OUT.with_name("ceuta_town_current_20261124.json")
panels = evidence.panels
HOLDS = (
    (4050, 8), (4650, 761), (5850, 51), (6450, 53), (6750, 823), (7650, 852),
    (7950, 865), (8250, 872), (8550, 874), (8850, 870), (10350, 63), (10950, 1177),
    (11250, 1178), (11850, 1177), (12750, 1177), (14250, 1148), (14850, 1148),
    (16950, 713), (17550, 713), (18450, 656), (19050, 658),
)
REVIEW = {
    8: ("Trader", (), ("Need help?",), "The Trader asks what the visitor needs.",
        "A quick greeting fits before the Market menu opens."),
    761: ("Trader", ("Governor's Office",),
          ("Sorry. Please sign a contract", "at the Governor's Office, then", "come back."),
          "The Trader apologizes and asks Hodram to return after signing a contract at the named facility.",
          "The current line preserves both steps. The longer substitution leaves 'come back' alone, so the staged rewrite puts the instruction together."),
    51: ("Barkeep", (), ("Welcome! What will you have?",),
         "The Barkeep welcomes the customer and asks for their order.",
         "The familiar question suits the Tavern greeting before any purchase."),
    53: ("Barkeep", (), ("5 coins.",), "The drink costs five gold coins.",
         "The spoken price is brief and matches the five-coin deduction from the gold balance."),
    823: ("Barkeep", ("Madeira",), ("Have you heard of a nearby town", "called Madeira?"),
          "The Barkeep asks about the named town and tells Hodram that it is nearby.",
          "Putting the location in the question keeps both the fact and the conversational lead-in."),
    852: ("Charles Rochefort", ("183",), ("It looks like it'll cost 183 gold.", "Is that all right?"),
          "Charles estimates the cost of a round and asks for permission.",
          "The estimate and polite confirmation sound like Charles and leave the amount and decision clear."),
    865: ("Hodram Bergstrom", (), ("Drinks for everyone!",),
          "Hodram tells the Barkeep to serve everyone in the room.",
          "The brisk announcement suits Hodram after approving the round."),
    872: ("Barkeep", ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
          "The Barkeep identifies the host and tells the patrons to enjoy the round.",
          "The complete surname and familiar 'this round's on' make the immediate announcement sound natural. The established English substitution uses the displayed surname."),
    874: ("Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
          "The patron expresses disbelief, gratitude and admiration for the host's generosity.",
          "The lively short reactions lead naturally into the patron's tip."),
    870: ("Patron", ("Sir", "Black Rapier", "the Mediterranean"),
          ("Sir, a tip about a rare treasure.", "They say Black Rapier is stashed", "in the Mediterranean."),
          "The patron addresses Hodram and shares a rumor about a rare treasure hidden in the supplied region.",
          "The casual tip keeps the treasure name, region and hearsay. 'Stashed' suits the patron's informal voice."),
    63: ("Innkeeper", (), ("Welcome! Come in.",), "The Innkeeper greets the visitor.",
         "The open invitation fits before the player chooses a stay."),
    1177: ("Innkeeper", (), ("That'll be 1 gold coin.",), "The stay costs one gold coin.",
           "The brief quote has the correct singular and leaves the decision to the existing choices."),
    1178: ("Innkeeper", (), ("Sleep well!",), "The Innkeeper bids the player good night.",
           "The farewell is warm and brief after the charge is accepted."),
    1148: ("Guard", (), ("Too bad. This city has no room", "for another faction."),
           "The Guard dismisses the request because the city has no room for another faction.",
           "The blunt introduction suits a refusal. Ceuta's two shares already fill the market."),
    713: ("Shopkeeper", (), ("They say Admiral Albuquerque's", "ancestor made his name long ago,",
          "commanding Portuguese fleets", "in the Indian Ocean."),
          "The Shopkeeper repeats that an ancestor of Admiral Albuquerque distinguished himself commanding Portuguese ships in the Indian Ocean long ago.",
          "The shop rumor preserves hearsay, the ancestor's achievement, the Portuguese fleets and their location."),
    656: ("Shopkeeper", (), ("We only sell retail.",), "The shop specializes in retail sales.",
          "The shopkeeper states the policy plainly while the player is in a Square shop."),
    658: ("Shopkeeper", (), ("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."),
          "Business has been fair, and the shopkeeper wonders if a good opportunity will come along.",
          "The question and modest answer preserve the chatty opening and the hope for better business."),
}


def capture(release):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[:len(play.ACTIONS)] == list(play.ACTIONS)
    assert max(frames) == commands[-2]["until"] == 19650
    earlier = read(play.PRIOR)["evidence"]
    assert refs["donor"]["sha256"] == earlier["donor"]["sha256"]
    history = read(earlier["capture"]["path"])["scripted_input_schedule"]
    original = [row for row in history if row["start"] <= play.FIRST_PAUSE]
    assert read(refs["capture"]["path"])["scripted_input_schedule"][:len(original)] == original
    return frames, calls, refs, commands


def review(source, current, frames, screens, calls, font):
    assert len(calls) == 2 * len(HOLDS)
    rows = {}
    for (frame, key), (getter, copier) in zip(HOLDS, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 350
        ja, en = source[key], current[key]
        voice, args, lines, meaning, reason = REVIEW[key]
        assert en.text.count(b"%s") == len(args) and ja.text.count(b"%s") == len(args) + (key == 872)
        english = " ".join(en.text.decode("ascii").split())
        assert (english % args).split() == " ".join(lines).split()
        if key not in rows:
            rows[key] = dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON,
                english=english, clean_Japanese=ja.text.decode("cp932"), speaker=voice,
                context="Hodram visits Ceuta's Market, Tavern, Inn, Governor's Office and Square.",
                source_meaning=meaning, localization_note=reason,
                decision="proposed_revision" if key == 761 else "retention",
                review=dict.fromkeys(GATES, True) | {"formatting": key != 761},
                source_reference=evidence.source_ref(ja), current_reference=evidence.source_ref(en),
                installed_reference=evidence.source_ref(en), holds=[])
        rows[key]["holds"].append(dict(capture=frames[frame], requests=[getter, copier], arguments=args, lines=lines,
            complete_body_pixels=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, voice, screens[frame])))
    return list(rows.values())


def review_sheets(screens):
    result = []
    distinct = tuple(dict((key, frame) for frame, key in reversed(HOLDS)).items())
    for start in range(0, len(distinct), 9):
        group = distinct[start:start + 9]
        sheet = Image.new("RGB", (768, 404 * ((len(group) + 2) // 3)), "#263238")
        painter = ImageDraw.Draw(sheet)
        for i, (key, frame) in enumerate(group):
            x, y = i % 3 * 256, i // 3 * 404
            painter.text((x + 4, y + 4), f"COMMON {key} at frame {frame}", fill="white")
            sheet.paste(screens[frame], (x, y + 20))
        path = OUT.with_name(f"ceuta_town_current_{start // 9 + 1}_20261124.png")
        sheet.save(path)
        result.append(reference(path))
    return result


def main():
    current = play.current
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    frames, calls, refs, commands = capture(release)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    clean, installed = map(NdsImage.open, (CLEAN, current.ROM))
    a, b = (rom.read_file(current.ARM) for rom in (clean, installed))
    archive = installed.read_file(current.COMMON)
    assert sha256(b).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    ja = evidence.base.common_message_entries(clean.read_file(current.COMMON), a)
    en = evidence.base.common_rows(archive, b)
    font = GameAsciiFont.from_arm9(b)
    records = review(ja, en, frames, screens, calls, font)
    wallet_bounds = (77, 350, 134, 362)
    wallets = {frame: dict(visible=amount, capture=frames[frame], crop=wallet_bounds,
                           wallet_pixels_sha256=sha256(screens[frame].crop(wallet_bounds).tobytes()).hexdigest())
               for frame, amount in ((3400, 8740), (7050, 8735), (9150, 8552), (11550, 8551), (15750, 8551))}
    assert wallets[11550]["wallet_pixels_sha256"] == wallets[15750]["wallet_pixels_sha256"]
    assert 8740 - 5 == 8735 and 8735 - 183 == 8552 and 8552 - 1 == 8551
    archived = {284, 318, 750, 751, 752}
    assert archived.isdisjoint(row["message_ID"] for row in calls)
    kept = [r for r in records if r["decision"] == "retention"]
    packet = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ordinary_gameplay=True, records=kept, open_review=[r for r in records if r not in kept],
        all_observed_holds=len(HOLDS), visually_read_wallets=wallets, controller_commands=commands, evidence=refs,
        archived_ids_unobserved_in_replay=sorted(archived), native_refusal_proposal=reference(draft.OUT),
        unvisited=["Other town variants", "Governor's Office contract acceptance in Ceuta", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(packet)
    packet["review_sheets"] = review_sheets(screens)
    write(OUT, packet)
    print(f"Verified {len(HOLDS)} ordinary Ceuta dialogue holds, {len(kept)} retentions, and one wrap lead.")


if __name__ == "__main__":
    main()
