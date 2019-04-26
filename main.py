from json import dumps as json_dumps
from pathlib import Path
from sys import stderr
from typing import Dict, Optional, List

from main_helpers import read_test_file_content, run_tests, Result, read_complete_test_config, CompleteTestConfig

# helpers
bash_red_esc: str = '\033[0;31m'

# read complete test configuration
test_config_path: Path = Path.cwd() / 'test_conf.json'

complete_test_config: Optional[CompleteTestConfig] = read_complete_test_config(test_config_path)

if complete_test_config is None:
    print(f'There is no test config file {test_config_path}', file=stderr)
    exit(21)

current_exercise: str = complete_test_config.function

ex_path: Path = Path.cwd() / current_exercise
result_file_path: Path = Path.cwd() / 'results.json'

# read unit test file content
test_file_path: Path = ex_path / "{}_test.py".format(current_exercise)
test_file_content: Optional[str] = read_test_file_content(test_file_path)
if test_file_content is None:
    print(f'{bash_red_esc}There is no test file {test_file_path}!', file=stderr)
    exit(22)

# ensure that result file is mounted
if not result_file_path.exists():
    print(f'{bash_red_esc}There is no result file {result_file_path}', file=stderr)
    exit(23)

# create copy of tests file
test_file_copy_path: Path = ex_path / "{}_test_copy.py".format(current_exercise)
if not test_file_copy_path.exists():
    test_file_copy_path.touch()

results: List[Dict] = []

for test_config in complete_test_config.test_configs:
    result: Optional[Result] = run_tests(ex_path, test_config, test_file_content, current_exercise, test_file_copy_path)

    if result is not None:
        results.append(result.to_json_dict())

# remove copy of tests file
test_file_copy_path.unlink()

result_file_path.write_text(json_dumps(results, indent=2))
