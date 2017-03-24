import os
import time

from welsh.ludlow.const import TRASH_BIN


def gen_trash_path(course, path):
    timestamp = str(int(time.time() * 1000))
    name = os.path.basename(os.path.normpath(path))
    filename = '{coursename}_{name}_{timestamp}'.format(coursename=course.name,
                                                        name=name,
                                                        timestamp=timestamp)
    return os.path.join(course.author.local_path, TRASH_BIN, filename)
