import DateTimePicker from '@react-native-community/datetimepicker';
import React, { useState } from 'react';
import { Dimensions, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

const { width } = Dimensions.get('window');

const DateDisplay = () => {
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [date, setDate] = useState(new Date());

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
  };

  return (
    <View className="w-2/5">
      <TouchableOpacity
        onPress={() => setShowDatePicker(true)}
        className="rounded-lg flex-row p-1 bg-gray mt-4 mb-12 elevation-5 items-center justify-center"
      >
        <Text className="text-black text-base ml-2.5">{date.toLocaleDateString()}</Text>
        <FontAwesome name="calendar" className="text-black text-base pl-5 pr-2.5"/>
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
