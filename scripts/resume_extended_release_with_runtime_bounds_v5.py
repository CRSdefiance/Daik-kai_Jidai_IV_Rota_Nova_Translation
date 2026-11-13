"""Expose the callable original runtime_bounds stage to the registered chain."""
from scripts.registered_canonical_extension_resume_v5 import run_driver

def main():
    run_driver('runtime_bounds',__file__)

if __name__=='__main__':main()
