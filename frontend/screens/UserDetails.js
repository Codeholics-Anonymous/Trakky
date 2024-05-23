import { Text, View, TextInput, TouchableOpacity, Button, Alert } from 'react-native';
import { Logo250x250 } from '../components/Logo250x250';
import { SelectList } from 'react-native-dropdown-select-list'
import DateTimePicker from '@react-native-community/datetimepicker';
import axios from 'axios';
import { useState } from 'react';
import { saveUserData } from '../utils/Auth'

export function UserDetails({ route, navigation }) {
  const { login, password } = route.params;

  const [userProfileData, setUserProfileData] = useState({
    sex: "",
    birthDate: new Date(),
    workType: 0,
    weight: 0,
    height: 0,
    userGoal: 0
  });

  const [showDatePicker, setShowDatePicker] = useState(false);

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || userProfileData.birthDate;
    setShowDatePicker(false);
    setUserProfileData(prevState => ({ ...prevState, birthDate: currentDate }));
  };

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const handleSubmit = () => {
    const formattedBirthDate = formatDate(userProfileData.birthDate); // Assuming formatDate function exists as defined previously
  
    axios.post(`https://trakky.onrender.com/register/`, {
      register_data: {
        username: login,
        password: password
      },
      userprofile_data: {
        sex: userProfileData.sex,
        birth_date: formattedBirthDate,
        work_type: userProfileData.workType,
        weight: userProfileData.weight,
        height: userProfileData.height,
        user_goal: userProfileData.userGoal
      }
    })
    .then(async (response) => {
      Alert.alert("Singed In successfully")
      await saveUserData(response.data.token, response.data.user.username);

      navigation.reset({
        index: 0,
        routes: [{name: 'HomeScreen'}]
      });
    })
    .catch((error) => {
      navigation.pop();
      Alert.alert("Error", "Something went wrong. Please try again.");
    });
  };

  return (
    <View className="bg-gray-100 flex min-h-full flex-col px-6 py-12 lg:px-8">
      <View className="m-2">
        <SelectList
          data={[{ key: 'M', value: 'Male' }, { key: 'F', value: 'Female' }, { key: 'O', value: 'Other' }]}
          setSelected={(val) => setUserProfileData(prevState => ({ ...prevState, sex: val }))}
          placeholder="Select Sex"
        />
      </View>
      <View className="m-2">
        <SelectList 
          data={[{ key: 1, value: 'Physical Worker' }, { key: 0, value: 'Intellectual Worker' }]}
          setSelected={(val) => setUserProfileData(prevState => ({ ...prevState, workType: val }))}
          placeholder="Select Work Type"
        />
      </View>
      <View className="m-2">
        <TextInput
          placeholder="Enter Weight"
          keyboardType="numeric"
          onChangeText={(val) => setUserProfileData(prevState => ({ ...prevState, weight: parseFloat(val) }))}
        />
      </View>
      <View className="m-2">
        <TextInput
          placeholder="Enter Height"
          keyboardType="numeric"
          onChangeText={(val) => setUserProfileData(prevState => ({ ...prevState, height: parseFloat(val) }))}
        />
      </View>

      <View className="m-2">
        <SelectList 
          data={[
            { key: -1, value: 'Lose Weight' },
            { key: 0, value: 'Maintain Weight' },
            { key: 1, value: 'Gain Weight' }
          ]}
          setSelected={(val) => setUserProfileData(prevState => ({ ...prevState, userGoal: val }))}
          placeholder="Select User Goal"
        />
      </View>
     
      <View className="m-2">
        <Button title="Select Birth Date" onPress={() => setShowDatePicker(true)} />
        {showDatePicker && (
          <DateTimePicker
            value={userProfileData.birthDate}
            mode="date"
            display="default"
            onChange={onDateChange}
          />
        )}
      </View>
      <View className="m-2">
        <Button 
          title="Submit"
          onPress={() => {
            handleSubmit()
          }}
        />
      </View>
    </View>
  );
}