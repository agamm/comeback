import itertools
import json
import operator
import pathlib
import time
from typing import (
    Any, Dict, Iterator, Optional, Tuple, Union
)


from comeback import paths


def create_path_entity(filepath: Union[str, pathlib.Path]) -> Dict[str, int]:
    filepath = str(filepath)
    last_used = int(time.time())
    return {filepath: last_used}


def create_and_get_basic_comeback_file() -> Dict[str, Any]:
    default_filepath = paths.get_default_comeback_file_path()
    default_filepath.touch()
    default_path_entity = create_path_entity(filepath=default_filepath)
    paths_file = paths.PATHS_DATA_FILE
    paths_file.write_text(json.dumps(default_path_entity))
    return default_path_entity


def get_comeback_paths() -> Dict[str, int]:
    paths_file = paths.PATHS_DATA_FILE
    paths_file.touch()
    try:
        return json.loads(paths_file.read_text())
    except json.JSONDecodeError:
        return create_and_get_basic_comeback_file()


def write_comeback_paths(paths_to_write: Dict[str, int]) -> None:
    paths_file = paths.PATHS_DATA_FILE
    paths_file.write_text(json.dumps(paths_to_write))


def add_comeback_path(path: Optional[Union[pathlib.Path, str]] = None) -> None:
    path = path if path is not None else pathlib.Path.cwd() / '.comeback'
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f'Can\'t locate {path}')
    path_to_add = create_path_entity(filepath=path)
    paths_to_write = {**get_comeback_paths(), **path_to_add}
    write_comeback_paths(paths_to_write)


def get_recent_comebacks(max_results: Optional[int] = None)\
                         -> Iterator[Tuple[str, int]]:
    comeback_files = get_comeback_paths()
    date_getter = operator.itemgetter(1)
    sorted_ = sorted(comeback_files.items(), key=date_getter, reverse=True)
    yield from itertools.islice(sorted_, max_results)


def get_last_comeback() -> pathlib.Path:
    FILEPATH_INDEX = 0
    single_comeback = get_recent_comebacks(max_results=1)
    last_comeback = next(single_comeback)
    return pathlib.Path(last_comeback[FILEPATH_INDEX])
