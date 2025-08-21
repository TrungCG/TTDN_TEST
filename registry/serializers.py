from rest_framework import serializers
from .models import CommuneCurrent, CommuneOld, Merger, Province, District


class CommuneCurrentSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()  # sẽ gọi __str__() của Province
    class Meta:
        model = CommuneCurrent
        fields = '__all__'
        
class CommuneOldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuneOld
        fields = '__all__'
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField() 
        
class MergerSerializer(serializers.ModelSerializer):
    new_commune = serializers.StringRelatedField()
    old_commune = serializers.StringRelatedField() 
    class Meta:
        model = Merger
        fields = '__all__'
        
# class CommuneAliasSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommuneAlias
#         fields = '__all__'
        
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
        
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'