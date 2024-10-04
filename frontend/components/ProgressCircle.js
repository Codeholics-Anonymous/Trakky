import axios from 'axios';
import { useEffect, useState } from 'react';
import { Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';
import { CircularProgressBase } from 'react-native-circular-progress-indicator';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import LoadingScreen from '../screens/LoadingScreen';
import { getUserData } from '../utils/Auth';
import { API_BASE_URL } from '../utils/config';
import { useMealData } from './MealDataContext';

const commonProps = {
  activeStrokeWidth: 25,
  inActiveStrokeWidth: 25,
  inActiveStrokeOpacity: 1
};

const calculateProgress = (current, total) => Math.min((current / total) * 100, 100);

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
    <CircularProgressBase {...commonProps} value={carbValue} radius={135} activeStrokeColor={'#363636'} inActiveStrokeColor={'#aaaaaa'}>
      <CircularProgressBase {...commonProps} value={fatValue} radius={110} activeStrokeColor={'#F0E68C'} inActiveStrokeColor={'#aaaaaa'}>
        <CircularProgressBase {...commonProps} value={proteinValue} radius={85} activeStrokeColor={'#ffffff'} inActiveStrokeColor={'#aaaaaa'}>
          <View>
            <Text className="text-white text-small font-bold">
              C: {carbCurrent}g<Text className="text-lgt-gray">/{carbTotal}g</Text>
            </Text>
            <Text className="text-white text-small font-bold">
              F: {fatCurrent}g<Text className="text-lgt-gray">/{fatTotal}g</Text>
            </Text>
            <Text className="text-white text-small font-bold">
              P: {proteinCurrent}g<Text className="text-lgt-gray">/{proteinTotal}g</Text>
            </Text>
          </View>
        </CircularProgressBase>
      </CircularProgressBase>
    </CircularProgressBase>
  );
};

const ProgressCircles = ({creationDate}) => {
  // is it dump or working, both....
  const [isAccountCreatedDate, setisAccountCreatedDate] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { height } = useWindowDimensions();
  const [showDefaultProgress, setShowDefaultProgress] = useState(true);
  const { mealData, date, setDate } = useMealData(); // Use mealData and date from context

  // arrow buttons operations
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
  
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  useEffect(() => {
    // Sorry for idiotic use iam sleepy now 
    if(formatDate(date) == creationDate) {
      setisAccountCreatedDate(true);
    } else {
      setisAccountCreatedDate(false);
    }

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const { token } = await getUserData(); // Make sure getUserData() is defined and returns an object with token
        const currDate = formatDate(date);
        const url = `${API_BASE_URL}/api/demand/${currDate}/${currDate}/`;
        const response = await axios.get(url, {
          headers: {
            Authorization: 'Token ' + token,
          },
        });
        console.log(response.data);
        const { demand_calories_sum, demand_protein_sum, demand_carbohydrates_sum, demand_fat_sum } = response.data;

        setTotal({
          kcalTotal: demand_calories_sum,
          carbTotal: demand_carbohydrates_sum,
          fatTotal: demand_fat_sum,
          proteinTotal: demand_protein_sum,
        });
        setIsLoading(false);
      } catch (error) {
        console.error(error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, [date]);

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

  if (isLoading) {
    return <LoadingScreen />;
  }

  function formatNumber(num) {
    // Format the number to 2 decimal places
    let formattedNum = num.toFixed(2);
    
    // Remove trailing zeros and the decimal point if not needed
    formattedNum = parseFloat(formattedNum).toString();
    
    return formattedNum;
}

  return (
    <View className="flex-row items-center justify-between w-full px-6 mt-8 mb-3" style={{ height: height * 0.31 }}>
      {isAccountCreatedDate ? <View style={{ width: 36 }} /> : 
      <TouchableOpacity onPress={goPreviousDay}>
        <FontAwesome5 name="angle-left" className="text-7xl transform text-gray" />
      </TouchableOpacity> }

      <View style={{ flex: 1, alignItems: 'center' }}>
        <TouchableOpacity onPress={toggleProgress}>
          {showDefaultProgress ? (
            <SingleCircle kcalCurrent={current.kcalCurrent} kcalTotal={total.kcalTotal} />
          ) : (
            <NestedCircles
              carbCurrent={formatNumber(current.carbCurrent)}
              carbTotal={formatNumber(total.carbTotal)}
              fatCurrent={formatNumber(current.fatCurrent)}
              fatTotal={formatNumber(total.fatTotal)}
              proteinCurrent={formatNumber(current.proteinCurrent)}
              proteinTotal={formatNumber(total.proteinTotal)}
            />
          )}
        </TouchableOpacity>
      </View>

      {date.toDateString() !== new Date().toDateString() ? (
        <TouchableOpacity onPress={goNextDay}>
          <FontAwesome5 name="angle-right" className="text-7xl h-1.2 transform text-gray" />
        </TouchableOpacity>
      ) : (
        <View style={{ width: 36 }} /> // Placeholder to keep spacing consistent
      )}
    </View>
  );
};

export default ProgressCircles;
