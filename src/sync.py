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


def sync(origin, copy):
    origin_hashes = {}
    # source 하위 폴더, 파일 탐색
    for folder, _, files in os.walk(origin):
        for fn in files:
            # 하위폴더 밑의 파일을 해시로 만들고 dictionary 등록
            origin_hashes[hash_file(Path(folder) / fn)] = fn

    seen = set()  # 사본 추적

    # 복사본 하위 폴더, 파일 탐색
    for folder, _, files in os.walk(copy):
        for fn in files:
            copy_path = Path(folder) / fn
            copy_hash = hash_file(copy_path)
            seen.add(copy_hash)

            # 복사본이 원본에 없다면 삭제
            if copy_hash not in origin_hashes:
                copy_path.remove()

            # 복사본이 원본에 있지만 파일 이름이 다르다면
            # 복사본을 원본으로 옮긴다.
            elif copy_hash in origin_hashes and fn != origin_hashes[copy_hash]:
                shutil.move(copy_path, Path(folder) / origin_hashes[copy_hash])
    # 원본에 있지만 사본엔 없으면 원본을 사본으로 복사
    for origin_hash, fn in origin_hashes.items():
        if origin_hash not in seen:
            shutil.copy(Path(origin) / fn, Path(copy) / fn)
