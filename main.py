from json import dumps as json_dumps, load as json_load
from pathlib import Path
from sys import stderr
from typing import Dict, Optional, List, Union

# noinspection Mypy
from jsonschema import validate as json_validate

from main_helpers import read_test_file_content, run_test, Result, CompleteTestConfig

# helpers
bash_red_esc: str = '\033[0;31m'
cwd: Path = Path.cwd()
test_data_schema_path = cwd / 'test_data.schema.json'

with test_data_schema_path.open('r') as test_data_schema_file:
    test_data_schema = json_load(test_data_schema_file)

# read complete test configuration
test_config_path: Path = cwd / 'test_data.json'

if not test_config_path.exists():
    print(f'There is no test config file {test_config_path}', file=stderr)
    exit(21)

with test_config_path.open() as test_config_file:
    complete_test_config: CompleteTestConfig = json_load(test_config_file)

try:
    json_validate(instance=complete_test_config, schema=test_data_schema)
except Exception as e:
    print(e)
    exit(25)

ex_path: Path = cwd / complete_test_config['folderName']
result_file_path: Path = cwd / 'result.json'

# read unit test file content
test_file_path: Path = ex_path / f'{complete_test_config["testFilename"]}.py'
test_file_content: Optional[str] = read_test_file_content(test_file_path)
if test_file_content is None:
    print(f'{bash_red_esc}There is no test file {test_file_path}!', file=stderr)
    exit(22)

# ensure that result file is mounted
if not result_file_path.exists():
    print(f'{bash_red_esc}There is no result file {result_file_path}', file=stderr)
    exit(23)

results: List[Dict] = []

for test_config in complete_test_config['testConfigs']:
    result: Union[str, Result] = run_test(
        ex_path,
        test_config,
        test_file_content,
        complete_test_config['folderName'],
        complete_test_config['filename'],
        complete_test_config['testFilename']
    )

    if isinstance(result, Result):
        results.append(result.to_json_dict())
    else:
        # TODO: process error msg further?!
        print(f'{bash_red_esc}There has been an error while correction: {result}')
        exit(24)

result_file_path.write_text(json_dumps({'results': results}, indent=2))
