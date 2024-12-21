"use client";

import { withAuth } from "@/components/withAuth.jsx";
import { navigate } from "@/components/actions";
import '@/styles/welcome.css';

function WelcomePage() {
  const handleEvent = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/events");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleAmenities = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/amenities");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="welcome-container">
      <div className="bg-black bg-opacity-90 rounded-lg p-10 shadow-md flex flex-col items-center justify-center">
        <h1 className="welcome-title">Welcome to Managy</h1>
        <h1 className="welcome-text">Worker View</h1>
        <p className="welcome-text">Choose a section to continue:</p>
        <div className="button-container">
          <button
            onClick={handleEvent}
            className="welcome-button"
          >
            <span className="text-lg">Go to Events</span>
          </button>
          <button
            onClick={handleAmenities}
            className="welcome-button"
          >
            <span className="text-lg">Go to Amenities</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default withAuth(WelcomePage, ["worker", "admin"]);
