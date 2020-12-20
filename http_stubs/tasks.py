from billiard.exceptions import SoftTimeLimitExceeded

from http_stubs.models import LogEntry
from parrot import celery_app


@celery_app.task()
def run_request_script(log_id: int, script: str) -> None:
    log: LogEntry = LogEntry.objects.get(pk=log_id)
    try:
        print(f'Request: {script!r}')
    except SoftTimeLimitExceeded:
        log.result_script = 'Time limit'
    except Exception as err:
        log.result_script = f'Error: {err}'
    else:
        log.result_script = 'Done'
    log.save()
