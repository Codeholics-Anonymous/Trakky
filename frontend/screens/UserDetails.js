import { Text, View, TextInput, TouchableOpacity } from 'react-native';
import { Logo250x250 } from '../components/Logo250x250';
import { SelectList } from 'react-native-dropdown-select-list'
import { useState } from 'react';

export function UserDetails( {navigation} ) {
  const [selected, setSelected] = useState("");
  
  const data = [
    {key:'1',value:'Jammu & Kashmir'},
    {key:'2',value:'Gujrat'},
    {key:'3',value:'Maharashtra'},
    {key:'4',value:'Goa'},
  ];

  return (
    <View className="bg-gray-100">
      <SelectList 
        onSelect={() => alert(selected)}
        setSelected={setSelected} 
        data={data}  
        search={false} 
        boxStyles={{borderRadius:0}} //override default styles
        defaultOption={{ key:'1', value:'Jammu & Kashmir' }}   //default selected option
      />
    </View>
  )
}