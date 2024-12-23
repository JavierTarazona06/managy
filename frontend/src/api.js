"use client";

import axios from "axios";
import { ACCESS_TOKEN } from "./constants";
/*import process from "next/dist/build/webpack/loaders/resolve-url-loader/lib/postcss.js";*/

const apiUrl = "https://managy-404252599785.us-central1.run.app";
//const apiUrl = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
    ? process.env.NEXT_PUBLIC_API_URL
    : apiUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default api;
