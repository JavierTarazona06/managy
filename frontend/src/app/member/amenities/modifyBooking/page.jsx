'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { withAuth } from "@/components/withAuth"
import api from '@/api.js'
import LoadingIndicator from "@/components/LoadingIndicator"
import DatePicker from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"

const api_viewBookings = "/api/amenity/booking/view"

function ModifyBooking() {
    const [bookings, setBookings] = useState([])
    const [selectedBooking, setSelectedBooking] = useState(null)
    const [newDate, setNewDate] = useState(null)
    const [newTime, setNewTime] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [minDate, setMinDate] = useState(new Date())

    const fetchBookings = async () => {
        setLoading(true)
        try {
            const response = await api.get(api_viewBookings)
            setBookings(response.data)
            setError(null)
        } catch (err) {
            setError('Error fetching bookings: ' + err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleSelectBooking = (booking) => {
        setSelectedBooking(booking)
        setNewDate(new Date(booking.date))
        setNewTime(booking.time.split(':')[0])
    }

    const handleUpdateBooking = async () => {
        if (!selectedBooking || !newDate || !newTime) {
            alert('Please select a booking and provide a new date and time')
            return
        }

        setLoading(true)
        try {
            const formattedTime = `${newTime}:00`

            const payload = {
                time: formattedTime,
                date: newDate.toISOString().split('T')[0],
                amenity_details: selectedBooking.amenity_details || '',
                amenity_capacity: selectedBooking.amenity_capacity
            }

            console.log('Request payload:', payload)

            const response = await api.put(`/api/amenity/booking/update/${selectedBooking.id}/`, payload)

            console.log('Update response:', response.data)

            alert('Booking updated successfully')
            await fetchBookings()
            setSelectedBooking(null)
            setNewDate(null)
            setNewTime('')
        } catch (err) {
            console.error('Error details:', {
                message: err.message,
                name: err.name,
                response: err.response?.data,
                requestPayload: err.config?.data
            })
            setError('Error updating booking: ' + (err.response?.data?.message || err.message))
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date()
            if (now.getHours() === 0 && now.getMinutes() === 0 && now.getSeconds() === 0) {
                setMinDate(now)
            }
        }, 1000)
        return () => clearInterval(timer)
    }, [])

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
                <h1 className="text-5xl font-bold text-center">Modify Booking</h1>

                <div className="w-full max-w-4xl space-y-8">
                    <button
                        onClick={fetchBookings}
                        disabled={loading}
                        className="w-full px-4 py-2 bg-blue-500 text-white font-bold rounded-md hover:bg-blue-700 transition duration-300 disabled:bg-gray-400"
                    >
                        {loading ? 'Fetching...' : 'Fetch Bookings'}
                    </button>

                    {error && <p className="text-center text-red-500">{error}</p>}

                    {loading ? (
                        <LoadingIndicator />
                    ) : bookings.length === 0 ? (
                        <p className="text-center text-gray-600">You have no bookings. Click &apos;Fetch Bookings&apos; to load your bookings.</p>
                    ) : (
                        <ul className="space-y-4">
                            {bookings.map((booking) => (
                                <li
                                    key={booking.id}
                                    className={`bg-orange-100 p-4 rounded-md shadow cursor-pointer ${selectedBooking?.id === booking.id ? 'border-2 border-orange-500' : ''}`}
                                    onClick={() => handleSelectBooking(booking)}
                                >
                                    <h3 className="text-xl font-semibold">{booking.amenity_name}</h3>
                                    <p className="text-gray-600">Date: {new Date(booking.date).toISOString().split('T')[0]}</p>
                                    <p className="text-gray-600">Time: {booking.time}</p>
                                    <p className="text-gray-600">ID: {booking.id}</p>
                                    <p className="text-gray-600">Capacity: {booking.amenity_capacity}</p>
                                </li>
                            ))}
                        </ul>
                    )}

                    {selectedBooking && (
                        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
                            <h2 className="text-2xl font-semibold mb-4">Modify Selected Booking</h2>
                            <div className="space-y-4">
                                <div>
                                    <label htmlFor="newDate" className="block text-sm font-medium text-gray-700">New Booking Date</label>
                                    <DatePicker
                                        id="newDate"
                                        selected={newDate}
                                        onChange={(date) => setNewDate(date)}
                                        minDate={minDate}
                                        className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="newTime" className="block text-sm font-medium text-gray-700">New Booking Time</label>
                                    <select
                                        id="newTime"
                                        value={newTime.split(':')[0]}
                                        onChange={(e) => setNewTime(`${e.target.value}:00`)}
                                        className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500"
                                    >
                                        {Array.from({ length: 24 }, (_, i) => i).map((hour) => (
                                            <option key={hour} value={hour.toString().padStart(2, '0')}>
                                                {hour.toString().padStart(2, '0')}:00
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <button
                                    onClick={handleUpdateBooking}
                                    className="w-full px-4 py-2 bg-blue-500 text-white font-bold rounded-md hover:bg-blue-700 transition duration-300 disabled:bg-gray-400"
                                    disabled={loading}
                                >
                                    {loading ? 'Updating...' : 'Update Booking'}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    )
}

export default withAuth(ModifyBooking, ["member", "admin"])