import sys
import logging
from vectorwave import initialize_database, vectorize
# 설치가 잘 되었다면 아래 import가 에러 없이 되어야 합니다.
from vectorwave.utils.scheduler import start_scheduler

# 로깅 설정
logging.basicConfig(level=logging.INFO)

@vectorize(team="qa_team", auto=False)
def buggy_adder(a, b):
    print(f"Adding {a} + {b}")
    return a + b

def main():
    print("🧪 Testing VectorWave Installation...")

    # 1. DB 연결 테스트
    if initialize_database():
        print("✅ VectorWave DB Connected Successfully!")
    else:
        print("❌ DB Connection Failed.")
        return

    # 2. AutoHealer 스케줄러 실행 테스트
    print("🚀 Starting Auto-Healer Scheduler (Press Ctrl+C to stop)...")
    try:
        # 1분마다 도는 스케줄러 실행
        start_scheduler(interval_minutes=1)
    except KeyboardInterrupt:
        print("\n🛑 Test Stopped.")

if __name__ == "__main__":
    main()