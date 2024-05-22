import React, { useState } from 'react';
import { Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';

const commonProps = {
  activeStrokeWidth: 25,
  inActiveStrokeWidth: 25,
  inActiveStrokeOpacity: 1
};

const calculateProgress = (current, total) => (current / total) * 100;

const SingleCircle = ({ kcalCurrent, kcalTotal }) => {
  const value = calculateProgress(kcalCurrent, kcalTotal);
  return (
    <CircularProgressBase {...commonProps} value={value} radius={110} activeStrokeColor={'#00564d'} inActiveStrokeColor={'#aaaaaa'}>
      <Text className="text-white text-xl font-bold">{kcalCurrent}kcal</Text>
      <Text className="text-lgt-gray text-xl font-bold">/{kcalTotal}kcal</Text>
    </CircularProgressBase>
  );
};

const NestedCircles = ({ carbCurrent, carbTotal, fatCurrent, fatTotal, proteinCurrent, proteinTotal }) => {
  const carbValue = calculateProgress(carbCurrent, carbTotal);
  const fatValue = calculateProgress(fatCurrent, fatTotal);
  const proteinValue = calculateProgress(proteinCurrent, proteinTotal);

  return (
    <CircularProgressBase {...commonProps} value={carbValue} radius={135} activeStrokeColor={'#323232'} inActiveStrokeColor={'#aaaaaa'}>
      <CircularProgressBase {...commonProps} value={fatValue} radius={110} activeStrokeColor={'#F0E68C'} inActiveStrokeColor={'#aaaaaa'}>
        <CircularProgressBase {...commonProps} value={proteinValue} radius={85} activeStrokeColor={'#ffffff'} inActiveStrokeColor={'#aaaaaa'}>
          <View>
            <Text className="text-white text-base font-bold">
              C: {carbCurrent}g<Text className="text-lgt-gray">/{carbTotal}g</Text>
            </Text>
            <Text className="text-white text-base font-bold">
              F: {fatCurrent}g<Text className="text-lgt-gray">/{fatTotal}g</Text>
            </Text>
            <Text className="text-white text-base font-bold">
              P: {proteinCurrent}g<Text className="text-lgt-gray">/{proteinTotal}g</Text>
            </Text>
          </View>
        </CircularProgressBase>
      </CircularProgressBase>
    </CircularProgressBase>
  );
};

const ProgressCircles = () => {
  const { height } = useWindowDimensions();
  const [showDefaultProgress, setShowDefaultProgress] = useState(true);

  const kcalCurrent = 7777;
  const kcalTotal = 9999;
  const carbCurrent = 100;
  const carbTotal = 150;
  const fatCurrent = 100;
  const fatTotal = 150;
  const proteinCurrent = 100;
  const proteinTotal = 150;

  const toggleProgress = () => {
    setShowDefaultProgress(!showDefaultProgress);
  };

  return (
    <View className="flex-row items-center justify-between w-full px-6 mt-8 mb-3" style={{ height: height * 0.31 }}>
      <TouchableOpacity>
        <FontAwesome5 name="angle-left" className="text-7xl transform text-gray" />
      </TouchableOpacity>

      <TouchableOpacity onPress={toggleProgress}>
        {showDefaultProgress ? (
          <SingleCircle kcalCurrent={kcalCurrent} kcalTotal={kcalTotal} />
        ) : (
          <NestedCircles
            carbCurrent={carbCurrent}
            carbTotal={carbTotal}
            fatCurrent={fatCurrent}
            fatTotal={fatTotal}
            proteinCurrent={proteinCurrent}
            proteinTotal={proteinTotal}
          />
        )}
      </TouchableOpacity>

      <TouchableOpacity>
        <FontAwesome5 name="angle-right" className="text-7xl h-1.2 transform text-gray" />
      </TouchableOpacity>
    </View>
  );
};

export default ProgressCircles;
