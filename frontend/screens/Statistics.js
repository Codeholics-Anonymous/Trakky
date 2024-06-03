import React, { useState, useEffect } from "react";
import { View, Text, Button } from "react-native";
import { getUserData } from '../utils/Auth';
import LoadingScreen from './LoadingScreen';
import axios from "axios";
import DateTimePicker from '@react-native-community/datetimepicker';

export function Statistics({ navigation }) {
  const [creationDate, setCreationDate] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [showDatePickerLeft, setshowDatePickerLeft] = useState(false);
  const [showDatePickerRight, setshowDatePickerRight] = useState(false);
  const [summaryData, setSummaryData] = useState(null);
  const [demandData, setDemandData] = useState(null);
  const [showResult, setShowResult] = useState(false);

  function parseDateString(dateString) {
    const [year, month, day] = dateString.split('-');
    return new Date(parseInt(year, 10), parseInt(month, 10) - 1, parseInt(day, 10));
  }

  useEffect(() => {
    const fetchCreationDate = async () => {
      try {
        setIsLoading(true);
        const { token } = await getUserData();
        const config = { headers: { 'Authorization': 'Token ' + token }};
        const response = await axios.get('https://trakky.onrender.com/user/account_creation_date/', config);
        setCreationDate(response.data.date);
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        console.error('Error fetching the creation date:', error);
      }
    };

    fetchCreationDate();
  }, []);

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const { token } = await getUserData();
      const config = { headers: { 'Authorization': 'Token ' + token }};

      const startDateFormatted = formatDate(startDate);
      const endDateFormatted = formatDate(endDate);

      const summaryResponse = await axios.get(`https://trakky.onrender.com/api/summary/${startDateFormatted}/${endDateFormatted}/`, config);
      const demandResponse = await axios.get(`https://trakky.onrender.com/api/demand/${startDateFormatted}/${endDateFormatted}/`, config);

      setSummaryData(summaryResponse.data);
      setDemandData(demandResponse.data);
      setShowResult(true);
      setIsLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error);
      setIsLoading(false)
    }
  };

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const onStartDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || startDate;
    setshowDatePickerLeft(false);
    setStartDate(currentDate);
  };

  const onEndDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || endDate;
    setshowDatePickerRight(false);
    setEndDate(currentDate);
  };

  if (isLoading) {
    return <LoadingScreen />;
  }
  
  return (
    <View className="bg-gray-100 flex min-h-full flex-col px-6 py-12 lg:px-8">
      <View className="m-2">
        <Button title="Select start date" onPress={() => setshowDatePickerLeft(true)} />
        {showDatePickerLeft &&  
          <DateTimePicker
          value={startDate}
          mode="date"
          display="default"
          onChange={onStartDateChange}
          minimumDate={parseDateString(creationDate)}
          maximumDate={endDate}
          />
        }
      </View>
      <View className="m-2">
        <Button title="Select end date" onPress={() => setshowDatePickerRight(true)} />
        {showDatePickerRight &&  
          <DateTimePicker
          value={endDate}
          mode="date"
          display="default"
          onChange={onEndDateChange}
          minimumDate={startDate}
          maximumDate={new Date()}
          />
        }
      </View>
      <View className="m-2">
        <Button title="Submit" onPress={handleSubmit} />
      </View>
      {showResult && summaryData && demandData && (
        <View className="m-2">
          <Text>Proteins: {summaryData.summary_protein_sum} / {demandData.demand_protein_sum}</Text>
          <Text>Carbohydrates: {summaryData.summary_carbohydrates_sum} / {demandData.demand_carbohydrates_sum}</Text>
          <Text>Fat: {summaryData.summary_fat_sum} / {demandData.demand_fat_sum}</Text>
          <Text>Calories: {summaryData.summary_calories_sum} / {demandData.demand_calories_sum}</Text>
        </View>
      )}
    </View>
  );
}
