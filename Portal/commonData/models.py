from django.db import models

# Create your models here.

class Subscription(models.Model):
    """ Subscripstion Plans """
    PLAN_RANGE = (
        ('M', 'Monthly'),
    )

    plan_name = models.CharField(
        max_length=100, null=True, help_text="plan name")
    plan_range = models.CharField(default=PLAN_RANGE[0][0],choices=PLAN_RANGE, blank=True, null=True, max_length=100, help_text="M=Monthly")
    amount = models.FloatField(default=0, blank=True, null=True)
    is_deleted = models.BooleanField(
        default=False, help_text="activate/deactivate plan")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.pk, self.plan_name, self.amount)

    class Meta:
        verbose_name_plural = "Subscription"
        db_table = 'subscription'