"""Explicit checkpoint continuation of the original runtime_bounds stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('runtime_bounds', __file__)


if __name__ == '__main__':
    main()
