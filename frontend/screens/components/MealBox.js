import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import styles from '../styles/styles';

const MealBox = ({ title }) => {
  return (
    <TouchableOpacity style={styles.box}>
      <Text style={styles.boxText}>{title}</Text>
    </TouchableOpacity>
  );
};

export default MealBox;
