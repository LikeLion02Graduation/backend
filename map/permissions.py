from rest_framework import permissions

# class IsAuthorOrBuyer(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.user == request.user
    
class IsOwner(permissions.BasePermission):
    # 게시물 작성자만 접근 가능하게 하기
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.user:
                return True
            return False
        else:
              return False