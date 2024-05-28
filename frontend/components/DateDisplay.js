import DateTimePicker from '@react-native-community/datetimepicker';
import React, { useState } from 'react';
import { Dimensions, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import { useMealData } from './MealDataContext'; // Adjust path as necessary

const { width } = Dimensions.get('window');

const DateDisplay = ( {creationDate} ) => {
  const [showDatePicker, setShowDatePicker] = useState(false);
  const { date, setDate, fetchData } = useMealData(); // Use date and fetchData from context

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
    fetchData(currentDate); // Fetch data for the new date
  };

  function parseDateString(dateString) {
    // Split the string by the dash delimiter
    const [year, month, day] = dateString.split('-');
  
    // Create and return a new Date object
    // Note: Month in JavaScript Date is zero-indexed (0 = January, 1 = February, ..., 11 = December)
    return new Date(parseInt(year, 10), parseInt(month, 10) - 1, parseInt(day, 10));
  }


  return (
    <View style={{ width: width * 0.4 }}>
      <TouchableOpacity
        onPress={() => setShowDatePicker(true)}
        className="rounded-lg flex-row p-1 bg-gray mt-4 mb-12 elevation-5 items-center justify-center"
      >
        <Text className="text-black text-base">
          {date.toLocaleDateString()}
        </Text>
        <FontAwesome name="calendar" className="text-black text-base pl-3" />
      </TouchableOpacity>

      {showDatePicker && (
        <DateTimePicker
          value={date}
          mode="date"
          display="default"
          onChange={onDateChange}
          minimumDate={parseDateString(creationDate)}
          maximumDate={new Date()} // Limit the maximum selectable date to today
        />
      )}
    </View>
  );
};

export default DateDisplay;
