from rest_framework import permissions


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
