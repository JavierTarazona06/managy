"use client";

import { jwtDecode } from "jwt-decode";
import api from "@/api.js";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "@/constants";

export async function isAuthorized() {
    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("/api/token/refresh/", {
                refresh: refreshToken,
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.log(error);
            return false;
        }
    };

    // Main authentication function
    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            return false;
        }
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        // Check if the token is expired
        if (tokenExpiration < now) {
            return await refreshToken(); // Refresh token if expired
        } else {
            return true; // Token is valid
        }
    };

    // Call auth to check if the user is authorized
    return await auth();
}
