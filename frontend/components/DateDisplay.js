import AsyncStorage from '@react-native-async-storage/async-storage';
import DateTimePicker from '@react-native-community/datetimepicker';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Alert, Dimensions, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import { useMealData } from './MealDataContext'; // Adjust path as necessary

const { width } = Dimensions.get('window');

const DateDisplay = () => {
  const [showDatePicker, setShowDatePicker] = useState(false);
  const { date, setDate, setMealData } = useMealData(); // Use date from context


  const fetchData = async (selectedDate) => {
    const token = await AsyncStorage.getItem('token');
    if (!token) {
      Alert.alert("Authorization Error", "No token found. Please login again.");
      return;
    }

    const dateString = `${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}`;
    const url = `https://trakky.onrender.com/api/meal/breakfast/${dateString}`;

    try {
      const response = await axios.get(url, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      // Ensure the response data is an array
      const meals = Array.isArray(response.data) ? response.data : [response.data];
      setMealData(meals); // Update context with new data
    } catch (error) {
      if (error.response) {
        Alert.alert("Server Error", `Response Error: ${error.response.status} ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        Alert.alert("Network Error", "No response was received");
      } else {
        Alert.alert("Error", error.message);
      }
    }
  };

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
    fetchData(currentDate);

    console.log("Data set in context:", meals);
    setMealData(meals); // Update context with new data


  };

  useEffect(() => {
    fetchData(date);
  }, []);

  return (
    <View className="w-2/5">
      <TouchableOpacity
        onPress={() => setShowDatePicker(true)}
        className="rounded-lg flex-row p-1 bg-gray mt-4 mb-12 elevation-5 items-center justify-center"
      >
        <Text className="text-black text-base ml-2.5">{date.toLocaleDateString()}</Text>
        <FontAwesome name="calendar" className="text-black text-base pl-5 pr-2.5" />
      </TouchableOpacity>

      {showDatePicker && (
        <DateTimePicker
          value={date}
          mode="date"
          display="default"
          onChange={onDateChange}
          
        />
      )}
    </View>
  );
};

export default DateDisplay;
