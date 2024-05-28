import { View, Text, TouchableOpacity, Alert } from "react-native"
import { useState } from "react";
import { resetUserData, getUserData } from "../utils/Auth"
import axios from 'axios';
import LoadingScreen from './LoadingScreen';

export function Settings({ navigation }) {
  const [isLoading, setIsLoading] = useState(false);
  const handleLogout = async () => {
    setIsLoading(true);
    const { token } = await getUserData();
    const config = {
      headers: {
        'Authorization': 'Token ' + token
      }
    };
  
    try {
      // Sending the logout request to the server
      await axios.post('https://trakky.onrender.com/logout/', null, config);
      console.log('Logout successful');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  
    // Resetting user data and navigating to the login screen
    await resetUserData();
    setIsLoading(false);
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }]
    });
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <View className="bg-gray-100 flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 ">
      <TouchableOpacity className='bg-light-green p-3 rounded-full shadow-xl shadow-dark-green my-4' onPress={() => {navigation.navigate("AddingProduct")}}>
        <Text className='text-center text-xl font-bold'>Add Product</Text>
      </TouchableOpacity>
      
      <TouchableOpacity className='bg-light-green p-3 rounded-full shadow-xl shadow-dark-green my-4' onPress={() => {navigation.navigate("SettingsUser")}}>
        <Text className='text-center text-xl font-bold'>Change User Data</Text>
      </TouchableOpacity>
      <TouchableOpacity className='bg-light-green p-3 rounded-full shadow-xl shadow-dark-green my-4' onPress={handleLogout}>
        <Text className='text-center text-xl font-bold'>Logout</Text>
      </TouchableOpacity>
    </View>
  )
}