# trigger_bug.py
import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 1. 버그 함수 정의 (여기가 원본 위치입니다!)
# auto=False: 수동 등록을 위해 (API 오류 방지)
@vectorize(team="qa_team", auto=False)
def buggy_adder(a, b):
    print(f"Adding {a} + {b}")
    return a + b

if __name__ == "__main__":
    print("🚀 [1] Registering Metadata (Updating file path in DB)...")
    # ★ 핵심: 이 함수가 실행되면 DB에 "buggy_adder는 trigger_bug.py에 있다"고 저장됨
    generate_and_register_metadata()

    print("🚀 [2] Generating Error...")
    try:
        buggy_adder(10, 1) # 에러 발생!
    except TypeError:
        print("✅ Error generated successfully.")

    print("🚀 [3] Flushing logs...")
    # 로그 강제 전송
    get_batch_manager().shutdown()
    time.sleep(7)
    print("✨ Done! Now check the Healer.")