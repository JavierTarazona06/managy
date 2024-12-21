"use client";
import Image from "next/image";
import { navigate } from "./actions";
import { useState } from "react";
import { ROLE } from "@/constants";

const WorkerHeader = () => {

  const handleHeaderText = async (e) => {
    e.preventDefault();
    try {
      if (localStorage.getItem(ROLE) === "worker")
        navigate("/worker");

      if (localStorage.getItem(ROLE) === "admin")
        navigate("/admin");

    } catch (error) {
    }
  }

  const handleLogout = async (e) => {
    e.preventDefault();
    try {
      navigate("/logout");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div>
      <header className="flex items-center p-4 bg-orange-500 text-white relative border-b-8 border-black">
        <button className="text-4xl" onClick={handleHeaderText}>
          Managy Worker
        </button>

        <div className="ml-auto">
          <button className="pr-2  transition duration-200 hover:text-gray-300">
            Profile
          </button>

          /

          <button className="pl-2  transition duration-200 hover:text-gray-300" onClick={handleLogout}>
            Logout
          </button>

        </div>



      </header>
    </div>
  );
};

export default WorkerHeader;
