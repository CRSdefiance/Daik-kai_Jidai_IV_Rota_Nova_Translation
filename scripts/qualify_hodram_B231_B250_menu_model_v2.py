"""Treat the existing strict pixel matcher's expected rejection as an assertion."""
import inspect
from scripts import qualify_hodram_B231_B250_menu_model_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "        assert not match(changed,ink,(8,8,8),[x],[y]);results.append(dict(case=name,rejected=True))":
        """        try:match(changed,ink,(8,8,8),[x],[y])
        except AssertionError:results.append(dict(case=name,rejected=True))
        else:raise AssertionError('Accepted damaged caption: '+name)""",
    "Path('scripts/analyze_hodram_B231_B250_menu_v1.py')]":
        "Path('scripts/analyze_hodram_B231_B250_menu_v1.py'),Path(previous.__file__)]",
})
env={**vars(previous),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-six-negative-cases-correct-asserting-matcher-ABI','exec'),env)
if __name__=='__main__':env['main']()
