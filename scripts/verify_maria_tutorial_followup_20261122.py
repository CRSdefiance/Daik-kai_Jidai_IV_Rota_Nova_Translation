"""Render each changed Maria B51–70 panel through the native story consumer."""

from inspect import getsource

from scripts import stage_maria_tutorial_followup_20261122 as stage
from scripts import verify_maria_B21_B32_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base,native,parent=stage.base,stage.native,stage.parent
previous,inherited,display=template.previous,template.inherited,template.display
ROOT,PROOF=stage.ROOT/"native_display",stage.ROOT/"native_display/native_display.json"
script=checked_text(getsource(template.main),{
    'assert names==previous.base.load(parent.display.PROOF)["default_names"]["3"]':
        'assert names==base.load(parent.display.PROOF)["default_names"]["3"]',
    'stage.review.ARCHIVE':'stage.ARCHIVE',
    '    assert not wanted and len(entries)==132':'    assert not wanted and len(entries)==12',
    '    assert sum(bool(row["layouts"]) for row in entries)==40':
        '    assert sum(bool(row["layouts"]) for row in entries)==6',
    '    assert len(menus)==1 and menus[0]["count"]==2 and menus[0]["block"]==29\n'
    '    assert len(voice_owners)==7 and sorted(i for row in voice_owners for i in row["slots"])==list(range(8))':
        '    assert not menus and not voice_owners',
    '"maria_B21_B32_native"':'"maria_tutorial_followup_native"',
    '    sheet=previous.rafael.prior.precedent.prior.sheet':'''    reclaimed=next(r for r in entries if r["id"]=="DK4_MES_B135_R0325")
    command,=reclaimed["stored_pages"]
    old=bytes.fromhex(command["current"])
    old_body=old[6:old.index(0,6)]
    old_expansion=ctx.execute(expand,old_body,old[5])["cases"]
    assert {r["output_hex"] for r in old_expansion}=={old_body.hex()}
    assert len(paint(ctx.arm,font,old_body)["pages"])==2
    current,=reclaimed["layouts"]
    assert len(current["pages"])==1
    sheet=previous.rafael.prior.precedent.prior.sheet''',
    'initialized_dependencies=ctx.receipt(),offline_native_only=True':
        'initialized_dependencies=ctx.receipt(),offline_native_only=True,reclaimed_previous_native_pages=1',
    'seven lookout bodies and two choice labels.':'six one-page story layouts.',
})
scope=vars(template)|globals()
exec(compile(script,__file__+"::Maria-tutorial-and-coin-native","exec"),scope)


if __name__=="__main__":
    scope["main"]()

