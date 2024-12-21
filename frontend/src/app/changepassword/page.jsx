"use client";

import Form from "@/components/FormChangePassword";

const ChangePass = () => {

    return (
        <div
            className="fixed top-0 left-0 w-full h-screen bg-cover bg-center bg-no-repeat
          flex justify-center items-center"
            style={{
                backgroundImage:
                    "url('/images/house_register.jpg?height=1080&width=1920')",
            }}
        >
            <Form routeToken="/user/resetpassword/" routeChange="/user/changepassword/"/>
        </div>
    );
};

export default ChangePass;