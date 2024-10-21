'use client';

import Form from "../../components/Form.jsx";
import {useEffect} from "react";

import './register.css';


const LogOutRegister = () => {

    useEffect(() => {
        const handleLogoutRegister = () => {
            localStorage.clear();
        };

        handleLogoutRegister(); // Call the logout function when the component mounts
    }, []);

    return (
        <div className="bg-container">
            <Form route="api/user/register/" method="register" />
        </div>
    );
};

export default LogOutRegister;