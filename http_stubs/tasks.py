import json

import requests
from billiard.exceptions import SoftTimeLimitExceeded
from RestrictedPython import (
    compile_restricted,
    limited_builtins,
    safe_builtins,
    utility_builtins,
)

from http_stubs.models import LogEntry
from parrot import celery_app

restricted_builtins = {'__builtins__': {
    **safe_builtins,
    **limited_builtins,
    **utility_builtins,
}}


@celery_app.task()
def run_request_script(log_id: int, script: str, request_body: str) -> None:
    """Task for run custom scripts from http stubs.

    :param log_id: LogEntry.id
    :param script: HTTPStub.request_script
    :param request_body: text body from a request
    """
    log: LogEntry = LogEntry.objects.get(pk=log_id)
    try:  # noqa: WPS229
        byte_code = compile_restricted(script)
        loc = {
            'requests': requests,
            'json': json,
            'request_body': request_body,
        }
        exec(byte_code, restricted_builtins, loc)  # noqa: S102, WPS421
    except SoftTimeLimitExceeded:
        log.result_script = 'Error: Execution time limit'
    except Exception as err:
        log.result_script = f'Error: {err}'
    else:
        log.result_script = 'Done'
    log.save()
