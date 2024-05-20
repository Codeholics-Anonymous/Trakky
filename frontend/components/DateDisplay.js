import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

const DateDisplay = () => {
  return (
    <TouchableOpacity className="rounded-lg flex-row justify-center items-center p-1 bg-gray mt-3 mb-9 w-1/2" style={{elevation: 5}}>
      <Text className="text-black text-base mx-2.5">Monday, 6.05.2024</Text>
      <FontAwesome name="calendar" className="text-black text-base pl-2"/>
    </TouchableOpacity>
  );
};

export default DateDisplay;
