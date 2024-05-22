import React, { useState } from 'react';
import { Modal, Pressable, Text, TextInput, TouchableOpacity, View } from 'react-native';
import CommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

const MealBox = ({ title }) => {
  const [expanded, setExpanded] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [content, setContent] = useState([]);
  const [productName, setProductName] = useState('');
  const [productCalories, setProductCalories] = useState('');

  const addContent = () => {
    if (productName && productCalories) {
      setContent([...content, { name: productName, calories: parseInt(productCalories) }]);
      setProductName('');
      setProductCalories('');
      setModalVisible(false);
    }
  };

  const totalCalories = content.reduce((total, item) => total + item.calories, 0);

  return (
    <View className="w-11/12 mb-4 relative">
      <TouchableOpacity
        className="flex flex-row items-center bg-gray h-16 mb-1 px-4 rounded-lg"
        onPress={() => setExpanded(!expanded)}
        style={{ elevation: 18 }}
      >
        <TouchableOpacity onPress={() => setModalVisible(true)}>
          <CommunityIcons name="plus-circle" className="text-dark-green text-4xl" />
        </TouchableOpacity>

        <Text className="text-black pl-4 text-xl font-bold flex-1">{title}</Text>

        <View className="absolute right-5 top-0 h-full flex flex-col justify-center">
          <Text className="text-black text-s">{totalCalories} kcal</Text>
        </View>
      </TouchableOpacity>

      {expanded && (
        <View className="rounded-lg bg-lgt-gray p-4" style={{ elevation: 5 }}>
          {content.map((item, index) => (
            <View key={index} className="p-1 m-1 bg-lgt-gray flex flex-row justify-between items-center">
              <Text className="text-black text-base">{item.name}</Text>
              <Text className="text-black text-s">{item.calories} kcal</Text>
            </View>
          ))}
        </View>
      )}

      <Modal
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(!modalVisible)}
      >
        <View className="flex-1 justify-center items-center bg-black/80">
          <View className="bg-lgt-gray p-6 rounded-lg w-3/5">
            <Text className="text-xl mb-4">Add Product</Text>
            <TextInput
              placeholder="Product Name"
              value={productName}
              onChangeText={setProductName}
              className="border-b border-black mb-4"
            />
            <TextInput
              placeholder="Calories"
              value={productCalories}
              onChangeText={setProductCalories}
              keyboardType="numeric"
              className="border-b border-black mb-10"
            />
            <Pressable
              className="bg-light-green rounded-lg p-2 mb-2"
              onPress={addContent}
            >
              <Text className="text-white text-center">Add</Text>
            </Pressable>
            <Pressable
              className="bg-dark-green rounded-lg p-2"
              onPress={() => setModalVisible(false)}
            >
              <Text className="text-white text-center">Cancel</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </View>
  );
};

export default MealBox;
