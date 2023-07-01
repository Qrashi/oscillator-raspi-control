from typing import Union

import singlejson
from datetime import datetime
from json import dumps
from static_info import VERSION, COMMIT


class Context:
    code: str
    task: str


context = Context()
context.code = "launch"
context.task = "initializing errors"

__errors = singlejson.load("errors.json", default="[]")


def report_error(description: str, exception: Union[None, Exception, str] = None):
    try:
        dumps(exception)
        exception = str(exception)
    except Exception:
        exception = "Could not save exception - not serializeable"

    # print("! " + description)

    __errors.json.append(
        {
            "timestamp": datetime.now().timestamp(),
            "time": datetime.now().strftime("%d.%m %H:%M:%S"),
            "exception": str(exception),
            "description": description,
            "version": VERSION,
            "commit": COMMIT,
            "section": context.code,
            "task": context.task
        }
    )
