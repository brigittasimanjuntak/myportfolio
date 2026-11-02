from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import CreativeSpace
from main.serializers import CreativeSpaceSerializer
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly

# ==========================================
# 1. ENDPOINT LIST (GET) & CREATE (POST)
# ==========================================
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def creativespace_list(request):
    if request.method in ("GET", "HEAD"):
        # Ambil semua data, urutin berdasarkan tanggal dibuat
        artworks = CreativeSpace.objects.prefetch_related("starred_by").all().order_by("-created_at")
        
        # Filter kalo ada pencarian (?title=...)
        title = request.query_params.get("title", "").strip()
        if title:
            artworks = artworks.filter(title__icontains=title)
            
        serializer = CreativeSpaceSerializer(artworks, many=True, context={"request": request})
        return Response(serializer.data)
    
    # Kalo POST (Tambah data baru)
    serializer = CreativeSpaceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==========================================
# 2. ENDPOINT DETAIL (GET), UPDATE (PUT/PATCH), DELETE
# ==========================================
@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def creativespace_detail(request, creative_space_id):
    artwork = get_object_or_404(
        CreativeSpace.objects.prefetch_related("starred_by"), 
        pk=creative_space_id
    )
    
    if request.method in ("GET", "HEAD"):
        serializer = CreativeSpaceSerializer(artwork, context={"request": request})
        return Response(serializer.data)
        
    if request.method == "DELETE":
        # Hapus cuma boleh superuser (dicek sama IsPortfolioOwnerOrEditorOrReadOnly)
        artwork.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    # Kalo PUT (ganti semua) atau PATCH (ganti sebagian)
    serializer = CreativeSpaceSerializer(
        artwork, 
        data=request.data, 
        partial=(request.method == "PATCH"),
        context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ==========================================
# 3. ENDPOINT STAR (POST)
# ==========================================
@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def creativespace_star(request, creative_space_id):
    artwork = get_object_or_404(CreativeSpace, pk=creative_space_id)

    # Toggle star
    if request.user in artwork.starred_by.all():
        artwork.starred_by.remove(request.user)
    else:
        artwork.starred_by.add(request.user)

    # Balikin data terbaru
    serializer = CreativeSpaceSerializer(artwork, context={"request": request})
    return Response(serializer.data)