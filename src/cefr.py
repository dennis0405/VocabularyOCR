import pandas as pd
import os
from typing import Dict

# 캐시 저장소
_cache = {
    "data": None,
    "a1b2_mtime": None,
    "c1c2_mtime": None,
}

def load_and_merge_cefr_data(a1b2_path: str, c1c2_path: str) -> pd.DataFrame:
    # 파일의 마지막 수정 시간 확인
    a1b2_mtime = os.path.getmtime(a1b2_path)
    c1c2_mtime = os.path.getmtime(c1c2_path)

    # 캐시가 존재하고 파일이 변경되지 않았다면 캐시된 데이터 반환
    if (_cache["data"] is not None 
        and _cache["a1b2_mtime"] == a1b2_mtime 
        and _cache["c1c2_mtime"] == c1c2_mtime):
        return _cache["data"]

    # A1~B2 데이터 읽기
    a1b2_df = pd.read_csv(a1b2_path)
    a1b2_df = a1b2_df[["headword", "CEFR"]]

    # C1~C2 데이터 읽기
    c1c2_df = pd.read_csv(c1c2_path)
    c1c2_df = c1c2_df[["headword", "CEFR"]]

    # 데이터 병합 및 결측치 제거
    merged_df = pd.concat([a1b2_df, c1c2_df], ignore_index=True)
    merged_df = merged_df.dropna(subset=["CEFR"])

    # 캐시에 저장
    _cache["data"] = merged_df
    _cache["a1b2_mtime"] = a1b2_mtime
    _cache["c1c2_mtime"] = c1c2_mtime

    return merged_df

def group_words_by_cefr(merged_df: pd.DataFrame) -> Dict[str, list]:
    grouped = merged_df.groupby("CEFR")["headword"].apply(list).to_dict()
    return grouped

# 결과: {'A1': ['cat', 'dog', 'apple'], 'A2': ['happy', 'friend', 'work'], ...}
