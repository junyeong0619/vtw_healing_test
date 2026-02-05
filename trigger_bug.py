# trigger_bug.py
import time
import logging
from vectorwave import vectorize, generate_and_register_metadata

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 1. 버그가 있는 함수 정의 (0으로 나누기)
@vectorize(team="qa_team", auto=True)
def critical_bug_func(a, b):
    print(f"Running calculation: {a} / {b}")
    return a / b  # b가 0이면 ZeroDivisionError 발생!

if __name__ == "__main__":
    print("🐛 [BugTrigger] Initializing...")
    
    # 2. 메타데이터(소스코드) DB 등록
    generate_and_register_metadata()
    time.sleep(2) # DB 저장 대기

    print("💥 [BugTrigger] Generating Error Log...")
    try:
        # 3. 에러 발생 시키기!
        critical_bug_func(100, 0)
    except ZeroDivisionError:
        print("✅ Error generated! Check your 'AutoHealer' terminal.")
