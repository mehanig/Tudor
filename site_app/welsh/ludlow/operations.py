import os
from welsh.ludlow.models import *


class Ops:
    ADD = 'add'
    RENAME = 'rename'
    DELETE = 'delete'
    START = 'start'
    STOP = 'stop'
    STATUS = 'status'


class UserAction:
    def __init__(self, course, request):
        try:
            if request.data['action'] == Ops.ADD:
                print("ADD")
                self.result = ServerFileSystemFolder.add_in_course(course=course,
                                                                   new_path=request.data['new_path'])
            elif request.data['action'] == Ops.RENAME:
                print("RENAME")
                new_name = request.data['new_name']
                old_path = request.data['old_path']
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                self.result = ServerFileSystemFolder.rename_in_course(course=course,
                                                                      old_path=old_path,
                                                                      new_path=new_path)
            elif request.data['action'] == Ops.DELETE:
                print("DELETE")
                self.result = ServerFileSystemFolder.delete_in_course(course=course,
                                                                      path=request.data['path'])
            elif request.data['action'] == Ops.START:
                pass
            elif request.data['action'] == Ops.STOP:
                pass
            elif request.data['action'] == Ops.STATUS:
                pass
            else:
                raise Exception('No Action Type')

        except Exception as e:
            print("EXCEPTION")
            print(e)
