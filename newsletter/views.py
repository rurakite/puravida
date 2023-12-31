from django.shortcuts import render, redirect
from . forms import SubscibersForm, MailMessageForm
from . models import Subscribers
from django.contrib import messages
from django.core.mail import send_mail
from django_pandas.io import read_frame
from .decorators import user_is_superuser
from django.template.loader import render_to_string


def subscribe(request):
    if request.method == 'POST':
        form = SubscibersForm(request.POST)
        email = request.POST.get('email', None)
        if form.is_valid():
            # Check if the user is already subscribed
            subscribe_user = Subscribers.objects.filter(
                email=email).first()
            if subscribe_user:
                messages.warning(
                    request, f"{email} email address is already subscribed.")
                return redirect(request.META.get("HTTP_REFERER", "/"))

            form.save()

            # Send a welcome email to the new subscriber
            subject = 'Welcome to Our Newsletter'
            message = render_to_string(
                'newsletter/coupone.txt', {'email': email})
            send_mail(subject, message, '', [email], fail_silently=False)

            messages.success(
                request, f'{email} email was successfully subscribed\
                    to our newsletter!')
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = SubscibersForm()

    context = {
        'form': form,
    }
    return render(request, 'newsletter/newsletter.html', context)


@user_is_superuser
def mail_letter(request):
    emails = Subscribers.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            send_mail(
                title,
                message,
                '',
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Message has been sent to the Mail List')
            return redirect('mail-letter')
    else:
        form = MailMessageForm()
    context = {
        'form': form,
    }
    return render(request, 'newsletter/mail_letter.html', context)
