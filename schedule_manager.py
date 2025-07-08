class Activity:
    def __init__(self, day, start_time, end_time, name, user_type):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.user_type = user_type # "학생" 또는 "교사"

    def __repr__(self):
        return f"Activity(day='{self.day}', start_time='{self.start_time}', end_time='{self.end_time}', name='{self.name}', user_type='{self.user_type}')"

class ScheduleManager:
    def __init__(self):
        self.timetable = [] # Activity 객체들을 저장할 리스트

    def _time_to_minutes(self, time_str):
        """HH:MM 형식의 시간을 분으로 변환. 시간 형식 및 범위 유효성 검사 포함."""
        try:
            h_str, m_str = time_str.split(':')
            h = int(h_str)
            m = int(m_str)
        except ValueError:
            # split 실패 또는 int 변환 실패 시
            raise ValueError("시간은 HH:MM 정수 형태로 입력해야 합니다.")

        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("시간 범위가 잘못되었습니다 (시는 0-23, 분은 0-59).")

        return h * 60 + m

    def _check_overlap(self, new_activity):
        """새로운 활동이 기존 활동과 겹치는지 확인"""
        new_start = self._time_to_minutes(new_activity.start_time)
        new_end = self._time_to_minutes(new_activity.end_time)

        for activity in self.timetable:
            if activity.day == new_activity.day:
                existing_start = self._time_to_minutes(activity.start_time)
                existing_end = self._time_to_minutes(activity.end_time)

                # 겹치는 조건:
                # (새 활동 시작 < 기존 활동 종료) AND (새 활동 종료 > 기존 활동 시작)
                if new_start < existing_end and new_end > existing_start:
                    return activity # 겹치는 활동 반환
        return None # 겹치지 않으면 None 반환

    def add_activity(self, day, start_time, end_time, name, user_type):
        """새로운 활동을 시간표에 추가"""
        # 시간 형식 유효성 검사 먼저 수행
        try:
            start_minutes = self._time_to_minutes(start_time)
            end_minutes = self._time_to_minutes(end_time)
            if start_minutes >= end_minutes:
                return "오류: 시작 시간은 종료 시간보다 빨라야 합니다."
        except ValueError:
            return "오류: 시간 형식이 잘못되었습니다. HH:MM 형식으로 입력해주세요."

        new_activity = Activity(day, start_time, end_time, name, user_type)
        overlapping_activity = self._check_overlap(new_activity)
        if overlapping_activity:
            return f"이 시간에는 '{overlapping_activity.name}' 활동이 있어서 신청할 수 없습니다."
        else:
            self.timetable.append(new_activity)
            # 요일과 시작 시간 순으로 정렬
            self.timetable.sort(key=lambda x: (self._day_to_int(x.day), self._time_to_minutes(x.start_time)))
            return "신청이 완료되었습니다. 일정에 추가했어요."

    def _day_to_int(self, day_str):
        """요일 문자열을 정렬을 위한 정수로 변환"""
        days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        try:
            return days.index(day_str)
        except ValueError:
            return len(days) # 알 수 없는 요일은 뒤로

    def get_schedule_table(self):
        """시간표를 표 형태로 반환"""
        if not self.timetable:
            return "현재 등록된 활동이 없습니다."

        table = "| 요일   | 시작 시간 | 종료 시간 | 활동 이름         | 등록자 유형 | 상태             |\n"
        table += "|--------|-----------|-----------|-------------------|-------------|------------------|\n"

        # 현재 시간표의 모든 활동은 성공적으로 등록된 활동들입니다.
        # 문제에서 요구한 "신청 가능" 또는 "신청 불가 (시간 중복)" 상태는
        # 특정 활동을 '시도'할 때의 결과를 나타내는 것으로 해석했습니다.
        # 따라서 현재 등록된 시간표를 보여줄 때는 모든 활동이 '등록됨' 상태로 표시됩니다.
        # 만약 사용자가 특정 시간대에 새로운 활동을 추가하려고 시도하는 경우,
        # 그 '시도'에 대한 결과를 표의 '상태' 열에 표시하도록 기능을 확장할 수 있습니다.
        # 여기서는 현재 등록된 일정을 보여주는 기능에 집중합니다.

        for activity in self.timetable:
            # 활동 이름이 너무 길 경우 잘릴 수 있으므로, 최대 길이 설정 (예: 15자 + '..')
            activity_name_display = (activity.name[:15] + '..') if len(activity.name) > 17 else activity.name
            table += f"| {activity.day:<6} | {activity.start_time:<9} | {activity.end_time:<9} | {activity_name_display:<17} | {activity.user_type:<11} | 등록됨           |\n"
        return table

    def display_schedule(self):
        """시간표를 콘솔에 출력"""
        print(self.get_schedule_table())

    def check_availability_and_display(self, day, start_time, end_time, name, user_type):
        """
        새로운 활동을 등록 시도하고, 그 결과를 포함한 시간표를 표 형태로 반환합니다.
        표의 마지막 행에는 시도한 활동과 그 결과를 표시합니다.
        """

        # 시간 형식 유효성 검사
        try:
            self._time_to_minutes(start_time)
            self._time_to_minutes(end_time)
            if self._time_to_minutes(start_time) >= self._time_to_minutes(end_time):
                return "오류: 시작 시간은 종료 시간보다 빨라야 합니다.\n" + self.get_schedule_table()
        except ValueError:
            return "오류: 시간 형식이 잘못되었습니다. HH:MM 형식으로 입력해주세요.\n" + self.get_schedule_table()

        prospective_activity = Activity(day, start_time, end_time, name, user_type)
        overlapping_activity = self._check_overlap(prospective_activity)

        status_message = ""
        if overlapping_activity:
            status_message = f"신청 불가 ({overlapping_activity.name}와(과) 중복)"
        else:
            status_message = "신청 가능"

        # 현재 시간표 가져오기
        table = self.get_schedule_table()
        if table == "현재 등록된 활동이 없습니다.": # 시간표가 비어있을 경우 헤더 추가
            table = "| 요일   | 시작 시간 | 종료 시간 | 활동 이름         | 등록자 유형 | 상태             |\n"
            table += "|--------|-----------|-----------|-------------------|-------------|------------------|\n"

        # 시도하는 활동 정보 추가 (마지막 줄에)
        # 활동 이름이 너무 길 경우 잘릴 수 있으므로, 최대 길이 설정
        name_display = (name[:15] + '..') if len(name) > 17 else name
        table += f"| {day:<6} | {start_time:<9} | {end_time:<9} | {name_display:<17} | {user_type:<11} | {status_message:<16} |\n"

        return table


if __name__ == '__main__':
    manager = ScheduleManager()

    # 초기 활동 등록
    print(manager.add_activity("월요일", "10:00", "11:00", "국어 수업", "교사"))
    print(manager.add_activity("월요일", "13:00", "14:00", "수학 자습", "학생"))
    print(manager.add_activity("수요일", "19:00", "20:00", "물리 정리 자습", "학생"))
    # --- 자동화된 테스트 시나리오 ---
    manager = ScheduleManager()
    print("===== 자동화된 테스트 시나리오 시작 =====")

    # 1. 초기 활동 등록
    print("\n[테스트 1: 초기 활동 등록]")
    print(f"월요일 10:00-11:00 '국어 수업'(교사) 등록: {manager.add_activity('월요일', '10:00', '11:00', '국어 수업', '교사')}")
    print(f"수요일 19:00-20:00 '물리 정리 자습'(학생) 등록: {manager.add_activity('수요일', '19:00', '20:00', '물리 정리 자습', '학생')}")
    manager.display_schedule()

    # 2. 문제에 제시된 예제 시나리오: 시간 중복 테스트
    print("\n[테스트 2: 시간 중복 (문제 예시)]")
    print("시도: 수요일 19:30-20:30 '화학 세특 활동'(교사)")
    # 실제 등록 시도 결과
    registration_attempt_result = manager.add_activity("수요일", "19:30", "20:30", "화학 세특 활동", "교사")
    print(f"등록 시도 결과: {registration_attempt_result}")
    # check_availability_and_display 로 상태 확인 (등록은 시도하지 않음)
    availability_check_table = manager.check_availability_and_display("수요일", "19:30", "20:30", "화학 세특 활동", "교사")
    print("시간표 (활동 가능 여부 확인 포함):")
    print(availability_check_table)
    print("등록 시도 후 실제 시간표 (변경 없어야 함):")
    manager.display_schedule()


    # 3. 새로운 활동 성공적으로 등록
    print("\n[테스트 3: 새로운 활동 성공적 등록]")
    print("시도: 화요일 15:00-16:30 '코딩 동아리'(학생)")
    registration_result = manager.add_activity("화요일", "15:00", "16:30", "코딩 동아리", "학생")
    print(f"등록 결과: {registration_result}")
    manager.display_schedule()

    # 4. 다른 요일에 동일 시간대 활동 등록 (성공해야 함)
    print("\n[테스트 4: 다른 요일 동일 시간대 등록]")
    print("시도: 목요일 19:00-20:00 '지구과학 스터디'(학생)")
    registration_result = manager.add_activity("목요일", "19:00", "20:00", "지구과학 스터디", "학생")
    print(f"등록 결과: {registration_result}")
    manager.display_schedule()

    # 5. 시간 형식 오류 테스트
    print("\n[테스트 5: 시간 형식 오류]")
    print("시도: 금요일 25:00-26:00 '오류 테스트'(학생)")
    result = manager.add_activity("금요일", "25:00", "26:00", "오류 테스트", "학생")
    print(f"등록 결과: {result}")
    availability_check_table = manager.check_availability_and_display("금요일", "25:00", "26:00", "오류 테스트", "학생")
    print("시간표 (활동 가능 여부 확인 포함):")
    print(availability_check_table)


    # 6. 시작/종료 시간 논리 오류 테스트
    print("\n[테스트 6: 시작/종료 시간 논리 오류]")
    print("시도: 금요일 10:00-09:00 '시간 역전'(학생)")
    result = manager.add_activity("금요일", "10:00", "09:00", "시간 역전", "학생")
    print(f"등록 결과: {result}")
    availability_check_table = manager.check_availability_and_display("금요일", "10:00", "09:00", "시간 역전", "학생")
    print("시간표 (활동 가능 여부 확인 포함):")
    print(availability_check_table)

    # 7. 비어있는 시간표에 활동 가능 여부 확인
    print("\n[테스트 7: 비어있는 시간표에서 활동 가능 여부 확인]")
    empty_manager = ScheduleManager()
    print("초기 상태 (비어있음):")
    empty_manager.display_schedule()
    availability_check_table = empty_manager.check_availability_and_display("월요일", "09:00", "10:00", "아침 조깅", "학생")
    print("시간표 (활동 가능 여부 확인 포함):")
    print(availability_check_table)

    print("\n===== 자동화된 테스트 시나리오 종료 =====")
