import asyncio
import logging
import time

from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

logging.basicConfig(level=logging.INFO)

# [수정] 클래스 대신 전역 상태 변수 사용 (Healer가 함수를 쉽게 찾게 하기 위함)
# 실제로는 DB나 Redis 같은 외부 저장소라고 가정
GLOBAL_STATE = {"is_processing": False}

@vectorize(team="payment_team", auto=True)
def process_payment(amount: int):
    """
    Processes a payment transaction asynchronously.
    Manages a global state lock to prevent concurrent processing.
    """
    print(f"💳 Request to process payment: ${amount}")

    # Check if the system is already processing a transaction
    if GLOBAL_STATE["is_processing"]:
        print("   ⛔ System is busy! (Cascading Error happens here)")
        raise RuntimeError("System is currently processing another transaction.")

    # Lock the state to indicate processing is underway
    GLOBAL_STATE["is_processing"] = True
    print("   🔒 Lock acquired.")

    try:
        # Simulate asynchronous operation delay
        asyncio.sleep(0.1)

        # Check for invalid input
        if amount < 0:
            raise ValueError("Negative amount not allowed!")

    finally:
        # Always release the lock, regardless of errors
        GLOBAL_STATE["is_processing"] = False
        print("   🔓 Lock released.")

    return "Success"

async def main():
    print("\n🚀 [Step 1] Registering Metadata...")
    generate_and_register_metadata()

    # (A) 첫 번째 요청: 에러 발생 (Root Cause)
    print("\n⚠️ [Step 2] Triggering Root Cause (Crash without unlocking)...")
    try:
        await process_payment(-100) # 음수 금액 -> ValueError -> 락 안 풀리고 죽음
    except ValueError as e:
        print(f"   ✅ Root Error Captured: {e}")

    # (B) 두 번째 요청: 정상 요청이지만 실패함 (Cascading Error)
    print("\n⚠️ [Step 3] Triggering Cascading Error (System locked forever)...")
    try:
        # 락이 안 풀려있어서 여기서 무조건 에러가 나야 함
        await process_payment(50)
    except RuntimeError as e:
        print(f"   ✅ Cascading Error Captured: {e}")
        print("   -> The system is now a 'Zombie'. AutoHealer needs to use 'try...finally' to fix this.")

    print("\n⏳ [Step 4] Flushing logs...")
    time.sleep(10)
    get_batch_manager().shutdown()
    print("\n✨ Check if AutoHealer adds a 'try...finally' block!")

if __name__ == "__main__":
    asyncio.run(main())