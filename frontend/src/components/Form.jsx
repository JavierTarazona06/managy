"use client";

import { useState } from "react";
import api from "@/api.js";
import {ACCESS_TOKEN, REFRESH_TOKEN, ROLE} from "@/constants.js";
import "@/styles/Form.css";
import LoadingIndicator from "./LoadingIndicator.jsx";
import { navigate } from "./actions.js";

const routeuserinfo = "/user/getinfo/";

// eslint-disable-next-line react/prop-types
function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        /*Avoid submitting the data, first perform other tasks*/

        try {
            const res = await api.post(route, { username, password });
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

                console.log(routeuserinfo);
                const res2 = await api.get(routeuserinfo+`?email=${username}`);
                console.log(res2.data);

                const role = res2.data.role; // Using dot notation to get the role

                localStorage.setItem(ROLE, role);
                console.log("Role is: "+role);

                if (role === "admin") {
                    navigate("/admin");
                } else if (role === "member") {
                    navigate("/member");
                } else if (role === "worker") {
                    navigate("/worker");
                } else {
                    // If the role doesn't match any known roles, navigate to an example or default page
                    navigate("/example");
                }

            } else {
                /*A registered user is redirected to login*/
                navigate("/login");
            }

        } catch (error) {
            alert(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="myform-container">
            <h1 className="text-3xl text-black font-bold">{name}</h1>
            <input
                className="myform-input text-black"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Email"
            />
            <input
                className="myform-input text-black"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {loading && <LoadingIndicator />}
            <button className="myform-button font-bold" type="submit">
                {name}
            </button>
        </form>
    );
}

export default Form;
