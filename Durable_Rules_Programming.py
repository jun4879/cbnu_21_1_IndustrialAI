from durable.lang import *

# 사원 a,b,c,d 리스트
employee_working_list = ['a','b','c','d']

# 출퇴큰 현황 리스트
# 발열 체크 37.5 이상일 시 list에서 빼기
#

with ruleset('dlit'): # 규칙 집합
    # antecedent(조건부), @whel_all, @when_any를 사용하여 표기
    @when_all(m.subject == 'world') # m: rule이 적용되는 데이터
    def say_hello(c):
        # consequent(결론부)
        print('Hello {0}'.format(c.m.subject))

    @when_all(m.temperature >= 37.5)
    def work_at_home(c):
        c.assert_fact({})


    @when_all(+m.subject)
    def output(c):




post('dlit', {'subject':'world'})
