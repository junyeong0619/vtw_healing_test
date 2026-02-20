import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

logging.basicConfig(level=logging.INFO)

@vectorize(team="qa_team", auto=False)
def concatenate_strings_with_length(s1: str, s2: str):
    print(f"🔗 Concatenating strings: '{s1}', '{s2}'")
    # [BUG]: Intentionally introduce a TypeError by trying to add string length directly to a string
    combined = s1 + s2
    total_length = len(combined)
    # The bug is introduced here: attempting to add an int (total_length) to a str (combined)
    # The expected fix would be: return combined + str(total_length)
    return combined + total_length 

if __name__ == "__main__":
    print("\n🚀 [Step 1] Registering Metadata...")
    generate_and_register_metadata()

    print("\n🚀 [Step 2] Simulating User Requests...")

    # (A) Successful call to generate a 'SUCCESS' log
    try:
        result = concatenate_strings_with_length("hello", "world")
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed unexpectedly: {e}")

    # (B) Call to trigger the TypeError
    print("\n⚠️ [Step 3] Triggering Bug (TypeError)...")
    try:
        # Pass an integer as s2, but the bug is inside trying to add total_length to combined.
        # This will still trigger the TypeError, as `combined + total_length` is the problematic part.
        # To make it more explicit to the function signature, one might pass non-string here,
        # but the current bug is more illustrative of an internal type error.
        result = concatenate_strings_with_length("test", "case")
        # To trigger a TypeError directly from input:
        # concatenate_strings_with_length("test", 123)
        # However, the current bug is more illustrative of an internal type error.
    except TypeError:
        print("   ✅ TypeError Captured! (AutoHealer should fix this)")
    except Exception as e:
        print(f"   ❓ Unexpected Error: {e}")
    time.sleep(7)

    print("\n⏳ [Step 4] Flushing logs to VectorWave...")
    get_batch_manager().shutdown()
    print("\n✨ Done! Check AutoHealer for the fix.")
