import asyncio
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager
import time

logging.basicConfig(level=logging.INFO)

class PaymentProcessor:
    def __init__(self):
        self.is_processing = False  # [State] 공유 상태 변수

    @vectorize(team="payment_team", auto=False)
    async def process_payment(self, amount: int):
        print(f"💳 Request to process payment: ${amount}")

        # 1. [State Check] 이미 처리 중이면 거부 (Locking)
        if self.is_processing:
            print("   ⛔ System is busy! (Cascading Error happens here)")
            raise RuntimeError("System is currently processing another transaction.")

        # 2. [State Update] 락 걸기
        self.is_processing = True
        print("   🔒 Lock acquired.")

        # 3. [Async Simulation] 비동기 작업 흉내
        await asyncio.sleep(0.1)

        # 💥 [BUG]: 작업 도중 에러 발생!
        # 문제점: 여기서 터지면 아래 'self.is_processing = False'가 실행되지 않음.
        # 결과: 락이 영원히 풀리지 않음 (Zombie Lock).
        if amount < 0:
            raise ValueError("Negative amount not allowed!")

        # 4. [State Update] 락 해제 (정상 흐름에서만 실행됨 -> 버그!)
        self.is_processing = False
        print("   🔓 Lock released.")
        return "Success"

async def main():
    print("\n🚀 [Step 1] Registering Metadata...")
    generate_and_register_metadata()

    processor = PaymentProcessor()

    # (A) 첫 번째 요청: 에러 발생 (Root Cause)
    print("\n⚠️ [Step 2] Triggering Root Cause (Crash without unlocking)...")
    try:
        await processor.process_payment(-100) # 음수 금액 -> ValueError 발생 -> 락 안 풀리고 죽음
    except ValueError as e:
        print(f"   ✅ Root Error Captured: {e}")

    # (B) 두 번째 요청: 정상 요청이지만 실패함 (Cascading Error)
    print("\n⚠️ [Step 3] Triggering Cascading Error (System locked forever)...")
    try:
        await processor.process_payment(50) # 정상 금액인데도 실패해야 함
    except RuntimeError as e:
        print(f"   ✅ Cascading Error Captured: {e}")
        print("   -> The system is now a 'Zombie'. AutoHealer needs to use 'try...finally' to fix this.")

    print("\n⏳ [Step 4] Flushing logs...")
    time.sleep(15)
    get_batch_manager().shutdown()
    print("\n✨ Check if AutoHealer adds a 'try...finally' block!")

if __name__ == "__main__":
    asyncio.run(main())