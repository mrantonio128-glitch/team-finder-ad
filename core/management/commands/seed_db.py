import random
from pathlib import Path
from typing import Any, List, Tuple

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from projects.models import Project

SEED_PASSWORD = "super_pass_123"


class Command(BaseCommand):
    help = "Generate fake test users and projects."

    @transaction.atomic
    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.stdout.write("Seeding data...")

        user_data = [
            {
                "email": "anna.ivanova@example.com",
                "name": "Анна",
                "surname": "Иванова",
                "phone": "+79990011122",
                "avatar_file": "anna.jpg",
                "github_url": "https://github.com/anna-ivanova",
            },
            {
                "email": "sergey.petrov@example.com",
                "name": "Сергей",
                "surname": "Петров",
                "phone": "+79990022233",
                "avatar_file": "sergey.jpg",
                "github_url": "https://github.com/sergey-petrov",
            },
            {
                "email": "irina.sokolova@example.com",
                "name": "Ирина",
                "surname": "Соколова",
                "phone": "+79990033344",
                "avatar_file": "irina.jpg",
                "github_url": "https://github.com/irina-sokolova",
            },
            {
                "email": "alexey.kovalev@example.com",
                "name": "Алексей",
                "surname": "Ковалев",
                "phone": "+79990044455",
                "github_url": "https://github.com/alexey-kovalev",
            },
            {
                "email": "yana.volkova@example.com",
                "name": "Яна",
                "surname": "Волкова",
                "phone": "+79990055566",
                "github_url": "https://github.com/yana-volkova",
            },
            {
                "email": "evgeny.mikhailov@example.com",
                "name": "Евгений",
                "surname": "Михайлов",
                "phone": "+79990066677",
                "github_url": "https://github.com/evgeny-mikhailov",
            },
            {
                "email": "olga.novikova@example.com",
                "name": "Ольга",
                "surname": "Новикова",
                "phone": "+79990077788",
                "github_url": "https://github.com/olga-novikova",
            },
            {
                "email": "pavel.kozlov@example.com",
                "name": "Павел",
                "surname": "Козлов",
                "phone": "+79990088899",
                "github_url": "https://github.com/pavel-kozlov",
            },
            {
                "email": "marina.fedorova@example.com",
                "name": "Марина",
                "surname": "Федорова",
                "phone": "+79990099900",
                "github_url": "https://github.com/marina-fedorova",
            },
            {
                "email": "vladislav.nikiforov@example.com",
                "name": "Владислав",
                "surname": "Никифоров",
                "phone": "+79990100011",
                "github_url": "https://github.com/vladislav-nikiforov",
            },
            {
                "email": "elena.gordeeva@example.com",
                "name": "Елена",
                "surname": "Гордеева",
                "phone": "+79990111122",
                "github_url": "https://github.com/elena-gordeeva",
            },
            {
                "email": "igor.lopatkin@example.com",
                "name": "Игорь",
                "surname": "Лопаткин",
                "phone": "+79990122233",
                "github_url": "https://github.com/igor-lopatkin",
            },
            {
                "email": "olga.zhuravleva@example.com",
                "name": "Ольга",
                "surname": "Журавлева",
                "phone": "+79990133344",
                "github_url": "https://github.com/olga-zhuravleva",
            },
        ]

        users: List[User] = []

        def create_or_get_user(data: dict) -> User:
            existing = User.objects.filter(email=data["email"]).first()
            if existing:
                return existing

            user = User(
                email=data["email"],
                name=data["name"],
                surname=data["surname"],
                phone=data["phone"],
                about="Работаю над интересными проектами и готов обмениваться опытом.",
                github_url=data.get("github_url", ""),
            )
            user.set_password(SEED_PASSWORD)

            avatar_fname = data.get("avatar_file")
            if avatar_fname:
                avatar_path = (
                    Path(settings.BASE_DIR) / "media" / "seed_avatars" / avatar_fname
                )
                if avatar_path.exists():
                    with avatar_path.open("rb") as f:
                        user.avatar.save(avatar_fname, File(f), save=False)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"File missing: {avatar_path}")
                    )

            user.save()
            return user

        for data in user_data:
            users.append(create_or_get_user(data))

        self.stdout.write(f"Done {len(users)} users.")

        project_data = [
            (
                "Cloud Monitoring Suite",
                "Система для контроля состояния серверов и приложений в облаке.",
            ),
            (
                "Recruitment Portal",
                "Платформа для публикации вакансий и отбора кандидатов.",
            ),
            (
                "Inventory Control",
                "Сервис управления складскими запасами и заказами.",
            ),
            (
                "Customer Feedback Hub",
                "Инструмент для сбора отзывов и анализа удовлетворенности клиентов.",
            ),
            (
                "Online Learning Platform",
                "Решение для проведения онлайн-курсов и дистанционного обучения.",
            ),
            (
                "Finance Reports Engine",
                "Система формирования финансовых отчетов и прогнозов.",
            ),
            (
                "Event Management System",
                "Платформа для организации мероприятий и управления гостями.",
            ),
            (
                "Delivery Route Optimizer",
                "Инструмент для планирования маршрутов доставки и логистики.",
            ),
            (
                "Digital Portfolio Builder",
                "Сервис для создания профессиональных портфолио и демонстрации работ.",
            ),
            (
                "Compliance Tracker",
                "Приложение для контроля соответствия регламентам и стандартам.",
            ),
            (
                "Team Collaboration Board",
                "Система совместной работы над задачами и проектами.",
            ),
            (
                "Media Content Hub",
                "Платформа управления публикацией фото, видео и статей.",
            ),
            (
                "Health Analytics Dashboard",
                "Приборная панель для анализа показателей здоровья и самочувствия.",
            ),
            (
                "Product Launch Planner",
                "Инструмент для подготовки и запуска маркетинговых кампаний.",
            ),
            (
                "Service Ticket Portal",
                "Сервис обработки запросов клиентов и распределения задач поддержки.",
            ),
            (
                "Warehouse Automation",
                "Решение для автоматизации операций на складе и оптимизации складских процессов.",
            ),
            (
                "Market Research Toolkit",
                "Платформа для сбора и анализа рыночных данных.",
            ),
            (
                "Mobile App Development Board",
                "Система планирования и контроля разработки мобильных приложений.",
            ),
            (
                "Smart Finance Assistant",
                "Приложение для управления личными финансами и бюджетом.",
            ),
            (
                "Security Incident Tracker",
                "Сервис для фиксации и анализа инцидентов безопасности.",
            ),
            (
                "Sales Funnel Manager",
                "Платформа управления воронкой продаж и сделками.",
            ),
            (
                "Content Publishing Engine",
                "Система автоматической публикации материалов и планирования контента.",
            ),
            (
                "Product Research Lab",
                "Инструмент для анализа пользовательских сценариев и идей продуктов.",
            ),
            (
                "Internal Knowledge Base",
                "Платформа для хранения и поиска документации внутри команды.",
            ),
            (
                "Customer Journey Mapper",
                "Сервис визуализации пути клиента и ключевых точек взаимодействия.",
            ),
        ]

        projects: List[Project] = []

        def create_or_get_project(title: str, desc: str, owners: List[User]) -> Project:
            if not owners:
                raise RuntimeError("No users available to assign project owners")
            owner = random.choice(owners)
            status = random.choices(
                [Project.Status.OPEN, Project.Status.CLOSED], weights=[3, 1], k=1
            )[0]
            project, _ = Project.objects.get_or_create(
                name=title,
                defaults={
                    "description": desc,
                    "owner": owner,
                    "status": status,
                    "github_url": "https://github.com/example-project",
                },
            )
            return project

        for title, desc in project_data:
            projects.append(create_or_get_project(title, desc, users))

        self.stdout.write(f"Done {len(projects)} projects.")

        for project in projects:
            if project.status == Project.Status.OPEN and random.random() > 0.3:
                potential_participants = [u for u in users if u != project.owner]
                if potential_participants:
                    max_count = min(3, len(potential_participants))
                    count = random.randint(1, max_count)
                    participants = random.sample(potential_participants, count)
                    project.participants.add(*participants)

            fan_count = 0
            if users:
                fan_count = random.randint(0, min(3, len(users)))
            if fan_count:
                fans = random.sample(users, fan_count)
                for fan in fans:
                    fan.favorites.add(project)

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
        self.stdout.write(
            self.style.WARNING(
                "Login with any seeded user email and password: super_pass_123"
            )
        )
