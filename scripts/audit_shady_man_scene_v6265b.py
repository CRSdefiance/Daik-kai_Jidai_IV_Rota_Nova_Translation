"""Retain the caught equality assumption and record exact differences before interpreting them."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/audit_shady_man_scene_v6265.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/shady_man_scene_v6265')":"ROOT=Path('work/analysis/shady_man_scene_v6265b')",
      "    assert pairs==old['command_pairs'] and following==old['following_native_commands']":"    differences=[dict(index=i,source=a,target=b) for i,(a,b) in enumerate(zip(old['command_pairs'],pairs,strict=True)) if a!=b]\n    save(ROOT/'exact_source_target_command_differences.json',dict(differences=differences,following_source=old['following_native_commands'],following_target=following))\n    assert pairs==old['command_pairs'] and following==old['following_native_commands']",
    })
    exec(compile(text,str(source)+'::equality-diagnostics','exec'),dict(__name__='__main__',__file__=__file__))
