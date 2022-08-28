## 파일 동기화 앱 ##
# 원본에 파일이 없지만 사본에 파일이 있으면 파일을 삭제한다.
# 원본에 파일이 있지만 사본에 없으면 파일을 사본으로 복사한다.
# 원본에 파일이 있지만 사본에 파일 이름이 다르고 내용이 같은 파일이 있으면
# 사본의 파일 이름을 원본의 파일 이름으로 변경한다.

import hashlib
import os
import shutil
from pathlib import Path

BLOCK_SIZE = 65536

# 같은 파일이라고 판정할 해시 함수
def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)
    return hasher.hexdigest()


# Read and Make hashes(I/O)
def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


# Business core
def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            src_path = Path(src_folder) / filename
            dst_path = Path(dst_folder) / filename
            yield "copy", src_path, dst_path
        elif dst_hashes[sha] != filename:
            old_dst_path = Path(dst_folder) / dst_hashes[sha]
            new_dst_path = Path(dst_folder) / filename
            yield "move", old_dst_path, new_dst_path

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield "delete", dst_folder / filename


# #3 - Edge to Edge test: need fake filesystem
# 하나의 함수에서 unit-test, e2e-test를 모두 충족하자.
# Edge to Edge test
# Using fake and DI
# reader와 filesystem의 의존성이 있다고 알려준다.
# def sync(reader, filesystem, src_root, dst_root):
#     src_hashes = reader(src_root)
#     dst_hashes = reader(dst_root)

#     for sha, filename in src_hashes.items():
#         if sha not in dst_hashes:
#             src_path = src_root / filename
#             dst_path = dst_root / filename
#             filesystem.copy(dst_path, src_path)

#         elif dst_hashes[sha] != filename:
#             old_dst_path = dst_root / dst_hashes[sha]
#             new_dst_path = dst_root / filename
#             filesystem.move(old_dst_path, new_dst_path)

#     for sha, filename in dst_hashes.items():
#         if sha not in src_hashes:
#             filesystem.delete(dst_root / filename)

# #2 - functinal core, imperative shell
# 외부 상태의 의존이 없는 순수 비즈니스 로직 코어를 만든다.
# 외부 세계 표현의 입력을 받는 로직을 분리한다.
# 리팩토링 후엔 아래 복잡한 sync코드와 비교해서
# 실제 파일 시스템없이도 테스트가 가능해졌다.
# Functional core, Imperative shell
def sync(origin, copy):
    # Path and Hash collect(Imperative shell #1)
    origin_hashes = read_paths_and_hashes(origin)
    copy_hashes = read_paths_and_hashes(copy)

    # functional core(Imperative shell #2)
    actions = determine_actions(origin_hashes, copy_hashes, origin, copy)

    # Print out(Imperative shell #3)
    for action, *paths in actions:
        if action == "copy":
            shutil.copyfile(*paths)
        if action == "move":
            shutil.move(*paths)
        if action == "delete":
            os.remove(paths[0])


# #1 - dirty magic
# def sync(origin, copy):
#     origin_hashes = {}
#     # source 하위 폴더, 파일 탐색
#     for folder, _, files in os.walk(origin):
#         for fn in files:
#             # 하위폴더 밑의 파일을 해시로 만들고 dictionary 등록
#             origin_hashes[hash_file(Path(folder) / fn)] = fn

#     seen = set()  # 사본 추적

#     # 복사본 하위 폴더, 파일 탐색
#     for folder, _, files in os.walk(copy):
#         for fn in files:
#             copy_path = Path(folder) / fn
#             copy_hash = hash_file(copy_path)
#             seen.add(copy_hash)

#             # 복사본이 원본에 없다면 삭제
#             if copy_hash not in origin_hashes:
#                 copy_path.remove()

#             # 복사본이 원본에 있지만 파일 이름이 다르다면
#             # 복사본을 원본으로 옮긴다.
#             elif copy_hash in origin_hashes and fn != origin_hashes[copy_hash]:
#                 shutil.move(copy_path, Path(folder) / origin_hashes[copy_hash])
#     # 원본에 있지만 사본엔 없으면 원본을 사본으로 복사
#     for origin_hash, fn in origin_hashes.items():
#         if origin_hash not in seen:
#             shutil.copy(Path(origin) / fn, Path(copy) / fn)
