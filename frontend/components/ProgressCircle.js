import React, { useState } from 'react';
import { Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';

const props = {
  activeStrokeWidth: 25,
  inActiveStrokeWidth: 25,
  inActiveStrokeOpacity: 0.9
};

const ProgressCircles = () => {
  const props = {
    activeStrokeWidth: 25,
    inActiveStrokeWidth: 25,
    inActiveStrokeOpacity: 0.2
  };

  const { height } = useWindowDimensions();

    // State to toggle between ProgressCircles and ProgressCircleContainer2
    const [showDefaultProgress, setShowDefaultProgress] = useState(true);

    // Handler to toggle the state
    const toggleProgress = () => {
      console.log('Toggle pressed');  // Check if this logs in the console when clicked
      setShowDefaultProgress(!showDefaultProgress);
    };
  
  return (
    <View className="flex-row items-center justify-between w-full px-8 mt-7 mb-2" style={{ height: height * 0.31 }}>
      <TouchableOpacity>
      <FontAwesome5 name="angle-left" className="text-7xl transform text-light-gray"/>
      </TouchableOpacity>

      <TouchableOpacity onPress={toggleProgress} style={{ alignItems: 'center' }}>

        {/* Calories circle : Macros Circle */}
        {showDefaultProgress ?
          (
            <CircularProgressBase {...props} value={24} radius={110} activeStrokeColor={'#F0E68C'} inActiveStrokeColor={'#eeeeee'}>
              <Text className="text-white text-lg font-bold">7777kcal</Text>
              <Text className="text-light-gray text-lg font-bold">/9999kcal</Text>
            </CircularProgressBase>
          ) : (
                <CircularProgressBase {...props} value={90} radius={135} activeStrokeColor={'#121212'} inActiveStrokeColor={'#eeeeee'}>
                <CircularProgressBase {...props} value={24} radius={110} activeStrokeColor={'#F0E68C'} inActiveStrokeColor={'#eeeeee'}>
                  <CircularProgressBase {...props} value={70} radius={85} activeStrokeColor={'#ffffff'} inActiveStrokeColor={'#eeeeee'}>
                  <View>
                    <Text className="text-white text-base font-bold">
                      C: 100g<Text className="text-light-gray">/150g</Text>
                    </Text>
                    <Text className="text-white text-base font-bold">
                      F: 100g<Text className="text-light-gray">/150g</Text>
                    </Text>
                    <Text className="text-white text-base font-bold">
                      P: 100g<Text className="text-light-gray">/150g</Text>
                    </Text>
                  </View>
                  </CircularProgressBase>
                </CircularProgressBase>
              </CircularProgressBase>
        )}


      </TouchableOpacity>


      <TouchableOpacity>
        <FontAwesome5 name="angle-right" className="text-7xl h-1.2 transform text-light-gray"/>
      </TouchableOpacity>
    </View>
  );
};

export default ProgressCircles;
