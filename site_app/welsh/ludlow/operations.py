from welsh.ludlow.models import *


class Ops:
    ADD = 'add'
    RENAME = 'rename'
    DELETE = 'delete'


class UserAction:
    def __init__(self, course, request):
        try:
            if request.data['action'] == Ops.ADD:
                print("ADD")
                self.result = ServerFileSystemFolder.add_in_course(course=course,
                                                                   new_path=request.data['new_path'])
            elif request.data['action'] == Ops.RENAME:
                print("RENAME")
                self.result = ServerFileSystemFolder.rename_in_course(course=course,
                                                                      old_path=request.data['old_path'],
                                                                      new_path=request.data['new_path'])
            elif request.data['action'] == Ops.DELETE:
                print("DELETE")
            else:
                raise Exception('No Action Type')

        except Exception as e:
            print("EXCEPTION")
            print(e)
