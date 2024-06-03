import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from './screens/HomeScreen';
import { Login } from './screens/Login';
import { Register } from './screens/Register';
import { UserDetails } from './screens/UserDetails';
import { Settings } from './screens/Settings';
import { SettingsUser } from './screens/SettingsUser'
import { AddingProduct } from './screens/AddingProduct';
import { CustomDemand } from './screens/CustomDemand';
import { Statistics } from './screens/Statistics';

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
  }, []) */

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Register" component={Register} />
        <Stack.Screen name="UserDetails" component={UserDetails} />
        <Stack.Screen options={{ headerShown: false }} name="HomeScreen" component={HomeScreen} />
        <Stack.Screen name="Settings" component={Settings} />
        <Stack.Screen name="SettingsUser" component={SettingsUser} />
        <Stack.Screen name="AddingProduct" component={AddingProduct} />
        <Stack.Screen name="CustomDemand" component={CustomDemand} />
        <Stack.Screen name="Statistics" component={Statistics} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;