

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
    path("login",views.user_login,name="login_user"),
    path("submit_feedback",views.submit_feedback,name="submit_feedback"),
    path("opd_queue_update/<int:hospital_id>",views.opd_queue_update,name="opd_queue_update"),
    path("serve_next_opd/<int:hospital_id>",views.serve_next_opd,name="serve_next_opd"),
    path("schedule_later/<int:queue_id>",views.schedule_later,name="schedule_later"),
    path("generate_prescription/<int:queue_id>",views.generate_prescription,name="generate_prescription"),
    path("doctor_dashboard",views.doctor_dashboard,name="doctor_dashboard"),
    path("departments",views.department_list,name="departments"),
    path("department/<int:department_id>",views.department_detail,name="department_detail"),
]
