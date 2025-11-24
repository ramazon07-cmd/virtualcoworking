from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user


class IsTeamMember(permissions.BasePermission):
    """
    Custom permission to only allow team members to access team resources.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a member of the team
        if hasattr(obj, 'team'):
            return obj.team.members.filter(id=request.user.id).exists()
        return False


class IsTeamAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow team admins or owners to modify team resources.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner or an admin of the team
        if hasattr(obj, 'team'):
            membership = obj.team.teammembership_set.filter(user=request.user).first()
            if membership:
                return membership.role in ['owner', 'admin']
        return False