from datacenter.models import (
    Mark, Chastisement, Schoolkid, Lesson, Subject, Commendation
)
import random


def get_schoolkid(student_name):
    if not student_name:
        print("Вы не ввели данные. Введите данные.")
        return None
    schoolkids = Schoolkid.objects.filter(full_name__contains=student_name)
    if not schoolkids.exists():
        print("Ученик не найден. Введите корректные данные.")
        return None
    elif schoolkids.count() > 1:
        print("Найдено несколько учеников с таким именем."
              "Пожалуйста, уточните запрос.")
        return None
    return schoolkids.first()


def fix_marks(student_name):
    schoolkid = get_schoolkid(student_name)
    if schoolkid is None:
        return

    schoolkid_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    )
    for mark in schoolkid_marks:
        mark.points = 5
        mark.save()
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
    except Subject.DoesNotExist:
        print(f"Ошибка: предмет '{subject_name}' не найден."
              "Введите корректное название предмета")
        return

    last_lesson = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject=subject
    ).last()

    feedback_list = [
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
    Commendation.objects.create(
        text=random.choice(feedback_list),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=last_lesson.teacher
        )
    print("Рекомендация добавлена.")
