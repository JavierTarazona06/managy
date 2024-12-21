"use client";

import AdminHeader from "@/components/AdminHeader";
import { useEffect, useState } from "react";
import UserPanel from "@/components/UserPanel";
import { withAuth } from "@/components/withAuth";
import api from "@/api";
import LoadingIndicator from "@/components/LoadingIndicator";
import { generateRandomString } from '@/utils/tools';

const api_createUsrAdmin = "/users/admin/createuser/";
const api_excel = "/api/excel/";
const routeCreateBatch = "/user/admin/createuserbatch/";
const api_searchUser = "/api/admin/search/"
const api_deleteuser = "/users/admin/deleteuser/";

const ManageUsers = () => {
  /*Add User*/
  const [firstName1, setFirstName1] = useState("");
  const [lastName1, setLastName1] = useState("");
  const [email1, setEmail1] = useState("");
  const [role1, setRole1] = useState("");

  /*Search user*/
  const [name2, setName2] = useState('');
  const [email2, setEmail2] = useState('');
  const [id2, setId2] = useState('');
  const [role2, setRole2] = useState('');
  const [usersFound, setUsersFound] = useState([]);


  const [role3, setRole3] = useState("");
  const [excelFile, setExcelFile] = useState(null);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    handleUserSearchBegin();
  }, []);


  // –– Mock methods to simulate API
  const [showEditForm, setShowEditForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const openEditForm = (user) => {
    setSelectedUser(user);
    setShowEditForm(true);
  };

  const closeEditForm = () => {
    setSelectedUser(null);
    setShowEditForm(false);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0]; // Get the first selected file
    if (file) {
      setExcelFile(file);
    }
  };


  const handleSubmitBatch = async (e) => {
    setLoading(true);
    e.preventDefault();
    /*Avoid submitting the data, first perform other tasks*/

    try {

      let cur_name = generateRandomString(10) + ".xlsx";
      const formData = new FormData();
      formData.append('file', excelFile);
      formData.append('title', cur_name);
      console.log(Array.from(formData.keys()));
      console.log(Array.from(formData.values()));
      const res = await api.post(api_excel, formData);
      console.log(res.data);

      let data1 = {
        "role": role3,
        "excel_link": res.data.url
      }
      console.log("!!!!!!Data: ", data1);
      const res1 = await api.post(routeCreateBatch, data1);
      console.log(res1.data);

      alert("Users Created successfully. Reload page to view them");

        } catch (error) {
            alert(error.response.data.error);
        } finally {
            setLoading(false);
        }
    };

  const mycreateUser = (e) => {
    e.preventDefault();

    let data1 = {
      'first_name': firstName1 + " " + lastName1,
      'email': email1,
      'role': role1,
      'recreational_venue_id': null
    }
    console.log(data1);

    api
      .post(api_createUsrAdmin, data1)
      .then((res) => {
        if (res.status === 201) {
          console.log(res.data);
          alert("User created with ID: " + res.data.id + "\nClick on search to view them");
        } else alert("Failed to make note.");

      })
      .catch((err) => alert("Error ", err));
  };

  const handleSubmitUser = (e) => {
    setLoading(true);
    e.preventDefault();
    try {
      mycreateUser(e);
      handleUserSearchBegin();

    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };



  const handleUserSearchBegin = async () => {
    setLoading(true);

    try {

      api
        .get(api_searchUser)
        .then((res) => res.data)
        .then((data) => {
          setUsersFound(data);
          console.log(data);
        })
        .catch((err) => alert(err));

    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };


  const handleUserSearch = (e) => {
    setLoading(true);
    e.preventDefault();

    try {

      let search = '';
      let flag = false;
      if ((name2 != null) && (name2 !== '')) {
        search = search + "?name=" + name2;
        flag = true;
      }
      if ((email2 != null) && (email2 !== '')) {
        if (flag) {
          search = search + "&email=" + email2;
        } else {
          search = search + "?email=" + email2;
          flag = true;
        }
      }
      if ((id2 != null) && (id2 !== '')) {
        if (flag) {
          search = search + "&id=" + id2;
        } else {
          search = search + "?id=" + id2;
          flag = true;
        }
      }
      if ((role2 != null) && (role2 !== '')) {
        if (flag) {
          search = search + "&role=" + role2;
        } else {
          search = search + "?role=" + role2;
        }
      }

      api
        .get(api_searchUser + search)
        .then((res) => res.data)
        .then((data) => {
          setUsersFound(data);
          console.log(data);
        })
        .catch((err) => alert(err));

    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = (id) => {
    api
      .delete(api_deleteuser + `${id}/`)
      .then((res) => {
        if (res.status === 204) alert("User deleted!");
        else alert("Failed to delete user.");
      })
      .catch((error) => alert(error));
  };


  return (
    <div className="min-h-screen bg-white text-black">
      <AdminHeader />
      <div className="text-center text-3xl font-bold py-4">
        <h2>Manage Users</h2>
      </div>
      <div className="flex mx-8 my-1">
        <div>
          <h2 className="mt-1 font-bold">
            Search By:
          </h2>
        </div>

        <form onSubmit={handleUserSearch} className="mx-4">
          <input
            type="text"
            name="User Search"
            value={name2}
            onChange={(e) => setName2(e.target.value)}
            placeholder="Name"
            className="w-full p-2 border-4 border-black rounded-xl"
          />
          <input
            type="text"
            name="User Search1"
            value={email2}
            onChange={(e) => setEmail2(e.target.value)}
            placeholder="Email"
            className="w-full p-2 mt-1 border-4 border-black rounded-xl"
          />
          <input
            type="text"
            name="User Search2"
            value={id2}
            onChange={(e) => setId2(e.target.value)}
            placeholder="ID"
            className="w-full p-2 mt-1 border-4 border-black rounded-xl"
          />
          <select
            name="role"
            value={role2}
            onChange={(e) => setRole2(e.target.value)}
            className="w-full p-2 mt-1 border-4 border-black rounded-xl"
          >
            <option value="" disabled>Select Role</option>
            <option value="admin">Admin</option>
            <option value="member">Member</option>
            <option value="worker">Worker</option>
            <option value=''>None</option>
          </select>
          {loading && <LoadingIndicator />}
          <button className=" mt-1 text-center myform-button font-bold border-black border-4 rounded-xl px-8 bg-orange-200 hover:bg-orange-300" type="submit font-bold">
            Search my user(s)
          </button>
        </form>

      </div>


      <div className="mx-8 flex flex-row items-start justify-center space-x-16">
        <div className="border-8 bg-orange-200 border-black rounded w-full flex-grow p-4 mb-4">
          {usersFound.length > 0 ? (
            usersFound.map((user) => (
              <div key={user.id}>
                <UserPanel user={user} onDeleteClick={() => openEditForm(user)} key={user.id} />
              </div>))
          ) : (<p className="text-center text-black font-bold">No users in the system</p>
          )}
        </div>

        <div className="border-8 border-black p-6 rounded shadow-lg w-80 text-center bg-orange-200">
          <h3 className="text-xl font-bold mb-4">Add User</h3>
          <form onSubmit={handleSubmitUser} className="space-y-4">
            <input
              type="text"
              name="first_name"
              value={firstName1}
              onChange={(e) => setFirstName1(e.target.value)}
              placeholder="First Name"
              className="w-full p-2 border-4 border-black rounded-xl"
              required
            />
            <input
              type="text"
              name="last_name"
              value={lastName1}
              onChange={(e) => setLastName1(e.target.value)}
              placeholder="Last Name"
              className="w-full p-2 border-4 border-black rounded-xl"
              required
            />
            <input
              type="email"
              name="email"
              value={email1}
              onChange={(e) => setEmail1(e.target.value)}
              placeholder="Email"
              className="w-full p-2 border-4 border-black rounded-xl"
              required
            />
            <select
              name="role"
              value={role1}
              onChange={(e) => setRole1(e.target.value)}
              className="w-full p-2 border-4 border-black rounded-xl"
              required
            >
              <option value="" disabled>Select Role</option>
              <option value="admin">Admin</option>
              <option value="member">Member</option>
              <option value="worker">Worker</option>
            </select>
            {loading && <LoadingIndicator />}
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded-3xl hover:bg-blue-600"
            >
              Add User
            </button>
          </form>
          <form onSubmit={handleSubmitBatch} className="space-y-4">
            <h3 className="text-xl font-bold mb-4"><br />Add User - Batch</h3>
            <p>Send users by Batch using an excel file(.xlsx). Take care of:</p>
            <p>1. Users having the same role</p>
            <p>2. First Column is name</p>
            <p>3. Second Column is email</p>
            <select
              name="role"
              value={role3}
              onChange={(e) => setRole3(e.target.value)}
              className="w-full p-2 border-4 border-black rounded-xl"
              required
            >
              <option value="" disabled>Select Role</option>
              <option value="admin">Admin</option>
              <option value="member">Member</option>
              <option value="worker">Worker</option>
            </select>
            <input
              className="myform-input text-black"
              type="file"
              accept=".xlsx" // This restricts the file picker to Excel files
              onChange={handleFileChange}
              placeholder="Excel File" // Update placeholder text to reflect the file type
              required
            />
            {loading && <LoadingIndicator />}
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded-3xl hover:bg-blue-600"
            >
              Add Users!
            </button>
          </form>

        </div>
      </div>
      {showEditForm && selectedUser && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-orange-200 p-6 rounded shadow-lg w-80 text-center border-black border-4">
            <h3 className="text-xl font-bold mb-4">Are you sure you want to delete this user?</h3>
            <div className="flex space-x-4 mt-4">
              <button
                type="button"
                className="w-full bg-red-500 text-white p-2 rounded-3xl hover:bg-red-600 shadow-xl"
                onClick={() => {
                  deleteUser(selectedUser.id)
                  closeEditForm()
                  handleUserSearchBegin()

                }}
              >
                Delete
              </button>

              <button
                type="button"
                className="w-full bg-gray-500 text-white p-2 rounded-3xl hover:bg-gray-600 shadow-xl"
                onClick={closeEditForm}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

//export default withAuth(ManageUsers);
export default withAuth(ManageUsers, ["admin"]);
