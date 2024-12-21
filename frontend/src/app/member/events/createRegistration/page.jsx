'use client'
import api from '@/api.js';
import { useState, useEffect } from 'react';
import EventPanel from '@/components/EventPanel';
import Image from 'next/image';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import MemberHeader from '@/components/MemberHeader';
import { withAuth } from "@/components/withAuth";
import { navigate } from '@/components/actions';

//const api_register_event = "/api/event/selection/register/"
const api_register_event = "/api/event/selection/create/"
const api_sort = "/api/event/get_event/";
const api_eventName = "/api/event/get_event_name/"
const api_eventdate = "/api/event/filter_event_date/"

const CreateBooking = () => {

  const [events, setEvents] = useState([]);   // Holds the events

  const [sortOrder, setSortOrder] = useState(0);  // 0 = Random, 1 = Ascending, 2 = Descending
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchName, setSearchName] = useState('');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleDateSelect = (date) => {
    if (!startDate || (startDate && endDate)) {
      setStartDate(date);
      setEndDate(null);
    } else if (startDate && !endDate && date > startDate) {
      setEndDate(date);
    }
  };

  const [showEditForm, setShowEditForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const closeRegisterForm = () => {
    setSelectedUser(null);
    setShowEditForm(false);
  };

  const openEditForm = (event) => {
    setSelectedUser(event);
    setShowEditForm(true);
  };

  const getEventsSort = () => {
    console.log("Sort order: " + sortOrder);
    api
      .get(api_sort + `${sortOrder}/`)
      .then((res) => res.data)
      .then((data) => {
        setEvents(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  // Be able to display all events (sorted or not)
  const fetchEvents = async () => {
    setLoading(true);

    try {
      await getEventsSort();
    } catch (err) {
      setError('There was an error fetching events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const registerEvent = (id) => {
    const data1 = {
      eventRef: id
    }
    api
      .post(api_register_event, data1)
      .then((res) => {
        console.log(res.data)
        if (res.status === 201) alert("Registed for event with ID " + res.data.id);
        else alert("Failed to register for event. Http error:" + res.status);
      })
      .catch((error) => alert(error.response.data.error));
  };

  // 1
  // Fetch events when the sort order changes
  useEffect(() => {
    fetchEvents();
  }, [sortOrder]);

  // 2
  // Display events with keyword typed or searched by user

  const getEventsName = () => {
    console.log("Search Name: " + searchName);
    api
      .get(api_eventName + `${searchName}/`)
      .then((res) => res.data)
      .then((data) => {
        setEvents(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const searchEventByName = async () => {
    setLoading(true);
    try {
      await getEventsName();
    } catch (err) {
      setError('There was an error fetching events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 3
  // allows user to select a start and end date range to display events in that range
  const getEventsDate = () => {
    let d1 = startDate.toISOString();
    d1 = d1.split("T")[0];
    let d2 = endDate.toISOString();
    d2 = d2.split("T")[0];

    console.log("Dates: " + d1 + " - " + d2);
    api
      .get(api_eventdate + `${d1}/${d2}/`)
      .then((res) => res.data)
      .then((data) => {
        setEvents(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const filterEventsByDate = async () => {
    if (!startDate || !endDate) {
      alert('Please select a start and end date');
      return;
    }
    setLoading(true);
    try {
      await getEventsDate();
    } catch (err) {
      setError('There was an error fetching events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-white text-black">
      <MemberHeader />
      <h2 className="text-2xl font-semibold mt-4 text-center">Events</h2>

      <div className="border-8 bg-orange-200 border-black rounded p-4 m-4">

        {events.length > 0 ? (
          events.map((event) => (
            <div key={event.id} className='flex justify-center'>
              <EventPanel event={event} onDeleteClick={() => openEditForm(event)} />
            </div>
          ))
        ) : (
          <p className="text-center text-black font-bold">No events in the system</p>
        )}
      </div>
      {showEditForm && selectedUser && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-orange-200 p-6 rounded shadow-lg w-80 text-center border-black border-4">
            <h3 className="text-xl font-bold mb-4">Do you want to register for {selectedUser.eventName}?</h3>
            <div className="flex space-x-4 mt-4">
              <button
                type="button"
                className="w-full bg-blue-500 text-white p-2 rounded-3xl hover:bg-blue-600 shadow-xl"
                onClick={() => {
                  closeRegisterForm()
                  registerEvent(selectedUser.id)

                }}
              >
                Register
              </button>

              <button
                type="button"
                className="w-full bg-gray-500 text-white p-2 rounded-3xl hover:bg-gray-600 shadow-xl"
                onClick={closeRegisterForm}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}

export default withAuth(CreateBooking, ['member', 'admin'])

