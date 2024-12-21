"use client";

import CancelBooking from "@/components/cancelBooking";
import { useEffect, useState } from "react";
import LoadingIndicator from "@/components/LoadingIndicator";
import api from "@/api";
import { withAuth } from "@/components/withAuth";

const get_booking_amenities = "/api/amenity/booking/view/";

function Page() {

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await api.get(get_booking_amenities);
                console.log(response.data);
            } catch (err) {
                alert("Error fetching bookings: ", err.response?.data?.error || err.message);
            }
        };

        fetchBookings();
    }, []);

    return (
        <div className="w-full px-4 bg-white">
            {/* Cancel Booking Section */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                <CancelBooking/>
            </div>
        </div>
    );
}

export default withAuth(Page, ["member", "admin"]);
