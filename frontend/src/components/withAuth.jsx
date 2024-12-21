"use client";

import { useEffect, useState } from "react";
import { isAuthorized } from "./ProtectedRoute.jsx";
import { navigate } from "./actions.js";
import { ROLE } from "@/constants";


/*Options for role can be ["admin", "member", "worker"]. An empty array allows any authenticated user.*/
export const withAuth = (WrappedComponent, roles = []) => {
    return function WithAuth(props) {
        const [isLoading, setIsLoading] = useState(true);
        const [isAuth, setIsAuth] = useState(false);

        useEffect(() => {
            const checkAuth = async () => {
                const authorized = await isAuthorized();
                if (!authorized) {
                    /*redirect("/login");*/
                    navigate("/login");
                    setIsAuth(false);
                } else {
                    setIsAuth(true);
                }
                setIsLoading(false);
            };

            checkAuth();
        }, []);

        if (isLoading) {
            return <div>Loading...</div>; // You can show a loading indicator here
        }

        if (!isAuth) {
            alert("User is no authenticated");
            navigate("/login");
            return null; // No need to render the component if not authorized
        }

        if (roles.length === 0) {
            return <WrappedComponent {...props} />;
        }

        const cur_role = localStorage.getItem(ROLE);
        console.log("Role is "+cur_role);

        if (!roles.includes(cur_role)) {
            alert("User does not have permission to access this page");
            navigate(`/${cur_role}`);
            return null;
        }

        return <WrappedComponent {...props} />;
    };
};
