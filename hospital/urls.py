

from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("<int:id>",views.show,name="show_hospital"),
    path("opd_queue/<int:hospital_id>",views.opd_queue,name="opd_queue"),
    path("join_opd_queue/<int:hospital_id>",views.join_opd_queue,name="join_opd_queue"),
    path("book_appointment/",views.book_appointment,name="book_appointment"),
    path("logout",views.logout_user,name="logout"),
    path("register",views.register,name="register_user"),
    path("login",views.user_login,name="login_user")
]
