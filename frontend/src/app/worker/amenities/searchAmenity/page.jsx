'use client';

import { useEffect, useState } from "react";
import api from "@/api.js";
import "@/styles/amenitiesPage.css";
import LoadingIndicator from "@/components/LoadingIndicator";
import { withAuth } from "@/components/withAuth";
import Image from "next/image";

const api_all_amenities = "/api/amenity/view/";
const api_sort_amenitiesName = "/api/amenity/get_amenity/";
const api_search_amenitiesName = "/api/amenity/search/";

function SearchAmenity() {

  const [amenities, setAmenities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sortOption, setSortOption] = useState("name");
  const [nameAmenityQ, setNameAmenityQ] = useState("");

  useEffect(() => {
    fetchAmenities();
  }, []);


  const fetchAmenities = () => {
    api
      .get(api_all_amenities)
      .then((res) => res.data)
      .then((data) => {
        setAmenities(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  /*Sort by name*/
  const getAmenitiesName = () => {
    console.log("Search Name: " + sortOption);
    api
      .get(api_sort_amenitiesName + `${sortOption}/`)
      .then((res) => res.data)
      .then((data) => {
        setAmenities(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const sortAmenitiesName = async () => {
    setLoading(true);
    try {
      await getAmenitiesName();
    } catch (err) {
      alert('There was an error fetching events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };


  /*Search by name*/
  const getAmenitiesSearchName = () => {
    console.log("Search Name: " + nameAmenityQ);
    api
      .get(api_search_amenitiesName + `${nameAmenityQ}/`)
      .then((res) => res.data)
      .then((data) => {
        setAmenities(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const searchAmenitiesName = async () => {
    setLoading(true);
    try {
      await getAmenitiesSearchName();
    } catch (err) {
      alert('There was an error fetching events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };


  if (loading) return <p>Loading amenities...</p>;

  return (
    <div className="amenities-container bg-white text-black">
      <Image
        src="/images/house.png"
        alt="Home Logo"
        className="amenities-logo"
        width={200}
        height={200}
        priority
      />
      <h2 className="amenities-title">Search Amenities</h2>

      {/* Sorting Controls */}
      <div className="sorting-controls">
        <label>
          Sort by:
          <select
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
          >
            <option value="0">Random</option>
            <option value="1">Ascending</option>
            <option value="2">Descending</option>
          </select>
        </label>
        {loading && <LoadingIndicator />}
        <button
          onClick={sortAmenitiesName}
          className="px-4 py-2 bg-orange-100 text-black font-bold rounded-r-md hover:bg-orange-900 hover:text-white transition duration-300"
        >
          Sort Amenities
        </button>
      </div>

      {/*Search Bar*/}
      <div className="search-container">
        <label>
          Search:
          <input
            type="text"
            value={nameAmenityQ}
            onChange={(e) => setNameAmenityQ(e.target.value)}
            placeholder="Search amenities by name..."
          />
        </label>
        {loading && <LoadingIndicator />}
        <button
          onClick={searchAmenitiesName}
          className="px-4 py-2 bg-orange-100 text-black font-bold rounded-r-md hover:bg-orange-900 hover:text-white transition duration-300"
        >
          Search Amenities
        </button>
      </div>

      {/* Amenities List */}
      <div className="amenities-list">
        {amenities.map((amenity) => (
          <div key={amenity.id} className="amenity-item">
            <h3>{amenity.name}</h3>
            <p>Description: {amenity.description}</p>
            <p>Capacity: {amenity.capacity}</p>
            <Image
              src={amenity.image}
              alt={`${amenity.name} image`}
              className="amenity-image w-full max-w-xs h-auto rounded-lg mt-2"
              width={300} // Adjust as needed
              height={200} // Adjust as needed
              layout="intrinsic" // Maintain aspect ratio
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default withAuth(SearchAmenity, ["worker", "admin"]);
