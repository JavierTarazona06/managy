"use client";

import { useEffect } from "react";
import { navigate } from "@/components/actions.js";
import LoadingIndicator from "@/components/LoadingIndicator";

const Logout = () => {
    useEffect(() => {
        const handleLogout = () => {
            localStorage.clear();
            navigate("/");
        };

        handleLogout(); // Call the logout function when the component mounts
    }, []);

    return (
        <div>
            <h1 className="text-black font-bold">Logging out...</h1>
            <LoadingIndicator />
        </div>
    );
};

export default Logout;
