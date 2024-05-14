import React from 'react';
import { Text, TouchableOpacity } from 'react-native';

const MealBox = ({ title }) => {
  return (
    <TouchableOpacity className="border-2 border-black rounded-xl items-center bg-light-gray h-16 w-11/12 mt-4 justify-center elevation-high">
      <Text className="text-dark-dark-gray text-xl font-bold">{title}</Text>
    </TouchableOpacity>
  );
};

export default MealBox;
