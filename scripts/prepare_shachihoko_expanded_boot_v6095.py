"""Keep identical startup inputs while testing the specifically disclosed expanded payload."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/run_shachihoko_startup_v6080.py','scripts/run_shachihoko_expanded_boot_v6095.py',{
        'shachihoko_runs_v6080':'shachihoko_runs_v6095','shachihoko_v6080':'shachihoko_v6095',
        "version='6079_RESEARCH_ONLY'":"version='6094_EXPANDED_RESEARCH_ONLY'",
        'work/analysis/shachihoko_item_name_research_v6079/research_image_receipt.json':'work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json',
    }))
