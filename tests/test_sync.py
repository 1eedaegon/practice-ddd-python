# 원본에 있지만 복사본에 없을 때
from pathlib import Path

from src.sync import determine_actions


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    # try:
    #     source = tempfile.mkdtemp()
    #     dest = tempfile.mkdtemp()

    #     content = "I'm very useful file."
    #     (Path(source) / "my-file").write_text(content)

    #     sync(source, dest)

    #     expected_path = Path(dest) / "my-file"
    #     assert expected_path.exists()
    #     assert expected_path.read_text == content

    # finally:
    #     shutil.rmtree(source)
    #     shutil.rmtree(dest)

    # 추상화된 로직에 대해 테스트하므로 비즈니스 로직에 좀 더 쉽게 다가갈 수 있다.
    src_hashes = {"hash1": "fn1"}
    dst_hashes = {}
    expected_actions = [("COPY", "/src/fn1", "/dst/fn1")]
    actions = determine_actions(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("copy", Path("/src/fn1"), Path("/dst/fn1"))]


# 원본에 같은 내용의 다른 이름 파일이 있을 떄
def test_when_a_file_has_been_renamed_in_the_source():
    # try:
    #     source = tempfile.mkdtemp()
    #     dest = tempfile.mkdtemp()

    #     content = "I'm very very important file"
    #     source_path = Path(source) / "source-file"
    #     old_dest_path = Path(dest) / "dest-file"
    #     expected_dest_path = Path(dest) / "source-file"

    #     source_path.write_text(content)
    #     old_dest_path.write_text(content)

    #     sync(source, dest)

    #     assert old_dest_path.exists() is False
    #     assert expected_dest_path.read_text() == content

    # finally:
    #     shutil.rmtree(source)
    #     shutil.rmtree(dest)

    src_hashes = {"hash1": "fn1"}
    dst_hashes = {"hash1": "fn2"}
    actions = determine_actions(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("move", Path("/dst/fn2"), Path("/dst/fn1"))]
