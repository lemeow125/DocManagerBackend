from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """
    Allows access only to users with staff role
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.role in ("head", "admin", "planning", "staff")
        )


class IsHead(BasePermission):
    """
    Allows access only to users with staff role
    """

    def has_permission(self, request, view):
        print(request.user.role)
        return bool(request.user and request.user.role == "head")
