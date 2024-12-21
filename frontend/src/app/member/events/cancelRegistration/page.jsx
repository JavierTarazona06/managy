"use client";

import CancelRegistration from "@/components/cancelRegistration";
import {useEffect, useState} from "react";
import LoadingIndicator from "@/components/LoadingIndicator"
import api from "@/api";
import {withAuth} from "@/components/withAuth";

const get_events_selections = "/api/event/selection/view/"

function Page() {
    const [eventsSelection, setEventsSelection] = useState([])
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const getEventsSelFirst = async () => {
            setLoading(true)
            try {
                const response = await api.get(get_events_selections)
                setEventsSelection(response.data)
                console.log(response.data)
            } catch (err) {
                alert("Error bringing the events selections", err.response.data.error)
            } finally {
                setLoading(false)
            }
        }
        getEventsSelFirst()
    }, [])

    return (
        <div className="container mx-auto px-4 bg-white">
            <section className="flex space-x-4">
                {/* Cancel Registration Section */}
                <div className="w-1/2 bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <CancelRegistration/>
                </div>

                {/* Events List Section */}
                <div className="w-1/2 bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    {loading ? (
                        <div className="flex justify-center">
                            <LoadingIndicator/>
                        </div>
                    ) : eventsSelection.length === 0 ? (
                        <p className="text-center text-gray-600">There are no events selections that match the criteria.</p>
                    ) : (
                        <ul className="space-y-4">
                            {eventsSelection.map((eventSel) => (
                                <li
                                    key={eventSel.id}
                                    className="bg-orange-100 p-4 rounded-lg shadow border border-orange-200"
                                >
                                    <h3 className="text-xl font-semibold text-orange-900">{eventSel.name}</h3>
                                    <div className="mt-2 text-gray-700">
                                        <p className="text-gray-600">
                                            <strong>Date:</strong> {new Date(eventSel.date).toISOString().split('T')[0]}
                                        </p>
                                        <p>
                                            <strong>Description:</strong> {eventSel.description}
                                        </p>
                                        <p>
                                            <strong>Number of registered:</strong> {eventSel.numRegistered}
                                        </p>
                                        <p>
                                            <strong>ID:</strong> {eventSel.id}
                                        </p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </section>
        </div>
    );
}

export default withAuth(Page, ["member", "admin"])