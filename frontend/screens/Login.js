import { Text, View, TextInput, TouchableOpacity, Button, Alert} from 'react-native';
import { Logo250x250 } from '../components/Logo250x250';
import { useState } from 'react';
import axios from 'axios';

export function Login( {navigation} ) {
  const [credentials, setCredentials] = useState({
    login: "", 
    password: ""
  });

  const handleLoginChange = (text) => {
    setCredentials({ ...credentials, login: text });
  };

  const handlePasswordChange = (text) => {
    setCredentials({ ...credentials, password: text });
  };

  const handleSubmit = () => {
    axios.post('http://127.0.0.1:8000/login/', {
      username: credentials.login,
      password: credentials.password
    })
    .then((response) =>{
      // save to local storage and stuff, change screen to homescreen, do later bcs stuff
    }, (error) => {
      Alert.alert("User not found, try again")
    })
  };

  return (
    <View className="bg-gray-100">
      <View className='flex min-h-full flex-col justify-center px-6 py-12 lg:px-8'>
        <View className='sm:mx-auto sm:w-full sm:max-w-sm'>
          <Logo250x250 className="mx-auto w-1/2"></Logo250x250>
          <Text className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-black">Login to your Account</Text>
        </View>
          
        <View className='m-2'>          
          <View className='flex items-center mx-8 space-y-4 '>
            <View className='bg-gray-100 p-5 rounded-full w-full border-2 border-dark-green shadow-xl shadow-dark-green'>
              <TextInput className='text-xl' placeholder='Login' value={credentials.login}
        onChangeText={handleLoginChange} />
            </View>

            <View className='bg-gray-100 p-5 rounded-full w-full border-2 border-dark-green shadow-xl shadow-dark-green'>
              <TextInput  className='text-xl' placeholder='Password'secureTextEntry value={credentials.password}
        onChangeText={handlePasswordChange}/>
            </View>
            
            <View className='w-full'>
              <TouchableOpacity className='bg-light-green p-3 rounded-full shadow-xl shadow-dark-green' onPress={handleSubmit}>
                <Text className='text-center text-xl font-bold'>Sign In</Text>
              </TouchableOpacity>
            </View>
          </View>

          <View className="fixed w-full p-4">
            <Text className='text-center'>Don`t have an account?</Text>
            <TouchableOpacity onPress={() => navigation.navigate("Register")}>
              <Text title="Sign Up!" className='text-center text-xl text-dark-green'>Sign Up!</Text>
            </TouchableOpacity>

          </View>
        </View>
      </View> 
    </View>
  )
}