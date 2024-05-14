import React from 'react';
import { SafeAreaView, StatusBar } from 'react-native';
import DateDisplay from '../components/DateDisplay.js';
import Header from '../components/Header.js';
import MealBox from '../components/MealBox.js';
import ProgressCircle from '../components/ProgressCircle.js';

export function HomeScreen() {
  return (
    <SafeAreaView className="bg-dark-gray h-full items-center pt-safe-top" style={{paddingTop: StatusBar.currentHeight}}>
      <Header />
      <ProgressCircle />
      <DateDisplay />
      <MealBox title="Breakfast" />
      <MealBox title="Brunch" />
      <MealBox title="Lunch" />
      <MealBox title="Dinner" />  
    </SafeAreaView>
  );
};
