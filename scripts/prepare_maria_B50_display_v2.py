"""Avoid loading a nonexistent menu receipt in the explicitly inventoried speech-only scope."""
from scripts.prepare_maria_B50_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "doc, native, menuproofs = map(load, [rebuilt['manuscript'], rebuilt['native'], rebuilt['menu']])":
        "doc, native = map(load, [rebuilt['manuscript'], rebuilt['native']]);menuproofs={}",
})
exec(compile(source,__file__+'::same-complete-fixture-guards-exact-no-menu-scope','exec'),globals())
