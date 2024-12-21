"use client";

import React, { useState } from "react";
import api from "@/api";

const deleteBookingPath = "api/amenity/booking/cancel/";
const viewBookingPath = "api/amenity/booking/view/";

const CancelBooking = () => {
    console.log("CancelBooking component loaded");

    const [bookingID, setBookingID] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [feedbackMessage, setFeedbackMessage] = useState("");
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(false);

    //fetch bookings
    const fetchBookings = async () => {
        setLoading(true);
        try {
            const response = await api.get(viewBookingPath);
            setBookings(response.data);
            setFeedbackMessage("");
        } catch (error) {
            console.error("Error fetching bookings:", error);
            setFeedbackMessage("Failed to load bookings. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    //call API to delete booking
    const handleDelBooking = () => {
        return new Promise((resolve, reject) => {
            api
                .delete(deleteBookingPath + `${bookingID}/`)
                .then((res) => {
                    if (res.status === 204) {
                        alert("Booking cancelled successfully.");
                        setBookings((prev) =>
                            prev.filter((booking) => booking.id !== parseInt(bookingID))
                        );
                        resolve(true); // Resolve promise if the deletion is successful
                    } else {
                        alert("Failed to cancel booking.");
                        resolve(false); // Resolve with false if the deletion fails
                    }
                })
                .catch((error) => {
                    alert(error.response.data.error)
                    console.error("Error cancelling booking:", error);
                    setFeedbackMessage("An error occurred. Please try again.");
                    reject(error); // Reject the promise if there's an error
                });
        });
    };

    const handleCancelBooking = async () => {
        console.log("Cancel Button Clicked.");

        if (!bookingID) {
            setFeedbackMessage("Please enter a valid booking ID.");
            return;
        }

        try {
            const isDeleted = await handleDelBooking();
            if (isDeleted) {
                setFeedbackMessage("Booking cancelled successfully.");
            } else {
                setFeedbackMessage("Something went wrong. Please try again.");
            }
        } catch (error) {
            setFeedbackMessage("An error occurred. Please try again later.");
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 text-center font-sans p-6">
            {/* Logo */}
            <img
                src="/images/house.png"
                alt="Logo"
                className="w-24 mx-auto mb-6"
            />

            {/* Page Title */}
            <h1 className="text-gray-800 text-2xl font-bold mb-4">Cancel Booking</h1>

            {/*fetch and display bookings */}
            <button
                onClick={fetchBookings}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition mb-4"
            >
                Load Bookings
            </button>

            <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
                {!showForm ? (
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition"
                    >
                        Start Cancellation
                    </button>
                ) : (
                    <>
                        <input
                            type="text"
                            placeholder="Enter Booking ID"
                            value={bookingID}
                            onChange={(e) => setBookingID(e.target.value)}
                            className="block w-full px-4 py-2 mb-4 border border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
                        />
                        <button
                            onClick={handleCancelBooking}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition"
                        >
                            Submit
                        </button>

                        {feedbackMessage && (
                            <p
                                className={`mt-4 ${
                                    feedbackMessage.includes("successfully")
                                        ? "text-green-500"
                                        : "text-red-500"
                                }`}
                            >
                                {feedbackMessage}
                            </p>
                        )}
                    </>
                )}
            </div>

            {/* Display bookings */}
            {loading ? (
                <p>Loading bookings...</p>
            ) : (
                <div className="mt-6">
                    {bookings.length > 0 ? (
                        bookings.map((booking) => (
                            <div
                                key={booking.id}
                                className="booking-item bg-white p-4 mb-4 rounded shadow text-gray-800"
                            >
                                <p>
                                    <strong>Booking Name:</strong> {booking.amenity_name}
                                </p>
                                <p>
                                    <strong>Booking Date:</strong> {booking.date}
                                </p>
                                <p>
                                    <strong>Time:</strong> {booking.time}
                                </p>
                                <p>
                                    <strong>Capacity:</strong> {booking.amenity_capacity}
                                </p>
                                <p>
                                    <strong>ID:</strong> {booking.id}
                                </p>
                            </div>
                        ))
                    ) : (
                        <p>No bookings available to display.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default CancelBooking;
