"""Render each changed Maria B51–70 panel through the native story consumer."""

from inspect import getsource

from scripts import stage_maria_B51_B70_20261122 as stage
from scripts import verify_maria_B21_B32_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base,native,parent=stage.base,stage.native,stage.parent
previous,inherited,display=template.previous,template.inherited,template.display
ROOT,PROOF=stage.ROOT/"native_display",stage.ROOT/"native_display/native_display.json"
script=checked_text(getsource(template.main),{
    'assert names==previous.base.load(parent.display.PROOF)["default_names"]["3"]':
        'assert names==base.load(parent.display.PROOF)["default_names"]["3"]',
    'stage.review.ARCHIVE':'stage.ARCHIVE',
    '    assert not wanted and len(entries)==132':'    assert not wanted and len(entries)==18',
    '    assert sum(bool(row["layouts"]) for row in entries)==40':
        '    assert sum(bool(row["layouts"]) for row in entries)==8',
    '    assert len(menus)==1 and menus[0]["count"]==2 and menus[0]["block"]==29\n'
    '    assert len(voice_owners)==7 and sorted(i for row in voice_owners for i in row["slots"])==list(range(8))':
        '    assert not menus and not voice_owners',
    '"maria_B21_B32_native"':'"maria_B51_B70_native"',
    'seven lookout bodies and two choice labels.':'all eight one-page layouts.',
})
scope=vars(template)|globals()
exec(compile(script,__file__+"::Maria-B51-B70-native","exec"),scope)


if __name__=="__main__":
    scope["main"]()

