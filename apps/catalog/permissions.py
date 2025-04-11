from rest_framework import permissions


class IsAdminOrLibrarian(permissions.BasePermission):
    """
    Custom permission to allow any user to read objects,
    but only allow users in the Admin or Librarian groups to create, update, or delete objects.
    """

    def has_permission(self, request, view):
        # Allow read permissions for any user (authenticated or not)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is authenticated and in the 'Admin' or 'Librarian' group for write permissions
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Librarian"]).exists()

        return False
