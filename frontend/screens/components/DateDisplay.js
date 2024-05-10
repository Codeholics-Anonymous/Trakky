import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import styles from '../styles/styles';


const DateDisplay = () => {
  return (
    <TouchableOpacity style={styles.dateContainer}>
      <Text style={styles.date}>Monday, 6.05.2024</Text>
      <FontAwesome name="calendar" size={20} color="#565656" style={{ marginLeft: 11 }}/>
    </TouchableOpacity>
  );
};

export default DateDisplay;
