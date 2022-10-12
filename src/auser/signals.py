'''
    For creating a group of this library managment 
    which is users of library, library staffs, admin of the system
    is done by using signals

'''
from django.apps import apps

def create_role(sender, plan, *args, **kwargs):
    '''
    Here is 
        User :- normal ordinery user who has a right to borrow books and use properly
        Staff user :- workers of the library and they checks every activity of users
    '''
    
    ROLES = ["user", "staff_user"]
    Group = apps.get_model("auth", "Group")

    for role in ROLES:
        Group.objects.get_or_create(name=role)