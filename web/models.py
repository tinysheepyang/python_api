from django.db import models

# Create your models here.

class feedback(models.Model):
    email = models.CharField(max_length=50, verbose_name='反馈用户邮箱')
    subject = models.CharField(max_length=200, verbose_name='反馈主题')
    message = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-createTime']
        db_table = 'feedback'

    def __str__(self):
        return '{}'.format(self.email)