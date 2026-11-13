"""Draft successor: require strict build rejection while formatting is unreviewed."""
import inspect
from scripts import author_hot_spring_dialogue_v1611 as prior
if __name__=='__main__':
    source=inspect.getsource(prior)
    old='    validate_natural_dialogue_batch(doc);save(OUT,doc)'
    new="""    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'formatting review' in str(error)
    else:
        raise AssertionError('Unreviewed formatting draft must not pass build validation')
    doc['strict_build_validation_rejects_draft_until_formatting_review']=True
    save(OUT,doc)"""
    assert source.count(old)==1;source=source.replace(old,new)
    env={**prior.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
