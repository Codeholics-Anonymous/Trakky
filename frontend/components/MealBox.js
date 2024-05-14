import React, { useState } from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import CommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

const MealBox = ({ title }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <View className="w-11/12 mt-4 shadow-lg relative">
      <TouchableOpacity
        className={`flex flex-row items-center border-2 border-black bg-light-gray h-16 mb-1 px-4 ${expanded ? 'rounded-t-lg' : 'rounded-lg'}`}
        onPress={() => setExpanded(!expanded)}
        >

        <TouchableOpacity>
          <CommunityIcons name="plus-circle" className="text-dark-green text-4xl"/>
        </TouchableOpacity>
        
        <Text className="text-dark-dark-gray pl-4 text-xl font-bold flex-1">{title}</Text>
        
        <View className="absolute right-5 top-0 h-full flex flex-col justify-center">
          <Text className="text-dark-dark-gray text-s">200kcal</Text>
        </View>

      </TouchableOpacity>

      {/* expanded part after pressing button */}
      {expanded && (
        <View className="border-2 border-t-0 border-black rounded-b-lg bg-light-gray p-4">
          <View className="p-1 m-1 bg-light-green"><Text className="text-dark-dark-gray text-base">Content 1</Text></View>
          <View className="p-1 m-1 bg-light-green"><Text className="text-dark-dark-gray text-base">Content 2</Text></View>
          <View className="p-1 m-1 bg-light-green"><Text className="text-dark-dark-gray text-base">Content 3</Text></View>
        </View>
      )}
    </View>
  );
};

export default MealBox;
