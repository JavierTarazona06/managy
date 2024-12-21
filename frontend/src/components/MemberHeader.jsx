"use client";
import { navigate } from "./actions";

const MemberHeader = () => {

  const handleHeaderText = async (e) => {
    e.preventDefault();
    try {
      navigate("/member");
    } catch (error) {
      alert(error.message);
    }
  };

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
          Managy
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

export default MemberHeader;
