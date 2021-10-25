"""coins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from wallet import views

schema_view = get_swagger_view(title='Coins Wallet API')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^apidocs/$', schema_view),
    url(r'^accounts/$', views.AccountsView.as_view(), name="all_accounts"),
    url(r'^accounts/(?P<account_id>\w+)$', views.AccountsView.as_view(), name="single_account"),
    url(r'^transactions/(?P<wallet_id>\w+)', views.TransactionsView.as_view(), name="transaction_summary"),
]
