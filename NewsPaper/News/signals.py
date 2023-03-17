from django.db.models.signals import post_save, m2m_changed
from django.template.loader import render_to_string
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscribers, PostCategory


@receiver(m2m_changed, sender=Post.category.through)
def notify_appointment(sender, instance, pk_set, **kwargs):
    email_list = []
    subject = f'{instance.author} {instance.timestamp}'
    for cat in pk_set:
        subs_usr = Subscribers.objects.filter(category=cat).values_list('user__email', flat=True)

    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{subject}',
        body=instance.text,  # сообщение с кратким описанием
        from_email='vm.obukhov@yandex.ru',  # здесь указываете почту, с которой будете отправлять
        to=list(subs_usr),
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()
