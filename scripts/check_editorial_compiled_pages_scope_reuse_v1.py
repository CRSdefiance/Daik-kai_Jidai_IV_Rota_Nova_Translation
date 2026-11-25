"""Retain every native page guard while qualifying an unchanged older own runtime."""
from scripts import check_editorial_compiled_pages_v8 as prior
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.check_editorial_compiled_pages_v7 import validate_documented_layouts
from scripts.extract_editorial_current_scope_reuse_v1 import qualify_scope
from scripts.source_locked_derivation_v5118 import checked_text


def qualified_current_native_context(doc,ctx):
    reuse=doc['exact_existing_native_context_reuse']
    assert reuse['native_runtime']==ctx.receipt()
    packet=dict(file_path=doc['file_path'],groups=[dict(block=n) for n in doc['blocks']])
    image,release,receipt=qualify_scope(ctx,packet,reuse['target_release'])
    assert doc['current_ROM_sha256']==release['candidate_sha256']
    assert image.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    return receipt


source=checked_text(prior.source,{
    "    assert doc['current_ROM_sha256']==sha(ctx.rompath.read_bytes())":
        '    scope_reuse=qualified_current_native_context(doc,ctx)',
    'runtime=ctx.receipt(),font_sha256=sha(font),records=rows,review_sheets=sheets,':
        'runtime=ctx.receipt(),native_context_reuse=scope_reuse,font_sha256=sha(font),records=rows,review_sheets=sheets,',
})
exec(compile(source,__file__+'::same-full-native-pages-canaries-bounds-and-pagination-exact-scope-reuse','exec'),globals())
