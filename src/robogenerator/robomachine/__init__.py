
from StringIO import StringIO

from parsing import parse
from robomachine.strategies import DepthFirstSearchStrategy


def _write_test(name, machine, output, test, values):
    output.write('\n%s\n' % name)
    if values:
        machine.write_variable_setting_step(values, output)
    machine.start_state.write_to(output)
    for action in test:
        action.write_to(output)

def _write_tests(machine, max_tests, max_actions, to_state, output, strategy_class):
    i = 1
    skipped = 0
    generated_tests = set()
    for test, values in strategy_class(machine, max_actions, to_state).tests():
        if i + skipped > max_tests:
            print '--tests-max generation try limit (%d) reached with (%d) tests generated' % (max_tests, i - 1)
            return
        if (tuple(test), tuple(values)) in generated_tests:
            skipped += 1
            continue
        else:
            generated_tests.add((tuple(test), tuple(values)))
        _write_test('Test %d' % i, machine, output, test, values)
        i += 1

def generate(machine, max_tests=1000, max_actions=None, to_state=None, output=None, strategy=DepthFirstSearchStrategy):
    max_actions = -1 if max_actions is None else max_actions
    machine.write_settings_table(output)
    machine.write_variables_table(output)
    output.write('*** Test Cases ***')
    _write_tests(machine, max_tests, max_actions, to_state, output, strategy)
    machine.write_keywords_table(output)

def transform(text):
    output = StringIO()
    generate(parse(text), output=output)
    return output.getvalue()