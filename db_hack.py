from datacenter.models import (
    Mark, Chastisement, Schoolkid, Lesson, Subject, Commendation
)
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


FEEDBACK_LIST = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Великолепно!",
    "Прекрасно!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Теперь у тебя точно все получится!"
]


def get_schoolkid(student_name):
    if not student_name:
        print("Вы не ввели данные. Введите данные.")
        return None
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=student_name)
        return schoolkid
    except ObjectDoesNotExist:
        print("Ученик не найден. Введите корректные данные.")
        return None
    except MultipleObjectsReturned:
        print("Найдено несколько учеников с таким именем. "
              "Пожалуйста, уточните запрос.")
        return None


def fix_marks(student_name):
    schoolkid = get_schoolkid(student_name)
    if schoolkid is None:
        return

    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)
    print("Оценки исправлены.")


def remove_chastisements(student_name):
    schoolkid = get_schoolkid(student_name)
    if schoolkid is None:
        return

    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisements.delete()
    print("Замечаний больше нет.")


def create_commendation(student_name, subject_name):
    schoolkid = get_schoolkid(student_name)
    if schoolkid is None:
        return
    try:
        subject = Subject.objects.get(
            title=subject_name,
            year_of_study=schoolkid.year_of_study
        )
    except ObjectDoesNotExist:
        print(f"Предмет '{subject_name}' не найден. "
              "Введите корректное название предмета.")
        return
    except MultipleObjectsReturned:
        print(f"Найдено несколько предметов. "
              "Пожалуйста, уточните запрос.")
        return

    last_lesson = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject=subject
    ).order_by("-date").last()
    if last_lesson is None:
        print(f"У ученика {schoolkid.full_name} нет уроков "
              f"по предмету {subject_name}.")

    Commendation.objects.create(
        text=random.choice(FEEDBACK_LIST),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=last_lesson.teacher
        )
    print("Рекомендация добавлена.")
