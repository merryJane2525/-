from flask import Flask, render_template, request, redirect, url_for, flash
from schedule_manager import ScheduleManager, Activity # schedule_manager.py에서 클래스 임포트

app = Flask(__name__)
app.secret_key = 'supersecretkey' # flash 메시지를 위해 필요

# ScheduleManager 인스턴스 생성
schedule_manager_instance = ScheduleManager()

# 예시로 초기 데이터 추가 (테스트용)
# schedule_manager_instance.add_activity("월요일", "10:00", "11:00", "국어 수업", "교사")
# schedule_manager_instance.add_activity("수요일", "19:00", "20:00", "물리 정리 자습", "학생")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        day = request.form.get('day')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        name = request.form.get('name')
        user_type = request.form.get('user_type')

        # 입력 값 유효성 검사 (간단하게)
        if not all([day, start_time, end_time, name, user_type]):
            flash("모든 필드를 입력해주세요.", "error")
        else:
            result = schedule_manager_instance.add_activity(day, start_time, end_time, name, user_type)
            if "완료" in result:
                flash(result, "success")
            else:
                flash(result, "error")
        return redirect(url_for('index'))

    # 시간표 데이터를 템플릿에 전달
    # schedule_manager.py의 get_schedule_table()은 텍스트 테이블을 반환하므로,
    # timetable 객체 리스트를 직접 사용. ScheduleManager.add_activity() 내부에서
    # self.timetable이 요일과 시작 시간 순으로 정렬됨.
    activities = schedule_manager_instance.timetable

    # 이전 주석 내용:
    # 요일 순서 정의 (정렬용) -> ScheduleManager에서 이미 정렬하므로 app.py에서 불필요
    # day_order = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일", "기타"]

    # 활동들을 요일과 시작 시간으로 정렬 -> ScheduleManager에서 이미 정렬하므로 app.py에서 불필요
    # Activity 객체에 _time_to_minutes가 없으므로 schedule_manager_instance의 것을 사용
    # 또는 Activity 객체 자체에 정렬 가능한 속성을 두는 것이 더 객체지향적일 수 있음.
    # 여기서는 schedule_manager_instance의 private 메소드를 임시로 사용 (좋은 방법은 아님)
    # 더 나은 방법은 Activity 객체가 스스로 정렬 키를 제공하거나, ScheduleManager에 정렬된 리스트를 요청하는 것.

    return render_template('index.html', activities=activities)

if __name__ == '__main__':
    # schedule_manager.py의 if __name__ == '__main__': 부분은 CLI/테스트용이므로 웹 서버 실행 시에는 사용하지 않음.
    app.run(debug=True)
