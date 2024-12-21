'use client';

import { useState } from "react";
import api from "@/api.js";
import "@/styles/createAmenity.css";
import LoadingIndicator from "@/components/LoadingIndicator.jsx";
import { withAuth } from "@/components/withAuth.jsx";

const api_images = "/api/image/";
const api_amenityCreate = "/api/amenity/create/";

function CreateAmenity() {
  const [amenityName, setAmenityName] = useState("");
  const [description, setDescription] = useState("");
  const [capacity, setCapacity] = useState("");

  const [imageURL, setImageURL] = useState("");
  const [imageFile, setImageFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0]; // Get the first selected file
    if (file) {
      setImageFile(file);
    }
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    /*Avoid submitting the data, first perform other tasks*/

    try {

      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('title', amenityName);
      console.log(Array.from(formData.keys()));
      console.log(Array.from(formData.values()));
      const res = await api.post(api_images, formData);
      console.log(res.data);
      setImageURL(res.data.url);

      const data1 = {
        "name": amenityName,
        "description": description,
        "capacity": capacity,
        "image": res.data.url,
      };
      console.log(data1);
      const res1 = await api.post(api_amenityCreate, data1);
      console.log(res1.data);

      if (res1.status === 201) {
        alert("Amenity Created! With ID: " + res1.data.id + "\nGo to view Amenities");
      }
      else alert("Failed to create Amenity.");

    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-container">
      <form onSubmit={handleSubmit} className="form-container">
        <h1 className="form-title">Add a New Amenity</h1>

        <input
          className="form-input"
          type="text"
          value={amenityName}
          onChange={(e) => setAmenityName(e.target.value)}
          placeholder="Amenity Name"
          required
        />

        <textarea
          className="form-input description-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Amenity Description"
          required
        ></textarea>

        <input
          className="form-input"
          type="number"
          value={capacity}
          onChange={(e) => setCapacity(e.target.value)}
          placeholder="Capacity (people)"
          required
        />

        <input
          className="myform-input text-black"
          type="file"
          accept="image/*" // This restricts the file picker to images only
          onChange={handleFileChange}
          placeholder="Photo"
        />

        {loading && <LoadingIndicator />}

        <button className="form-button" type="submit">
          {loading ? "Adding..." : "Add Amenity"}
        </button>
      </form>
    </div>
  );
}

export default withAuth(CreateAmenity, ["worker", "admin"]);
