"""Record the formatting-unapproved draft only after its explicit draft gate."""
import inspect
from scripts import record_hot_spring_prose_v1612 as prior
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    assert read(prior.MANUSCRIPT)['strict_build_validation_rejects_draft_until_formatting_review']
    source=inspect.getsource(prior)
    env={**prior.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
