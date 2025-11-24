# jobs/views.py
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Job
from .forms import JobApplicationForm

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    
    # Filtering options
    job_type = request.GET.get('job_type')
    department = request.GET.get('department')
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if department:
        jobs = jobs.filter(department__icontains=department)
    
    context = {
        'jobs': jobs,
        'job_types': Job.JOB_TYPES,
        'departments': Job.objects.filter(is_active=True).values_list('department', flat=True).distinct(),
    }
    return render(request, './jobs/job_list.html', context)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the application without saving to database
            application_data = form.cleaned_data
            resume_file = request.FILES['resume']
            
            # Send email to admin
            send_application_email(job, application_data, resume_file)
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    return render(request, './jobs/job_detail.html', context)

def send_application_email(job, application_data, resume_file):
    """Send application details to admin via email"""
    
    # Email subject
    subject = f"New Job Application: {job.title} - {application_data['name']}"
    
    # Email body (HTML)
    context = {
        'job': job,
        'application': application_data,
        'submission_date': timezone.now(),
    }
    
    html_message = render_to_string('./jobs/email/application_notification.html', context)
    text_message = render_to_string('./jobs/email/application_notification.txt', context)
    
    # Create email
    email = EmailMessage(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
        reply_to=[application_data['email']],
    )
    
    # Attach HTML version
    email.content_subtype = "html"
    email.body = html_message
    
    # Attach resume
    email.attach(resume_file.name, resume_file.read(), resume_file.content_type)
    
    # Send email
    email.send()

def application_success(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, './jobs/application_success.html', {'job': job})