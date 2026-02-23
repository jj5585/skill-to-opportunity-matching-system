"""
Management command: python manage.py seed_skills
Seeds the Skill master table with common tech skills.
"""

from django.core.management.base import BaseCommand
from apps.accounts.models import Skill


SKILLS = [
    # Programming
    ('Python', 'Programming'),
    ('JavaScript', 'Programming'),
    ('TypeScript', 'Programming'),
    ('Java', 'Programming'),
    ('C++', 'Programming'),
    ('Go', 'Programming'),
    ('Rust', 'Programming'),
    ('PHP', 'Programming'),
    ('Ruby', 'Programming'),
    ('Swift', 'Programming'),
    # Frameworks & Libraries
    ('Django', 'Frameworks'),
    ('React', 'Frameworks'),
    ('Vue.js', 'Frameworks'),
    ('Angular', 'Frameworks'),
    ('Node.js', 'Frameworks'),
    ('FastAPI', 'Frameworks'),
    ('Spring Boot', 'Frameworks'),
    ('Laravel', 'Frameworks'),
    # Databases
    ('MySQL', 'Databases'),
    ('PostgreSQL', 'Databases'),
    ('MongoDB', 'Databases'),
    ('Redis', 'Databases'),
    ('SQLite', 'Databases'),
    ('Elasticsearch', 'Databases'),
    # DevOps & Cloud
    ('Docker', 'DevOps'),
    ('Kubernetes', 'DevOps'),
    ('AWS', 'Cloud'),
    ('GCP', 'Cloud'),
    ('Azure', 'Cloud'),
    ('CI/CD', 'DevOps'),
    ('Linux', 'DevOps'),
    ('Terraform', 'DevOps'),
    # Data & AI
    ('Machine Learning', 'Data & AI'),
    ('Data Science', 'Data & AI'),
    ('TensorFlow', 'Data & AI'),
    ('PyTorch', 'Data & AI'),
    ('SQL', 'Data & AI'),
    ('Pandas', 'Data & AI'),
    ('NumPy', 'Data & AI'),
    # Soft Skills
    ('Communication', 'Soft Skills'),
    ('Problem Solving', 'Soft Skills'),
    ('Teamwork', 'Soft Skills'),
    ('Project Management', 'Soft Skills'),
    ('Leadership', 'Soft Skills'),
    # Design
    ('UI/UX Design', 'Design'),
    ('Figma', 'Design'),
    ('Adobe Photoshop', 'Design'),
    # Testing
    ('Unit Testing', 'Testing'),
    ('Selenium', 'Testing'),
    ('Jest', 'Testing'),
]


class Command(BaseCommand):
    help = 'Seed the Skill table with common skills.'

    def handle(self, *args, **options):
        created = 0
        for name, category in SKILLS:
            _, was_created = Skill.objects.get_or_create(
                name=name, defaults={'category': category}
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Done. {created} new skills seeded.'))
