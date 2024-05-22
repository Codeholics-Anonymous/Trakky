import { View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Login } from './screens/Login';
import { Register } from './screens/Register';
import { UserDetails } from './screens/UserDetails';
import { HomeScreen } from './screens/HomeScreen';
import { useEffect, useState } from 'react';
import { hasUserData } from './utils/Auth';

const Stack = createNativeStackNavigator();

function App() {
/*
  const [isSignedIn, setIsSignedIn] = useState(false);

  useEffect(() => {
    const checkUserData = async () => {
      const userDataExists = await hasUserData();
      setIsSignedIn(userDataExists);
    };

    checkUserData();
  }, []);
*/

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="HomeScreen" component={HomeScreen} />
        <Stack.Screen name="Register" component={Register} />
        <Stack.Screen name="UserDetails" component={UserDetails} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;