import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

logging.basicConfig(level=logging.INFO)

@vectorize(team="logistics_team", auto=False)
def calculate_shipping_cost(weight_kg: float, distance_km: float, is_international: bool = False) -> float:
    print(f"📦 Calculating shipping cost: Weight={weight_kg}kg, Distance={distance_km}km, International={is_international}")

    # Base cost calculation
    base_cost = weight_kg * 0.5 + distance_km * 0.01

    if is_international:
        base_cost += 10.0 # Add international surcharge

    final_cost = base_cost # [BUG]: Minimum cost ($5) is not applied at the very end.
                            # So, if base_cost is very low and it's not international,
                            # final_cost could be < 5.0.

    # Simulate a validation layer that detects the logical error
    if final_cost < 5.0 and (weight_kg > 0 or distance_km > 0 or is_international):
        raise ValueError(f"Shipping cost {final_cost:.2f} is below minimum $5.00, which is a logical error.")

    return final_cost

if __name__ == "__main__":
    print("\n🚀 [Step 1] Registering Metadata...")
    generate_and_register_metadata()

    print("\n🚀 [Step 2] Simulating User Requests...")

    # (A) Normal scenario - expected to succeed and be >= 5.0
    try:
        cost1 = calculate_shipping_cost(10.0, 500.0, False) # base_cost = 5 + 5 = 10.0
        print(f"   ✅ Cost (10kg, 500km, local): ${cost1:.2f}")
    except Exception as e:
        print(f"   ❌ Failed unexpectedly: {e}")

    # (B) Scenario triggering the logical error leading to ValueError
    print("\n⚠️ [Step 3] Triggering Bug (Logical Error: Below Minimum Cost)...")
    try:
        # Inputs: weight_kg=0.1, distance_km=1.0, is_international=False
        # base_cost = 0.1 * 0.5 + 1.0 * 0.01 = 0.05 + 0.01 = 0.06
        # is_international is False, so no surcharge.
        # final_cost = 0.06. This is < 5.0, so it should trigger the ValueError.
        cost2 = calculate_shipping_cost(0.1, 1.0, False)
        print(f"   ❌ Unexpected Success: ${cost2:.2f} (Should have been $5.00 or raised error)")
    except ValueError as e:
        print(f"   ✅ ValueError Captured! ({e}) (AutoHealer should fix this to ensure minimum $5.00)")
    except Exception as e:
        print(f"   ❓ Unexpected Error: {e}")
    time.sleep(7)

    print("\n⏳ [Step 4] Flushing logs to VectorWave...")
    get_batch_manager().shutdown()
    print("\n✨ Done! Check AutoHealer for the fix (should ensure final cost >= $5.00).")
