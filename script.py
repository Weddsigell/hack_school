from django.utils.crypto import random
from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson, Subject


chastisement_texts = (
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


def search_subject(schoolkid, lesson):
    try:
        return Subject.objects.get(title=lesson, year_of_study=schoolkid.year_of_study)
    except Subject.DoesNotExist:
        print("Предмет не найден!")
        return
    except Subject.MultipleObjectsReturned:
        print("Найдено более 1 предмета!")
        return


def search_lesson(schoolkid, subject):
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    )

    if last_lesson:
        return last_lesson.order_by('date').last()
    else:
        print('Урока еще не было!')
        return


def create_commendation(schoolkid, lesson):
    text = random.choice(chastisement_texts)
    Commendation.objects.create(
        text=text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def search_student(full_name="Фролов Иван Григорьевич"):
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено более 1 ученика!")
        return
    except Schoolkid.DoesNotExist:
        print("Ни одного ученика не найдено!")
        return


def main():
    kid_name = input('Введите ФИО ученика')
    kid = search_student(kid_name)
    if not kid:
        return

    fix_marks(kid)
    print('3 и 2 исправлены!')

    remove_chastisements(kid)
    print('Замечаний больше нет!')

    subject_name = input('Введите предмет по которому нужна похвала!')
    subject = search_subject(kid, subject_name)
    if not subject:
        return
    lesson = search_lesson(kid, subject)
    if not lesson:
        return
    create_commendation(kid, lesson)
    print('готово, похвала получена!')
