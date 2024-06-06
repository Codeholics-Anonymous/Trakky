import axios from 'axios';
import { Text, View, TextInput, TouchableOpacity, Button, Alert } from 'react-native';
import { getUserData } from '../utils/Auth';
import { useState } from 'react';
import LoadingScreen from './LoadingScreen';

export function AddingProduct({ navigation }) {
  const [isLoading, setIsLoading] = useState(false);
  const [product, setProduct] = useState({
    name: "",
    protein: "",
    carbohydrates: "",
    fat: ""
  });

  const clearProduct = () => {
    setProduct({
      name: "",
      protein: "",
      carbohydrates: "",
      fat: ""
    });
  };

  const handleInputChange = (field, value) => {
    if (field !== 'name' && value !== '' && parseFloat(value) < 0) {
      Alert.alert('Invalid input', 'Please enter a non-negative number.');
      setProduct({
        ...product,
        [field]: ''
      });
    } else {
      setProduct({
        ...product,
        [field]: value
      });
    }
  };

  const handlePress = async () => {
    setIsLoading(true);
    const { token } = await getUserData();
    const config = {
      headers: {
        'Authorization': 'Token ' + token
      }
    };

    const productManagerUrl = 'https://trakky.onrender.com/api/product_manager/create_product/';
    const normalUrl = 'https://trakky.onrender.com/api/create_product/';

    try {
      // Try to create the product as a product manager
      await axios.post(productManagerUrl, product, config);
      setIsLoading(false);
      clearProduct();
      Alert.alert('Product created successfully as a product manager');
      navigation.pop();
    } catch (error) {
      try {
        // If the first request fails, try the normal route
        await axios.post(normalUrl, product, config);
        setIsLoading(false);
        clearProduct();
        Alert.alert('Product created successfully');
        navigation.pop();
      } catch (error) {
        clearProduct();
        setIsLoading(false);
        Alert.alert('Try again, something went wrong');
        navigation.pop();
      }
    }
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <View className="bg-gray-100 flex min-h-full flex-col px-6 py-12 lg:px-8">
      <View className="m-2">
        <Text>Name:</Text>
        <TextInput
          value={product.name}
          onChangeText={(text) => handleInputChange('name', text)}
          placeholder="Enter product name"
          style={{ borderWidth: 1, borderColor: '#ccc', padding: 8, borderRadius: 4 }}
        />
      </View>
      <View className="m-2">
        <Text>Protein:</Text>
        <TextInput
          value={product.protein}
          onChangeText={(text) => handleInputChange('protein', text)}
          placeholder="Enter protein amount"
          keyboardType="numeric"
          style={{ borderWidth: 1, borderColor: '#ccc', padding: 8, borderRadius: 4 }}
        />
      </View>
      <View className="m-2">
        <Text>Carbohydrates:</Text>
        <TextInput
          value={product.carbohydrates}
          onChangeText={(text) => handleInputChange('carbohydrates', text)}
          placeholder="Enter carbohydrates amount"
          keyboardType="numeric"
          style={{ borderWidth: 1, borderColor: '#ccc', padding: 8, borderRadius: 4 }}
        />
      </View>
      <View className="m-2">
        <Text>Fat:</Text>
        <TextInput
          value={product.fat}
          onChangeText={(text) => handleInputChange('fat', text)}
          placeholder="Enter fat amount"
          keyboardType="numeric"
          style={{ borderWidth: 1, borderColor: '#ccc', padding: 8, borderRadius: 4 }}
        />
      </View >
      <View className="m-2">
        <Button onPress={handlePress} title="Add Product" />
      </View>
    </View>
  );
}
