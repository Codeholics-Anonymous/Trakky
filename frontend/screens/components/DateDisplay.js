import React from 'react';
import { Image, Text, TouchableOpacity } from 'react-native';
import styles from '../styles/styles';

const DateDisplay = () => {
  return (
    <TouchableOpacity style={styles.dateContainer}>
      <Text style={styles.date}>Monday, 6.05.2024</Text>
      <Image source={require('../../assets/calendar.png')} style={styles.calendar} />
    </TouchableOpacity>
  );
};

export default DateDisplay;
