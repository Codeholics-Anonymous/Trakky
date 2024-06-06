import React, { useEffect, useState } from 'react';
import { Modal, Pressable, ScrollView, Text, TextInput, TouchableOpacity, View } from 'react-native';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import CommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import LoadingScreen from '../screens/LoadingScreen';
import { useMealData } from './MealDataContext'; // Adjust path as necessary

const MealBox = ({ title }) => {
  const [expanded, setExpanded] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const { mealData, searchResults, searchProducts, searchError, createMealItem, deleteMealItem, date } = useMealData();
  const [content, setContent] = useState([]);
  const [searchQuery, setSearchQuery] = useState(''); // State for search query
  const [gramAmount, setGramAmount] = useState(''); // State for gram amount
  const [isLoading, setIsLoading] = useState(false);

  const addContent = (product) => {
    if (product && gramAmount) {
      const dateString = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
      createMealItem(title.toLowerCase(), dateString, product.product_id, parseInt(gramAmount));
      setModalVisible(false);
      setGramAmount('');
    }
  };

  const handleDelete = (mealItemId) => {
    deleteMealItem(mealItemId);
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
      mealitem_id: item.mealitem_id
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
    const fetchData = async () => {
      setIsLoading(true);  // Set loading to true before fetching data
      try {
        // Simulate fetching data
        console.log("Meal data received in MealBox:", flattenedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);  // Set loading to false after fetching data
      }
    };

    fetchData();
  }, [mealData]); // Dependencies array ensures this only re-runs if mealData changes
  
  if (isLoading) {
    return <LoadingScreen />;
  }

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
              <View className="flex flex-row items-center">
                <TouchableOpacity onPress={() => handleDelete(item.mealitem_id)}>
                  <FontAwesome5 name="times-circle" className="text-red-500 text-xl mr-2" />
                </TouchableOpacity>
                <Text className="text-black text-base">{item.name}</Text>
              </View>
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
              value={searchQuery}
              onChangeText={(text) => {
                setSearchQuery(text);
                searchProducts(text);
              }}
              className="border-b border-black mb-2"
            />
            <TextInput
              placeholder="Gram Amount"
              value={gramAmount}
              onChangeText={setGramAmount}
              keyboardType="numeric"
              className="border-b border-black mb-2"
            />
            {searchError ? (
              <Text className="text-red-500">{searchError}</Text>
            ) : (
              <ScrollView className="max-h-60">
                {searchResults.map((product, index) => (
                  <Pressable
                    key={index}
                    className="p-2 bg-white my-1 rounded-lg"
                    onPress={() => addContent(product)}
                  >
                    <Text className="text-black">{product.name}</Text>
                  </Pressable>
                ))}
              </ScrollView>
            )}
            <Pressable
              className="bg-dark-green rounded-lg p-2 mt-4"
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
