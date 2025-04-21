from rest_framework import permissions


class IsAdminOrLibrarianModify(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Librarian"]).exists()

        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin"]).exists()

        return False


class IsAdminOrLibrarianOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Librarian"]).exists()

        return False


class IsAdminOrLibrarianOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name__in=["Admin", "Librarian"]).exists():
            return True

        if hasattr(view, "get_object"):
            obj = view.get_object()
            return obj.account == request.user

        return False
