import { useEffect, useState } from 'react';
import { SafeAreaView, ScrollView, StatusBar } from 'react-native';
import DateDisplay from '../components/DateDisplay.js';
import Header from '../components/Header.js';
import MealBox from '../components/MealBox.js';
import ProgressCircle from '../components/ProgressCircle.js';
import { getUserData } from '../utils/Auth'

export function HomeScreen() {
  const [showDefaultProgress, setShowDefaultProgress] = useState(true);

  const toggleProgress = () => {
    console.log('Toggle pressed');
    setShowDefaultProgress(!showDefaultProgress);
  };

  useEffect(() => {
    StatusBar.setBackgroundColor('#363636', true); // 'true' to animate the color transition, color dark-grey
    StatusBar.setBarStyle('light-content', true); // changes the color of the status bar items to light
  }, []);

  return (
    <SafeAreaView className="bg-light-green flex-1" style={{ flex: 1, paddingTop: StatusBar.currentHeight }}>
      <ScrollView className="w-full" contentContainerStyle={{ flexGrow: 1, alignItems: 'center' }}>
        <Header />
        <ProgressCircle />
        <DateDisplay />
        <MealBox title="Breakfast" />
        <MealBox title="Breakfast" />
        <MealBox title="Breakfast" />
        <MealBox title="Breakfast" />
      </ScrollView>
    </SafeAreaView>
  );
};
