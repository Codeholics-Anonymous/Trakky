import React, { useState } from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import CommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

const MealBox = ({ title }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <View className="w-11/12 mb-4 relative">
      <TouchableOpacity
        className={`flex flex-row items-center bg-gray h-16 mb-1 px-4 rounded-lg`}
        onPress={() => setExpanded(!expanded)}
        style={{elevation: 18}}
        >

        <TouchableOpacity>
          <CommunityIcons name="plus-circle" className="text-dark-green text-4xl"/>
        </TouchableOpacity>
        
        <Text className="text-black pl-4 text-xl font-bold flex-1">{title}</Text>
        
        <View className="absolute right-5 top-0 h-full flex flex-col justify-center">
          <Text className="text-black text-s">200kcal</Text>
        </View>

      </TouchableOpacity>

      {/* expanded part after pressing button */}
      {expanded && (
        <View className="rounded-lg bg-lgt-gray p-4" style={{ elevation: 5 }}>
          <View className="p-1 m-1 bg-lgt-gray flex flex-row justify-between items-center">
            <Text className="text-black text-base">Content 1</Text>
            <Text className="text-black text-s">299kcal</Text>
          </View>
          <View className="p-1 m-1 bg-lgt-gray flex flex-row justify-between items-center">
            <Text className="text-black text-base">Content 2</Text>
            <Text className="text-black text-s">299kcal</Text>
          </View>
          <View className="p-1 m-1 bg-lgt-gray flex flex-row justify-between items-center">
            <Text className="text-black text-base">Content 3</Text>
            <Text className="text-black text-s">299kcal</Text>
          </View>
        </View>
      )}
    </View>
  );
};

export default MealBox;

