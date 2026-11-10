"""Keep Japanese regional metadata while requiring all public getter strings to be ASCII."""
import inspect
from scripts import review_hodram_B231_B250_names_terms_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "            assert not raw or raw.isascii()\n":"",
    "text=raw.decode('ascii') if pointer else None":"text=raw.decode('cp932') if pointer else None",
    "for p in (asset,terms_path,PROSE,Path('dk4tool/script/arm9_profiles.py'),Path(__file__))":
        "for p in (asset,terms_path,PROSE,Path('dk4tool/script/arm9_profiles.py'),Path(previous.__file__),Path(__file__))",
})
env={**vars(previous),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-public-names-with-opaque-regional-metadata','exec'),env)
if __name__=='__main__':env['main']()
