'use client'

import MemberHeader from "@/components/MemberHeader"
import { withAuth } from "@/components/withAuth"
import Image from "next/image";
import '@/styles/welcome.css';
import { navigate } from "@/components/actions";
import api from "@/api";
import { useState, useEffect } from "react";

const get_recreationalvenue = "/api/recreational_venue/view/"

const Member = () => {
  const [recrImage, setRecrImage] = useState("")
  const [recrName, setRecrName] = useState("")

  useEffect(() => {
    const handleRecreVenue = async () => {
      try {
        const response = await api.get(get_recreationalvenue)
        console.log(response.data)
        setRecrName(response.data[0].name);
        setRecrImage(response.data[0].photo);
      } catch (error) {
        alert(error.response.data.error)
      }
    }

    handleRecreVenue(); // Call the logout function when the component mounts
  }, []);



  const handleAmenities = async (e) => {
    e.preventDefault();
    try {
      navigate("/member/amenities");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleEvents = async (e) => {
    e.preventDefault();
    try {
      navigate("/member/events");
    } catch (error) {
      alert(error.message);
    }
  };


  return (
    <div className="min-h-screen bg-white text-black">
      <MemberHeader />

      <div className="text-center py-6">
        <h1 className="text-4xl font-bold">
          Welcome Back, Member!
        </h1>
      </div>

      <div className="flex flex-row">
        <div className="w-1/2 flex flex-col">
          <Image
            src={recrImage}
            alt="Logo"
            width={700}
            height={700}
            priority
            className="shadow-xl border-black border-4 self-center ml-4 mr-2 rounded-xl max-h-[60vh] max-w-[40vw] object-contain"
          />
          <h1 className="mt-4 text-4xl font-bold text-center">
            Recreational Venue Name: {recrName}
          </h1>

        </div>

        <div className="w-1/2 h-1/4 flex flex-col">
          <button
            onClick={handleAmenities}
            className="flex flex-col items-center border-4 border-black mr-4 ml-2 p-4 shadow-xl bg-orange-100 rounded-xl h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          >
            <Image
              src="/images/amenity-manage.png"
              alt="Manage Users"
              width={200}
              height={200}
              priority
              className="mb-4"
            />
            <span className="text-lg">Amenities</span>
          </button>
          <button
            onClick={handleEvents}
            className="flex flex-col items-center border-4 border-black mr-4 ml-2 p-4 my-4 shadow-xl bg-orange-100 rounded-xl h-80 transition duration-300 ease-in-out transform hover:bg-orange-200 hover:scale-105"
          >
            <Image
              src="/images/AdminEvent.png"
              alt="Manage Users"
              width={200}
              height={200}
              priority
              className="mb-4"
            />
            <span className="text-lg">Events</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default withAuth(Member, ['member', 'admin']);
