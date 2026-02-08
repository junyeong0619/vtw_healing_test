import os
import time
import asyncio


# 2. VectorWave 임포트 & DB 초기화 함수 가져오기
from vectorwave import vectorize, initialize_database, generate_and_register_metadata
import logging
logging.basicConfig(level=logging.INFO)


# [핵심] DB 스키마 생성 (이게 없으면 'non-existing index' 에러 남)
print("🌊 [Init] 데이터베이스 스키마를 생성합니다...")
initialize_database()
print("✅ [Init] DB 준비 완료.")

# 테스트용 전역 변수
GLOBAL_STATE = {"count": 0}

@vectorize(auto=True)
async def risky_function():
    """
    3번 호출될 때까지는 에러를 뱉고, 고쳐지면 성공해야 하는 함수
    """
    print(f"   ▶️ Function called! (Count: {GLOBAL_STATE['count']})")

    # 시나리오: 카운트가 0이면 에러 발생
    if GLOBAL_STATE['count'] < 1:
        GLOBAL_STATE['count'] += 1
        raise ValueError("💥 Boom! An error occurred!")

    return "✅ Success!"

async def main():
    generate_and_register_metadata()
    print("\n🚀 [Step 1] Initial Call (Will Fail)")
    try:
        await risky_function()
    except Exception as e:
        print(f"   ❌ Expected Error Caught: {e}")

    print("\n⏳ [Step 2] Waiting for AutoHealer...")
    print("   (백그라운드에서 Healer가 로그를 보고 PR을 만들 때까지 대기합니다)")

    # 30초 ~ 1분 대기
    for i in range(200, 0, -1):
        print(f"\r   waiting... {i}s ", end="", flush=True)
        time.sleep(1)
    print("\n")

    print("\n🚀 [Step 3] Second Call (Check result)")
    try:
        await risky_function()
    except Exception as e:
        print(f"   ❌ Still failing: {e}")
    else:
        print("   ✅ Function executed successfully!")

    print("\n✨ Test Finished.")

if __name__ == "__main__":
    asyncio.run(main())