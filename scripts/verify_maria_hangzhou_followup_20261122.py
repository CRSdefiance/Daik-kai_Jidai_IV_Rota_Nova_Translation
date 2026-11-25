"""Validate complete glyphs and native wraps for the staged Maria and Hangzhou panels."""

from inspect import getsource

from scripts import stage_maria_hangzhou_followup_20261122 as stage
from scripts import verify_maria_B21_B32_20261122 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
previous, inherited, display = earlier.previous, earlier.inherited, earlier.display
ROOT, PROOF = stage.ROOT / "native_display", stage.ROOT / "native_display/native_display.json"


def installed_preview_context(ctx, image, saved):
    for asset in display.ASSETS:
        if asset != stage.COMMON:
            assert ctx.image.read_file(asset) == image.read_file(asset)
    current = image.read_file(stage.COMMON)
    proof = saved["briefing"]
    assert native.digest(ctx.common) == proof["parent_shared_sha256"]
    assert native.digest(current) == proof["target_shared_sha256"]
    return stage.town.with_components(ctx,ctx.arm,current)


def briefing_preview(ctx, font, saved):
    town=stage.town
    brief=saved["briefing"]
    row=brief["record"]
    key=row["message_ID"]
    cpu,get,provider=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    body=bytes.fromhex(row["staged_hex"])
    assert bytes(cpu.mem_read(get(0x5528C,key),len(body)+1)) == body + b"\0"
    visible,rows=town.native_layout(cpu,body,key,())
    expected=base.load(stage.shared.OUT)["visible"]["proposed wrap"]
    assert rows == expected["lines"] and visible.hex() == expected["native_display_hex"]
    painter,_,_=town.font_tools(ctx.image)
    plane,glyphs=town.render_portrait(painter,ctx.arm,font,visible)
    assert [g["code"] for g in glyphs] == town.glyph_codes(visible) and provider.reads
    assert native.digest(plane)==expected["plane_sha256"]
    sheets=town.portrait_sheets(ROOT,[(f"{key} final Hangzhou briefing",plane)])
    return dict(lines=rows,stored_hex=body.hex(),display_hex=visible.hex(),plane_sha256=native.digest(plane),
        shared_plane_bytes=plane.hex(),sheets=sheets,current_lookup_verified=True)


script=checked_text(getsource(earlier.main),{
    'assert all(ctx.image.read_file(asset)==image.read_file(asset) for asset in display.ASSETS)':
        'ctx = installed_preview_context(ctx,image,saved)',
    'assert names==previous.base.load(parent.display.PROOF)["default_names"]["3"]':
        'assert names==base.load(parent.display.PROOF)["default_names"]["3"]',
    'stage.review.ARCHIVE':'stage.ARCHIVE',
    '    assert not wanted and len(entries)==132':'    assert not wanted and len(entries)==19',
    '    assert sum(bool(row["layouts"]) for row in entries)==40':
        '    assert sum(bool(row["layouts"]) for row in entries)==9',
    '    assert len(menus)==1 and menus[0]["count"]==2 and menus[0]["block"]==29\n'
    '    assert len(voice_owners)==7 and sorted(i for row in voice_owners for i in row["slots"])==list(range(8))':
        '    assert not menus and not voice_owners\n    briefing = briefing_preview(ctx,font,saved)',
    '"maria_B21_B32_native"':'"maria_followup_native"',
    'sheets=sheets+[m["sheet"] for m in menus],menus=menus,lookout_voice_owners=voice_owners,':
        'sheets=sheets+briefing["sheets"],briefing=briefing,',
    'seven lookout bodies and two choice labels.':'the four-line Hangzhou briefing.',
})
scope=vars(earlier)|globals()
exec(compile(script,__file__+"::Maria-and-town-native","exec"),scope)

if __name__=="__main__":
    scope["main"]()

