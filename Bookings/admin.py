from django.contrib import admin
from django.db import connection
from django.db.models import Sum
from .models import *

admin.site.register(City)
admin.site.register(Route)
admin.site.register(Flight)
#admin.site.register(Booking)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["booking_ref", "created_at", "passenger", "flight", "total_cost"]
    date_hierarchy = "created_at"
    change_list_template = "admin/bookings/booking_changelist.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if not hasattr(response, "context_data"):
            return response

        baggage_price = Booking.BAGGAGE_UNIT_PRICE
        terminal_fee = Booking.TERMINAL_FEE_PRICE
        insurance_price = Booking.INSURANCE_PRICE

        # ---------- REVENUE BY MONTH  ----------
        # group by created_at, YYYY-MM
        monthly_revenue = []
        sql_month = """
            SELECT
                substr(b.created_at, 1, 7) AS month,  -- 'YYYY-MM'
                SUM(
                    f.base_fare
                    + b.baggage_allowance_qty * %s
                    + %s
                    + CASE WHEN b.travel_insurance = 1 THEN %s ELSE 0 END
                ) AS total_revenue,
                COUNT(*) AS bookings_count
            FROM Bookings_booking b
            JOIN Bookings_flight f
                ON b.flight_id = f.id
            GROUP BY month
            ORDER BY month;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_month, [baggage_price, terminal_fee, insurance_price])
            rows = cursor.fetchall()

        for month, total_rev, count in rows:
            monthly_revenue.append(
                {
                    "month": month,
                    "total_revenue": total_rev or 0,
                    "bookings_count": count,
                }
            )

        # ---------- REVENUE BY ROUTE ----------
        route_revenue = []
        sql_route = """
            SELECT
                o.city AS origin_city,
                d.city AS destination_city,
                SUM(
                    f.base_fare
                    + b.baggage_allowance_qty * %s
                    + %s
                    + CASE WHEN b.travel_insurance = 1 THEN %s ELSE 0 END
                ) AS total_revenue,
                COUNT(*) AS bookings_count
            FROM Bookings_booking b
            JOIN Bookings_flight f
                ON b.flight_id = f.id
            JOIN Bookings_route r
                ON f.route_id = r.id
            JOIN Bookings_city o
                ON r.origin_id = o.id
            JOIN Bookings_city d
                ON r.destination_id = d.id
            GROUP BY origin_city, destination_city
            ORDER BY total_revenue DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_route, [baggage_price, terminal_fee, insurance_price])
            rows = cursor.fetchall()

        for origin_city, dest_city, total_rev, count in rows:
            route_revenue.append(
                {
                    "origin_city": origin_city,
                    "destination_city": dest_city,
                    "total_revenue": total_rev or 0,
                    "bookings_count": count,
                }
            )

        extra_context = extra_context or {}
        extra_context.update(
            {
                "monthly_revenue": monthly_revenue,
                "route_revenue": route_revenue,
            }
        )
        response.context_data.update(extra_context)
        return response

