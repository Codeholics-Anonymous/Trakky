import axios from 'axios';
import { Text, View, TextInput, TouchableOpacity, Button } from 'react-native';
import { getUserData } from '../utils/Auth';

export function AddingProduct({ navigation }) {
  const [product, setProduct] = ({
    name: "",
    protein: 0,
    carbohydrates: 0,
    fat: 0
  });

  const handlePress = async () => {
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
        console.log('Product created successfully as a product manager.');
    } catch (error) {        
        try {
            // If the first request fails, try the normal route
            await axios.post(normalUrl, product, config);
            console.log('Product created successfully via normal route.');
        } catch (error) {
            console.error('Failed to create product via normal route.', error);
        }
    }
  }
  
  return (
    <View>
      <Button onPress={handlePress} title="aaa" />
    </View>
  )
}