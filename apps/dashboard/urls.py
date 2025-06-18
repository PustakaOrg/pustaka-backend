from django.urls import path

from apps.dashboard.views import (
    get_home_data,
)


urlpatterns = [
    path("dashboard/home/", get_home_data, name="dashboard-home"),
    # path("dashboard/loan/", get_loan_data, name="dashboard-loan"),
    # path("dashboard/reservation/", get_reservation_data, name="dashboard-reservation"),
    # path("dashboard/fine/", get_fines_data, name="dashboard-fine"),
]
