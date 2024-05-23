import React, { createContext, useContext, useState } from 'react';

const MealDataContext = createContext();

export const useMealData = () => useContext(MealDataContext);

export const MealDataProvider = ({ children }) => {
  const [mealData, setMealData] = useState([]);

  return (
    <MealDataContext.Provider value={{ mealData, setMealData }}>
      {children}
    </MealDataContext.Provider>
  );
};
