import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

logging.basicConfig(level=logging.INFO)

@vectorize(team="sales_team", auto=False)
def calculate_discounted_price(original_price: float, discount_percentage: float) -> float:
    print(f"💰 Calculating discounted price: Original={original_price}, Discount={discount_percentage}%")

    if not (0 <= discount_percentage <= 100):
        raise ValueError("Discount percentage must be between 0 and 100.")

    discount_amount = original_price * (discount_percentage / 100)
    final_price = original_price - discount_amount

    if final_price < 0:
        final_price = 0

    return final_price

if __name__ == "__main__":
    print("\n🚀 [Step 1] Registering Metadata...")
    generate_and_register_metadata()

    print("\n🚀 [Step 2] Simulating User Requests...")

    # (A) Normal discount - expected to succeed
    try:
        price1 = calculate_discounted_price(100.0, 10.0) # 90.0
        print(f"   ✅ Price (100, 10%): {price1}")
    except Exception as e:
        print(f"   ❌ Failed unexpectedly: {e}")

    # (B) Discount resulting in negative price - expected to trigger ValueError
    print("\n⚠️ [Step 3] Triggering Bug (Negative Price ValueError)...")
    try:
        price2 = calculate_discounted_price(50.0, 120.0) # Should be 0, but current bug will raise ValueError
        print(f"   ❌ Unexpected Success: {price2} (Should have been 0 or raised error)")
    except ValueError as e:
        print(f"   ✅ ValueError Captured! ({e}) (AutoHealer should fix this to return 0 instead of raising error)")
    except Exception as e:
        print(f"   ❓ Unexpected Error: {e}")
    time.sleep(7)

    print("\n⏳ [Step 4] Flushing logs to VectorWave...")
    get_batch_manager().shutdown()
    print("\n✨ Done! Check AutoHealer for the fix (should set price to 0 if negative).")
