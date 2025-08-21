from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class Province(models.Model):
    TYPE_CHOICES = ( ('Tỉnh', 'Tỉnh'), ('Thành phố', 'Thành phố'))
    province_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Tỉnh')
    def __str__(self):
        return self.name


class District(models.Model):
    TYPE_CHOICES = (('Thị xã', 'Thị xã'), ('Huyện', 'Huyện'), ('Quận', 'Quận'), ('Thành phố', 'Thành phố'))
    district_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Huyện')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    #on_delete=models.CASCADE đảm bảo rằng nếu một tỉnh bị xóa, tất cả các quận của tỉnh đó cũng bị xóa
    #related_name='districts' cho phép truy cập các quận của tỉnh thông qua thuộc tính 'districts' của đối tượng Province
    
    def __str__(self):
        return self.name

    
class CommuneCurrent(models.Model):
    TYPE_CHOICES = (
        ('Xã', 'Xã'),
        ('Phường', 'Phường'),
        ('Thị trấn', 'Thị trấn'),
    )
    commune_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Xã')
    # Chỉ trực thuộc tỉnh (vì bỏ cấp huyện rồi)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='communes')

    def __str__(self):
        return f"{self.name}, {self.province.name}"


class CommuneOld(models.Model):
    TYPE_CHOICES = (
        ('Xã', 'Xã'),
        ('Phường', 'Phường'),
        ('Thị trấn', 'Thị trấn'),
    )
    old_commune_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Xã')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='old_communes')
    district = ChainedForeignKey(
        District,
        chained_field="province",          # field trong model này
        chained_model_field="province",    # field trong model District
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        related_name='old_communes'
    )

    def __str__(self):
        return f"{self.name}, {self.district.name}, {self.province.name}" 
    
class Merger(models.Model):
    old_commune = models.ForeignKey(CommuneOld, on_delete=models.CASCADE, related_name='mergers')
    new_commune = models.ForeignKey(CommuneCurrent, on_delete=models.CASCADE, related_name='mergers')
    date = models.DateField()

    def __str__(self):
        return f"{self.old_commune.name} -> {self.new_commune.name} on {self.date}"
    
    class Meta:
        unique_together = ('old_commune', 'new_commune')
    
    
# class CommuneAlias(models.Model):
#     commune = models.ForeignKey(CommuneCurrent, on_delete=models.CASCADE, related_name='aliases')
#     alias = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.commune.name} alias: {self.alias}"
    
#     class Meta:
#         unique_together = ('commune', 'alias')  # Ensure no duplicate aliases for the same commune