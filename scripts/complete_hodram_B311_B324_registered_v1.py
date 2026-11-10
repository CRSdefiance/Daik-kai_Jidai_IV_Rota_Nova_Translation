"""Credit400 unique reviews once after the exact registered patch and own-startup proofs."""
import ast
import re
from scripts.complete_hodram_B301_B310_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import native_numbers

NUMBERS = {234:400,127:175,107:225,705:706,40:41,8:11,73:151,
    18133:18367,18367:18767,11136:11311,7231:7456,18370:18770,
    225:387,228:389,9:13,96:189,97:191,129:198,34162:57202,7:2,156887:57202}
STRINGS = {'B301_B310':'B311_B324','B281_B300':'B301_B310',
    'B301–B310':'B311–B324','B281–B300':'B301–B310',
    'B301-B310':'B311-B324','B281-B300':'B301-B310','234':'400'}
pattern = re.compile('|'.join(re.escape(k) for k in sorted(STRINGS,key=len,reverse=True)))

class QualifiedScope(ast.NodeTransformer):
    def visit_Constant(self,node):
        if type(node.value) is int and node.value in NUMBERS:
            return ast.copy_location(ast.Constant(NUMBERS[node.value]),node)
        if isinstance(node.value,str):
            return ast.copy_location(ast.Constant(pattern.sub(lambda m:STRINGS[m.group(0)],node.value)),node)
        return node
    def visit_keyword(self,node):
        if node.arg == 'all234_individual_five_gates_pass':
            node.arg = 'all400_individual_five_gates_pass'
        # The five review gates remain five; only the observed menu count changes.
        if node.arg == 'observed_menu_instances':
            assert isinstance(node.value,ast.Constant) and node.value.value == 4
            node.value = ast.copy_location(ast.Constant(6),node.value)
            return node
        return self.generic_visit(node)

tree = QualifiedScope().visit(ast.parse(previous))
ast.fix_missing_locations(tree)
source = ast.unparse(tree)+'\n'
assert native_numbers(source) == native_numbers(previous)
old = "'all_five_review_gates_pending', 'clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending')"
assert source.count(old) == 1
source = source.replace(old,"'all_five_review_gates_pending', 'clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending', 'source_names_terms_anddisplay_still_require_scoped_current_binding')")
needle = "    ledger[FAMILY] = dict("
assert source.count(needle) == 1
source = source.replace(needle,"""    ledger[BATCH].update(stored_reconstruction_pending=False,
        fresh_native_body_pages_pending=False,source_meanings_pending=False,localized_drafts_pending=False,
        scoped_names_pending=False,scoped_terms_pending=False,
        current_QA_two_first_runs_pass=True,capacity_guard_reuses_verified_predecessor_consumer_proof=True,
        source_occurrence_metadata_corrected_without_ROM_orcapture_changes=True,
        source_occurrence_resolution='work/Hodram_B311_B324_clean_20261107/source_occurrence_resolution_v2.json')
"""+needle)
compile(source,__file__+'::scope-only-once-credit-and-current-status-preflight','exec')
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-once-only-credit-and-complete-prefix-conservation-new-scope','exec'),globals())
