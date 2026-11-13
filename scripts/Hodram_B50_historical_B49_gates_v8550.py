"""Requalify completed B49 against its exact saved registry,then verify current additive registration."""
from pathlib import Path
from scripts import complete_Hodram_B49_v8480 as original
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

SNAPSHOT=Path('work/analysis/Hodram_B50_registration_v8542/release_stack.before.raw')
REGISTRATION=Path('work/analysis/Hodram_B50_registration_v8542/registration_receipt.json')
text=Path(original.__file__).read_text(encoding='utf-8');start=text.index('def gates():');stop=text.index('\ndef stage():',start)
ADAPTER=checked_text(text[start:stop],{
    "read('translations/release_stack.json')":"read('work/analysis/Hodram_B50_registration_v8542/release_stack.before.raw')",
    "Path('translations/release_stack.json').read_bytes()":"Path('work/analysis/Hodram_B50_registration_v8542/release_stack.before.raw').read_bytes()",
})
env=dict(original.__dict__);exec(compile(ADAPTER,__file__+'::exact-historical-registry-not-live-state','exec'),env)

def gates():
    release=env['gates']();reg=read(REGISTRATION);current=read('translations/release_stack.json');before=read(SNAPSHOT)
    assert sha(SNAPSHOT.read_bytes())==reg['registry_before_sha256']==read(release['manifest'])['release_stack_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes())==reg['registry_after_sha256']
    assert current['profiles'].pop(reg['profile']) and current==before
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==reg['builder_after_sha256']
    return release
