from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from medbook.models import Doctor, Chat, Message

User = get_user_model()


class Command(BaseCommand):
    help = "Создает 44 пациента с чатами и тестовыми сообщениями для доктора"

    def handle(self, *args, **kwargs):

        doctor_user, created = User.objects.get_or_create(
            id=1,
            defaults={
                'username': 'dr_ivanov',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            doctor_user.set_password('123')
            doctor_user.save()
        doctor, _ = Doctor.objects.get_or_create(user=doctor_user)

        now = timezone.now()
        created_count = 0
        chat_count = 0

        for i in range(1, 45):
            username = f'patient_{i}'
            first_name = f'Пациент{i}'
            last_name = f'Тест{i}'
            user_id = i + 1

            patient, created = User.objects.get_or_create(
                id=user_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )
            if created:
                patient.set_password('123')
                patient.save()

            chat, created_chat = Chat.objects.get_or_create(patient=patient, doctor=doctor)
            if created_chat:
                chat_count += 1

            messages = [
                (patient, "patient", f"Привет, доктор! Я пациент {i}.", now - timedelta(hours=2), True),
                (doctor_user, "doctor", f"Здравствуйте! Я доктор Иванов. Как ваше состояние, пациент {i}?", now - timedelta(hours=1, minutes=45), False),
                (patient, "patient", "Спасибо, всё в порядке.", now - timedelta(hours=1, minutes=30), True),
            ]

            for sender, sender_type, content, ts, read_status in messages:
                if not Message.objects.filter(chat=chat, content=content).exists():
                    Message.objects.create(
                        chat=chat,
                        sender=sender,
                        sender_type=sender_type,
                        content=content,
                        created_at=ts,
                        is_read=read_status
                    )
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"ГОТОВО!\n"
                f"Чатов создано: {chat_count}\n"
                f"Сообщений создано: {created_count}\n"
                f"Доктор → dr_ivanov / 123\n"
                f"Пациенты → patient_2..patient_45 / 123\n"
            )
        )
