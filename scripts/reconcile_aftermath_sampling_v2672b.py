"""Bind the completed2551b proof;preserve the pre-output2551-path refusal."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/reconcile_aftermath_sampling_v2672.py').read_text()
    source=source.replace('aftermath_defeat_history_v2551/','aftermath_defeat_history_v2551b/')
    source=source.replace('aftermath_sampling_v2672','aftermath_sampling_v2672b')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
