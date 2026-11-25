"""Keep observer installation inside the isolated in-memory harness namespace."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/recommendation_runner_tools_v4984b');assert not root.exists()
    a=derive('scripts/recommendation_harness_v4983.py','scripts/recommendation_harness_v4984b.py',{
        "HARNESS=Path('scripts/headless_desmume_v193.py')":"HARNESS=Path('scripts/headless_desmume_v193.py')\nPROXY=None",
        '    replacements={':"    assert PROXY is not None\n    replacements={\n        'import ctypes as ct':'ct=observer_ct_proxy',",
        "{'__name__':'__main__','__file__':str(HARNESS.resolve())}":"{'__name__':'__main__','__file__':str(HARNESS.resolve()),'observer_ct_proxy':PROXY}",
    })
    b=derive('scripts/run_recommendation_focus_v4984.py','scripts/run_recommendation_focus_v4984b.py',{
        "        import runpy\n        runpy.run_module('scripts.recommendation_harness_v4983',run_name='__main__')":
        "        from scripts import recommendation_harness_v4984b as adapter\n        adapter.PROXY=Proxy()\n        adapter.main()",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tools=[a,b],unexecuted_prior_runner_preserved=True,no_new_ROMs_or_emulator_runs=True))
