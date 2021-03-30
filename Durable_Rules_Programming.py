from durable.lang import *

# 규칙 15가지
# 1. AI팀 오전 10시 데이터 EDA 회의
# 2. 팀장은 월요일마다 팀장 회의 참석
# 3. 연차 시 사무실 화이트보드에 연차 현황 작성
# 4. 전 직원 월요일 아침 청소
# 5. 회의실 화이트보드에 회의실 사용 알림 사항 작성
# 6. 사무실 화이트보드에 외근 현황 작성
# 7. 외근 중 회사 차량 사용 시 사용일지 작성
# 8. 야근 시 저녁 식사 인원 조사하여 취합
# 9. 수요일 자유 발표 시간 발표자 8:40분까지 발표 준비
# 10.
# 11.
# 12.
# 13.
# 14.
# 15.

fact_dict_list = [{'subject': 'A', 'position': '사원', 'vacation': True,  'part': 'AI',
                   'added_work': False, 'wants_dinner': False, 'presentation': False,
                   'out_work': False, 'use_company_car': False},
                  {'subject': 'B', 'position': '사원', 'vacation': False, 'part': 'AI',
                   'added_work': True,  'wants_dinner': True, 'presentation': False,
                   'out_work': False, 'use_company_car': False},
                  {'subject': 'C', 'position': '사원', 'vacation': False, 'part': 'AI',
                   'added_work': True,  'wants_dinner': False, 'presentation': True,
                   'out_work': False, 'use_company_car': False},
                  {'subject': 'D', 'position': '팀장', 'vacation': False, 'part': 'AI',
                   'added_work': False, 'wants_dinner': False, 'presentation': False,
                   'out_work': True, 'use_company_car': False},
                  {'subject': 'E', 'position': '팀장', 'vacation': False, 'part': 'MES',
                   'added_work': False, 'wants_dinner': False, 'presentation': False,
                   'out_work': False, 'use_company_car': False},
                  {'subject': 'F', 'position': '사원', 'vacation': False, 'part': 'MES',
                   'added_work': True, 'wants_dinner': False, 'presentation': False,
                   'out_work': True, 'use_company_car': True}
                  ]

meeting_room_white_board_list = []
vacation_list = []
added_work_list = []
dinner_list = []
outside_work_list = []
company_car_using = {'state': False, 'person': 'None'}

with ruleset('dlit'):
    @when_all(+m.position)
    def cleaning(c):
        print('{0}는 월요일 아침 청소 실시'.format(c.m.subject))

    @when_all(m.vacation == True)
    def vacation_notification(c):
        vacation_list.append(c.m.subject)

    @when_all(m.position == '팀장')
    def team_leader_meeting(c):
        print('{0}는 월요일 팀장 회의 참석'.format(c.m.subject))
        if {'내용':'월요일 팀장 회의'} not in meeting_room_white_board_list:
            meeting_room_white_board_list.append({'내용':'월요일 팀장 회의'})

    @when_all((m.part == 'AI') & (m.vacation != True))
    def AI_team_meeting(c):
        print('{0}는 오전 10시 AI팀 EDA 회의 참석'.format(c.m.subject))
        if {'내용': 'AI팀 EDA 회의', '시간': '오전 10시'} not in meeting_room_white_board_list:
            meeting_room_white_board_list.append({'내용': 'AI팀 EDA 회의', '시간': '오전 10시'})

    @when_all(m.added_work == True)
    def eat_dinner(c):
        if c.m.subject not in added_work_list:
            added_work_list.append(c.m.subject)
        if (c.m.wants_dinner == True):
            if c.m.subject not in dinner_list:
                dinner_list.append(c.m.subject)

    @when_all(m.out_work == True)
    def using_car(c):
        if c.m.subject not in outside_work_list:
            outside_work_list.append(c.m.subject)
        if (c.m.use_company_car == True):
            company_car_using['state'] = True
            company_car_using['person'] = c.m.subject

    @when_all(m.presentation == True)
    def presentation(c):
        print('{0}는 수요일 발표 준비'.format(c.m.subject))
        if "수요일 발표 : ".format(c.m.subject) not in meeting_room_white_board_list:
            meeting_room_white_board_list.append("수요일 발표 : {0}".format(c.m.subject))

print("===직원별 fact 목록===")
# assert_fact
for i in fact_dict_list:
    assert_fact('dlit', {'subject': i['subject'], 'position': i['position'], 'vacation': i['vacation'],
                         'part': i['part'], 'added_work': i['added_work'],  'wants_dinner': i['wants_dinner'],
                         'out_work': i['out_work'], 'use_company_car': i['use_company_car'],
                         'presentation': i['presentation']})

print("======알림======")
print("휴가자: ", " ".join(str(vacation) for vacation in vacation_list))
print("야근자: ", " ".join(str(worker) for worker in added_work_list))
print("석식자: ", " ".join(str(eater) for eater in dinner_list))
print("외근자: ", " ".join(str(out_worker) for out_worker in outside_work_list))
if company_car_using['state']:
    print("회사 차량 : 현재 {0} 사용 중, 사용 불가".format(company_car_using['person']))
else:
    print("회사 차량 : 미사용 중, 사용 가능")

print("======회의======")
for meeting_plan in meeting_room_white_board_list:
    print(meeting_plan)
