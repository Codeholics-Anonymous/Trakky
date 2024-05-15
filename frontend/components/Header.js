import React from 'react';
import { Image, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

const Header = () => {
  return (
    <View className="bg-dark-green flex-row items-center justify-start w-full h-7.5 p-4" style={{elevation: 15}}>
      {/* logo */}
      <View className="flex-row items-center absolute left-0 right-0 justify-center">
        <Image source={require('../assets/LOGO.png')} className="mr-3 w-7"
            style={{ resizeMode: 'contain' }} />
        <Text className="text-white text-lg font-bold">TRAKKY</Text>
      </View>
      {/* settings icon */}
      <TouchableOpacity className="ml-auto mr-2">
        <FontAwesome name="bars" size={34} className="text-gray"/>
      </TouchableOpacity>
      </View>
  );
};

export default Header;
