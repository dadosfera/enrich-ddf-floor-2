"""
Celery configuration for background task processing.
"""

from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "enrich-ddf-floor-2",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.enrichment",
        "app.tasks.notifications",
        "app.tasks.data_processing"
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Optional: Configure task routes
celery_app.conf.task_routes = {
    "app.tasks.enrichment.*": {"queue": "enrichment"},
    "app.tasks.notifications.*": {"queue": "notifications"},
    "app.tasks.data_processing.*": {"queue": "data_processing"},
}

if __name__ == "__main__":
    celery_app.start() 