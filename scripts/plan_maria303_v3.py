"""Select the completed reference projection; retain every source/current native check."""
from scripts.plan_maria303_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{"FORMATTING=ROOT/'formatting_v1'":"FORMATTING=ROOT/'formatting_v3'"})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-planner-completed-input-projection','exec'),globals())
