"use client";

import WorkerHeader from "@/components/WorkerHeader";
import Image from "next/image";
import { withAuth } from "@/components/withAuth.jsx";
import { navigate } from "@/components/actions";

const Events = () => {
  const handleEventCreate = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/events/createEvent");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleRemindEvent = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/events/reminderEvent");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleViewEvent = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/events/viewEvent");
    } catch (error) {
      alert(error.message);
    }
  };


  return (
    <div className="min-h-screen flex flex-col bg-white text-black">
      <WorkerHeader />
      <main className="flex flex-grow flex-col items-center justify-start p-8 overflow-y-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl">
          <button
            onClick={handleEventCreate}
            className="flex flex-col items-center border-4 border-black p-4 shadow-xl bg-orange-100 rounded h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          >
            <Image
              src="/images/admin-user.png"
              alt="Manage Users"
              width={200}
              height={200}
              priority
              className="mb-4"
            />
            <span className="text-lg">Create an Event</span>
          </button>
          <button
            onClick={handleViewEvent}
            className="flex flex-col items-center border-4 border-black p-4 shadow-xl bg-orange-100 rounded h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          >
            <Image
              src="/images/amenity-manage.png"
              alt="Manage Amenities"
              width={200}
              height={200}
              priority
              className="mb-4"
            />
            <span className="text-lg">View Event</span>
          </button>
          <button
            onClick={handleRemindEvent}
            className="flex flex-col items-center border-4 border-black p-4 shadow-xl bg-orange-100 rounded h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          >
            <Image
              src="/images/amenity-manage.png"
              alt="Manage Amenities"
              width={200}
              height={200}
              priority
              className="mb-4"
            />
            <span className="text-lg">Reminders of Event</span>
          </button>
        </div>
      </main>
    </div>);
};


//export default withAuth(Admin); ––use when implementing API
export default withAuth(Events, ["worker", "admin"]);
