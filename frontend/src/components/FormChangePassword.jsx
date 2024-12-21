"use client";

import { useState } from "react";
import api from "@/api.js";
import "@/styles/FormRegister.css";
import LoadingIndicator from "./LoadingIndicator.jsx";
import { navigate } from "./actions.js";



// eslint-disable-next-line react/prop-types
function FormChangePass({ routeToken, routeChange }) {
    const [email, setEmail] = useState("");
    const [token, setToken] = useState("");
    const [nw_password, setNw_password] = useState("");
    const [co_password, setCo_password] = useState("");
    const [loading, setLoading] = useState(false);


    const handleSubmitToken = async (e) => {
        setLoading(true);
        e.preventDefault();
        /*Avoid submitting the data, first perform other tasks*/

        try {

            const formData = new FormData();
            formData.append('email', email);
            console.log(Array.from(formData.keys()));
            console.log(Array.from(formData.values()));
            const res = await api.post(routeToken, formData);
            console.log(res.data);

            alert("Email with the pass token was sent!");

        } catch (error) {
            alert(error.response.data.error);
        } finally {
            setLoading(false);
        }
    };


    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        /*Avoid submitting the data, first perform other tasks*/

        try {

            let data1  = {
                "new_password": nw_password,
                "confirm_password": co_password
            }
            console.log("!!!!!!Data: ", data1);

            let routeChangeMod = routeChange+`${token}/`

            const res = await api.post(routeChangeMod, data1);
            console.log(res.data);
            console.log(res.status);

            alert("Password has been successfully changed!");

            navigate("/login");
        } catch (error) {
            alert(error.response.data.error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="h-screen w-[70%] overflow-y-auto scrollbar-hidden">
            <form onSubmit={handleSubmitToken} className="myform-container">
                <h1 className="text-3xl text-black font-bold">Ask for the token</h1>
                <p className="text-black"><br/>The token will be sent through
                    e-mail. You must copy it and paste it here</p>
                <input
                    className="myform-input text-black"
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                {loading && <LoadingIndicator/>}
                <button className="myform-button font-bold" type="submit">
                    Submit
                </button>
            </form>
            <form onSubmit={handleSubmit} className="myform-container">
                <h1 className="text-3xl text-black font-bold">Change Password</h1>
                <p className="text-black"><br/> If you did not receive the email
                    with the token then... If admin, you are not registered,
                    if member/worker, your admin has not included you in
                    qhe system.</p>
                <input
                    className="myform-input text-black"
                    type="text"
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    placeholder="Token"
                />
                <input
                    className="myform-input text-black"
                    type="password"
                    value={nw_password}
                    onChange={(e) => setNw_password(e.target.value)}
                    placeholder="New Password"
                />
                <input
                    className="myform-input text-black"
                    type="password"
                    value={co_password}
                    onChange={(e) => setCo_password(e.target.value)}
                    placeholder="Confirm Password"
                />
                {loading && <LoadingIndicator/>}
                <button className="myform-button font-bold" type="submit">
                    Submit
                </button>
            </form>
        </div>
    );
}

export default FormChangePass;
