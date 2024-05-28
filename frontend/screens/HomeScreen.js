import { useEffect, useState } from 'react';
import { SafeAreaView, ScrollView, StatusBar } from 'react-native';
import DateDisplay from '../components/DateDisplay';
import Header from '../components/Header';
import MealBox from '../components/MealBox';
import { MealDataProvider } from '../components/MealDataContext'; // Adjust path as necessary
import ProgressCircle from '../components/ProgressCircle';
import LoadingScreen from './LoadingScreen';
import { getUserData } from '../utils/Auth'
import axios from 'axios';

export function HomeScreen({ navigation }) {
  const [creationDate, setCreationDate] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    StatusBar.setBackgroundColor('#363636', true);
    StatusBar.setBarStyle('light-content', true);

    const fetchCreationDate = async () => {
      try {
        setIsLoading(true)
        const { token } = await getUserData();
        const config = {
          headers: {
            'Authorization': 'Token ' + token
          }
        };
        const response = await axios.get('https://trakky.onrender.com/user/account_creation_date/', config);
        setCreationDate(response.data.date);
        setIsLoading(false)
      } catch (error) {
        setIsLoading(false)
        console.error('Error fetching the creation date:', error);
      }
    };

    fetchCreationDate();
  }, []);

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <MealDataProvider>
      <SafeAreaView className="bg-light-green flex-1" style={{ flex: 1, paddingTop: StatusBar.currentHeight }}>
        <ScrollView className="w-full" contentContainerStyle={{ flexGrow: 1, alignItems: 'center' }}>
          <Header navigation={navigation}/>
          <ProgressCircle creationDate={creationDate} />
          <DateDisplay creationDate={creationDate} />
          <MealBox title="Breakfast"/>
          <MealBox title="Lunch"/>
          <MealBox title="Dinner"/>
        </ScrollView>
      </SafeAreaView>
    </MealDataProvider>
  );
}
