import React from 'react';
import { Image, Text, View } from 'react-native';
import styles from '../styles/styles';

const Header = () => {
  return (
    <View style={styles.headerContainer}>
      <View style={styles.centerContainer}>
        <Image source={require('../img/z123.png')} style={styles.logo} />
        <Text style={styles.header}>TRAKKY</Text>
      </View>
      <Image source={require('../img/setting.png')} style={styles.options} />
    </View>
  );
};

export default Header;
