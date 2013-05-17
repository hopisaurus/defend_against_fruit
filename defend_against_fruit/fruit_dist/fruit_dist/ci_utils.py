import argparse
import sys
from ci_multi_module_utils import execute_submodule_run, deploy_all_modules
from fruit_dist.build_info_utils import collect_env_info
from fruit_dist.ci_single_module_utils import execute_sdist_run, deploy_module


def standard_sdist_run(submodule_order=None):
    args = _parse_args(sys.argv[1:])

    env_info = collect_env_info() if args.publish else None
    verify_cert = not args.no_cert_verify

    if submodule_order:
        execute_submodule_run(submodule_order)
        if args.publish:
            deploy_all_modules(
                module_order=submodule_order, env_info=env_info, verify_cert=verify_cert)
    else:
        execute_sdist_run()
        if args.publish:
            deploy_module(env_info=env_info, verify_cert=verify_cert)


def _parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Continuous integration utility responsible for invoking the '
                    'build system within a virtual environment')

    parser.add_argument(
        '--publish',
        action='store_true',
        help='Publish to build artifact repository.')

    parser.add_argument(
        '--no-cert-verify',
        action='store_false',
        help='Do not verify authenticity of host cert when using SSL.')

    return parser.parse_args(args)