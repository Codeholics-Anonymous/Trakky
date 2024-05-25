import axios from 'axios';
import { useEffect, useState } from 'react';
import { Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import { getUserData } from '../utils/Auth';
import { useMealData } from './MealDataContext';

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
  const { mealData, date, setDate } = useMealData(); // Use mealData and date from context

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

  const [total, setTotal] = useState({
    kcalTotal: 0,
    carbTotal: 0,
    fatTotal: 0,
    proteinTotal: 0
  });

  const [current, setCurrent] = useState({
    kcalCurrent: 0,
    carbCurrent: 0,
    fatCurrent: 0,
    proteinCurrent: 0
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

  useEffect(() => {
    const calculateCurrentValues = () => {
      let kcalCurrent = 0;
      let carbCurrent = 0;
      let fatCurrent = 0;
      let proteinCurrent = 0;

      Object.keys(mealData).forEach(mealType => {
        const mealItems = mealData[mealType];
        Object.values(mealItems).forEach(item => {
          kcalCurrent += item.calories || 0;
          carbCurrent += item.carbohydrates || 0;
          fatCurrent += item.fat || 0;
          proteinCurrent += item.protein || 0;
        });
      });

      setCurrent({
        kcalCurrent,
        carbCurrent,
        fatCurrent,
        proteinCurrent,
      });
    };

    calculateCurrentValues();
  }, [mealData]);

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
          <SingleCircle kcalCurrent={current.kcalCurrent} kcalTotal={total.kcalTotal} />
        ) : (
          <NestedCircles
            carbCurrent={current.carbCurrent}
            carbTotal={total.carbTotal}
            fatCurrent={current.fatCurrent}
            fatTotal={total.fatTotal}
            proteinCurrent={current.proteinCurrent}
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
