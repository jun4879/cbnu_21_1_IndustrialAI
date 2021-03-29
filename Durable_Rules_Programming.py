from durable.lang import *

# 규칙 15가지
# 1. AI팀 오전 10시 데이터 EDA 회의
# 2.
# 3. 팀장은 월요일 팀장 회의 참석
# 4. 외근 중 회사 차량 사용 시 사용일지 작성
# 5. 회의실 화이트보드에 회의실 사용 알림 사항 작성
# 6. 사무실 화이트보드에 연차 현황 작성
# 7. 사무실 화이트보드에 외근 현황 작성
# 8.
# 9.
# 10.
# 11.
# 12.
# 13.
# 14.
# 15.

with ruleset('dlit'): # 규칙 집합
    # antecedent(조건부), @whel_all, @when_any를 사용하여 표기
    @when_all(m.position == '팀장') # m: rule이 적용되는 데이터
    def team_leader_meeting(c):
        # consequent(결론부)
        c.assert_fact({'subject':c.m.subject, 'predicate':'는','object':'월요일에 팀장 회의에 참석해야 함'})

    @when_all(m.vacation == 1)
    def vacation_notification(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': '는', 'object': '알림판에 연차일 작성'})

    @when_all((m.part == 'AI') and (m.vacation != 1))
    def AI_team_meeting(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': '는', 'object': '오전 10시 EDA 회의 참석'})
        # object에 미팅 바로 쓰지 말고 회의 유무 상태로 넘겨서 회의실 알림판에 작성
        # 인원 단위로 묶어서 알림판 작성하지 않고 팀 단위로 알림판 작성되도록

    @when_all(+m.subject) # m.subject가 한 번 이상
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.object))

post('dlit', {'subject':'A','position':'사원','vacation':True,'part':'AI'})
post('dlit', {'subject':'B','position':'사원','vacation':False,'part':'AI'})
post('dlit', {'subject':'C','position':'팀장','vacation':False,'part':'MES'})

