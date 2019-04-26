import re
from json import load as json_load
from pathlib import Path
from subprocess import CompletedProcess, run as subprocess_run
from typing import Optional, List, Dict

id_regex = re.compile(r'.*_(\d+)\.py')


class TestConfig:
    def __init__(self, test_id: int, should_fail: bool, cause: Optional[str]):
        if not isinstance(test_id, int):
            raise Exception(f'the field test_id of a test must be an int but was {type(test_id)}!')
        self.test_id: int = test_id

        if not isinstance(should_fail, bool):
            raise Exception(f'the field should_fail of a test must be a bool but was {type(should_fail)}!')
        self.should_fail: bool = should_fail

        if not (cause is None or isinstance(cause, str)):
            raise Exception(f'the field cause of a test must be a str or None but was {type(cause)}!')
        self.cause: Optional[str] = cause

    def to_json_dict(self) -> Dict:
        return self.__dict__


class CompleteTestConfig:
    def __init__(self, function: str, test_configs: List[TestConfig]):
        self.function: str = function
        self.test_configs: List[TestConfig] = test_configs


class Result:
    def __init__(self, test_config: TestConfig, file: str, status: int, stdout: str, stderr: str):
        self.test_config: TestConfig = test_config
        self.file: str = file
        self.status: int = status
        self.stdout: str = stdout
        self.stderr: str = stderr

    def to_json_dict(self) -> Dict:
        return {
            'testConfig': self.test_config.to_json_dict(),
            'successful': (self.status == 0) != self.test_config.should_fail,
            'file': self.file,
            'status': self.status,
            'stdout': self.stdout,
            'stderr': self.stderr
        }


def read_complete_test_config(test_config_file_path: Path) -> Optional[CompleteTestConfig]:
    if not test_config_file_path.exists():
        return None

    with test_config_file_path.open() as test_config_file:
        parsed_json = json_load(test_config_file)

    function_name: str = parsed_json.get('function')
    test_configs: List[TestConfig] = []

    for tc in parsed_json.get('testConfigs'):
        test_configs.append(TestConfig(
            tc.get('id'), tc.get('shouldFail'), tc.get('cause')
        ))

    return CompleteTestConfig(function_name, test_configs)


def read_test_file_content(test_file_path: Path) -> Optional[str]:
    if not test_file_path.exists():
        return None

    with test_file_path.open() as test_file:
        return test_file.read()


def run_tests(ex_path: Path, test: TestConfig, test_file_content: str, current_ex: str,
              test_file_copy_path: Path) -> Optional[Result]:
    file_to_test_path: Path = ex_path / ''

    test_file_copy_path.write_text(test_file_content.replace(
        "from {}_0 import {}".format(current_ex, current_ex),
        "from {}_{} import {}".format(current_ex, test.test_id, current_ex)
    ))

    completed_process: CompletedProcess = subprocess_run(
        f'(cd {current_ex} && timeout -t 2 python3 {test_file_copy_path.name})',
        capture_output=True, shell=True, text=True
    )

    return Result(
        test, str(file_to_test_path),
        completed_process.returncode,
        completed_process.stdout[:1000].split('\n')[:50],
        completed_process.stderr[:1000].split('\n')[:50]
    )
