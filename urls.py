"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from services import BotList, BotDetail, Register, Login, Logout, EmailVerificationCheck, EmailVerificationResend, EmailVerificationVerify
from django.urls import path
from django.contrib import admin
from services.base import MessageBase, DialogueBase, DialogueIdBase
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/users/", Register.Register().as_view()),
    path("api/v0/users/login/", Login.Login().as_view()),
    path("api/v0/users/logout/", Logout.Logout().as_view()),
    path("api/v0/users/email-verification/check/", EmailVerificationCheck.EmailVerificationCheck().as_view()),
    path("api/v0/users/email-verification/resend/", EmailVerificationResend.EmailVerificationResend().as_view()),
    path("api/v0/users/email-verification/verify/", EmailVerificationVerify.EmailVerificationVerify().as_view()),
    path("api/v0/bots/", BotList.BotList().as_view()),
    path("api/v0/bots/<int:bot_id>/", BotDetail.BotDetail().as_view()),
    path("api/v0/dialogues/", DialogueBase.DialogueBase().as_view()),
    path("api/v0/dialogues/<int:dialogue_id>/", DialogueIdBase.DialogueIdBase().as_view()),
    path("api/v0/dialogues/<int:dialogue_id>/messages/", MessageBase.MessageBase.as_view()),
]
