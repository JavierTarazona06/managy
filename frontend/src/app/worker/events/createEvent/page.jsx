'use client';

// as per Form.jsx
import { useState } from "react";
import api from "@/api.js";
import "@/styles/createEvent.css";
import LoadingIndicator from "@/components/LoadingIndicator.jsx";
import { withAuth } from "@/components/withAuth.jsx";

const api_createEvent = "/api/event/create/";

// defines a functional component named `CreateEvent`.
function CreateEvent() {
  const [eventName, setEventName] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [eventLocation, setEventLocation] = useState("");
  const [eventTime, setEventTime] = useState("");
  const [eventDescription, setEventDescription] = useState("");
  const [eventCapacity, setEventCapacity] = useState("");
  const [loading, setLoading] = useState(false);

  const createEvent = () => {

    let data1 = {
      "eventName": eventName,
      "eventDate": eventDate,
      "eventLocation": eventLocation,
      "eventTime": eventTime,
      "eventDescription": eventDescription,
      "eventCapacity": eventCapacity
    };
    console.log(data1);

    api
      .post(api_createEvent, data1)
      .then((res) => {
        if (res.status === 201) {
          alert("Event Created! With ID: " + res.data.id + "\nGo to view events");
          console.log(res.data);
        }
        else alert("Failed to make event.");
      })
      .catch((err) => alert(err));
  };

  // handles form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createEvent();
    } catch (error) {
      alert("Error creating event: " + error.message);
    } finally { // reset the loading state
      setLoading(false);
    }
  };

  return (
    <div className="bg-container">
      <form onSubmit={handleSubmit} className="form-container">
        <h1>Create New Event</h1>

        <input
          className="form-input"
          type="text"
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          placeholder="Event Name"
          required // input field must be filled out before the form can be submitted
        />

        <input
          className="form-input"
          type="date"
          value={eventDate}
          onChange={(e) => setEventDate(e.target.value)}
          required
        />

        <input
          className="form-input"
          type="time"
          value={eventTime}
          onChange={(e) => setEventTime(e.target.value)}
          required
        />

        <input
          className="form-input"
          type="text"
          value={eventLocation}
          onChange={(e) => setEventLocation(e.target.value)}
          placeholder="Event Location"
          required
        />

        <textarea
          className="form-input"
          value={eventDescription}
          onChange={(e) => setEventDescription(e.target.value)}
          placeholder="Event Description"
          required
        />

        <input
          className="form-input"
          type="number"
          value={eventCapacity}
          onChange={(e) => setEventCapacity(e.target.value)}
          placeholder="Event Capacity"
          required
          min="1"
        />
        {loading && < LoadingIndicator />}
        <button className="form-button" type="submit">
          Create Event
        </button>
      </form>
    </div>
  );
}

export default withAuth(CreateEvent, ["worker", "admin"]);
