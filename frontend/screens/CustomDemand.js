import React, { useState } from "react";
import { View, TextInput, Button, Alert } from "react-native";
import axios from "axios";
import LoadingScreen from './LoadingScreen';
import { getUserData } from "../utils/Auth";

export function CustomDemand( {navigation} ) {
  const [isLoading, setIsLoading] = useState(false);
  const [userProfileData, setUserProfileData] = useState({
    fat: '',
    carbs: '',
    protein: ''
  });

  const handleChange = (key, val) => {
    if (val === '' || parseFloat(val) >= 0) {
      setUserProfileData(prevState => ({ ...prevState, [key]: val }));
    } else {
      Alert.alert('Invalid input', 'Please enter a non-negative number.');
      setUserProfileData(prevState => ({ ...prevState, [key]: '' }));
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);

    try {
      const { token } = await getUserData();
      const config = {
        headers: {
          'Authorization': 'Token ' + token
        }
      };

      const demandUrl = 'https://trakky.onrender.com/api/create_demand/';

      await axios.post(demandUrl, {
        fat : parseFloat(userProfileData.fat),
        protein : parseFloat(userProfileData.protein),
        carbohydrates : parseFloat(userProfileData.carbs),
        daily_calory_demand : parseFloat(userProfileData.fat) * 9 + parseFloat(userProfileData.protein) * 4 + parseFloat(userProfileData.carbs) * 4

      }, config);
      console.log('Demand created successfully.');
      // Add further logic here for handling successful response
    } catch (error) {
      console.error('Error creating demand:', error);
      // Add further error handling logic here
    } finally {
      setIsLoading(false);
      navigation.reset({
        index: 0,
        routes: [{name: 'HomeScreen'}]
      });
    }
  };

  const handleBackToBasic = async () => {
    setIsLoading(true);
  
    try {
      const { token } = await getUserData();
      const config = {
        headers: {
          'Authorization': 'Token ' + token
        }
      };

      console.log(token)
  
      const basicDemandUrl = 'https://trakky.onrender.com/api/basic_demand/';
  
      const response = await axios.get(basicDemandUrl, config);
      const { protein, carbohydrates, fat, demand } = response.data;
  
      const demandUrl = 'https://trakky.onrender.com/api/create_demand/';
  
      await axios.post(demandUrl, {
        fat: fat,
        protein: protein,
        carbohydrates: carbohydrates,
        daily_calory_demand: demand
      }, config);
  
      console.log('Demand created successfully.');
      // Add further logic here for handling successful response
    } catch (error) {
      console.error('Error creating demand:', error);
      // Add further error handling logic here
    } finally {
      setIsLoading(false);
      navigation.reset({
        index: 0,
        routes: [{ name: 'HomeScreen' }]
      });
    }
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <View className="bg-gray-100 flex min-h-full flex-col px-6 py-12 lg:px-8">
      <View className="m-2">
        <TextInput
          placeholder="Enter Custom Fat Demand"
          keyboardType="numeric"
          value={userProfileData.fat}
          onChangeText={(val) => handleChange("fat", val)}
        />
      </View>
      <View className="m-2">
        <TextInput
          placeholder="Enter Custom Carbs Demand"
          keyboardType="numeric"
          value={userProfileData.carbs}
          onChangeText={(val) => handleChange("carbs", val)}
        />
      </View>
      <View className="m-2">
        <TextInput
          placeholder="Enter Custom Protein Demand"
          keyboardType="numeric"
          value={userProfileData.protein}
          onChangeText={(val) => handleChange("protein", val)}
        />
      </View>
      <View className="m-2">
        <Button title='Set Basic Demand' onPress={handleBackToBasic} />
      </View>
      <View className="m-2">
        <Button 
          title="Submit"
          onPress={() => {
            handleSubmit()
          }}
        />
      </View>
    </View>
  );
}
