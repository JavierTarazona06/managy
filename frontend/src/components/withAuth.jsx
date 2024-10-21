"use client"

import { useEffect, useState } from "react";
import { isAuthorized } from "./ProtectedRoute.jsx";
import { redirect } from "next/navigation";

/*import { useRouter } from 'next/navigation'*/
import {navigate} from "./actions.js";

export const withAuth = (WrappedComponent) => {

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
      return null; // No need to render the component if not authorized
    }

    return <WrappedComponent {...props} />;
  };
};