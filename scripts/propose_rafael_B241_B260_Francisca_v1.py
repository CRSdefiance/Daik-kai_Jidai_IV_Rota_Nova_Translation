"""Propose and prove the exclusive actor-186 Francisca width correction."""
import inspect
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B169_contextual_v1 import getter

from scripts.write_rafael_B241_B260_contextual_v1 import ROOT

parent = Path('scripts/propose_fernan_name_glyph.py')
target = ROOT/'Francisca_name_field_v1'
adapted = checked_text(parent.read_text(encoding='utf-8'), {
    "ROOT=Path('work/analysis/Rafael_Fernan_name_field_20261104')": f"ROOT=Path({str(target)!r})",
    "RELEASE=Path('work/analysis/Rafael_B36_B41_release_verified_20261104/registered_release_verification.json')":
        "RELEASE=Path('work/Rafael3222_extended_release_verified_v1_20261106/registered_release_verification.json')",
    "NAMES=Path('work/analysis/Rafael_B51_B60_new_name_bindings_20261104/names.json')":
        f"NAMES=Path({str(ROOT/'names_and_terms_v1.json')!r})",
    "consumers=[r for r in names['current_names']['rows'] if r['actor_ID']==35]":
        "consumers=next(r['current_consumers'] for r in names['name_bindings'] if r['actor_ID']==186)",
    "r['text']=='Ｆernan Silveira'": "r['text']=='Ｆrancisca'",
    "32*35":"32*186", "actor=35":"actor=186", "actor_ID=35":"actor_ID=186",
    "'フェルナン'":"'フランシスカ'", "Ｆernan":"Ｆrancisca", "Fernan":"Francisca",
})
if __name__ == '__main__':
    exec(compile(adapted,__file__+'::exact-single-owned-name-field','exec'),globals())
    adapter = checked_text(inspect.getsource(getter), {'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    save(target/'native_getter_binding.json',dict(runtime=ctx.receipt(),current_names=dict(rows=consumers),
        source_owned_current_adapter=adapter,source_name_binding=str(NAMES),source_name_binding_sha256=sha(NAMES.read_bytes()),
        new_credit=0))

