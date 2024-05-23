import { View, Text, TouchableOpacity } from "react-native"
import { resetUserData } from "../utils/Auth"

export function Settings({ navigation }) {
  const handleLogout = async () => {
    await resetUserData();
    navigation.reset({
      index: 0,
      routes: [{name: 'Login'}]
    });
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