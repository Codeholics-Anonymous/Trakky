import axios from 'axios';
import React, { createContext, useContext, useEffect, useState } from 'react';
import { getUserData } from '../utils/Auth.js'; // Ensure path is correct

const MealDataContext = createContext();

export const useMealData = () => useContext(MealDataContext);

export const MealDataProvider = ({ children }) => {
  const [mealData, setMealData] = useState({
    breakfast: {},
    lunch: {},
    dinner: {}
  });
  const [date, setDate] = useState(new Date());
  const [searchResults, setSearchResults] = useState([]);
  const [searchError, setSearchError] = useState(''); // State to store search error

  const fetchData = async (selectedDate) => {
    try {
      const { token } = await getUserData();
      if (!token) {
        console.error("No token found. Please login again.");
        return;
      }
      const dateString = `${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}`;
      const url = `https://trakky.onrender.com/api/meal/${dateString}/`;

      const response = await axios.get(url, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      const meals = response.data;
      setMealData(meals);
    } catch (error) {
      console.error("Error fetching meals:", error);
      if (error.response) {
        console.error(`Response Error: ${error.response.status} ${JSON.stringify(error.response.data)}`);
      }
    }
  };

  const searchProducts = async (query) => {
    setSearchError(''); // Clear previous errors
    try {
      const { token } = await getUserData();
      if (!token) {
        console.error("No token found. Please login again.");
        return;
      }
      const url = `https://trakky.onrender.com/api/product/${query}/`;
      const response = await axios.get(url, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      setSearchResults(response.data);
      if (response.data.length === 0) {
        setSearchError('Product not found. Add product in settings menu.');
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        setSearchError('Product not found. Add product in settings menu.');
      } else {
        setSearchError('Error searching products');
      }
      setSearchResults([]);
    }
  };

  const createMealItem = async (mealType, date, productId, gramAmount) => {
    try {
      const { token } = await getUserData();
      if (!token) {
        console.error("No token found. Please login again.");
        return;
      }
      const url = `https://trakky.onrender.com/api/create_mealitem/${mealType}/${date}/`;
      const response = await axios.post(url, {
        "product_id": productId,
        "gram_amount": gramAmount
      }, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      // Refresh meal data after creating a meal item
      fetchData(new Date(date));
    } catch (error) {
      console.error("Error creating meal item:", error);
      if (error.response) {
        console.error(`Response Error: ${error.response.status} ${JSON.stringify(error.response.data)}`);
      }
    }
  };

  useEffect(() => {
    fetchData(date); // Trigger a fetch when the date changes
  }, [date]);

  return (
    <MealDataContext.Provider value={{ mealData, setMealData, date, setDate, searchResults, searchProducts, searchError, createMealItem }}>
      {children}
    </MealDataContext.Provider>
  );
};
