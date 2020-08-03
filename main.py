from json import dumps as json_dumps, load as json_load
from pathlib import Path
from sys import stderr
from typing import Dict, Optional, List

# noinspection Mypy
from jsonschema import validate as json_validate

from main_helpers import run_test
from model import CompleteTestConfig, CompleteResult, UnitTestCorrectionResult, FileResult

# helpers
cwd: Path = Path.cwd()

test_data_schema_path = cwd / 'test_data.schema.json'
test_config_path: Path = cwd / 'test_data.json'
result_file_path: Path = cwd / 'result.json'

file_results: List[FileResult] = [
    FileResult.for_file(test_data_schema_path),
    FileResult.for_file(test_config_path),
    FileResult.for_file(result_file_path)
]

missing_files: List[FileResult] = [x for x in file_results if not x.exists]

if len(missing_files) > 0:
    print(f'Could not find all required files:', file=stderr)

    for f in missing_files:
        print(f'\t{f}', file=stderr)

    exit(21)

with test_data_schema_path.open('r') as test_data_schema_file:
    test_data_schema = json_load(test_data_schema_file)

with test_config_path.open('r') as test_config_file:
    loaded_json: Dict = json_load(test_config_file)

try:
    json_validate(instance=loaded_json, schema=test_data_schema)
except Exception as e:
    print(e)
    exit(22)

complete_test_config: CompleteTestConfig = CompleteTestConfig.parse_from_json(loaded_json)

folder_name: str = complete_test_config.folder_name
test_file_name: str = complete_test_config.test_file_name

# read unit test file content
test_file_path: Path = cwd / folder_name / f'{test_file_name}.py'
file_results.append(FileResult.for_file(test_file_path))

test_file_content: Optional[str] = test_file_path.read_text()
if not test_file_path.exists():
    exit(23)

if test_file_content is None:
    print(f'There is no test file {test_file_path}!', file=stderr)
    exit(24)

results: List[UnitTestCorrectionResult] = []

for test_config in complete_test_config.test_configs:
    file_result, result = run_test(
        cwd, test_config, test_file_content, folder_name, complete_test_config.file_name, test_file_name
    )

    file_results.append(file_result)

    if isinstance(result, UnitTestCorrectionResult):
        results.append(result)

complete_result = CompleteResult(file_results, results)

result_file_path.write_text(
    json_dumps(complete_result.to_json_dict(), indent=2)
)
