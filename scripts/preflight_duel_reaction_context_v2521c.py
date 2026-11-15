"""Honor this legacy registered layer's dependency hashes and native_IDs schema."""
from pathlib import Path
OLD=Path('scripts/preflight_duel_reaction_context_v2521b.py')
if __name__=='__main__':
 source=OLD.read_text()
 assert source.count("config['manuscript_sha256']")==1 and source.count("stage['proof']['reviewed_native_IDs']")==1
 source=source.replace("config['manuscript_sha256']","config['dependencies'][str(docpath)]")
 source=source.replace("stage['proof']['reviewed_native_IDs']","stage['proof']['native_IDs']")
 source=source.replace("prior_failure_after_successful_source_packet='KeyError b:original main local variable was not available in outer execution namespace',","prior_failure_after_successful_source_packet='The source packet completed;successors read ARM9 directly and honor this legacy dependency/native_IDs schema. All failed preflight producers are preserved;none adds credit.',")
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
