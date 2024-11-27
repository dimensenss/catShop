from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_to_topic

@receiver(pre_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous_status = sender.objects.get(pk=instance.pk).status
        if previous_status != instance.status:
            if instance.status == 'Скасовано':
                send_to_topic.delay('canceled_orders', {
                    'order_id': instance.pk,
                    'reason': 'Updated manually in admin',
                    'lost_revenue': 0
                })
            elif instance.status in ['Відправлено', 'Доставлено']:
                send_to_topic.delay('confirmed_orders', {
                    'order_id': instance.pk,
                    'new_status': instance.status,
                    'user': instance.user.get_full_name() if instance.user else "Гість"
                })
