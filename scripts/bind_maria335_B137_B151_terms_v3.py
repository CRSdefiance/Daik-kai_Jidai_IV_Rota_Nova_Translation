"""Bind the installed singular Tomato catalogue label; plural prose remains grammatical."""
from scripts import bind_maria335_B137_B151_terms_v2 as v2
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(v2.source,{
    "('トマト','Tomatoes')":"('トマト','Tomato')",
    'Path(previous.__file__),Path(__file__)':'Path(previous.__file__),Path(v2.__file__),Path(__file__)',
})
env={**v2.env,'v2':v2,'__file__':__file__}
exec(compile(source,__file__+'::same-reference-guards-current-Tomato-singular-label','exec'),env)
if __name__=='__main__':env['main']()
