'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { withAuth } from "@/components/withAuth"
import api from '@/api.js'
import LoadingIndicator from "@/components/LoadingIndicator"
// import { useRouter } from 'next/navigation'

// Define API endpoints
const api_allAmenities = "/api/amenity/view/"
const api_sort_amenitiesName = "/api/amenity/get_amenity/"
const api_search_amenitiesName = "/api/amenity/search/"

const navigate = (path) => {
    window.location.href = path;
};

function MemberAmenities() {
    // const router = useRouter()
    const [amenities, setAmenities] = useState([])
    // Remove this line
    // const [selectedAmenity, setSelectedAmenity] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [searchName, setSearchName] = useState('')
    const [sortOption, setSortOption] = useState("0")

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

    const getAmenitiesName = async () => {
        setLoading(true)
        try {
            const response = await api.get(api_sort_amenitiesName + `${sortOption}/`)
            setAmenities(response.data)
        } catch (err) {
            setError('Error sorting amenities: ' + err.message)
        } finally {
            setLoading(false)
        }
    }

    const searchAmenityByName = async () => {
        setLoading(true)
        try {
            const response = await api.get(api_search_amenitiesName + `${searchName}/`)
            setAmenities(response.data)
        } catch (err) {
            setError('Error searching amenities: ' + err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleCreateBooking = (e) => {
        e.preventDefault();
        navigate("/member/amenities/createBooking");
    };

    const handleCancelBooking = (e) => {
        e.preventDefault();
        navigate("/member/amenities/cancelBooking");
    };

    const handleModifyBooking = (e) => {
        e.preventDefault();
        navigate("/member/amenities/modifyBooking");
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
                <h1 className="text-5xl font-bold text-center">Member Amenities</h1>

                <div className="w-full max-w-4xl space-y-8">
                    <div>
                        <h2 className="text-2xl font-semibold mb-4">Search Amenities</h2>
                        <div className="flex mb-4">
                            <input
                                type="text"
                                value={searchName}
                                onChange={(e) => setSearchName(e.target.value)}
                                placeholder="Enter amenity name"
                                className="flex-grow p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                            />
                            <button
                                onClick={searchAmenityByName}
                                className="px-4 py-2 bg-orange-100 text-black font-bold rounded-r-md hover:bg-orange-900 hover:text-white transition duration-300"
                            >
                                Search
                            </button>
                        </div>

                        <div className="mt-4">
                            <h3 className="text-xl font-semibold mb-2">Sort Amenities</h3>
                            <div className="flex items-center space-x-4">
                                <select
                                    value={sortOption}
                                    onChange={(e) => setSortOption(e.target.value)}
                                    className="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                                >
                                    <option value="0">Random</option>
                                    <option value="1">Ascending</option>
                                    <option value="2">Descending</option>
                                </select>
                                <button
                                    onClick={getAmenitiesName}
                                    className="px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
                                >
                                    Sort Amenities
                                </button>
                            </div>
                        </div>

                        <button
                            onClick={fetchAmenities}
                            className="w-full mt-4 px-4 py-2 bg-orange-100 text-black font-bold rounded-md hover:bg-orange-900 hover:text-white transition duration-300"
                        >
                            Fetch All Amenities
                        </button>

                        {amenities.length > 0 && (
                            <ul className="mt-4 space-y-4">
                                {amenities.map((amenity) => (
                                    <li key={amenity.id}
                                        className="bg-orange-100 p-4 rounded-md shadow cursor-pointer"
                                    >
                                        <h3 className="text-xl font-semibold">{amenity.name}</h3>
                                        <p className="mt-2">{amenity.description}</p>
                                        <p className="mt-2">Capacity: {amenity.capacity}</p>
                                        <p className="mt-2">ID: {amenity.id}</p>
                                        {amenity.image && (
                                            <Image
                                                src={amenity.image}
                                                alt={`${amenity.name} image`}
                                                className="w-full max-w-xs h-auto rounded-lg mt-2"
                                                width={300}
                                                height={200}
                                                layout="responsive"
                                            />
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>

                    <div>
                        <h2 className="text-2xl font-semibold mb-4">Manage Bookings</h2>
                        <div className="mt-4 space-y-4">
                            <div>
                                <h3 className="text-xl font-semibold mb-2">Create, Modify, or Cancel Booking</h3>
                                <button
                                    onClick={handleCreateBooking}
                                    className="w-full mt-2 px-4 py-2 bg-green-500 text-white font-bold rounded-md hover:bg-green-700 transition duration-300"
                                >
                                    Create Booking
                                </button>
                                <button
                                    onClick={handleModifyBooking}
                                    className="w-full mt-2 px-4 py-2 bg-blue-500 text-white font-bold rounded-md hover:bg-blue-700 transition duration-300"
                                >
                                    Modify Booking
                                </button>
                                <button
                                    onClick={handleCancelBooking}
                                    className="w-full mt-2 px-4 py-2 bg-red-500 text-white font-bold rounded-md hover:bg-red-700 transition duration-300"
                                >
                                    Cancel Booking
                                </button>
                            </div>
                        </div>
                    </div>

                    {loading && <LoadingIndicator />}
                    {error && <p className="text-center text-red-500">{error}</p>}
                </div>
            </main>
        </div>
    )
}

export default withAuth(MemberAmenities, ["member", "admin"])
