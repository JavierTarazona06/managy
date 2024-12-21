"use client";

import Image from "next/image";
import { navigate } from "@/components/actions";

function Home() {
  const scrollToInfo = () => {
    const infoSection = document.getElementById("info-section");
    infoSection?.scrollIntoView({ behavior: "smooth" });
  };

  const handleButtonRegs = async (e) => {
    e.preventDefault();
    try {
      navigate("/register");
    } catch (error) {
      alert(error.message);
    }
  };

  const handleButtonLogin = async (e) => {
    e.preventDefault();
    try {
      navigate("/login");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
      <div className="min-h-screen flex flex-col bg-white text-black">
        <main className="h-screen flex flex-col items-center justify-center p-4 space-y-8 overflow-y-auto">
          <Image
              src="/images/house.png"
              alt="Logo"
              width={450}
              height={450}
              priority
          />
          <h1 className="text-5xl font-bold text-center"> Managy </h1>
          <div className="flex flex-wrap justify-center gap-4 text-black font-bold">
            <button
                className="mt-4 px-4 py-2 bg-orange-100 rounded hover:bg-orange-900"
                onClick={handleButtonLogin}
            >
              Login
            </button>
            <button
                className="mt-4 px-4 py-2 bg-orange-100 rounded hover:bg-orange-900"
                onClick={handleButtonRegs}
            >
              Register
            </button>
            <button
                className="mt-4 px-4 py-2 bg-orange-100 rounded hover:bg-orange-900"
                onClick={scrollToInfo}
            >
              Learn More
            </button>
          </div>
        </main>
        <section id="info-section" className="bg-muted py-16 bg-orange-100">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-semibold mb-6 text-center">
              Information
            </h2>
            <p className="text-lg text-center max-w-2xl mx-auto">
              Managy is a web platform that serves as a booking system for
              hospitality venues (hotels, resorts, clubhouses, and community
              centres). Its features are User authentication and the Creation,
              Retainment, Updating and Deletion of the entity or space that will
              be booked. Smaller businesses or establishments would need an
              automated system to input, retain and remove information. Indeed,
              what is currently available mostly uses google sheets, etc. Our
              platform would make the process automatic without a third person
              (ei. Receptionist) to input the information. Finally, our main
              stakeholder is the Clubhouse Avatar. Potentially: Lakewood Civic
              Centre and Resident Services Usask.
            </p>
          </div>
        </section>
      </div>
  );
}

export default Home;