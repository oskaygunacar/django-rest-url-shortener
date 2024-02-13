from rest_framework.permissions import BasePermission


class APIViewPermission(BasePermission):
    def has_permission(self, request, view):
        profile= request.user.profile
        if profile.premium:
            if profile.api_view > 0:
                return True
            self.message = 'Your api display limit is 0. Please Upgrade your account.'
            return False
        self.message = 'You are not premium. Only premium users can use api.'
        return False
    
class APICreatePermission(BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        if profile.premium:
            if profile.api_create > 0:
                return True
            self.message = 'Your api create limit is 0. Please upgrade your account.'
            return False
        self.message = 'You are not premium. Only premium users can use api'
        return False