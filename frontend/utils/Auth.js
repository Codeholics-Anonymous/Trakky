import AsyncStorage from '@react-native-async-storage/async-storage';

// Function to save token and username
export const saveUserData = async (token, username) => {
  try {
    await AsyncStorage.multiSet([
      ['token', token],
      ['username', username],
    ]);
  } catch (e) {
    console.error('Failed to save user data:', e);
  }
};

// Function to get token and username
export const getUserData = async () => {
  try {
    const values = await AsyncStorage.multiGet(['token', 'username']);
    const userData = {};
    values.forEach(([key, value]) => {
      userData[key] = value;
    });
    return userData;
  } catch (e) {
    console.error('Failed to fetch user data:', e);
  }
};

// Function to check if token and username exist
export const hasUserData = async () => {
  const { token, username } = await getUserData();
  return token !== null && username !== null;
};

// Function to reset user data
export const resetUserData = async () => {
  try {
    await AsyncStorage.multiRemove(['token', 'username']);
  } catch (e) {
    console.error('Failed to reset user data:', e);
  }
};

/*
  to get token and username
  import { getUserData } from ...
  const { token, username } = await getUserData();
*/