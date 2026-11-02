from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Hanya Superuser (Pemilik) yang bisa Create (POST) dan Delete (DELETE).
    Pengunjung bisa melihat (GET).
    """
    message = "Hanya pemilik portofolio yang dapat mengubah data ini."

    def has_permission(self, request, view):
        # Kalo cuma mau liat (GET, HEAD, OPTIONS), izinkan
        if request.method in SAFE_METHODS:
            return True
        
        # Kalo mau nulis (POST, DELETE), harus superuser
        return bool(request.user and request.user.is_superuser)


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Superuser bisa semuanya.
    Editor HANYA bisa PUT/PATCH (Update).
    Pengunjung bisa melihat (GET).
    """
    message = "Hanya pemilik atau Editor yang dapat mengubah data ini."

    def has_permission(self, request, view):
        # Kalo cuma mau liat, izinkan
        if request.method in SAFE_METHODS:
            return True

        # Kalo belum login, tolak
        if not (request.user and request.user.is_authenticated):
            return False

        # Kalo Superuser, izinkan semuanya
        if request.user.is_superuser:
            return True

        # Kalo user biasa, cek apakah dia di group 'Editor' DAN mau ngedit (PUT/PATCH)
        if request.method in ("PUT", "PATCH"):
            return request.user.groups.filter(name="Editor").exists()

        # Selain itu (misal mau POST/DELETE), tolak
        return False