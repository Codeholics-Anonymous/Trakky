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

  const fetchData = async (selectedDate) => {
    try {
      const { token } = await getUserData();
      if (!token) {
        console.error("No token found. Please login again.");
        return;
      }
      const dateString = `${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}`;
      const url = `https://trakky.onrender.com/api/meal/${dateString}`;

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

  useEffect(() => {
    fetchData(date); // Trigger a fetch when the date changes
  }, [date]);

  return (
    <MealDataContext.Provider value={{ mealData, setMealData, date, setDate }}>
      {children}
    </MealDataContext.Provider>
  );
};
