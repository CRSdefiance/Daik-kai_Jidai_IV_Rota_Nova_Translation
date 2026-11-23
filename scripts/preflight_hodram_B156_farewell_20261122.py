"""Check proposed farewell text at the four existing modal positions."""

from types import SimpleNamespace

from scripts import register_hodram_B131_B150_20261122 as release
from scripts import review_hodram_B156_20261122 as draft


base, modal, native = draft.base, release.writer.modal, release.native
REFINED = draft.OUTPUT.with_name("B156_contextual_v2.json")
OUT = draft.ROOT / "B156_farewell_preflight_v1.json"
SPEECH = {
    188: ("Don't look so sad.", "This isn't forever."),
    252: ("It won't be easy.", "Take care of yourself."),
    256: ("(She nods.)",),
    260: ("See you again... Goodbye.",),
}


def replace_text(raw, fragments):
    lines = []
    remaining = iter(fragments)
    for line in raw.split(b"\n"):
        content = line.strip(b" ")
        if content:
            lead = len(line) - len(line.lstrip(b" "))
            tail = len(line) - len(line.rstrip(b" "))
            line = b" " * lead + next(remaining).encode("ascii") + b" " * tail
        lines.append(line)
    assert next(remaining,None) is None
    return b"\n".join(lines)


def main():
    assert not REFINED.exists() and not OUT.exists()
    review = base.load(draft.OUTPUT)
    assert review["previous_sha256"] == base.digest(release.ROM)
    rom = base.NdsImage.open(release.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=rom,arm=rom.read_file(native.ARM)))
    results = {}
    for row in review["records"]:
        if row["kind"] != "system-FE" or row["decision"] != "revision":
            continue
        text = SPEECH[int(row["id"][-4:])]
        row["english"] = " ".join(text)
        row["protected_phrases"] = list(text)
        row["layout_finding"] = "Retain the source-scoped empty lead rows and visible dialogue origins."
        raw = bytes.fromhex(row["current_hex"])[1:]
        body = replace_text(raw,text)
        pad = b" " * ((len(body) ^ len(raw)) & 1)
        before, _ = modal.paint(painter,raw)
        rows, plane = modal.paint(painter,body + pad)
        assert [(y,x) for y,x,_ in before] == [(y,x) for y,x,_ in rows]
        assert tuple(t for _,_,t in rows) == text
        assert all(x + len(t)*6 <= 222 for _,x,t in rows)
        results[row["id"]] = dict(compiled_hex=body.hex(),expected_hex=(b"\xfe"+body+pad).hex(),
                                    before=before,rows=rows,plane_sha256=native.digest(plane))
    assert len(results) == len(SPEECH)
    base.save(REFINED,review)
    base.save(OUT,dict(candidate_sha256=review["previous_sha256"],manuscript=str(REFINED),
        manuscript_sha256=base.digest(REFINED),earlier_manuscript_sha256=base.digest(draft.OUTPUT),
        native_FE_preflight_only=True,records=results))
    print(f"Verified all {len(results)} revised farewell panels at the earlier native positions.")


if __name__ == "__main__":
    main()

