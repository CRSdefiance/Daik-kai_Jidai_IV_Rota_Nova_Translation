"""Keep choice-reference locals separate from the reusable native macro receipt."""
from scripts.prepare_maria303_formatting_v4 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "out=ROOT/'formatting_v2'":"out=ROOT/'formatting_v3'",
    "prior=row['source_reference'];complete=choice_refs[row['id']]":"choice_prior=row['source_reference'];complete=choice_refs[row['id']]",
    'for k,v in prior.items())':'for k,v in choice_prior.items())',
    'set(complete)-set(prior)':'set(complete)-set(choice_prior)',
    'original_reference=prior,complete_native_reference':'original_reference=choice_prior,complete_native_reference',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-choice-schema-withseparate-reference-local','exec'),globals())
