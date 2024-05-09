import { Text, View, TextInput, TouchableOpacity } from 'react-native';
import React from 'react';
import { StatusBar } from 'expo-status-bar';

export const Login = () => {
  return (
    <View className='bg-gray-50'>
      <View className='flex min-h-full flex-col justify-center px-6 py-12 lg:px-8'>
        <View className='sm:mx-auto sm:w-full sm:max-w-sm'>
          <Text className="text-black text-6xl font-bold text-center m-10">LOGO</Text>
          <Text className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Login in to your account</Text>
        </View>
          
        <View className='m-2'>          
          <View className='flex items-center mx-8 space-y-4'>
            <View className='bg-gray-100 p-5 rounded-2xl w-full border border-gray-800 shadow-inner'>
              <TextInput className='text-xl' placeholder='Enter Login' />
            </View>

            <View className='bg-gray-100 p-5 rounded-2xl w-full mb-3 border border-gray-800 shadow-inner'>
              <TextInput  className='text-xl' placeholder='Enter Password'secureTextEntry/>
            </View>
            
            <View className='w-full'>
              <TouchableOpacity className='bg-green-200 p-3 rounded-2xl'>
                <Text className='text-center text-xl font-bold'>Login</Text>
              </TouchableOpacity>
            </View>
          </View>

          <View>
            <Text className='text-center'>Don`t have account?</Text>
            <Text className='text-center'>Register Now!</Text>
          </View>
        </View>
      </View>
    </View>
  )
}