import { Image, View } from "react-native";

export function Logo250x250() {
  return (
    <View className="mx-auto">
       <Image
        source={require('../assets/LOGO.png')}
        style={{ width: 250, height: 250 }}
      />
    </View>
  );
}