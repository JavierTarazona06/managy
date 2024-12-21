'use client'

import {useEffect, useState} from 'react'
import Image from 'next/image'
import DatePicker from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"
import { withAuth } from "@/components/withAuth"
import api from '@/api.js'
import LoadingIndicator from "@/components/LoadingIndicator"
import { navigate } from "@/components/actions"

// Define API endpoints
const api_sort = "/api/event/get_event/"
const api_eventName = "/api/event/get_event_name/"
const api_eventdate = "/api/event/filter_event_date/"

function MemberEvents() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchName, setSearchName] = useState('')
  const [startDate, setStartDate] = useState(null)
  const [endDate, setEndDate] = useState(null)

  useEffect(() => {
    const getEventsFirst = async () => {
      setLoading(true)
      try {
        const response = await api.get(api_sort + `1/`)
        setEvents(response.data)
      } catch (err) {
        setError('Error fetching amenities: ' + err.message)
      } finally {
        setLoading(false)
      }
    }

    getEventsFirst()
  }, [])

  const fetchEvents = async (sortOrder) => {
    setLoading(true)
    try {
      const response = await api.get(api_sort + `${sortOrder}/`)
      setEvents(response.data)
    } catch (err) {
      setError('There was an error fetching events: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const searchEventByName = async () => {
    setLoading(true)
    try {
      const response = await api.get(api_eventName + `${searchName}/`)
      setEvents(response.data)
    } catch (err) {
      setError('There was an error searching events: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const filterEventsByDate = async () => {
    if (!startDate || !endDate) {
      alert('Please select a start and end date')
      return
    }
    setLoading(true)
    try {
      const d1 = startDate.toISOString().split("T")[0]
      const d2 = endDate.toISOString().split("T")[0]
      const response = await api.get(api_eventdate + `${d1}/${d2}/`)
      setEvents(response.data)
    } catch (err) {
      setError('There was an error filtering events: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRegistration = () => {
    navigate("/member/events/createRegistration");
  };

  const handleCancelRegistration = () => {
    navigate("/member/events/cancelRegistration");
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
        <h1 className="text-5xl font-bold text-center">Member Events</h1>

        <div className="w-full max-w-4xl space-y-8">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Search by Name</h2>
            <div className="flex">
              <input
                type="text"
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                placeholder="Enter event name"
                className="flex-grow p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <button
                onClick={searchEventByName}
                className="px-4 py-2 bg-orange-100 text-black font-bold rounded-r-md hover:bg-orange-900 hover:text-white transition duration-300"
              >
                Search
              </button>
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Filter by Date Range</h2>
            <div className="flex space-x-4 mb-4">
              <DatePicker
                selected={startDate}
                onChange={date => setStartDate(date)}
                selectsStart
                startDate={startDate}
                endDate={endDate}
                placeholderText="Start Date"
                className="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <DatePicker
                selected={endDate}
                onChange={date => setEndDate(date)}
                selectsEnd
                startDate={startDate}
                endDate={endDate}
                minDate={startDate}
                placeholderText="End Date"
                className="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <button
              onClick={filterEventsByDate}
              className="w-full px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
            >
              Apply Date Filter
            </button>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Sort Events</h2>
            <div className="flex space-x-4">
              <button
                onClick={() => fetchEvents(0)}
                className="flex-1 px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
              >
                Random
              </button>
              <button
                onClick={() => fetchEvents(1)}
                className="flex-1 px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
              >
                Ascending Date
              </button>
              <button
                onClick={() => fetchEvents(2)}
                className="flex-1 px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
              >
                Descending Date
              </button>
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Events</h2>
            {loading ? (
              <LoadingIndicator />
            ) : error ? (
              <p className="text-center text-red-500">{error}</p>
            ) : events.length === 0 ? (
              <p className="text-center text-gray-600">There are no events that match the criteria.</p>
            ) : (
              <>
                <ul className="space-y-4 mb-8">
                  {events.map((event) => (
                      <li key={event.id} className="bg-orange-100 p-4 rounded-md shadow">
                        <h3 className="text-xl font-semibold">{event.eventName}</h3>
                        <p className="text-gray-600">Date: {new Date(event.eventDate).toISOString().split('T')[0]}</p>
                        <p className="mt-2">ID: {event.id}</p>
                        <p className="mt-2">{event.eventDescription}</p>
                        <p className="mt-2">{event.eventTime}</p>
                        <p className="mt-2">{event.eventLocation}</p>
                      </li>
                  ))}
                </ul>
                <div className="flex justify-center space-x-4">
                  <button
                    onClick={handleCreateRegistration}
                    className="px-6 py-3 bg-green-500 text-white font-bold rounded-md hover:bg-green-700 transition duration-300"
                  >
                    Create Registration
                  </button>
                  <button
                    onClick={handleCancelRegistration}
                    className="px-6 py-3 bg-red-500 text-white font-bold rounded-md hover:bg-red-700 transition duration-300"
                  >
                    Cancel Registration
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default withAuth(MemberEvents, ["member", "admin"])
