'use client';

import { useEffect } from 'react';
import {navigate} from "../../components/actions.js";

const Logout = () => {

    useEffect(() => {
        const handleLogout = () => {
            localStorage.clear();
            navigate('/login');
        };

        handleLogout(); // Call the logout function when the component mounts
    }, []);

    return <div>Logging out...</div>;
};

export default Logout;