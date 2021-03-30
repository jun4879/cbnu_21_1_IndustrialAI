from durable.lang import *

# 규칙 15가지
# 1. AI팀 오전 10시 데이터 EDA 회의
# 2. 팀장은 월요일마다 팀장 회의 참석
# 3. 휴가 시 사무실 화이트보드에 연차 현황 작성
# 4. 전 직원 월요일 아침 청소
# 5.
# 6.
# 7.
# 8. 협업 간 코드 수정 부분 pull, push 하기 전 팀원들과 공유
# 9. 사무실 화이트보드에 외근 현황 작성
# 10.야근 시 저녁 식사 인원 조사하여 취합
# 11.외근 중 회사 차량 사용 시 사용일지 작성
# 12.회의실 화이트보드에 회의실 사용 알림 사항 작성
# 13.
# 14.
# 15.

fact_list = [{'subject': 'A', 'position': '사원', 'vacation': True,  'part': 'AI',
              'added_work': False, 'wants_dinner': False},
             {'subject': 'B', 'position': '사원', 'vacation': False, 'part': 'AI',
              'added_work': True,  'wants_dinner': True},
             {'subject': 'C', 'position': '사원', 'vacation': False, 'part': 'AI',
              'added_work': True,  'wants_dinner': False},
             {'subject': 'D', 'position': '팀장', 'vacation': False, 'part': 'AI',
              'added_work': False, 'wants_dinner': False},
             {'subject': 'E', 'position': '팀장', 'vacation': False, 'part': 'MES',
              'added_work': False, 'wants_dinner': False}
             ]


with ruleset('dlit'):  # 규칙 집합
    @when_all(m.position != 0)
    def cleaning(c):
        print('{0}는 월요일 아침 청소 실시'.format(c.m.subject))

    @when_all(m.vacation == True)
    def vacation_notification(c):
        print('{0}는 알림판에 연차일 작성'.format(c.m.subject))

    @when_all(m.position == '팀장')
    def team_leader_meeting(c):
        print('{0}는 월요일 팀장 회의 참석'.format(c.m.subject))

    @when_all((m.part=='AI') & (m.vacation != True))
    def AI_team_meeting(c):
        print('{0}는 오전 10시 AI팀 EDA 회의 참석'.format(c.m.subject))

    @when_all((m.added_work == True) & (m.wants_dinner == True))
    def eat_dinner(c):
        print('{0}는 저녁 식사 인원'.format(c.m.subject))

# assert_fact

for i in fact_list:
    assert_fact('dlit', {'subject': i['subject'], 'position': i['position'], 'vacation': i['vacation'],
                         'part': i['part'], 'added_work': i['added_work'],  'wants_dinner': i['wants_dinner']})
