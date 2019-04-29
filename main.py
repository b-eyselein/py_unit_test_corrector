from json import dumps as json_dumps
from pathlib import Path
from sys import stderr
from typing import Dict, Optional, List, Union

from main_helpers import read_test_file_content, run_test, Result, read_complete_test_config, CompleteTestConfig

# helpers
bash_red_esc: str = '\033[0;31m'
cwd: Path = Path.cwd()

# read complete test configuration
test_config_path: Path = cwd / 'test_conf.json'

complete_test_config: Optional[CompleteTestConfig] = read_complete_test_config(test_config_path)

if complete_test_config is None:
    print(f'There is no test config file {test_config_path}', file=stderr)
    exit(21)

current_exercise: str = complete_test_config.function

ex_path: Path = cwd / current_exercise
result_file_path: Path = cwd / 'results.json'

# read unit test file content
test_file_path: Path = ex_path / f'{current_exercise}_test.py'
test_file_content: Optional[str] = read_test_file_content(test_file_path)
if test_file_content is None:
    print(f'{bash_red_esc}There is no test file {test_file_path}!', file=stderr)
    exit(22)

# ensure that result file is mounted
if not result_file_path.exists():
    print(f'{bash_red_esc}There is no result file {result_file_path}', file=stderr)
    exit(23)

results: List[Dict] = []

for test_config in complete_test_config.test_configs:
    result: Union[str, Result] = run_test(ex_path, test_config, test_file_content, current_exercise)

    if isinstance(result, Result):
        results.append(result.to_json_dict())
    else:
        # TODO: process error msg further?!
        print(f'{bash_red_esc}There has been an error while correction: {result}')
        exit(24)

result_file_path.write_text(json_dumps(results, indent=2))
