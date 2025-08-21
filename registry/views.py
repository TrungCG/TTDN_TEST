from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics
from django.shortcuts import render


from .serializers import CommuneCurrentSerializer, CommuneOldSerializer, MergerSerializer, ProvinceSerializer, DistrictSerializer 
from .models import Province, CommuneCurrent, CommuneOld, Merger, District

# Tạo các API để truy xuất thông tin về tỉnh, quận/huyện, xã/phường hiện tại và cũ, cũng như các quan hệ sáp nhập
class ProvinceList(APIView):
    def get(self, request):
        data = Province.objects.all()
        serializer = ProvinceSerializer(data, many=True)
        return Response(serializer.data)    
# # Danh sách tỉnh
# class ProvinceList(generics.ListAPIView):
#     queryset = Province.objects.all()
#     serializer_class = ProvinceSerializer

    
# Tìm xã/phường hiện tại (có thể lọc theo tỉnh + tên)
class CommuneCurrentSearch(APIView):
    def get(self,request):
        q = request.query_params.get("q", "")
        province_id = request.query_params.get("province", None)
        queryset = CommuneCurrent.objects.all()
        if q:
            queryset = queryset.filter(name__icontains=q)
        if province_id:
            queryset = queryset.filter(province_id=province_id)
        serializer = CommuneCurrentSerializer(queryset, many=True)
        return Response(serializer.data)
# class CommuneCurrentSearch(generics.ListAPIView):
#     serializer_class = CommuneCurrentSerializer

#     def get_queryset(self):
#         q = self.request.query_params.get("q", "")
#         province_id = self.request.query_params.get("province", None)
#         queryset = CommuneCurrent.objects.all()
#         if q:
#             queryset = queryset.filter(name__icontains=q)
#         if province_id:
#             queryset = queryset.filter(province_id=province_id)
#         return queryset
    
# Tìm xã/phường cũ (có thể lọc theo tỉnh + tên)
class CommuneOldSearch(APIView):
    def get(self, request):
        q = request.query_params.get("q", "")
        province_id = request.query_params.get("province", None)
        queryset = CommuneOld.objects.all()
        if q:
            queryset = queryset.filter(name__icontains=q)
        if province_id:
            queryset = queryset.filter(province_id=province_id)
        serializer = CommuneOldSerializer(queryset, many=True)
        return Response(serializer.data)
# class CommuneOldSearch(generics.ListAPIView):
#     serializer_class = CommuneOldSerializer

#     def get_queryset(self):
#         q = self.request.query_params.get("q", "")
#         province_id = self.request.query_params.get("province", None)
#         queryset = CommuneOld.objects.all()
#         if q:
#             queryset = queryset.filter(name__icontains=q)
#         if province_id:
#             queryset = queryset.filter(province_id=province_id)
#         return queryset
        
# Xem quan hệ sáp nhập
class MergerList(APIView):
    def get(self, request):
        commune_id = request.query_params.get("commune", None)
        if commune_id:
            queryset = Merger.objects.filter(Q(old_commune_id=commune_id) | Q(new_commune_id=commune_id))
        else:
            queryset = Merger.objects.all()
        serializer = MergerSerializer(queryset, many=True)
        return Response(serializer.data)
# class MergerList(generics.ListAPIView):
#     serializer_class = MergerSerializer

#     def get_queryset(self):
#         commune_id = self.request.query_params.get("commune", None)
#         if commune_id:
#             return Merger.objects.filter(Q(old_commune_id=commune_id) | Q(new_commune_id=commune_id))
#         return Merger.objects.all()
    
'''
# Note: Các chế độ xem CommuneAlias và District không được bao gồm trong đoạn mã được cung cấp.
# Nếu cần, có thể thêm các lớp tương tự cho CommuneAlias và District.
class CommuneAliasList(APIView):
    def get(self, request):
        queryset = CommuneAlias.objects.all()
        serializer = CommuneAliasSerializer(queryset, many=True)
        return Response(serializer.data)
    
class DistrictList(APIView):
    def get(self, request):
        queryset = District.objects.all()
        serializer = DistrictSerializer(queryset, many=True)
        return Response(serializer.data)
# Note: Đảm bảo rằng các URL trong registry/urls.py được cập nhật để bao gồm các chế độ xem mới này nếu chúng được sử dụng.
'''
    

def search_view(request):
    provinces = Province.objects.all().order_by("name")
    q = (request.GET.get("q") or "").strip()
    province_id = (request.GET.get("province") or "").strip()

    results = []

    # --- Current communes (Mới → Cũ) ---
    current_qs = CommuneCurrent.objects.all().select_related("province")
    if province_id:
        current_qs = current_qs.filter(province_id=province_id)
    if q:
        current_qs = current_qs.filter(name__icontains=q)
    current_qs = current_qs.distinct().order_by("province__name", "name")

    for c in current_qs:
        merged_from = list(
            Merger.objects.filter(new_commune=c)
            .select_related("old_commune")
            .values_list("old_commune__name", flat=True)
        )
        results.append({
            "direction": "Mới → Cũ",
            "commune": c,
            "merged_from": merged_from,
            "merged_to": None,
        })

    # --- Old communes (Cũ → Mới) ---
    old_qs = CommuneOld.objects.all().select_related("province", "district")
    if province_id:
        old_qs = old_qs.filter(province_id=province_id)
    if q:
        old_qs = old_qs.filter(name__icontains=q)
    old_qs = old_qs.order_by("province__name", "name")

    for o in old_qs:
        merged_to = list(
            Merger.objects.filter(old_commune=o)
            .select_related("new_commune")
            .values_list("new_commune__name", flat=True)
        )
        results.append({
            "direction": "Cũ → Mới",
            "commune": o,
            "merged_from": None,
            "merged_to": merged_to,
        })

    return render(request, "registry/search.html", {
        "provinces": provinces,
        "selected_province": province_id,
        "query": q,
        "results": results,
    })