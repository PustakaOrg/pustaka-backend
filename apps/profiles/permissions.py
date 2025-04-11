from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    """
    Custom permission to only allow users in a specific group to access the view.
    """

    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if the user is in the specified group
        # TODO: : optimize posible double query 
        return any(request.user.groups.filter(name=group).exists() for group in self.group_names)
