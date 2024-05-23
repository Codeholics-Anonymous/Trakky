import { Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import { Logo250x250 } from '../components/Logo250x250';
import { useState } from 'react';

export function Register( {navigation} ) {
  const [credentials, setCredentials] = useState({
    login: "", 
    password: ""
  });

  function passwordValidation(password) {
    // Check if password is alphanumeric and has at least 8 characters
    if (!password.match(/^[a-zA-Z0-9]{8,}$/) || password.match(/^\d+$/)) {
        return 0;
    }

    // Check if password contains at least one digit
    let containDigit = false;
    for (let i = 0; i < password.length; i++) {
        if (!isNaN(parseInt(password[i]))) {
            containDigit = true;
            break;
        }
    }

    if (!containDigit) {
        return 0;
    }

    return 1;
  }

  const handleLoginChange = (text) => {
    setCredentials({ ...credentials, login: text });
  };

  const handlePasswordChange = (text) => {
    setCredentials({ ...credentials, password: text });
  };

  const handleSubmit = () => {
    if(passwordValidation(credentials.password)) {
      navigation.navigate("UserDetails", {
        login: credentials.login,
        password: credentials.password
      })
    } else {
      Alert.alert("Password must be alphanumeric, at least 8 characters long, and contain at least one digit.")
      setCredentials({login: credentials.login, password: ""})
    }
  }
  
  return (
    <View className="bg-gray-100">
      <View className='flex min-h-full flex-col justify-center px-6 py-12 lg:px-8'>
        <View className='sm:mx-auto sm:w-full sm:max-w-sm'>
          <Logo250x250 className="mx-auto w-1/2"></Logo250x250>
          <Text className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-black">Create your Account</Text>
        </View>
          
        <View className='m-2'>          
          <View className='flex items-center mx-8 space-y-4'>
            <View className='bg-gray-100 p-5 rounded-full w-full border-2 border-dark-green shadow-xl shadow-dark-green'>
              <TextInput className='text-xl' placeholder='Login' value={credentials.login}
        onChangeText={handleLoginChange} />
            </View>

            <View className='bg-gray-100 p-5 rounded-full w-full border-2 border-dark-green shadow-xl shadow-dark-green'>
              <TextInput  className='text-xl' placeholder='Password'secureTextEntry value={credentials.password}
        onChangeText={handlePasswordChange}/>
            </View>
            <View className='w-full' >
              <TouchableOpacity className='bg-light-green p-3 rounded-full shadow-xl shadow-dark-green ' onPress={handleSubmit}>
                <Text className='text-center text-xl font-bold'>Sign Up</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </View>
    </View>
  )
}