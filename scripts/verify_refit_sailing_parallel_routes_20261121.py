"""Check every revised lesson page and the four original choice menus."""
from inspect import getsource

from scripts import stage_refit_sailing_parallel_routes_20261121 as stage
from scripts import verify_fernando_parallel_routes_20261121 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display = stage.base, stage.native, template.display
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"

menu_scope = vars(template.menu_proof) | {"ROOT": ROOT}
exec(compile(getsource(template.menu_proof.captions), __file__ + "::caption-consumer", "exec"), menu_scope)


source = checked_text(getsource(template.main), {
    '''                    elif stage.review.TOKEN.findall(row["english"]):
                        assert route == 3 and row["source_record_index"] in (149, 163)
                        body = new[6:new.index(0, 6)]
                        got = ctx[route].execute(expand, body, row["source_selector"])
                        expected = body.replace(b"FO", names[route]["FO"].encode("ascii"))
                        assert {r["output_hex"] for r in got["cases"]} == {expected.hex()}
                        page, = paint(ctx[route].arm, font, expected)["pages"]
                        assert page["native_independent_plane_equal"]
                        ret.update(retained_original_company_resolution=got, native_pages=1)''':
        '''                    else:
                        assert not stage.review.TOKEN.findall(row["english"])''',
    'assert (new == old) == (ident == BYTE_EXACT)': 'assert new != old',
    'len(records) == 121 and [m["block"] for m in menus] == [169, 136]':
        'len(records) == 134 and [m["block"] for m in menus] == [171, 166, 167, 138]',
    'assert default == 63 and len(pictures) == 69': 'assert default == 85 and len(pictures) == 100',
    'native_caption_count=4, native_menu_count=2': 'native_caption_count=8, native_menu_count=4',
    'Verified 62 changed pages, one exact reflow, six name-length cases and both retained menus.':
        'Verified 85 changed pages, 15 name-length cases and four retained menus.',
})
scope = vars(template) | globals()
exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
