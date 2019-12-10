from dataclasses import dataclass
from pathlib import Path
from re import compile as re_compile
from subprocess import CompletedProcess, run as subprocess_run
from typing import Optional, List, Dict, Pattern, Union, Any

from typing_extensions import TypedDict

id_regex: Pattern[str] = re_compile(r'.*_(\d+)\.py')


class TestConfig(TypedDict):
    id: int
    shouldFail: bool
    description: str
    file: Any


class CompleteTestConfig(TypedDict):
    folderName: str
    filename: str
    testFilename: str
    testConfigs: List[TestConfig]


@dataclass
class Result:
    test_config: TestConfig
    file: str
    status: int
    stdout: str
    stderr: str

    def to_json_dict(self) -> Dict:
        return {
            'testConfig': self.test_config,
            'successful': (self.status == 0) != self.test_config['shouldFail'],
            'file': self.file,
            'status': self.status,
            'stdout': self.stdout,
            'stderr': self.stderr
        }


def read_test_file_content(test_file_path: Path) -> Optional[str]:
    if not test_file_path.exists():
        return None

    with test_file_path.open() as test_file:
        return test_file.read()


def run_test(
        ex_path: Path,
        test: TestConfig,
        test_file_content: str,
        folder_name: str,
        file_name: str,
        test_filename: str
) -> Union[str, Result]:
    file_to_test_path: Path = ex_path / f'{file_name}_{test["id"]}.py'

    test_file_path: Path = ex_path / f'{test_filename}_{test["id"]}.py'

    if not file_to_test_path.exists():
        return f'The file to test {str(file_to_test_path)} does not exist!'

    test_file_path.write_text(
        test_file_content.replace(
            f'from {file_name} import',
            f'from {str(file_to_test_path.name)[:-3]} import'
        )
    )

    cmd: str = f'(cd {folder_name} && timeout 2 python -m unittest {test_file_path.name})'

    completed_process: CompletedProcess = subprocess_run(cmd, capture_output=True, shell=True, text=True)

    test_file_path.unlink()

    return Result(
        test,
        str(file_to_test_path),
        completed_process.returncode,
        completed_process.stdout[:10_000].split('\n')[:50],
        completed_process.stderr[:10_000].split('\n')[:50]
    )
