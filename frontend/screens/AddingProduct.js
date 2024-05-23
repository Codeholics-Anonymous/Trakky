import axios from 'axios';
import { Text, View, TextInput, TouchableOpacity, Button } from 'react-native';

export function AddingProduct({ navigation }) {
  const token = "7b903ccfd8d8596d45d4b4a3edd43f4d4c58865e";

  const handlePress = () => {
      axios.get('https://trakky.onrender.com/api/basic_demand/', {
        headers: {
          'Authorization' : 'Token ' + token
        }
      }).then((response) =>{
        console.log(response.data);
      }, (error) => {
        console.log(error)
        Alert.alert("Error, try again")
      })
  }
  
  return (
    <View>
      <Button onPress={handlePress} title="aaa" />
    </View>
  )
}