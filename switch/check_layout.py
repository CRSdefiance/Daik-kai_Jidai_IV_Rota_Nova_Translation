"""Check and reflow English dialogue for the Japanese Switch v1.0.2 renderer."""

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import struct

from .inspect_script import report, text_details


ENGINE_SHA256 = "577b985b2441c3cfe5ee95b544147570b1293c5ddd6d1cbb89eb06172e242b41"
ASCII_TABLE_START = 0x3FE718
DECIPIXELS = 10
# Eden wraps around 960 px. Leave a margin for rounding and glyph overhang.
DEFAULT_WIDTH_PX = 940
LINES_PER_PAGE = 3
SUBSTITUTIONS = {"FI", "FA", "FO", "FU", "FN", "IC"}


@dataclass(frozen=True)
class Line:
    text: str
    width_px: float | None
    issues: tuple[str, ...]


def switch_advances(engine):
    data = engine.read_bytes()
    if sha256(data).hexdigest() != ENGINE_SHA256:
        raise ValueError("Expected the extracted Japanese v1.0.2 main-uncompressed.nso.")
    nominal = struct.unpack_from("<95I", data, ASCII_TABLE_START)
    # On the 1920x1080 dialogue surface, the observed ordinary advance is 1.2
    # times the table entry plus one pixel. These two inputs use a separate path.
    advances = {chr(code): 12 * advance + 10
                for code, advance in enumerate(nominal, start=0x20)}
    advances.update({" ": 240, "'": 240})
    return advances


def measure(line, advances, expansions, width_px):
    visible = line.rstrip(" ")
    try:
        raw = visible.encode("cp932")
    except UnicodeEncodeError as exc:
        return Line(line, None, (f"Unencodable character {visible[exc.start]!r}.",))
    tokens = {entry["offset"]: entry for entry in text_details(raw, 0, dialogue=True)["tokens"]}

    width = byte_offset = consumed = 0
    issues = []
    for index, char in enumerate(visible):
        if index < consumed:
            continue
        token = tokens.get(byte_offset)
        if token is None:
            advance = advances.get(char)
            if advance is None:
                issues.append(f"No verified width for {char!r}.")
            else:
                width += advance
            byte_offset += len(char.encode("cp932"))
            continue
        value, kind = token["value"], token["kind"]
        consumed = index + len(value)
        byte_offset += len(value.encode("cp932"))
        if kind in {"name_token", "pronoun_token_candidate"} and value in expansions:
            width += max(sum(advances[c] for c in candidate) for candidate in expansions[value])
        elif kind in {"name_token", "pronoun_token_candidate"}:
            issues.append(f"Supply a rendered expansion for {value}.")
        elif kind == "possible_pronoun_collision":
            issues.append("Capital I can consume the next byte as a pronoun command.")
        else:
            issues.append(f"Unverified control or format sequence {value!r}.")
    if issues:
        return Line(line, None, tuple(dict.fromkeys(issues)))
    px = width / DECIPIXELS
    return Line(line, px, (f"Exceeds {width_px} px by {px - width_px:.1f} px.",) if px > width_px else ())


def check_page(text, advances, expansions, width_px=DEFAULT_WIDTH_PX):
    lines = [measure(line, advances, expansions, width_px) for line in text.split("\n")]
    issues = []
    if len(lines) > LINES_PER_PAGE:
        issues.append(f"{len(lines)} stored lines exceed the {LINES_PER_PAGE}-line page budget.")
    return {"lines": [asdict(line) for line in lines], "issues": issues,
            "fits": not issues and all(not line.issues for line in lines)}


def wrap_pages(text, advances, expansions, width_px=DEFAULT_WIDTH_PX, *, first_page_prefix=""):
    """Reflow at ASCII spaces or line feeds without splitting words or substitutions."""
    if first_page_prefix and not first_page_prefix.endswith("\n"):
        raise ValueError("The first-page prefix must occupy full lines.")
    first_page_lines = LINES_PER_PAGE - first_page_prefix.count("\n")
    if first_page_lines < 1:
        raise ValueError("The first-page prefix leaves no room for dialogue.")
    if not text.strip(" \n"):
        raise ValueError("Dialogue is empty.")
    checked = check_page(text, advances, expansions, width_px)
    unmeasured = [issue for row in checked["lines"] if row["width_px"] is None
                  for issue in row["issues"]]
    if unmeasured:
        raise ValueError(" ".join(dict.fromkeys(unmeasured)))

    lines = []
    words = re.split(r"[ \n]+", text.strip(" \n"))
    current = ""
    for word in words:
        measured_word = measure(word, advances, expansions, width_px)
        if measured_word.issues:
            raise ValueError(f"{word!r} cannot fit on an empty line. {measured_word.issues[0]}")
        proposed = f"{current} {word}" if current else word
        if measure(proposed, advances, expansions, width_px).issues:
            lines.append(current)
            current = word
        else:
            current = proposed
    lines.append(current)
    return [first_page_prefix + "\n".join(lines[:first_page_lines])] + [
        "\n".join(lines[i:i + LINES_PER_PAGE]) for i in range(first_page_lines, len(lines), LINES_PER_PAGE)
    ]


def parse_expansions(raw):
    expansions = {}
    for argument in raw:
        token, _, rendered = argument.partition("=")
        if (token not in SUBSTITUTIONS or not rendered.strip(" ")
                or any(not 0x20 <= ord(c) <= 0x7E for c in rendered)):
            raise ValueError(f"Use a known token and printable English expansion, such as FI=Rafael: {argument!r}")
        expansions.setdefault(token, []).append(rendered)
    return expansions


def bank_pages(path, block, turn):
    for block_report in report(path, block)["blocks"]:
        for entry in block_report["records"]:
            if entry["kind"] == "speech" and (turn is None or entry["turn"] == turn):
                yield {"block": block_report["index"], "turn": entry["turn"], "text": entry["text"]}
            if entry["kind"] == "style_alternatives" and turn is None:
                for alternate in entry["alternatives"]:
                    yield {"block": block_report["index"], "offset": entry["offset"],
                           "style_slots": alternate["style_slots"], "text": alternate["text"]}


def print_checks(result):
    print(f"{result['counts']['fits']}/{result['counts']['total']} source pages fit the "
          f"{result['width_px']} px by {LINES_PER_PAGE} lines budget.")
    for row in result["pages"]:
        if "turn" in row:
            print(f"Block {row['block']}, turn {row['turn']}")
        elif "style_slots" in row:
            print(f"Block {row['block']} +{row['offset']:04x}, style slots {row['style_slots']}")
        else:
            print("Input")
        for line in row["lines"]:
            width = "unknown" if line["width_px"] is None else f"{line['width_px']:.1f} px"
            print(f"  {width:>10}  {line['text']!r}")
            for issue in line["issues"]:
                print(f"      {issue}")
        for issue in row["issues"]:
            print(f"      {issue}")
        for i, page in enumerate(row.get("wrapped_pages", []), start=1):
            print(f"  Proposed page {i}")
            for line in page["lines"]:
                print(f"  {line['width_px']:7.1f} px  {line['text']}")
        if "wrap_error" in row:
            print(f"  Cannot reflow. {row['wrap_error']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True, type=Path, help="Extracted v1.0.2 main-uncompressed.nso.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--text", type=Path, help="UTF-8 prose file.")
    mode.add_argument("--bank", type=Path, help="Extracted or translated Sc*.dk4.")
    parser.add_argument("--block", type=int, help="Zero-based bank block number.")
    parser.add_argument("--turn", type=int, help="Zero-based ordinary speech in the selected block.")
    parser.add_argument("--expand", action="append", default=[], metavar="TOKEN=TEXT",
                        help="Supply a rendered substitution. Repeat to budget the widest value.")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH_PX, help="Line budget in 1080p pixels.")
    parser.add_argument("--wrap", action="store_true", help="Propose editable pages by reflowing spaces and line breaks.")
    parser.add_argument("--issues-only", action="store_true", help="Show only source pages with issues.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable reports.")
    args = parser.parse_args()
    if args.width <= 0:
        parser.error("--width must be positive.")
    if ((args.block is not None and args.bank is None)
            or (args.turn is not None and args.block is None)):
        parser.error("--block requires --bank, and --turn requires --block.")
    try:
        advances = switch_advances(args.engine)
        expansions = parse_expansions(args.expand)
        sources = ([{"text": args.text.read_text(encoding="utf-8-sig")}]
                   if args.text else list(bank_pages(args.bank, args.block, args.turn)))
        if not sources:
            raise ValueError("No matching dialogue records.")
        rows = []
        for source in sources:
            body = source.pop("text")
            if args.text:
                body = body.removesuffix("\n")
            row = {**source, **check_page(body, advances, expansions, args.width)}
            if args.wrap:
                try:
                    wrapped = wrap_pages(body, advances, expansions, args.width)
                    row["wrapped_pages"] = [{"text": page, **check_page(page, advances, expansions, args.width)}
                                            for page in wrapped]
                except ValueError as exc:
                    row["wrap_error"] = str(exc)
            rows.append(row)
        counts = Counter("fits" if row["fits"] else "flagged" for row in rows)
        result = {"width_px": args.width, "lines_per_page": LINES_PER_PAGE, "expansions": expansions,
                  "counts": {"total": len(rows), "fits": counts["fits"], "flagged": counts["flagged"]},
                  "pages": rows}
        if args.issues_only:
            result["pages"] = [row for row in rows if not row["fits"]]
        if args.json:
            print(json.dumps(result, ensure_ascii=True, indent=2))
        else:
            print_checks(result)
        return int(bool(counts["flagged"]))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
