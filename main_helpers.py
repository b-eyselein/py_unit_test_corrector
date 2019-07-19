from dataclasses import dataclass
from pathlib import Path
from re import compile as re_compile
from subprocess import CompletedProcess, run as subprocess_run
from typing import Optional, List, Dict, Pattern, Union

id_regex: Pattern[str] = re_compile(r'.*_(\d+)\.py')


class TestConfig:
    def __init__(self, test_id: int, should_fail: bool, cause: Optional[str], description: str):
        if not isinstance(test_id, int):
            raise Exception(f'the field test_id of a test must be an int but was {type(test_id)}!')
        self.id: int = test_id

        if not isinstance(should_fail, bool):
            raise Exception(f'the field should_fail of a test must be a bool but was {type(should_fail)}!')
        self.should_fail: bool = should_fail

        if cause is not None and not isinstance(cause, str):
            raise Exception(f'the field cause of a test must be a str or None but was {type(cause)}!')
        self.cause: Optional[str] = cause

        if not isinstance(description, str):
            raise Exception(f'the field description of a test must be a str but was {type(description)}')
        self.description: str = description

    def to_json_dict(self) -> Dict:
        return {
            "id": self.id,
            "shouldFail": self.should_fail,
            "cause": self.cause,
            "description": self.description
        }


@dataclass
class CompleteTestConfig:
    folder_name: str
    filename: str
    test_filename: str
    test_configs: List[TestConfig]


@dataclass
class Result:
    test_config: TestConfig
    file: str
    status: int
    stdout: str
    stderr: str

    def to_json_dict(self) -> Dict:
        return {
            'testConfig': self.test_config.to_json_dict(),
            'successful': (self.status == 0) != self.test_config.should_fail,
            'file': self.file,
            'status': self.status,
            'stdout': self.stdout,
            'stderr': self.stderr
        }


def read_complete_test_config(parsed_json: Dict) -> CompleteTestConfig:
    folder_name: str = parsed_json['foldername']
    file_name: str = parsed_json['filename']
    test_filename: str = parsed_json['testFilename']

    test_configs: List[TestConfig] = []
    for tc in parsed_json['testConfigs']:
        test_configs.append(TestConfig(tc.get('id'), tc.get('shouldFail'), tc.get('cause'), tc.get('description')))

    return CompleteTestConfig(folder_name, file_name, test_filename, test_configs)


def read_test_file_content(test_file_path: Path) -> Optional[str]:
    if not test_file_path.exists():
        return None

    with test_file_path.open() as test_file:
        return test_file.read()


def run_test(ex_path: Path, test: TestConfig, test_file_content: str,
             folder_name: str, file_name: str, test_filename: str) -> Union[str, Result]:
    file_to_test_path: Path = ex_path / f'{file_name}_{test.id}.py'

    test_file_path: Path = ex_path / test_filename

    if not file_to_test_path.exists():
        return f'The file to test {str(file_to_test_path)} does not exist!'

    test_file_path.write_text(test_file_content.replace(
        f'from {file_name} import',
        f'from {str(file_to_test_path.name)[:-3]} import'
    ))

    cmd: str = f'(cd {folder_name} && timeout -t 2 python3 -m unittest {test_file_path.name})'

    completed_process: CompletedProcess = subprocess_run(cmd, capture_output=True, shell=True, text=True)

    test_file_path.unlink()

    return Result(
        test,
        str(file_to_test_path),
        completed_process.returncode,
        completed_process.stdout[:10_000].split('\n')[:50],
        completed_process.stderr[:10_000].split('\n')[:50]
    )
