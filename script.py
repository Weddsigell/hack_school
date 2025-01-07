from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.crypto import random
from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson, Subject

chastisement_text = (
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Великолепно!",
    "Сказано здорово – просто и ясно!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Так держать!",
    "Ты на верном пути!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Теперь у тебя точно все получится!"
)


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=random.randint(4,5))


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, lesson):
    subject = Subject.objects.get(title=lesson, year_of_study=schoolkid.year_of_study)
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('date').last()

    text = random.choice(chastisement_text)
    Commendation.objects.create(
        text=text,
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )


def good_student(lesson, full_name="Фролов Иван Григорьевич"):
    try:
        kid = Schoolkid.objects.get(full_name__contains=full_name)
    except MultipleObjectsReturned:
        print("Найдено более 1 ученика!")
        return
    except ObjectDoesNotExist:
        print("Ни одного ученика не найдено!")
        return

    fix_marks(kid)
    remove_chastisements(kid)
    create_commendation(kid, lesson)