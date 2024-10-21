'use client';

import Form from "../../components/Form.jsx";

import './login.css';

const Login = () => {
    return (
        <div className="bg-container">
            <Form route="api/token/" method="login"/>
        </div>
    );
};

export default Login;