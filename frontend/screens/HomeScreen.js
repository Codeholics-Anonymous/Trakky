import React, { useEffect, useState } from 'react';
import { SafeAreaView } from 'react-native';
import DateDisplay from './components/DateDisplay.js';
import Header from './components/Header.js';
import MealBox from './components/MealBox.js';
import ProgressCircles from './components/ProgressCircles.js';
import styles from './styles/styles.js';


export function HomeScreen() {
  const [statusBarColor, setStatusBarColor] = useState('#000000');

  useEffect(() => {
    setStatusBarColor('#111111'); // Evening (Dark Slate Gray)
  }, []);

  return (
    <SafeAreaView style={styles.container}>
        <Header />
        <ProgressCircles />
        <DateDisplay />
        <MealBox title="Breakfast" />
        <MealBox title="Brunch" />
        <MealBox title="Lunch" />
        <MealBox title="Dinner" />  
      </SafeAreaView>
  );
};
