import { useEffect, useState } from 'react';
import { SafeAreaView, ScrollView, StatusBar } from 'react-native';
import DateDisplay from '../components/DateDisplay';
import Header from '../components/Header';
import MealBox from '../components/MealBox';
import { MealDataProvider } from '../components/MealDataContext'; // Adjust path as necessary
import ProgressCircle from '../components/ProgressCircle';

export function HomeScreen({ navigation }) {
  const [showDefaultProgress, setShowDefaultProgress] = useState(true);

  const toggleProgress = () => {
    console.log('Toggle pressed');
    setShowDefaultProgress(!showDefaultProgress);
  };

  useEffect(() => {
    StatusBar.setBackgroundColor('#363636', true);
    StatusBar.setBarStyle('light-content', true);
  }, []);

  const [howMuchEaten, sethowMuchEaten] = useState({
    protein: 0,
    carb : 0,
    fat: 0
  })

  return (
    <MealDataProvider>
      <SafeAreaView className="bg-light-green flex-1" style={{ flex: 1, paddingTop: StatusBar.currentHeight }}>
        <ScrollView className="w-full" contentContainerStyle={{ flexGrow: 1, alignItems: 'center' }}>
          <Header navigation={navigation}/>
          <ProgressCircle howMuchEaten={howMuchEaten}/>
          <DateDisplay />
          <MealBox title="Breakfast" howMuchEaten={howMuchEaten} />
          <MealBox title="Lunch" howMuchEaten={howMuchEaten} />
          <MealBox title="Dinner" howMuchEaten={howMuchEaten} />
        </ScrollView>
      </SafeAreaView>
    </MealDataProvider>
  );
}
