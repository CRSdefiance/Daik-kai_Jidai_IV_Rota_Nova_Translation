"""Native display checks for all revised Rafael contract and Proof pages."""

from inspect import getsource

from scripts import stage_rafael_contract_and_proof_20261119 as build
from scripts import verify_story_short_phrase_wraps_20261119 as inherited
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
PRIOR = build.ROOT.with_name("research_v1")


if __name__ == "__main__":
    source = checked_text(getsource(inherited.main), {
        'len(stored["groups"]) == 11': 'len(stored["groups"]) == 5',
        'len(checked) == len(previews) == 19 and len(retained) == 176':
            'len(checked) == len(previews) == 37 and len(retained) == 92',
        'sum(r["kind"] == "system-FE" for r in checked) == 3':
            'all(r["kind"] == "progressive" for r in checked)',
        'build.review.TOKEN.findall': 'build.review.review_workflow.TOKEN.findall',
        '    font = image.read_file(assets[2])':
            '    font = image.read_file(assets[2])\n'
            '    prior_proof = PRIOR / "native_display/native_display.json"\n'
            '    prior_stage = PRIOR / "stored_proof.json"\n'
            '    earlier = base.load(prior_proof)\n'
            '    prior_rom = PRIOR / build.ROM.name\n'
            '    prior_image = base.NdsImage.open(prior_rom)\n'
            '    assert base.digest(prior_stage) == earlier["stage_proof_sha256"]\n'
            '    assert earlier["candidate_sha256"] == base.digest(prior_rom)\n'
            '    assert base.load(prior_stage)["predecessor_sha256"] == stored["predecessor_sha256"]\n'
            '    assert all(image.read_file(p) == prior_image.read_file(p) for p in assets)\n'
            '    previous = {r["id"]: r for r in earlier["revisions"]}\n'
            '    reused = []',
        '            result = workflow.validate_paragraph(ctx, font, paint, expand, fe, row, body, plan)':
            '            prior = previous[row["id"]]\n'
            '            if prior["target_hex"] == body.hex() and prior["planned_lines"] == plan["lines"]:\n'
            '                result = prior\n'
            '                reused.append(row["id"])\n'
            '            else:\n'
            '                result = workflow.validate_paragraph(ctx, font, paint, expand, fe, row, body, plan)',
        '        integration_pending=True, new_editorial_credit=0))':
            '        exact_native_pages_reused=reused, prior_proof_sha256=base.digest(prior_proof),\n'
            '        audit_reused_identical_assets={p: native.digest(image.read_file(p)) for p in assets},\n'
            '        integration_pending=True, new_editorial_credit=0))',
        '    ROOT.mkdir()': '    assert len(reused) == 33\n    ROOT.mkdir()',
        "Verified all 19 revised pages and 176 exact retentions.":
            "Verified all 37 revised pages and 92 exact retentions.",
    })
    scope = vars(inherited) | globals()
    exec(compile(source, __file__ + "::early-rafael-native", "exec"), scope)
    scope["main"]()
