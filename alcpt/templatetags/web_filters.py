from django import template

from alcpt.definitions import UserType, QuestionType, ExamType
from alcpt.models import User, Student, Question
from alcpt.utility import set_query_parameter
from alcpt.exceptions import IllegalArgumentError, ObjectNotFoundError

register = template.Library()


# Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>"
@register.filter(name='has_perm')
def has_perm(user: User, required_privilege: UserType):
    return user.has_perm(UserType[required_privilege])


# Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>"
@register.filter(name='has_perms')
def has_perms(user: User, required_privilege: UserType):
    return user.has_perm(required_privilege)


# check whether question_type is readable question_type
@register.filter(name='readable_question_type')
def readable_question_type(question_type: int):
    for q in QuestionType.__members__.values():
        if question_type is q.value[0]:
            return q.value[1]
    else:
        raise IllegalArgumentError(message='Unknown question type {}.'.format(question_type))


# check whether user_type is readable user_type(int or str)
@register.filter(name='readable_privilege')
def readable_user_type(privilege):
    if type(privilege) is str:
        for u_type in UserType.__members__.values():
            if u_type.name == privilege:
                return u_type.value[1]
    elif type(privilege) is int:
        for u_type in UserType.__members__.values():
            if u_type is UserType.Admin:
                if privilege is UserType.SystemManager.value[0]:
                    return UserType.SystemManager.value[1]
            elif (privilege & u_type.value[0]) > 0:
                return u_type.value[1]
        else:
            raise IllegalArgumentError(message='Unknown user type {}.'.format(privilege))
    else:
        raise IllegalArgumentError(message='Unknown user type argument which type is {}'.format(type(privilege)))


# check whether exam_type is readable type
@register.filter(name='readable_exam_type')
def readable_state(exam_type: int):
    for et in ExamType.__members__.values():
        if exam_type is et.value[0]:
            return et.value[1]
    else:
        raise IllegalArgumentError(message='Unknown question type {}.'.format(exam_type))


@register.filter(name='replace_page')
def replace_page(full_path: str, page: int):
    return set_query_parameter(full_path, 'page', page)


@register.filter(name='range_to')
def range_to(from_val: int, to_val: int):
    return range(from_val, to_val + 1)


@register.filter(name='lookup')
def range_to(arr: list, i: int):
    return arr[i]


# check whether user is student
@register.filter(name='is_student')
def is_student(user: User):
    try:
        student = Student.objects.get(user=user)
        return student

    except Exception:
        return False


@register.filter(name='student_data')
def student_data(user: User):
    student = Student.objects.get(user=user)
    try:
        data = [student.department.name, student.grade, student.squadron.name]
        return data

    except Exception:
        data = ['None', student.grade, 'None']
        return data



@register.filter(name='check_correct')
def check_correct(option: str, question: Question):
    if question.option.index(option) == question.answer:
        return True

    else:
        return False


@register.filter(name='readable_state')
def readable_state(state: int):
    STATE = (
        (0, '暫存'),
        (1, '審核通過'),
        (2, '審核未通過'),
        (3, '等待審核'),
        (4, '被回報錯誤'),
        (5, '被回報錯誤，已處理'),
    )
    return STATE[state][1]
