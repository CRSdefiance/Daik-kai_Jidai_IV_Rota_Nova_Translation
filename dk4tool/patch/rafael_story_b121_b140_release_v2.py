"""Bind fixture menu evidence by complete proof identity across clean/current offsets."""
import inspect
from dk4tool.patch import rafael_story_b121_b140_release_v1 as original
from scripts.source_locked_derivation_v5118 import checked_text

qualification = checked_text(inspect.getsource(original.qualify_evidence), {
    "{r['source_command_offset'] for r in observed} == {r['source_command_offset'] for r in menu['menus']}":
        "{(str(Path(r['proof'])),r['proof_sha256']) for r in observed} == {(str(Path(r['native_proof'])),r['native_proof_sha256']) for r in menu['menus']}",
})
env = dict(original.qualify_evidence.__globals__)
exec(compile(qualification, __file__+'::exact-native-menu-proof-hashes-not-different-address-spaces', 'exec'), env)
qualify_evidence = env['qualify_evidence']
source = original.source
plan_env = {**original.plan_release.__globals__, 'qualify_evidence': qualify_evidence}
exec(compile(source, __file__+'::unchanged-source-bound-transaction-proof-identity-menu-binding', 'exec'), plan_env)
plan_release = plan_env['plan_release']
