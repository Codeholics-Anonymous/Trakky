import axios from 'axios';
import { Text, View, TextInput, TouchableOpacity, Button } from 'react-native';

export function AddingProduct({ navigation }) {
  const token = ""; // token you get after login in 

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