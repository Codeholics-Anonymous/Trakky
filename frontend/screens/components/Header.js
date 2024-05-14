import React from 'react';
import { Image, Text, TouchableOpacity, View } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import styles from '../styles/styles';

const Header = () => {
  return (
    <View style={styles.headerContainer}>
      <View style={styles.centerContainer}>
        <Image source={require('../../assets/z123.png')} style={styles.logo} />
        <Text style={styles.header}>TRAKKY</Text>
      </View>
      <TouchableOpacity style={{ marginLeft: 'auto', marginRight: 8 }}>
        <FontAwesome name="bars" size={34} color="#565656"/>
      </TouchableOpacity>
    </View>
  );
};

export default Header;
