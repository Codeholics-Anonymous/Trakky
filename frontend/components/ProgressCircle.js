import { useState, useEffect } from 'react';
import { Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import { useMealData } from './MealDataContext';
import { getUserData } from '../utils/Auth';
import axios from 'axios';

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
  const { date, setDate } = useMealData(); // Use date from context

  const goPreviousDay = () => {
    const previousDay = new Date(date);
    previousDay.setDate(date.getDate() - 1);
    setDate(previousDay);
  };

  const goNextDay = () => {
    const nextDay = new Date(date);
    nextDay.setDate(date.getDate() + 1);
    setDate(nextDay);
  };

  const kcalCurrent = 111;
  const carbCurrent = 100;
  const fatCurrent = 100;
  const proteinCurrent = 100;

  const [total, setTotal] = useState({
    kcalTotal : 0,
    carbTotal : 0,
    fatTotal : 0,
    proteinTotal: 0
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { token } = await getUserData(); // Make sure getUserData() is defined and returns an object with token
        const response = await axios.get('https://trakky.onrender.com/api/basic_demand/', {
          headers: {
            Authorization: 'Token ' + token,
          },
        });
        
        const { demand, protein, carbohydrates, fat } = response.data;

        setTotal({
          kcalTotal: demand,
          carbTotal: carbohydrates,
          fatTotal: fat,
          proteinTotal: protein,
        });
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  const toggleProgress = () => {
    setShowDefaultProgress(!showDefaultProgress);
  };



  return (
    <View className="flex-row items-center justify-between w-full px-6 mt-8 mb-3" style={{ height: height * 0.31 }}>
      <TouchableOpacity onPress={goPreviousDay}>
        <FontAwesome5 name="angle-left" className="text-7xl transform text-gray" />
      </TouchableOpacity>

      <TouchableOpacity onPress={toggleProgress}>
        {showDefaultProgress ? (
          <SingleCircle kcalCurrent={kcalCurrent} kcalTotal={total.kcalTotal} />
        ) : (
          <NestedCircles
            carbCurrent={carbCurrent}
            carbTotal={total.carbTotal}
            fatCurrent={fatCurrent}
            fatTotal={total.fatTotal}
            proteinCurrent={proteinCurrent}
            proteinTotal={total.proteinTotal}
          />
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={goNextDay}>
        <FontAwesome5 name="angle-right" className="text-7xl h-1.2 transform text-gray" />
      </TouchableOpacity>
    </View>
  );
};

export default ProgressCircles;
