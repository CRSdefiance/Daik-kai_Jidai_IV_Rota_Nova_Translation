"""Bind the actual observer's sibling run plan explicitly in the frozen dependency set."""
import inspect
from dk4tool.patch import hodram_residual_release_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text

evidence_source=checked_text(inspect.getsource(prior.qualify_evidence),{
    "        terminal=load(run['terminal']);plan=load(terminal['run_plan']);fixture=load(plan['fixture'])":
    "        terminal=load(run['terminal']);run_plan_path=Path(run['terminal']).parent/'run_plan.json'\n        require(conf['dependencies'].get(str(run_plan_path))==sha(run_plan_path.read_bytes()),'frozen actual run plan')\n        plan=load(run_plan_path);fixture=load(plan['fixture'])",
})
evidence_env=dict(prior.qualify_evidence.__globals__)
exec(compile(evidence_source,__file__+'::same-evidence-contract-exact-observer-run-plan-path','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
env={**prior.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(prior.source,__file__+'::unchanged-complete-SC1-transaction','exec'),env)
plan_release=env['plan_release']
