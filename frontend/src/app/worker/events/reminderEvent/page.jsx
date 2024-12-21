'use client'

import { useState, useEffect } from 'react';
import api from '@/api.js';
import Image from 'next/image';
import { withAuth } from "@/components/withAuth";

function EventReminder({ eventId }) {
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEventDetails = async () => {
      setLoading(true);
      try {
        const response = await api.get(`/api/event/${eventId}`);
        if (response.status === 200) {
          setEvent(response.data);
        } else {
          setError('Failed to fetch event details');
        }
      } catch (err) {
        setError('There was an error fetching event details: ' + err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchEventDetails();
  }, [eventId]);

  const formatDateTime = (dateTimeString) => {
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateTimeString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="min-h-screen flex flex-col bg-white text-black">
      <main className="flex-grow flex flex-col items-center justify-start p-4 space-y-8 overflow-y-auto">
        <Image
          src="/images/house.png"
          alt="Logo"
          width={200}
          height={200}
          priority
        />
        <h1 className="text-5xl font-bold text-center">Event Reminder</h1>

        {loading ? (
          <p className="text-center">Loading event details...</p>
        ) : error ? (
          <p className="text-center text-red-500">{error}</p>
        ) : event ? (
          <div className="w-full max-w-2xl bg-orange-100 p-8 rounded-lg shadow-lg">
            <h2 className="text-3xl font-semibold mb-4">{event.name}</h2>
            <p className="text-xl mb-2">
              <strong>Time:</strong> {formatDateTime(event.time)}
            </p>
            <p className="text-xl mb-2">
              <strong>Day:</strong> {new Date(event.day).toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
            <p className="text-xl mb-4">
              <strong>Location:</strong> {event.location}
            </p>
            <p className="text-lg">
              <strong>Description:</strong> {event.description}
            </p>
          </div>
        ) : (
          <p className="text-center text-gray-600">No event details found.</p>
        )}
      </main>
    </div>
  );
}

export default withAuth(EventReminder, ["worker", "admin"]);
