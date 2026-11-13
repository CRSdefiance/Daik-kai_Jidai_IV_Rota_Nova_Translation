"""Expose the callable original owned_names stage to the registered chain."""
from scripts.registered_canonical_extension_resume_v5 import run_driver

def main():
    run_driver('owned_names',__file__)

if __name__=='__main__':main()
