import axios from 'axios';
import { Text, View, TextInput, TouchableOpacity, Button } from 'react-native';
import { getUserData } from '../utils/Auth';

export function AddingProduct({ navigation }) {
  
  const handlePress = async () => {
    const { token } = await getUserData();    
    axios.get('https://trakky.onrender.com/api/basic_demand/', {
        headers: {
          'Authorization' : 'Token ' + token
        }
      }).then((response) =>{
        console.log(response.data);
      }, (error) => {
        Alert.alert("Error, try again")
      })
  }
  
  return (
    <View>
      <Button onPress={handlePress} title="aaa" />
    </View>
  )
}