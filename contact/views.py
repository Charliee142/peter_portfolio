import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .forms import ContactForm

logger = logging.getLogger('portfolio')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = request.META.get('REMOTE_ADDR')
            msg.save()
            try:
                send_mail(
                    subject=f'[Portfolio] {msg.subject}',
                    message=f'From: {msg.full_name} <{msg.email}>\n\n{msg.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f'Email send failed: {e}')
            if request.htmx:
                return render(request, 'contact/partials/success.html')
            messages.success(request, 'Message sent! I will get back to you shortly.')
            return redirect('contact:contact')
        else:
            if request.htmx:
                return render(request, 'contact/partials/form.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
