"""Reuse qualified Rafael geometry for229 source-bound speeches, including captain role0."""
import inspect
import linecache
from pathlib import Path
from types import SimpleNamespace
from scripts import plan_rafael_B85_B100_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

CURRENT=Path('work/analysis/Rafael_B101_B120_current678_20261105/current_effective.json')
PROOF=Path('work/analysis/Rafael241_names_terms_20261105/names_terms_roles_andconsumer_dependency_qualification_v1.json')
qualification=checked_text(inspect.getsource(previous.qualify_source),{
    "list(range(85, 101))":"list(range(101, 121))",
    "proof['fresh_actors'] == 12 and proof['qualified_reused_actors'] == 8":"proof['fresh_actors'] == 11 and proof['qualified_reused_actors'] == 7",
    "doc['all261_individual_four_prose_gates_pass']":"doc['all241_individual_four_prose_gates_pass']",
    "set(proof['actors']) | {254}":"set(proof['actors']) | set(proof['dynamic_selectors']) | {254}",
    "len(bindings) == 255":"len(bindings) == 229",
})
qual_env={**previous.qualify_source.__globals__,'CURRENT':CURRENT,'PROOF':PROOF}
exec(compile(qualification,__file__+'::same-complete-source-preamble-binding-with-qualified-dynamic-role', 'exec'),qual_env)
qualify_source=qual_env['qualify_source']
parameters={**vars(previous.env['previous'])}
parameters['PAIRS'] |= {('minerva','shield'),('cape','of'),('of','good'),('good','hope'),('peacock','mail'),
    ('jaguar',"god's"),("god's",'vest'),('aristarchus','telescope'),("hestia's",'pot'),('suryavarman','ii'),
    ('ancient','megalithic'),('megalithic','civilization'),('civilization','research'),('research','society'),('holy','spirit')}
env={**previous.env,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
source=previous.source
filename=__file__+'::same-native-paragraph-geometry-229-speeches-no-inherited-source-specific-wraps'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
