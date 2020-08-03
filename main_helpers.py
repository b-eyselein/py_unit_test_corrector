from pathlib import Path
from subprocess import CompletedProcess, run as subprocess_run
from typing import Tuple, Optional

from model import TestConfig, UnitTestCorrectionResult, FileResult


def run_test(
        cwd: Path,
        test: TestConfig,
        test_file_content: str,
        folder_name: str,
        file_name: str,
        test_filename: str
) -> Tuple[FileResult, Optional[UnitTestCorrectionResult]]:
    file_to_test_path: Path = cwd / folder_name / f'{file_name}_{test.id}.py'
    test_file_path: Path = cwd / folder_name / f'{test_filename}_{test.id}.py'

    file_result = FileResult.for_file(file_to_test_path)

    if not file_result.exists:
        return file_result, None

    test_file_path.write_text(
        test_file_content.replace(
            f'from {file_name} import',
            f'from {str(file_to_test_path.name)[:-3]} import'
        )
    )

    cmd: str = f'(cd {folder_name} && timeout 2 python -m unittest {test_file_path.name})'

    completed_process: CompletedProcess = subprocess_run(cmd, capture_output=True, shell=True, text=True)

    test_file_path.unlink()

    return file_result, UnitTestCorrectionResult(
        test_id=test.id,
        description=test.description,
        should_fail=test.should_fail,
        status=completed_process.returncode,
        stdout=completed_process.stdout[:10_000].split('\n')[:50],
        stderr=completed_process.stderr[:10_000].split('\n')[:50]
    )
