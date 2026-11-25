"""Use the complete typed-choice source reference projection with unchanged native guards."""
from scripts.plan_maria303_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{"FORMATTING=ROOT/'formatting_v1'":"FORMATTING=ROOT/'formatting_v2'"})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-planner-complete-choice-reference-schema','exec'),globals())
