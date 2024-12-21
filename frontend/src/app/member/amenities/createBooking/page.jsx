'use client'
import api from '@/api.js';
import { useState, useEffect } from 'react';
import "react-datepicker/dist/react-datepicker.css";
import MemberHeader from '@/components/MemberHeader';
import { withAuth } from "@/components/withAuth";
import AmenityPanel from '@/components/AmenityPanel';
import Image from 'next/image';
const api_allAmenities = "/api/amenity/view/"

const api_createbooking = "/api/amenity/booking/create/"
const api_get_available_booking_slots = "/api/amenity/booking/timeslots/"
const navigate = (path) => {
  window.location.href = path;
};

const CreateBooking = () => {
  const [amenities, setAmenities] = useState([])

  const [showEditForm, setShowEditForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const [timeSlotPageNumber, setTimeSlotPageNumber] = useState(0);
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [timeSlots, setTimeSlots] = useState([]);
  const [amenity_id, setAmenityId] = useState(null);
  const [am_start_time, setStartTime] = useState('');
  const [am_details, setAmDetails] = useState('');
  const [am_capacity, setAmCapacity] = useState('');
  const [am_start_date, setAmDate] = useState('');

  useEffect(() => {
    fetchAmenities()
  }, [])
  const changeTimeSlotPageNumber = (direction) => {
    setTimeSlotPageNumber((prevPageNumber) => {
      const newPageNumber = direction === 1 ? prevPageNumber + 1 : prevPageNumber - 1;
      setAmDate(timeSlots[newPageNumber]?.day);

      const maxPageNumber = timeSlots.length - 1;
      if (newPageNumber < 0) return 0;
      if (newPageNumber > maxPageNumber) return maxPageNumber;
      if (timeSlots[newPageNumber]) {
        setAmDate(timeSlots[newPageNumber]?.day);
      }
      return newPageNumber;
    });
  };


  const closeRegisterForm = () => {
    setSelectedUser(null);
    setShowEditForm(false);
  };

  const openEditForm = async (event) => {
    setSelectedUser(event);
    setShowEditForm(true);
    setTimeSlotPageNumber(0);
    await fetchAvailableTimeSlots(event.id);
  };

  useEffect(() => {
    fetchAmenities()
  }, [])

  const fetchAmenities = async () => {
    setLoading(true)
    try {
      const response = await api.get(api_allAmenities)
      setAmenities(response.data)
    } catch (err) {
      setError('Error fetching amenities: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchAvailableTimeSlots = async (id) => {
    setLoading(true)
    try {
      const response = await api.get(api_get_available_booking_slots + `${id}/`)
      setTimeSlots(response.data)
    } catch (err) {
      setError('Error fetching time slots')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitBooking = async () => {
    setLoading(true);

    try {

      const data1 = {
        "amenities": amenity_id,
        "date": am_start_date,
        "time": am_start_time,
        "amenity_details": am_details,
        "amenity_capacity": am_capacity,
      }
      console.log("!!!!!!Data: ", data1);

      const res = await api.post(api_createbooking, data1);

      alert("The ID of the Booking venue is: " + res.data.id);

    } catch (error) {
      alert(error.response.data.error);
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="min-h-screen bg-white text-black">
      <MemberHeader />
      <h2 className="text-2xl font-semibold mt-4 text-center">Amenities</h2>

      <div className="border-8 bg-orange-200 border-black rounded p-4 m-4 flex flex-col justify-center">

        {amenities.length > 0 ? (
          amenities.map((amenity) => (
            <AmenityPanel key={amenity.id} amenity={amenity} onDeleteClick={() => {
              setAmenityId(amenity.id)
              setAmDetails(amenity.description)
              setAmCapacity(amenity.capacity)
              openEditForm(amenity)
              setAmDate(timeSlots[0]?.day);

            }} />
          ))
        ) : (
          <p className="text-center text-black font-bold">No amenities in the system</p>
        )}
      </div>
      {showEditForm && selectedUser && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-orange-200 p-6 rounded shadow-lg w-2/5 h-5/7 text-center border-black border-4 overflow-hidden">
            <h3 className="text-xl font-bold mb-4 flex flex-col">Would you like to book this amenity?</h3>
            <div className="flex flex-row space-x-8">
              <div className="flex-1 overflow-auto max-h-80 border-black border-4 bg-white">
                {loading ? (
                  <p>Loading time slots...</p>
                ) : timeSlots.length > 0 ? (
                  <div>
                    <div className="text-lg font-semibold mb-2 border-black border-b-4 flex justify-between items-center space-x-2">
                      <h4 className='ml-2'>Available time slots for {timeSlots[timeSlotPageNumber]?.day}</h4>
                      <div className='mt-2'>
                        <button className='border-4 border-black rounded-full hover:bg-gray-400' onClick={() => changeTimeSlotPageNumber(0)}>
                          <Image
                            src="/images/left-arrow.png"
                            alt="Left Arrow"
                            width={20}
                            height={20}
                            priority
                          />
                        </button>
                        <button className='border-4 border-black rounded-full hover:bg-gray-400 mr-2' onClick={() => changeTimeSlotPageNumber(1)}>
                          <Image
                            src="/images/right-arrow.png"
                            alt="Right Arrow"
                            width={20}
                            height={20}
                            priority
                          />
                        </button>
                      </div>
                    </div>
                    <div>

                    </div>

                    <ul className="flex flex-col space-y-2 max-h-60 overflow-y-auto">
                      {timeSlots[timeSlotPageNumber]?.times?.length > 0 ? (
                        timeSlots[timeSlotPageNumber].times.map((time, index) => (
                          <li key={index} className="flex items-center space-x-2">
                            <input
                              type="radio"
                              value={time}
                              name="time-slot"
                              className="ml-2 w-5 h-5 border-2 border-gray-300 rounded-full appearance-none checked:border-blue-500 checked:bg-blue-500 focus:outline-none hover:ring-2 hover:ring-blue-300 focus:ring-2 focus:ring-blue-500 dark:border-gray-500 dark:checked:bg-blue-500 dark:focus:ring-blue-500"
                              id={`time-radio-${index}`}
                              onChange={() => setStartTime(time)}
                            />
                            <label htmlFor={`time-radio-${index}`} className="text-sm">{time}</label>
                          </li>
                        ))
                      ) : (
                        <p>No available time slots</p>
                      )}
                    </ul>
                  </div>
                ) : (
                  <p>No available time slots</p>
                )}
              </div>
            </div>
            <div className="flex space-x-4 mt-4">
              <button
                type="button"
                className="w-full bg-blue-500 text-white p-3 rounded-3xl hover:bg-blue-600 shadow-xl"
                onClick={() => {
                  closeRegisterForm();
                  handleSubmitBooking();
                }}
              >
                Register
              </button>
              <button
                type="button"
                className="w-full bg-gray-500 text-white p-3 rounded-3xl hover:bg-gray-600 shadow-xl"
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
