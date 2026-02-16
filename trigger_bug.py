import time
import logging
from vectorwave import vectorize, generate_and_register_metadata
from vectorwave.batch.batch import get_batch_manager

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------
# 💥 현실적인 버그 함수: "유저 활동 점수 계산기"
# ---------------------------------------------------------
# 상황: 커뮤니티 활동 점수를 계산하는 로직
# 공식: (댓글 수 * 10) / 게시글 수
# 버그: 게시글이 0개인 신규 유저가 들어오면 'ZeroDivisionError' 발생!
# ---------------------------------------------------------
@vectorize(team="growth_team", auto=False)
def calculate_activity_score(post_count: int, comment_count: int):
    print(f"📊 Calculating score -> Posts: {post_count}, Comments: {comment_count}")

    if post_count == 0:
        if comment_count == 0:
            return 0
        else:
            return 10 * comment_count  # Arbitrary scaling factor for cases with comments but no posts
    else:
        score = (comment_count * 10) / post_count

    return int(score)

if __name__ == "__main__":
    print("\n🚀 [Step 1] Registering Metadata...")
    # DB에 함수 코드와 위치 정보 등록
    generate_and_register_metadata()

    print("\n🚀 [Step 2] Simulating User Requests...")

    # (A) 정상 유저 (게시글 5개, 댓글 20개) -> 성공
    try:
        score = calculate_activity_score(5, 20)
        print(f"   ✅ User A (Normal): Score = {score}")
    except Exception as e:
        print(f"   ❌ User A Failed: {e}")

    # (B) 신규 유저 (게시글 0개, 댓글 2개) -> 💥 에러 발생!
    print("\n⚠️ [Step 3] Triggering Bug (ZeroDivisionError)...")
    try:
        calculate_activity_score(0, 2)
    except ZeroDivisionError:
        print("   ✅ ZeroDivisionError Captured! (AutoHealer가 이걸 고쳐야 합니다)")
    except Exception as e:
        print(f"   ❓ Unexpected Error: {e}")
    time.sleep(7)


    # (C) 로그 전송
    print("\n⏳ [Step 4] Flushing logs to VectorWave...")
    get_batch_manager().shutdown()
    print("\n✨ Done! AutoHealer를 확인해보세요.")