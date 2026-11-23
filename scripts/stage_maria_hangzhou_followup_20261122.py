"""Build the localized Maria lines and the Hangzhou briefing in one exact transaction."""

from inspect import getsource
from types import SimpleNamespace

from scripts import preflight_hangzhou_ming_wrap_20261122 as shared
from scripts import review_maria_B33_B49_followup_20261122 as review
from scripts.source_locked_derivation_v5118 import checked_text


parent, base, native = review.parent, review.base, review.parent.native
town = shared.town
engine, compiler = parent.writer.engine, parent.writer.compiler
ROOT = review.ROOT / "maria_and_hangzhou_staged"
ROM, PROOF = ROOT / "Maria_Hangzhou_STAGED.nds", ROOT / "stored_proof.json"
PACKET = review.ROOT / "maria_followup_combined_source.json"
MANUSCRIPT = review.ROOT / "maria_followup_scoped_manuscript.json"
COMMON = "/COMMON/MESFILE.DK4"
ARCHIVE = "/data/SC3.DK4"


def bind_packet(draft):
    existing = base.load(review.SOURCE)
    missing = {29,31}
    src = parent.parent.writer.review
    program = checked_text(getsource(src.maria_packet), {
        'return scope["source_and_current"](parent,range(18))':
        'return scope["source_and_current"](parent,missing)',
    })
    scope = src.maria_packet.__globals__ | {"parent":parent,"missing":sorted(missing)}
    exec(compile(program,__file__+"::paired-Maria-refs","exec"),scope)
    more = scope["maria_packet"]()
    assert existing["candidate_sha256"] == more["candidate_sha256"]
    wanted = {(r["block"],r["id"]):r for r in draft["records"]}
    group_index = {g["block"]:g for g in existing["groups"] + more["groups"]}
    blocks = sorted({r["block"] for r in draft["records"]})
    for n in blocks:
        for row in group_index[n]["records"]:
            reviewed = wanted.pop((n,row["id"]),None)
            if reviewed is None:
                continue
            assert reviewed["source_reference"] == row["source_reference"]
            assert reviewed["current_reference"]["offset"] == row["current_reference"]["offset"]
            assert reviewed["current_reference"]["block_sha256"] == row["current_reference"]["block_sha256"]
            assert reviewed["current_hex"] == f'{row["selector"]:02x}' + row["current_reference"]["exact_body_hex"]
    assert not wanted
    packet = existing | {"groups":[group_index[n] for n in blocks]}
    if PACKET.exists():
        assert base.load(PACKET) == packet
    else:
        base.save(PACKET,packet)
    return ((),(),(),blocks)


def deploy_briefing(target, clean, ctx):
    art = base.load(shared.OUT)
    visual = base.load(shared.OUT.with_name("native_preflight_visual_review.json"))
    assert art["preflight_only"] and visual == {s["path"]:s["sha256"] for s in art["sheets"]}
    assert all(base.digest(path)==digest for path,digest in visual.items())
    release,prior = map(base.load,(parent.RELEASE,shared.parent.RELEASE))
    assert art["candidate_sha256"] == prior["candidate_sha256"]
    assert release["target_COMMON_sha256"] == prior["target_COMMON_sha256"] == native.digest(ctx.common)
    assert release["target_ARM9_sha256"] == prior["target_ARM9_sha256"] == native.digest(ctx.arm)
    clean_arm = clean.read_file(town.ARM)
    assert all(ctx.arm[start:end]==clean_arm[start:end] for start,end in town.SOURCE_RANGES)
    assert town.selectors(ctx.arm) == town.selectors(clean_arm)
    source = town.common_message_entries(clean.read_file(COMMON),clean_arm)
    directory = native.digest(ctx.arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET])
    old = town.owned_entries(ctx.common,ctx.arm,directory)
    key = shared.KEY
    row = art["record"]
    assert row["source_hex"] == source[key].text.hex() and row["current_hex"] == old[key].text.hex()
    assert row["source_reference"] == town.reference(source[key]) and row["current_reference"] == town.reference(old[key])
    body = bytes.fromhex(art["staged_text_hex"])
    assert body == town.compile_paragraph(row["english"])
    deployed, rebound, slots = town.owned_deployment(ctx.common,ctx.arm,old,{key:body})
    assert rebound[key].text == body and len(rebound) == len(old)
    assert [entry.message_id for entry, new in zip(old,rebound,strict=True) if entry.text!=new.text] == [key]
    target.replace_file(COMMON,deployed)
    return dict(record=row|{"staged_reference":town.reference(rebound[key]),"staged_hex":body.hex()},
        allocation=slots[key],reused_preflight_sha256=base.digest(shared.OUT),
        parent_shared_sha256=native.digest(ctx.common),target_shared_sha256=native.digest(deployed),
        fixed_slot_and_complete_COMMON_inverse=True,original_directory_and_table_exact=True,
        other_COMMON_bodies_preserved=len(old)-1)


def main():
    assert not ROOT.exists()
    draft, preflight = map(base.load,(review.DRAFT,review.PLANS))
    assert preflight["draft_sha256"] == base.digest(review.DRAFT)
    blocks = bind_packet(draft)
    draft["source_packet_sha256"] = base.digest(PACKET)
    draft["source_packet"] = str(PACKET)
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT) == draft
    else:
        base.save(MANUSCRIPT,draft)
    scope = compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT,SOURCE=PACKET),paired=SimpleNamespace(BLOCKS=blocks),
        draft=draft,assemble=engine.assemble)
    program = checked_text(engine.program, {
        'if g["block"] in paired.BLOCKS[1]':'if g["block"] in paired.BLOCKS[3]',
        '    final = native.files(target)':'    briefing = deploy_briefing(target,clean,ctx)\n    final = native.files(target)',
        '== changed.keys()':'== set(changed)|{COMMON}',
        '    for file in changed:':'    for file in set(changed)|{COMMON}:',
        'whole_parent_inverse=True, source25=controls':'whole_parent_inverse=True, briefing=briefing, source25=controls',
    })
    exec(compile(program,__file__+"::installed-story-and-shared","exec"),scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"] and set(proof["changed_blocks"]) == {ARCHIVE}
    parent.writer.parent.writer.reconcile_plans(proof,draft,preflight["plans"])
    print("Verified the nine story plans and the single fixed-slot Hangzhou briefing.")


if __name__ == "__main__":
    main()

