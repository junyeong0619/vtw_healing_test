# trigger_bug.py
import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------
# 💥 현실적인 버그 함수: "사용자 포인트 계산기"
# ---------------------------------------------------------
# 의도: 사용자 정보(Dict)를 받아서 보너스 포인트를 계산해야 함.
# 문제점 1: 'points' 키가 없으면 KeyError 발생 (방어 로직 부재)
# 문제점 2: 'points'가 문자열로 오면("100") 덧셈 실패 (TypeError)
# ---------------------------------------------------------
@vectorize(team="backend", auto=False)
def calculate_user_bonus(user_data):
    print(f"Processing user: {user_data.get('name')}")

    # Safely get points, defaulting to 0 if not present
    base_points = user_data.get('points', 0)

    # Ensure base_points is an integer, convert if it's a string
    if isinstance(base_points, str):
        base_points = int(base_points)

    # Calculate bonus by adding 10%
    bonus = base_points * 1.1

    # Return the bonus as an integer
    return int(bonus)

if __name__ == "__main__":
    print("🚀 [1] Registering Metadata...")
    generate_and_register_metadata()

    print("🚀 [2] Generating Error...")

    # 1. 정상 케이스 (AI에게 정답을 가르쳐줌)
    try:
        print(f"Success: {calculate_user_bonus({'name': 'Alice', 'points': 100})}")
    except: pass

    # 2. 에러 케이스 (API가 이상한 데이터를 줌)
    try:
        # points가 문자열 "500"으로 들어옴 -> TypeError 유발!
        calculate_user_bonus({'name': 'Bob', 'points': "500"})
    except TypeError:
        print("✅ TypeError generated successfully.")
    except KeyError:
        print("✅ KeyError generated successfully.")
    except Exception as e:
        print(f"✅ Unexpected Error: {e}")

    time.sleep(7)

    print("🚀 [3] Flushing logs...")
    get_batch_manager().shutdown()
    print("✨ Done! Now check the Healer.")