"""Expose the original runtime_bounds stage through the qualified final check."""
from scripts.registered_canonical_extension_resume_v6 import run_driver

def main():
    run_driver('runtime_bounds',__file__)

if __name__=='__main__':main()
