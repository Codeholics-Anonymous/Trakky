import React, { useEffect, useState } from 'react';
import { Modal, Pressable, Text, TextInput, TouchableOpacity, View } from 'react-native';
import CommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { useMealData } from './MealDataContext'; // Adjust path as necessary

const MealBox = ({ title }) => {
  const [expanded, setExpanded] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const { mealData } = useMealData();
  const [productName, setProductName] = useState('');
  const [productCalories, setProductCalories] = useState('');
  const [content, setContent] = useState([]);

  const addContent = () => {
    if (productName && productCalories) {
      const newProduct = { name: productName, calories: parseInt(productCalories) };
      setContent([...content, newProduct]);
      setProductName('');
      setProductCalories('');
      setModalVisible(false);
    }
  };

  // Helper function to flatten the data structure
  const flattenMealData = (data) => {
    return Object.values(data).map(item => ({
      name: item.name,
      calories: item.calories,
      protein: item.protein,
      carbohydrates: item.carbohydrates,
      fat: item.fat,
      grams: item.grams,
    }));
  };

  // Filter the meal data based on the title of the MealBox
  const filteredMealData = mealData[title.toLowerCase()] || {};

  // Flattened data for rendering
  const flattenedData = flattenMealData(filteredMealData);

  // Combined data from fetched and manually added products
  const combinedData = [...flattenedData, ...content];

  // Calculate total calories using reduce, handle case where combinedData may be empty or improperly formatted
  const totalCalories = combinedData.reduce((total, item) => total + (item.calories || 0), 0);

  useEffect(() => {
    console.log("Meal data received in MealBox:", mealData);
  }, [mealData]); // Dependencies array ensures this only re-runs if mealData changes

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
          {combinedData.map((item, index) => (
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
