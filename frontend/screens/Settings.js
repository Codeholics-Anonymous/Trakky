import { View, Text, TouchableOpacity, Alert } from "react-native"
import { resetUserData } from "../utils/Auth"
import { useEffect, useState } from "react";
import { getUserData } from "../utils/Auth";
import axios from 'axios';

export function Settings({ navigation }) {
  const handleLogout = async () => {
    await resetUserData();
    navigation.reset({
      index: 0,
      routes: [{name: 'Login'}]
    });
  }

  const [isManager, setIsManager] = useState(false);

  useEffect(() => {
    const checkIfManager = async () => {
      try {
        const { token } = await getUserData(); // Make sure getUserData() is defined and returns an object with token
        const response = await axios.get('https://trakky.onrender.com/user/is_product_manager', {
          headers: {
            'Authorization': 'Token ' + token
          }
        });
        
        if (response.data.manager === 1) {
          setIsManager(true);
        }
      } catch (error) {
        console.log(error)
      }
    };

    checkIfManager();
  }, []); 

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
      {isManager && (
        <View>
          <Text>Welcome, Manager!</Text>
        </View>
      )}
    </View>
  )
}