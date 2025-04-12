from rest_framework import permissions

"""
TODO: Rework all permissions
1. Admin only -> Settings, WA Connection
2. Admin, Owner can edit, others read only
3. Admin, Librarian, Owner, can edit, others read only
"""

class IsAdminOrLibrarianModify(permissions.BasePermission):
    """
    Custom permission to allow any user to read objects,
    but only allow users in the Admin or Librarian groups to create, update, or delete objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Librarian"]).exists()

        return False

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow any user to read objects,
    but only allow users in the Admin or Librarian groups to create, update, or delete objects.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin"]).exists()

        return False

class IsAdminOrLibrarianOnly(permissions.BasePermission):
    """
    Custom permission to allow any user to read objects,
    but only allow users in the Admin or Librarian groups to create, update, or delete objects.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Librarian"]).exists()

        return False
