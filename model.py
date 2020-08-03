from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


# Input

@dataclass()
class TestConfig:
    id: int
    should_fail: bool
    description: str

    @staticmethod
    def parse_from_json(json_object: Dict) -> 'TestConfig':
        return TestConfig(
            id=json_object['id'],
            should_fail=json_object['shouldFail'],
            description=json_object['description']
        )


@dataclass()
class CompleteTestConfig:
    folder_name: str
    file_name: str
    test_file_name: str
    test_configs: List[TestConfig]

    @staticmethod
    def parse_from_json(json_object: Dict) -> 'CompleteTestConfig':
        return CompleteTestConfig(
            folder_name=json_object['folderName'],
            file_name=json_object['filename'],
            test_file_name=json_object['testFilename'],
            test_configs=[
                TestConfig.parse_from_json(sub_object) for sub_object in json_object['testConfigs']
            ]
        )


# Result

@dataclass()
class FileResult:
    file_name: str
    exists: bool

    def to_json_dict(self) -> Dict:
        return {
            'file_name': self.file_name,
            'exists': self.exists
        }

    @staticmethod
    def for_file(file: Path) -> 'FileResult':
        return FileResult(file.name, file.exists())


@dataclass()
class UnitTestCorrectionResult:
    test_id: int
    description: str
    should_fail: bool
    status: int
    stdout: str
    stderr: str

    def to_json_dict(self) -> Dict:
        return {
            'testId': self.test_id,
            'description': self.description,
            'successful': (self.status == 0) != self.should_fail,
            'stdout': self.stdout,
            'stderr': self.stderr,
        }


@dataclass()
class CompleteResult:
    file_results: List[FileResult]
    results: List[UnitTestCorrectionResult]

    def to_json_dict(self) -> Dict:
        return {
            'fileResults': [fr.to_json_dict() for fr in self.file_results],
            'results': [r.to_json_dict() for r in self.results]
        }
