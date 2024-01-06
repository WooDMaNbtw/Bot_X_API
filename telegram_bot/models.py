from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=120)
    balance = models.FloatField(blank=True, null=True)
    tariff = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} | {self.email} | {self.created_at}"

    class Meta:
        ordering = ["id"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    max_value = models.IntegerField()
    min_value = models.IntegerField()

    def __str__(self):
        return f"{self.user} | {self.type} | {self.name}"

    class Meta:
        ordering = ["user_id"]
        verbose_name = "UserStatistic"
        verbose_name_plural = "UserStatistics"
