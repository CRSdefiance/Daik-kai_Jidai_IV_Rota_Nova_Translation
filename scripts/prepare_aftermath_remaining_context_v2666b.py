"""Honor this legacy owner's dependency manifest rather than a newer schema."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/prepare_aftermath_remaining_context_v2666.py').read_text()
    source=source.replace("config['manuscript_sha256']","config['dependencies'][config['manuscript']]")
    source=source.replace('aftermath_remaining_context_v2666','aftermath_remaining_context_v2666b')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
