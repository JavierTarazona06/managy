"use client";

import AdminHeader from "@/components/AdminHeader";
import Image from "next/image";
import { withAuth } from "@/components/withAuth.jsx";
import { navigate } from "@/components/actions";

const Admin = () => {
  const handleManageUsers = async (e) => {
    e.preventDefault();
    try {
      navigate("/admin/manage-users");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleManageAmenities = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/amenities");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleManageEvents = async (e) => {
    e.preventDefault();
    try {
      navigate("/worker/events");
    } catch (error) {
      alert(error.message);
    }
  };
  return (
    <div className="min-h-screen flex flex-col bg-white text-black">
      <AdminHeader />
      <main className="flex flex-grow items-center justify-center p-8 overflow-y-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl">
          <button
            onClick={handleManageUsers}
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
            <span className="text-lg">Manage Users</span>
          </button>
          <button
            onClick={handleManageAmenities}
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
            <span className="text-lg">Manage Amenities</span>
          </button>
          <button
            onClick={handleManageEvents}
            className="flex flex-col items-center border-4 border-black p-4 shadow-xl bg-orange-100 rounded h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          > <Image src="/images/AdminEvent.png" alt="Manage Events" width={200} height={200} priority className="mb-4" /> <span className="text-lg">Manage Events</span> </button> </div> </main> </div>);
};


//export default withAuth(Admin); ––use when implementing API
export default withAuth(Admin, ["admin"]);
