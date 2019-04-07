TEST_DIR = 'sometmpdir'


def create_directory(tmp_path, dirname=TEST_DIR):
    test_dir = tmp_path / dirname
    test_dir.mkdir()
    return test_dir


def create_test_file(tmp_path, text_content, file_name='test.txt'):
    test_dir = create_directory(tmp_path)
    test_file = test_dir / file_name
    test_file.write_text(text_content)
    return test_file


def create_test_dir(tmp_path, empty=False):
    test_dir = create_directory(tmp_path)
    if empty:
        return test_dir

    create_directory(tmp_path, '1')
    create_directory(tmp_path, '2')
    create_directory(tmp_path, '3')
    return tmp_path / TEST_DIR
