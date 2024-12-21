"use client";

import Form from "@/components/Form.jsx";
import {navigate} from "@/components/actions";

const Login = () => {

    const handleForgot = async (e) => {
        e.preventDefault();
        try {
            navigate("/changepassword");
        } catch (error) {
            alert(error.message);
        }
    };

    return (
        <div
            className="fixed top-0 left-0 w-full h-screen bg-cover bg-center bg-no-repeat
        flex flex-col justify-center items-center"
            style={{
                backgroundImage:
                    "url('/images/house_login.jpg?height=1080&width=1920')",
            }}
        >
            <Form route="api/token/" method="login"/>
            <button
                className="mt-4 px-4 py-2 bg-gray-900 text-orange-600 font-bold border border-orange-600 rounded hover:bg-orange-600 hover:text-white"
                onClick={handleForgot}
            >
                Forgot Password
            </button>
        </div>
    );
};

export default Login;