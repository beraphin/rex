import rex
import nose

import os
bin_location = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../binaries-private'))


def _do_pov_test(pov, enable_randomness=True):
    """ Test a POV """
    for _ in range(10):
        if pov.test_binary(enable_randomness=enable_randomness):
            return True
    return False


def test_chall_response():
    crash_input = "465f2770".decode('hex') + \
                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
    crash = rex.Crash(bin_location + "/tests/i386/overflow_after_challenge_response2", crash=crash_input)
    exploit_f = crash.exploit()
    for e in exploit_f.register_setters:
        nose.tools.assert_true(_do_pov_test(e))
    for e in exploit_f.leakers:
        nose.tools.assert_true(_do_pov_test(e))


def run_all():
    functions = globals()
    all_functions = dict(filter((lambda (k, v): k.startswith('test_')), functions.items()))
    for f in sorted(all_functions.keys()):
        if hasattr(all_functions[f], '__call__'):
            all_functions[f]()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        globals()['test_' + sys.argv[1]]()
    else:
        run_all()


