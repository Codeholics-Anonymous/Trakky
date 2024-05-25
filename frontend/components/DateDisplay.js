import DateTimePicker from '@react-native-community/datetimepicker';
import React, { useState } from 'react';
import { Dimensions, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import { useMealData } from './MealDataContext'; // Adjust path as necessary

const { width } = Dimensions.get('window');

const DateDisplay = () => {
  const [showDatePicker, setShowDatePicker] = useState(false);
  const { date, setDate, fetchData } = useMealData(); // Use date and fetchData from context

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
    fetchData(currentDate); // Fetch data for the new date
  };

  return (
    <View style={{ width: width * 0.4 }}>
      <TouchableOpacity
        onPress={() => setShowDatePicker(true)}
        className="rounded-lg flex-row p-1 bg-gray mt-4 mb-12 elevation-5 items-center justify-center"
      >
        <Text style={{ color: 'black', fontSize: 16, marginLeft: 10 }}>
          {date.toLocaleDateString()}
        </Text>
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
