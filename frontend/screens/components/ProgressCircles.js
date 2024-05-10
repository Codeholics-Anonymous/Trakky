import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import styles from '../styles/styles';

const props = {
  activeStrokeWidth: 25,
  inActiveStrokeWidth: 25,
  inActiveStrokeOpacity: 0.2
};

const ProgressCircles = () => {
  return (
    <View style={styles.circleContainer}>
      <TouchableOpacity style={styles.navText}>
        <Text style={styles.navText}>{"<"}</Text>
      </TouchableOpacity>
      <CircularProgressBase {...props} value={40} radius={130} activeStrokeColor={'#333333'} inActiveStrokeColor={'#343434'}>
        <CircularProgressBase {...props} value={74} radius={105} activeStrokeColor={'#F0E68C'} inActiveStrokeColor={'#FFFFE0'}>
          <CircularProgressBase {...props} value={30} radius={80} activeStrokeColor={'#ffffff'} inActiveStrokeColor={'#eeeeee'}>
            <Text style={styles.caloriesCurrent}>7777kcal</Text>
            <Text style={styles.caloriesGoal}>/9999kcal</Text>
          </CircularProgressBase>
        </CircularProgressBase>
      </CircularProgressBase>
      <TouchableOpacity style={styles.navText}>
        <Text style={styles.navText}>{">"}</Text>
      </TouchableOpacity>
    </View>
  );
};

export default ProgressCircles;
