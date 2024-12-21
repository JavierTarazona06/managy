"use client";

import React, { useState } from "react";
import api from "@/api";

const deleteRegPath = "api/event/selection/register/cancel/";

const CancelRegistration = () => {
    console.log("CancelRegistration component loaded");

    const [registrationID, setRegistrationID] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [feedbackMessage, setFeedbackMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [couldDelete, setCouldDelete] = useState(false);

    // Modify handleDelReg to return a promise
    const handleDelReg = () => {
        return new Promise((resolve, reject) => {
            api
                .delete(deleteRegPath + `${registrationID}/`)
                .then((res) => {
                    console.log(res.data);
                    if (res.status === 204) {
                        alert("Event Selection deleted!\n" + res.data.message);
                        window.location.reload();
                        setCouldDelete(true);
                        resolve(true); // Resolve the promise if deletion is successful
                    } else {
                        alert("Failed to delete event selection.");
                        window.location.reload();
                        setCouldDelete(false);
                        resolve(false); // Resolve with false if deletion fails
                    }
                })
                .catch((error) => {
                    alert(error.response.data.error);
                    window.location.reload();
                    setFeedbackMessage(error.response.data.error);
                    reject(error); // Reject the promise if there's an error
                })
                .finally(() => {
                    window.location.reload();
                });
        });
    };

    const handleCancelRegistration = async () => {
        console.log("Cancel Button Clicked");

        if (!registrationID) {
            setFeedbackMessage("Please enter a valid registration ID.");
            return;
        }

        try {
            // Wait for handleDelReg to complete
            const isDeleted = await handleDelReg();

            if (isDeleted) {
                setFeedbackMessage("Registration cancelled successfully.");
            } else {
                setFeedbackMessage("Something went wrong. Please try again.");
                alert("Invalid ID");
                window.location.reload();
            }
            setCouldDelete(false);
            window.location.reload();
        } catch (error) {
            console.error("API Call Failed", error);
            setFeedbackMessage("An error occurred while cancelling your booking. Please try again.");
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
            <h1 className="text-gray-800 text-2xl font-bold mb-4">Cancel Registration</h1>

            {/* Cancel Registration Form */}
            <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
                {!showForm ? (
                    <button
                        onClick={() => {
                            console.log("Show Form Button Clicked");
                            setShowForm(true);
                        }}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition"
                    >
                        Start Cancellation
                    </button>
                ) : (
                    <>
                        <input
                            type="text"
                            placeholder="Enter Registration ID"
                            value={registrationID}
                            onChange={(e) => setRegistrationID(e.target.value)}
                            className="block w-full px-4 py-2 mb-4 border border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
                        />
                        <button
                            onClick={handleCancelRegistration}
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
        </div>
    );
};

export default CancelRegistration;
