import json

import requests
from RestrictedPython import (
    compile_restricted,
    limited_builtins,
    safe_builtins,
    utility_builtins,
)
from billiard.exceptions import SoftTimeLimitExceeded

from http_stubs.models import LogEntry
from parrot import celery_app


@celery_app.task()
def run_request_script(log_id: int, script: str) -> None:
    log: LogEntry = LogEntry.objects.get(pk=log_id)
    try:
        byte_code = compile_restricted(script)
        builtins = {
            **safe_builtins,
            **limited_builtins,
            **utility_builtins,
        }
        loc = {
            'requests': requests,
            'json': json,
        }
        exec(byte_code, {'__builtins__': builtins}, loc)
    except SoftTimeLimitExceeded:
        log.result_script = 'Error: Execution time limit'
    except Exception as err:
        log.result_script = f'Error: {err}'
    else:
        log.result_script = 'Done'
    log.save()
